---
name: audit-sft-data-quality
description: Build, audit, repair, and promote supervised fine-tuning datasets from model evaluation failures. Use when validating eval evidence, mining failed attempts and feedback turns, designing failure-conditioned synthetic variants, proving code or agent examples with executable oracles, checking prompt-target/action harmony, deduplicating revisions, preventing benchmark contamination, composing anchor-plus-augmentation mixtures, or deciding whether data and checkpoints are eligible for training or promotion. Also use for general SFT JSONL, chat, tool-trajectory, provenance, tokenizer, split, correctness, and corpus-composition audits.
---

# Failure-Conditioned SFT Audit

## Mission

Turn trustworthy evaluation failures into the smallest verified SFT intervention
that can improve held-out behavior without corrupting the data contract.

Run this chain in order:

```text
valid evaluation evidence
  -> atomic failure ledger
  -> mechanism-level diagnosis
  -> synthesis decision
  -> task and oracle design
  -> executable target proof
  -> exact SFT serialization proof
  -> lineage and contamination audit
  -> bounded pinned training
  -> repeated held-out promotion gate
```

Do not skip forward. A row that compiles can still be unusable SFT. A dataset
that passes every row gate can still produce a bad checkpoint. Keep those claims
separate.

Read [failure-conditioned-workflow.md](references/failure-conditioned-workflow.md)
when performing the workflow. Use
[artifact-contracts.md](references/artifact-contracts.md) for portable records
and report schemas. Use
[iterative-sft-data-design.md](references/iterative-sft-data-design.md) for the
broader pass@k, curriculum, judge, mixture, and capability-planning doctrine.

## Non-negotiable doctrine

1. Validate the evaluator before learning from its failures.
2. Preserve raw attempts, compiler or tool feedback, tests, hashes, and runtime
   configuration before transforming anything.
3. Distinguish an observed failure from a test that never ran.
4. Diagnose the narrow causal mechanism, not merely the first diagnostic line.
5. Generate the new task and its oracle before generating the target answer.
6. Require the oracle to reject the starter, the observed failure mechanism,
   and a distinct compiling semantic error.
7. Verify the exact serialized SFT action, not an ideal solution stored beside
   it.
8. Replace defective ancestors with verified corrections; never train both as
   independent positive examples.
9. Keep held-out tasks and their exact artifacts out of training.
10. Call close failure-conditioned synthesis reliability reinforcement, not
    independent out-of-family generalization.
11. Treat data eligibility and checkpoint promotion as separate gates.
12. Preserve negative experimental results and revise the hypothesis instead of
    weakening the success criterion.

## Phase 0: Write the iteration contract

Write a falsifiable contract before mining or synthesis:

```text
iteration_id
parent_dataset_and_hash
base_checkpoint_and_hash
target_behavior
held_out_task_distribution
evaluation_contract_and_revision
observed_failure_hypothesis
planned_data_intervention
variables_that_must_stay_fixed
primary_metric
regression_metrics
promotion_threshold
stop_condition
```

Reject “add more hard examples” as an iteration contract. Name the behavior,
evidence, intervention, and measurement that can falsify the idea.

## Phase 1: Freeze and validate the evaluation contract

Record exact values for:

- checkpoint, base model, adapter, and tokenizer hashes;
- harness, benchmark, overlay, repository, and evaluator revisions;
- task IDs, task and test hashes, exclusions, and split policy;
- system prompt, chat template, reasoning mode, decoding, seed policy, and token
  limit;
- tool availability, sandbox, permissions, working directory, and environment;
- turn count, feedback timing, compiler or tool feedback source, and stopping
  rules;
- oracle command, dependencies, timeout, and expected terminal task count.

Run health gates before interpreting model quality:

- every expected task appears exactly once per trial;
- every attempt has an unambiguous terminal status;
- candidate and feedback artifacts are present and correctly routed;
- requested reasoning or content channels were not silently dropped;
- adapters and checkpoints actually loaded;
- compiler, test, and tool feedback came from the declared environment;
- malformed outputs, context exhaustion, timeouts, and infrastructure failures
  are separated from semantic failures.

