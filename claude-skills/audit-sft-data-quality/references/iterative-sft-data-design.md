# Iterative SFT Capability and Data Design

## Contents

- [Purpose](#purpose)
- [Start with a fixed base evaluation](#start-with-a-fixed-base-evaluation)
- [Interpret pass@k as a skill map](#interpret-passk-as-a-skill-map)
- [Convert the map into SFT priorities](#convert-the-map-into-sft-priorities)
- [Properties SFT can teach](#properties-sft-can-teach)
- [Write an iteration contract](#write-an-iteration-contract)
- [Build a property-to-data matrix](#build-a-property-to-data-matrix)
- [Source data in descending confidence](#source-data-in-descending-confidence)
- [Synthesize data from contracts](#synthesize-data-from-contracts)
- [Augment for useful coverage](#augment-for-useful-coverage)
- [Correct data without erasing lineage](#correct-data-without-erasing-lineage)
- [Use model judges as a review layer](#use-model-judges-as-a-review-layer)
- [Design a diverse verified corpus](#design-a-diverse-verified-corpus)
- [Compose the training mixture](#compose-the-training-mixture)
- [Measure each property separately](#measure-each-property-separately)
- [Diagnose outcomes before creating more data](#diagnose-outcomes-before-creating-more-data)
- [Optimize iteration ROI](#optimize-iteration-roi)
- [Promotion contract](#promotion-contract)
- [Iteration record](#iteration-record)

## Purpose

Use supervised fine-tuning to change observable conditional behavior. Define
the property to teach, create evidence that the examples express it, and measure
whether that property improves on held-out tasks without unacceptable
regressions.

SFT is not automatically a knowledge upgrade. It can improve task recognition,
action selection, formatting, reliability, tool use, or repair behavior while
leaving core problem-solving capability unchanged or even weakening it.

Begin with a fixed base-model evaluation. It reveals which skills are already
reliable, which exist in the model but are selected inconsistently, and which
remain outside the model's observed capability. Use those distinctions to
decide what to preserve, teach, decompose, or exclude from the current
iteration.

## Start with a fixed base evaluation

Build the evaluation before selecting training rows:

1. define the deployment task distribution and deterministic success oracle;
2. group tasks by latent skill, not only topic or benchmark name;
3. hold out complete task, template, and revision lineages from training;
4. sample `n` independent responses per task under a recorded decoding policy;
5. retain every response and oracle result, including failures;
6. report per-task and per-skill results with uncertainty.

For `n` sampled responses with `c` correct responses and `n >= k`, estimate
pass@k as:

```text
pass@k = 1 - C(n - c, k) / C(n, k)
```

This estimates the probability that at least one of `k` samples succeeds.
Compute all compared `k` values from the same response pool when possible.
Record the model and tokenizer revision, prompt template, tool environment,
sampling temperature, top-p, maximum tokens, seed policy, oracle revision, and
task exclusions. Do not compare a greedy base `pass@1` with a sampled post-SFT
`pass@k` as though they measured the same behavior.

Store at least these fields per task:

```text
task_id
skill_tags
difficulty_tags
sample_count
correct_count
pass_at_1
pass_at_k
format_validity
failure_categories
tokens_and_latency
oracle_revision
```

Treat sampled `pass@1` as single-attempt reliability and larger `pass@k` as
evidence about whether a successful behavior exists in the model's sampled
support. Measure greedy accuracy separately when it matters. The gap between
`pass@1` and a larger `pass@k` is a useful selection diagnostic, not proof of a
particular internal mechanism.

## Interpret pass@k as a skill map

Aggregate by skill family and inspect task-level variation. Use thresholds
chosen before training and appropriate to the benchmark size; do not impose one
universal percentage boundary.

| Base-eval pattern | Interpretation | Training decision |
| --- | --- | --- |
| High `pass@1`, high `pass@k` | Easy and stable | Preserve with a small anchor set; spend little new data |
| Low or medium `pass@1`, high `pass@k` | Latent but selection-hard | Highest SFT opportunity: teach direct successful choices and discriminative cues |
| Medium values at every `k` | Unstable or partially learned | Add verified coverage around observed failure modes and boundaries |
| Low `pass@1`, low `pass@k` | Capability-hard or missing prerequisites | Decompose the skill and build a verified difficulty ladder |
| Zero success with invalid outputs or tool failures | Contract- or interface-blocked | Teach format, state, or tool prerequisites before deeper reasoning |
| Zero success with ambiguous tasks or judge disagreement | Possibly broken evaluation | Repair the specification or oracle; do not create supervision yet |

Call a skill easy or hard only after examining enough independent tasks,
samples, and seeds. A single task may reflect prompt sensitivity, evaluator
noise, context exhaustion, or an unusually difficult instance. Report bootstrap
confidence intervals or another suitable uncertainty estimate for aggregated
rates.

Difficulty is relative to the evaluated model and runtime. Tag each task with
primary and secondary skills, then use contrastive tasks that differ in one
requirement to isolate the failing prerequisite. A compound task with low
`pass@k` does not establish that every skill inside it is hard.

The base run should produce a transition-ready skill ledger:

```text
skill_family
task_count
base_pass_at_1
base_pass_at_k
selection_gap
dominant_failure_modes
confidence_interval
assigned_bucket
```

## Convert the map into SFT priorities

Use the base buckets to select the smallest useful intervention:

| Skill bucket | Data strategy | Why |
| --- | --- | --- |
| Easy and stable | Keep diverse verified anchors at low weight | Prevent regression without wasting capacity |
| Latent but selection-hard | Distill concise successful samples, vary surface cues, emphasize first-pass targets | Move existing successful modes toward the model's default response |
| Partially learned | Add verified boundary cases and counterexamples to the dominant wrong heuristic | Increase reliability where behavior changes |
| Capability-hard | Teach prerequisites, decompositions, and progressively harder compositions | Avoid asking SFT to imitate solutions the model cannot meaningfully absorb |
| Contract-blocked | Add valid schemas, tool trajectories, state transitions, and final-state assertions | Remove interface failures before judging reasoning |
| Evaluation-broken | Fix or remove the task | Bad measurement creates bad supervision |

Never place the exact held-out evaluation problems or their answers into the
training set. Successful base samples are candidate evidence, not automatically
valid SFT rows. Reverify them, extract the underlying skill, and synthesize
different tasks that preserve the skill while changing identifiers, structure,
domain, and hidden tests. Failed base samples diagnose the missing behavior;
they are not positive imitation targets unless represented explicitly as a
critique-and-repair trajectory.

Prioritize skills by expected return rather than raw failure count. A useful
ranking considers deployment frequency, consequence of failure, base selection
gap, confidence in the oracle, estimated teachability, data cost, and regression
risk. Latent high-value skills often give the fastest SFT gains. Capability-hard
skills may have greater upside but need staged curricula, tool support,
pretraining-style data, or execution-reward optimization after SFT.

Build the curriculum from the resulting prerequisite graph. Preserve easy
prerequisites, concentrate verified supervision on valuable selection-hard
skills, and teach the missing components of hard compound tasks before adding
full compositions. Do not let abundant easy examples dominate merely because
they are cheaper to generate.

## Properties SFT can teach

| Property | Teaching signal | Useful measurement | Common failure |
| --- | --- | --- | --- |
| Task recognition | Clear mapping from request to intended task | Correct task framing and routing | Solves a nearby task |
| Contract following | Valid outputs, files, schemas, or actions | Format and protocol validity | Polished but unusable response |
| Planning | Compact decomposition before irreversible action | Plan validity and downstream success | Ritualized or excessive reasoning |
| First-pass correctness | Direct, verified successful responses | pass@1 or task success | Learns only to repair after failure |
| State discipline | Correct mutation, rollback, and lifecycle behavior | Invariant and state-transition tests | Partial mutation on rejection |
| Boundary handling | Examples centered on limits and edge cases | Boundary and property tests | Memorizes ordinary cases |
| Determinism | Stable ordering and tie behavior | Repeated-run consistency | Hidden nondeterminism |
| Efficiency | Correct complexity and resource choices | Time, memory, calls, and token use | Correct but impractical solution |
| Tool selection | Appropriate tools and valid arguments | Tool success and final-state assertions | Tool-shaped text without execution |
| Feedback repair | Concise correction from real failure evidence | Recovery rate and repair cost | Rewrites blindly or loops |
| Calibration | Abstain, ask, or qualify when evidence is insufficient | Selective accuracy and false confidence | Confident fabrication |
| Concision | Minimum sufficient output and reasoning | Tokens per successful task | Verbosity without added success |
| Robustness | Same behavior across domains and surface forms | Held-out template and domain success | Template memorization |
| Safety | Refusal or constrained action under defined risk | Policy-specific true and false positives | Over-refusal or unsafe compliance |

Do not optimize all properties in every iteration. Choose a small number of
primary properties and treat the rest as regression gates.

## Write an iteration contract

Before changing data, record:

```text
Primary property:
Target task distribution:
Base evaluation revision:
Base pass@1 and pass@k by skill:
Target skill bucket:
Observed failure:
Evidence for the diagnosis:
Rows or families affected:
Data intervention:
What stays fixed:
Primary metric:
Regression metrics:
Promotion threshold:
Stop condition:
```

An iteration without a falsifiable contract is corpus accumulation, not an
experiment.

## Build a property-to-data matrix

Map every property to an explicit data form:

| Property target | Prefer | Avoid |
| --- | --- | --- |
| First-pass correctness | Direct verified solutions | Large volumes of failed attempts |
| Boundary reliability | Minimal counterexamples and exhaustive edges | Repeated ordinary examples |
| Tool use | Replayed successful actions with final-state evidence | Unexecuted tool-call prose |
| Repair | One real failure, relevant feedback, minimal correction | Synthetic error chatter and long loops |
| Calibration | Answerable and unanswerable matched pairs | Blanket refusal demonstrations |
| Concision | Shortest complete successful answer | Style-only compression that removes proof |
| Generalization | New templates and domains with same latent skill | Paraphrases that preserve every surface cue |
| Efficiency | Correct solutions under measured constraints | Unchecked complexity claims |

## Source data in descending confidence

Prefer:

1. independently verified human or canonical solutions;
2. successful production or sandbox trajectories with replayable evidence;
3. deterministic solver- or test-generated examples;
4. model-generated candidates that pass independent execution and semantic
   review;
5. repaired examples with recorded parent, defect, correction, and revalidation.

Treat provenance as part of the example. Preserve source revision, generator,
judge, oracle, test hash, and correction lineage.

Use successful base responses only after the same verification. Prefer them for
selection-hard skills, where the base evaluation has already shown that the
model can produce a valid behavior. For capability-hard skills, source targets
from stronger verified solutions and construct prerequisite examples rather
than repeatedly sampling a model that never succeeds.

## Synthesize data from contracts

Generate the task and oracle before generating the answer whenever possible.

1. Define the capability and invariant.
2. Generate a task specification with unambiguous valid and invalid behavior.
3. Create hidden tests, properties, or a deterministic checker.
4. Verify that the checker distinguishes intended counterexamples.
5. Generate one or more candidate solutions without access to hidden answers.
6. Execute candidates and retain only verified targets.
7. Inspect a stratified sample for specification loopholes.
8. Record generator, prompt, seed, checker, and result hashes.

Vary dimensions independently:

- domain and terminology;
- data type and scale;
- API shape and file layout;
- state lifecycle;
- boundary and invalid-input behavior;
- algorithmic strategy;
- tool sequence;
- output representation;
- difficulty and resource limits.

Do not count cosmetic renaming as meaningful diversity.

## Augment for useful coverage

Useful augmentation methods include:

- domain transfer while preserving the latent contract;
- boundary expansion around a known failure;
- adversarial counterexamples to a specific wrong heuristic;
- difficulty ladders with independently verified steps;
- alternative valid algorithms under the same contract;
- tool and environment variations;
- concise repair trajectories from real compiler, test, or state feedback;
- matched answerable and unanswerable cases for calibration;
- state-transition permutations and rollback cases;
- resource-constrained variants for efficiency.

Require each augmentation to add a tag, oracle case, or held-out dimension that
the parent did not cover. Otherwise treat it as a duplicate or down-weight it.

## Correct data without erasing lineage

When a row is wrong:

1. identify whether the defect is in the specification, input, answer, test, or
   metadata;
2. write the smallest counterexample that proves the defect;
3. correct the responsible artifact;
4. rerun the full oracle, not only the new counterexample;
5. create a new revision with `revision_of`, defect reason, verifier, and hashes;
6. replace the ancestor in positive SFT mixtures;
7. retain the old row only in a structured critique or repair dataset where the
   failed response is clearly not the imitation target.

Never silently edit a released row or train conflicting ancestor and corrected
targets as independent positive examples.

## Use model judges as a review layer

Use an agent judge to find ambiguities, missed counterexamples, style-contract
violations, and semantic mismatches. Do not use it as the sole proof of
correctness when an executable oracle is possible.

For each judgment, require:

- verdict: pass, fail, or uncertain;
- confidence;
- contract evidence;
- a concrete counterexample or explanation of why none was found;
- specification-ambiguity flag;
- recommended disposition.

Blind judges to selection intent and expected acceptance. Adjudicate judge
disagreements and high-impact uncertain rows independently.

## Design a diverse verified corpus

High success means the target is correct and verifiable. High entropy means the
corpus covers genuinely different tasks, strategies, states, and failure modes.
It does not mean the supervision itself should be ambiguous.

Increase useful entropy through:

- balanced latent capabilities rather than balanced topic names;
- multiple domains for the same skill;
- multiple valid strategies where the task allows them;
- rare edge and failure cases;
- different tool and state transitions;
- held-out templates and combinations;
- answer-length and difficulty ranges appropriate to deployment.

Keep the task contract and final target deterministic enough to learn.

## Compose the training mixture

Maintain an immutable verified anchor set. Add the smallest new tranche that can
test the current hypothesis. A reasonable starting mixture, to be adapted by
task, is:

| Data role | Starting share |
| --- | ---: |
| Direct verified successful responses | 50–70% |
| Boundary and adversarial successes | 15–25% |
| Tool-use or feedback-repair trajectories | 10–20% |
| Calibration, clarification, or abstention | 5–10% |

These are starting points, not universal constants. Use family caps, revision
deduplication, and source caps to prevent a large synthetic family from
dominating.

Sequence the curriculum when useful:

1. direct contract-following successes;
2. boundary and state-discipline cases;
3. harder compositional tasks;
4. concise real-feedback repair;
5. preference optimization or execution-reward RL after the SFT checkpoint is
   proven stable.

## Measure each property separately

Track:

- pass@1 for first-pass capability;
- pass@N or best-of-N for distributional capability;
- repair success conditional on initial failure;
- format and protocol validity;
- held-out domain and template success;
- tokens, latency, calls, and context exhaustion per success;
- calibration and abstention quality;
- safety true positives and false positives;
- per-family gains, retained tasks, and regressions;
- multiple seeds and confidence intervals for stochastic evaluation.

Training loss measures imitation fit. It does not prove task improvement.

Compare post-SFT results against the frozen base run at every evaluated `k` and
for every skill family:

| Metric transition | Likely effect | Interpretation |
| --- | --- | --- |
| `pass@1` rises, larger `pass@k` is flat | Better selection | Existing capability became a more likely first response |
| `pass@1` and larger `pass@k` rise | Reliability and sampled support improved | Strong evidence that the skill family advanced |
| `pass@1` is flat, larger `pass@k` rises | More successful modes exist | Improve selection, calibration, or ranking next |
| `pass@1` rises, larger `pass@k` falls | Distribution narrowed | Check mode collapse and loss of alternative valid strategies |
| Both remain flat | Intervention missed its target | Revisit diagnosis, examples, weight, or optimization |
| Either metric falls on an easy skill | Regression | Restore anchors, rebalance the mixture, or reject the checkpoint |

These transitions describe aggregates across a skill family. On an individual
task evaluated from one fixed sample pool, every `pass@k` is determined by the
same correct count; apparently divergent movements therefore require
task-level inspection.

Also report task transitions such as `hard -> latent`, `latent -> stable`, and
`stable -> regressed`. Aggregate scores can hide the exact skills gained and
lost.

## Diagnose outcomes before creating more data

| Observation | Likely interpretation | Next intervention |
| --- | --- | --- |
| Format improves, correctness flat | Contract learned, capability unchanged | Add verified reasoning or task coverage |
| pass@N high, pass@1 low | Capability exists but selection is weak | Improve calibration, ranking, or first-pass targets |
| Repair improves, pass@1 falls | Corpus overweights correction behavior | Increase direct successes and shorten repairs |
| Some families gain while others regress | Distribution shifted | Rebalance anchors and add regression examples |
| Loss falls, held-out success falls | Overfit or target mismatch | Stop earlier and repair composition |
| Responses grow longer without gains | Reasoning or style imitation | Select concise successful targets |
| Tool syntax works, final state fails | Protocol learned without task grounding | Add replayed trajectories and state assertions |
| Safety improves but benign tasks fail | Over-refusal | Add matched safe boundary cases |

## Optimize iteration ROI

Spend effort in this order:

1. correctness and leakage gates;
2. revision-aware deduplication;
3. task and capability coverage;
4. fixed held-out evaluation;
5. checkpoint and mixture selection;
6. synthesis and augmentation for diagnosed failures;
7. training throughput after the data signal is credible.

Use short training canaries and intermediate checkpoints. Reject weak mixtures
early with a balanced canary, but require the complete fixed evaluation before
promotion. Parallelize evaluation when it dominates wall time.

## Promotion contract

Promote a dataset or checkpoint only when:

- every selected row passes its hard evidence gates;
- duplicate and correction lineage is resolved;
- benchmark and split contamination checks pass;
- the primary property improves on held-out tasks across enough seeds;
- regression metrics remain within declared limits;
- cost, latency, and output validity are acceptable;
- artifacts, hashes, configuration, and limitations are recoverable.

If an iteration does not improve the targeted property, preserve the evidence,
reject the mixture, and update the diagnosis. Do not hide the negative result or
convert it into a weaker success criterion.

## Iteration record

Store at least:

```text
iteration_id
parent_dataset
source_hashes
selected_rows
replaced_rows
rejected_rows
capability_tags
verification_receipts
mixture_weights
model_and_tokenizer_revision
training_config
checkpoint_ids
evaluation_revision
seeded_results
task_transitions
promotion_decision
residual_risks
```

The record should let another operator reproduce both the data decision and the
model decision without relying on conversational history.