If a health gate fails, mark the run `invalid-eval-evidence`. Repair and rerun it.
Do not synthesize SFT rows from a broken evaluator.

Use repeated independent trials for stochastic evaluation. Keep single-turn
first-attempt performance separate from feedback-assisted recovery. A strong
default for a small fixed suite is four independent single-turn trials and four
independent feedback trials, unless the iteration contract specifies another
predeclared design.

## Phase 2: Build the atomic failure ledger

Preserve an immutable record for every task, attempt, and turn:

- prompt, starter files, protected files, candidate response, and applied files;
- build or action command, environment, diagnostic stream, and terminal result;
- test names, inputs, expected values, observed values, and reachability;
- response, candidate, chat, file, test, and configuration hashes;
- token count, latency, duration, context use, and tool-call sequence;
- feedback shown to the model and the next action it took.

Classify the terminal stage using a stable taxonomy:

```text
format-or-apply
syntax
compile
link-or-odr
runtime-or-sanitizer
semantic-counterexample
resource-limit
pass
infrastructure-invalid
```

Classify each test independently:

```text
passed-observed
failed-observed
not-reached-build-blocked
not-reached-runtime-blocked
not-run-harness-invalid
```

Never convert “not reached” into “failed.” Report masked tests separately. If a
compile error prevents 200 tests from running, the evidence is one observed
build failure plus 200 unobserved tests, not 201 model failures.

## Phase 3: Diagnose every task, not only every log

For each task, compare all attempts and feedback turns. Determine:

- the first terminal defect;
- the narrow mechanism that caused it;
- whether later diagnostics reveal an independent defect;
- whether another attempt demonstrates latent success;
- whether feedback produces a minimal repair, a blind rewrite, or repeated error;
- the smallest counterexample or probe that would discriminate rival diagnoses;
- diagnosis strength: `direct`, `strong-inference`, `weak-inference`, or
  `unresolved`.

Use mechanism tags such as:

- exact API or header drift;
- missing include or namespace qualification;
- templates, overload resolution, or type genericity;
- linkage, ODR, or header isolation;
- state lifecycle, mutation atomicity, or recursion discipline;
- boundary semantics, representation, or deterministic ordering;
- undefined behavior, portability, or warnings-as-errors;
- algorithm selection, complexity, or resource exhaustion;
- file emission, tool protocol, or feedback interpretation.

Do not equate the first compiler message with the full cause. Add targeted probes
until the diagnosis is sufficient to design a discriminating oracle, or mark the
case unresolved.

Produce one task failure packet containing the task ID, observed stage,
diagnostics, test reachability, candidate hashes, counterexample, cross-attempt
comparison, mechanism tags, evidence strength, next probe, and disposition.

## Phase 4: Decide what the evidence authorizes

Route each packet as follows:

| Evidence | Authorized action |
| --- | --- |
| Broken spec, oracle, or harness | Repair evaluation; create no SFT row |
| Format or action-contract failure | Teach the exact protocol with replayable final-state checks |
| Build-blocked attempt | Teach the observed build, API, type, or linkage mechanism; do not invent downstream semantic failures |
| Direct executed counterexample | Build new tasks around that latent property and boundary |
| Inconsistent success across attempts | Emphasize first-pass selection and discriminative cues |
| Repair succeeds after real feedback | Optionally add concise feedback-repair trajectories, at controlled weight |
| Stable held-out success | Add only sparse preservation anchors |
| Unresolved diagnosis | Add a probe or retain as eval-only; do not synthesize yet |

Reject cosmetic reskins that change names but add no independent oracle case,
contract dimension, failure discriminator, or meaningful domain shift.

## Phase 5: Design failure-conditioned variants

Create variants around the latent skill, not around the held-out task identity.
Change task IDs, filenames, symbols, surface structure, and inputs. Exclude exact
held-out prompts, answers, tests, reference code, hashes, and metadata.

For each diagnosed family, consider these roles:

1. foundation;
2. exact API contract;
3. boundary case;
4. adversarial wrong heuristic;
5. state discipline;
6. representation variation;
7. efficiency or scale;
8. type genericity or portability;
9. composition with another prerequisite;
10. capstone.

Use only roles that are applicable. Do not fill a quota with weak examples.

Define before the target:

- the observable contract and invariants;
- starter state and editable files;
- protected files and exact API requirements;
- hidden behavior tests;
- failure-class negative control;
- distinct compiling semantic negative control;
- isolation, integration, resource, safety, or state probes appropriate to the
  task;
- lineage and the specific oracle delta over the parent.

For C++ repository tasks, default to strict C++17 compilation with warnings as
errors, full behavior tests, ASan/UBSan where applicable, header-isolation
compilation, byte-identical protected headers, and multi-translation-unit link
and run probes. Adapt the proof surface for other languages and agent tasks.

## Phase 6: Prove each task and target

Require the same oracle to demonstrate all applicable facts:

1. the intended target passes;
2. the starter does not already pass;
3. the observed failure-class mutation is rejected;
4. a distinct compiling semantic mutation is rejected;
5. protected artifacts remain unchanged;
6. isolation and integration probes pass;
7. sanitizers, invariants, resource bounds, and final-state assertions pass.

Retain commands, toolchain versions, test counts, assertion counts, hashes, and
logs in a per-row verification receipt. Do not claim new test coverage merely
because an inherited test suite was replayed; distinguish inherited assertions
from added oracle cases.

After any prompt, starter, solution, test, metadata, or serialization repair,
rerun the complete row oracle. A local patch-specific check is insufficient.

## Phase 7: Prove prompt-target and action harmony

Render every row exactly as the trainer will see it, using the pinned tokenizer
and chat template. Audit the loss-bearing target, not a neighboring canonical
solution.

Check every row for:

- legal role order and nonempty loss-bearing assistant target;
- exact system and interaction contract;
- parseable, complete file or action listings;
- no duplicate, elided, or phantom files;
- target files are editable and requested;
- protected or unchanged files are not emitted unless explicitly required;
- source-only requests emit only source files;
- requested explanation or prose appears in the required position;
- no hidden tests, reference answers, private state, or judge labels in messages;
- starter and target hashes match the versions proved by the oracle;
- official tokenization, loss masking, EOS behavior, and context length pass;
- tool calls and results pair correctly and replay to the asserted final state.

This is a hard gate. Executable correctness outside the serialized conversation
does not rescue a contradictory or untrainable row.

## Phase 8: Audit the corpus and resolve lineage

Compare the candidate set against every parent, neighbor, train, validation, and
held-out set at these levels:

1. row hash and task ID;
2. exact and normalized messages;
3. prompt-only and answer-only content;
4. tests, APIs, symbols, filenames, and declared source hashes;
5. explicit revisions and parent-child lineage;
6. templates, paraphrases, and semantic contract adjacency.

Group splits by underlying task, source, template, and revision lineage.
Disclose close semantic adjacency even when exact contamination is zero.

Apply these corpus gates:

- provenance is known for every selected row;
- exact duplicate and held-out collisions are zero;
- a verified correction replaces its defective ancestor;
- unresolved `review` or `repair-and-reverify` rows are not selected;
- template monoculture and family imbalance are measured and bounded;
- suspiciously high starter-copy targets receive independent recomputation;
- licenses, consent, privacy, and secrets permit training;
- the final manifest binds the exact selected JSONL, tokenizer, contract, and
  verification receipts by hash.

Tag provenance precisely: human, organic trajectory, imported, model-generated,
synthetic, repaired, or close failure-conditioned synthetic. Do not relabel
synthetic descendants as organic.

## Phase 9: Compose the smallest defensible mixture

Keep a verified anchor set from the last successful training iteration. Add the
smallest verified tranche that tests the current hypothesis. Balance by latent
behavior and family, not merely topic or row count.

Do not append source datasets again if the candidate artifact already contains
them. Resolve its manifest and lineage first. Record exact row identities,
weights, sampling policy, and ancestor replacements.

Control repair trajectories so they do not overwhelm direct first-pass
successes. Preserve stable skills with sparse anchors and spend new capacity on
diagnosed, teachable mechanisms.

## Phase 10: Train under a pinned comparison contract

Before expensive training, diff the proposed run against the last successful
control:

- base checkpoint and adapter lineage;
- trainer and launcher revisions;
- optimizer, scheduler, precision, rank or full-parameter mode;
- batch, accumulation, sequence length, packing, epochs or updates;
- tokenizer, chat template, masking, EOS, and reasoning mode;
- world size, hardware, distributed strategy, and resume semantics;
- data path, manifest hash, mixture, shuffle, and seed;
- checkpoint and evaluation selection policy.

Change only the variables authorized by the iteration contract. Run bounded
canaries and save enough intermediate evidence to distinguish optimization,
overfit, and data effects.

## Phase 11: Evaluate and promote

Evaluate candidate checkpoints on the frozen held-out contract with the same
trial structure used for the control. Report:

- trial-level and aggregate single-turn success;
- feedback-assisted success and success conditional on initial failure;
- per-task transitions and regressions;
- format, application, compiler, tool, and harness failure rates;
- tokens, latency, context exhaustion, and cost;
- confidence intervals or trial variability;
- exact checkpoint, adapter, evaluator, and artifact hashes.

Promote only if the predeclared primary metric improves without unacceptable
regressions. Data eligibility means “safe to train,” not “proven to improve the
model.” Training loss is not promotion evidence.

## Row dispositions

Assign exactly one current disposition:

- `train` — all applicable hard gates pass;
- `replace-ancestor` — verified correction selected in place of its parent;
- `review` — ambiguity or weak evidence requires adjudication;
- `repair-and-reverify` — deterministic defect is recoverable but full replay is
  pending;
- `reject` — wrong, leaked, contradictory, unverifiable, prohibited, or
  malformed;
- `eval-only` — useful diagnostic that must not enter positive SFT.

## Immediate rejection and invalidation rules

Nuke or quarantine:

- failures from an invalid evaluator;
- exact held-out tasks, answers, tests, or private evaluator artifacts;
- masked or unexecuted tests reported as observed model failures;
- cosmetic variants with no measurable oracle delta;
- targets that are wrong, unverifiable, or contradicted by a counterexample;
- action outputs that modify protected or unrequested artifacts;
- prompt-target contradictions and missing requested content;
- rows that exceed the actual trainer context or use the wrong template;
- exact duplicates, unknown provenance, and unresolved contamination;
- ancestor and correction pairs presented as independent positive examples;
- unresolved review or repair rows in a supposedly train-ready manifest;
- checkpoints that fail the predeclared held-out promotion gate.

## Supporting audit plus points

After the core gates, retain the broader audit benefits:

- category, capability, source, difficulty, token, and verification summaries;
- strongest applicable deterministic oracle for code, math, extraction,
  transformation, tools, structured output, safety, and open-ended tasks;
- independent model judges for ambiguity discovery, never as a substitute for
  executable proof;
- signal-density scoring for directness, clarity, realism, novelty, concision,
  difficulty, and deployment relevance;
- source caps, family caps, difficulty balance, and synthetic-monoculture checks;
- privacy, licensing, consent, policy, and secret-handling review;
- pass@k skill mapping, curricula, calibration, safety, and tool-use analysis.

Apply these as additions to the failure-conditioned chain, never as a way to
average away a failed hard gate.

## Required deliverables

Produce, at minimum:

- immutable source and evaluation manifests with hashes;
- evaluation health report and invalid-run ledger;
- attempt/turn ledger and per-test reachability matrix;
- one failure packet per task;
- synthesis decision and task-oracle specification per proposed variant;
- per-row executable or replay verification receipts;
- exact serialized-row and tokenizer/action-harmony audit;
- duplicate, lineage, contamination, provenance, and split reports;
- selected, replaced, rejected, review, repair, and eval-only manifests;
- final train manifest bound to exact bytes and receipts;
- pinned training diff and canary evidence;
- repeated held-out evaluation report and promotion decision;
- limitations, residual risks, and the next falsifiable probe.

Lead the report with confirmed counts, invalid evidence, selected rows, rejected
rows, unresolved risks, and the next gate. Keep observed evidence, inference,
and hypothesis visibly distinct.
