# Failure-Conditioned SFT Workflow

## Contents

- [Purpose](#purpose)
- [Evidence tiers](#evidence-tiers)
- [Stage A: establish valid evaluation evidence](#stage-a-establish-valid-evaluation-evidence)
- [Stage B: reconstruct attempts and test reachability](#stage-b-reconstruct-attempts-and-test-reachability)
- [Stage C: isolate failure mechanisms](#stage-c-isolate-failure-mechanisms)
- [Stage D: authorize or reject synthesis](#stage-d-authorize-or-reject-synthesis)
- [Stage E: design new tasks and discriminating oracles](#stage-e-design-new-tasks-and-discriminating-oracles)
- [Stage F: prove targets and negative controls](#stage-f-prove-targets-and-negative-controls)
- [Stage G: prove exact SFT serialization](#stage-g-prove-exact-sft-serialization)
- [Stage H: repair without hiding lineage](#stage-h-repair-without-hiding-lineage)
- [Stage I: audit the combined corpus](#stage-i-audit-the-combined-corpus)
- [Stage J: run a controlled training experiment](#stage-j-run-a-controlled-training-experiment)
- [Stage K: evaluate and decide promotion](#stage-k-evaluate-and-decide-promotion)
- [Code-task proof profile](#code-task-proof-profile)
- [Agent and tool-task proof profile](#agent-and-tool-task-proof-profile)
- [Human-review protocol](#human-review-protocol)
- [Final report order](#final-report-order)

## Purpose

Use this workflow when an evaluation produces failures that may justify new SFT
data. Its job is not to maximize row count. Its job is to preserve causal
evidence from the failing model, create new examples that target the diagnosed
behavior without copying the held-out task, and prove both the target behavior
and the exact training representation.

The workflow has four independent verdicts:

```text
evaluation valid?
failure diagnosis supported?
row train-eligible?
checkpoint promotable?
```

Never collapse them into one “quality” score.

## Evidence tiers

Label every material claim with one tier:

| Tier | Meaning | Example |
| --- | --- | --- |
| Observed | Directly present in immutable artifacts | Compiler rejected candidate with diagnostic X |
| Derived | Deterministic computation from observed artifacts | 431 tests were unreachable because build stopped |
| Strong inference | Best explanation with discriminating evidence | API drift caused repeated compile failures |
| Weak inference | Plausible but not isolated | Model may lack the algorithm |
| Hypothesis | Proposed intervention to test | Boundary variants may improve first-pass choice |

Do not write inference as observation. Store the supporting artifact IDs and the
next probe for every unresolved inference.

## Stage A: establish valid evaluation evidence

### A1. Snapshot the contract

Create immutable manifests for the model, harness, tasks, tests, prompts,
runtime, and sampling policy. Hash files and serialized configuration. Record
environment images or package locks when they affect results.

### A2. Assert run health

Check task cardinality, uniqueness, terminal statuses, adapter activation,
candidate persistence, feedback routing, channel routing, timeout behavior, and
oracle completion. Reconcile aggregate scores with row-level receipts.

### A3. Separate model failure from harness failure

Use explicit statuses:

```text
model-failure
model-pass
malformed-model-output
context-exhaustion
tool-or-sandbox-blocked
timeout-ambiguous
harness-error
oracle-error
missing-artifact
```

Only `model-failure` and valid `model-pass` rows inform capability. Repair and
rerun the rest. If a global routing or loading bug affects the suite, invalidate
the suite rather than selectively trusting favorable rows.

### A4. Freeze the accepted evidence set

Write an accepted-run manifest listing trial IDs, included attempts, excluded
attempts, reasons, hashes, and the evaluator revision. Downstream scripts must
read this manifest rather than globbing an output directory.

## Stage B: reconstruct attempts and test reachability

### B1. Preserve raw and normalized views

Keep raw response text and logs immutable. Create normalized records separately.
Link both by content hash.

### B2. Reconstruct the applied candidate

Do not assume the final assistant message equals the tested code or state.
Capture parsing, patch application, file writes, tool actions, and the exact
artifact passed to the oracle.

### B3. Record turn causality

For feedback evaluations, store:

```text
turn_input
assistant_action
applied_state_hash
oracle_feedback
next_turn_input
```

This establishes whether the model saw real feedback and whether its repair was
causally responsive.

### B4. Build the reachability matrix

For every declared test or assertion, record whether it was executed. If a
stage fails, propagate an explicit block reason to downstream tests. Do not
manufacture expected/observed comparisons for unexecuted cases.

Report at least:

```text
declared tests
executed tests
observed passes
observed failures
build-blocked
runtime-blocked
harness-invalid
```

## Stage C: isolate failure mechanisms

### C1. Start with the terminal boundary

Identify the earliest stage at which the tested artifact cannot proceed. This
is the first authorized target for synthesis, not necessarily the only defect.

### C2. Compare independent attempts

Use repeated attempts as natural interventions:

- same diagnostic across attempts strengthens a stable mechanism;
- different diagnostics suggest multiple routes or prompt instability;
- one pass among failures demonstrates latent capability;
- a successful feedback repair demonstrates recoverability, not first-pass
  reliability;
- identical output hashes show the attempts were not actually independent.

### C3. Add discriminating probes

Where logs permit multiple explanations, write the smallest probe that separates
them. Examples include an isolated include, one alternative boundary input, a
second translation unit, a reordered state transition, or a replay with the
same tool permission.

### C4. Produce the task packet

Write one packet per underlying task, even if it has many trials. Include:

```text
task identity and hashes
valid attempt IDs
terminal stages
diagnostics and counterexamples
test reachability totals
candidate and applied-state hashes
cross-attempt and cross-turn comparison
primary and secondary mechanisms
evidence tier
unresolved rival explanations
next probe
synthesis disposition
```

## Stage D: authorize or reject synthesis

Synthesis is authorized only when the evidence identifies a behavior that a new
task and oracle can express without reproducing the held-out task.

### Authorized patterns

- exact contract or action errors with replayable proof;
- build, type, API, linkage, or portability failures with isolated probes;
- executed semantic counterexamples;
- unstable first-pass selection where valid alternate attempts exist;
- concise repairs driven by real feedback;
- prerequisite gaps that can be decomposed into verified tasks.

### Unauthorized patterns

- invalid evaluation runs;
- ambiguous specifications;
- unexecuted tests treated as failures;
- a general “reasoning weakness” label without a discriminating oracle;
- variants that differ only in nouns, names, or formatting;
- exact or near-exact benchmark reconstruction;
- targets sourced from unverified model output.

Assign `probe-first`, `eval-repair`, `eval-only`, or `reject` when synthesis is
not authorized.

## Stage E: design new tasks and discriminating oracles

### E1. Design the oracle before the target

Specify observable behavior, boundaries, invalid behavior, protected state,
resource limits, and success criteria. Ensure the task is unambiguous to a
competent solver who cannot see hidden tests.

### E2. Add a measurable delta

Every descendant must add at least one independently useful dimension:

- new boundary or state transition;
- new API or representation constraint;
- new failure-class discriminator;
- new integration, isolation, or portability probe;
- new scale or complexity requirement;
- new composition of prerequisites;
- meaningful domain transfer that changes the solution cues.

Record the delta. If it cannot be named, reject the variant as a cosmetic reskin.

### E3. Build negative controls

Require at least:

1. the original starter or incomplete state;
2. a mutation reproducing the diagnosed failure class;
3. a distinct candidate that compiles or executes but violates semantics.

An oracle that accepts these controls is not discriminating enough for SFT.

### E4. Use roles as a menu, not a quota

Foundation, API, boundary, adversarial, state, representation, efficiency,
genericity, composition, and capstone variants are useful coverage roles. Skip
roles that cannot add independent evidence.

### E5. Preserve honest provenance

Store parent task packet, generator, prompt, seed, model, editor, tests, and
revision hashes. Label close analyzed descendants as synthetic reliability
reinforcement. Do not claim organic provenance or independent generalization.

## Stage F: prove targets and negative controls

### F1. Execute answer-blind where possible

The verifier should consume task artifacts and candidate output without knowing
the selection decision. Keep the target solution separate from hidden oracle
inputs.

### F2. Record a per-row receipt

Include command lines, runtime image or tool versions, exit statuses, test and
assertion counts, negative-control outcomes, sanitizer or invariant outcomes,
hashes, duration, and captured logs.

### F3. Count evidence honestly

Separate:

- inherited tests replayed;
- new tests added;
- new oracle dimensions added;
- assertions executed;
- candidate variants rejected.

Do not describe wrappers, replays, or duplicated assertions as new semantic
coverage.

### F4. Replay after every material repair

Any change to task wording, starter state, target, tests, metadata that drives
verification, or serialized actions invalidates the old receipt. Rerun the full
oracle and create a new receipt linked to the prior revision.

## Stage G: prove exact SFT serialization

### G1. Render through the production path

Use the real data loader, chat template, tokenizer revision, special tokens,
loss mask, packing behavior, truncation policy, and EOS handling. Hash the
rendered bytes and token IDs when possible.

### G2. Parse the action from the target

For file-editing data, reconstruct every emitted file and compare it with the
proved target. For tool data, replay tool calls and assert final state. For
structured output, validate schema and semantics. Do not accept metadata claims
about what the response edits; inspect the response itself.

### G3. Assert action harmony

Check that the prompt, editable surface, emitted action, prose requirement,
protected state, and oracle all describe the same task. Common hard failures
include:

- returning an unchanged protected header;
- emitting files outside a source-only scope;
- omitting requested explanation before code;
- verifying one solution while training on another;
- leaking hidden tests or expected values into the conversation;
- declaring an approximate token count from a different template;
- training on a response truncated before the actionable content.

### G4. Refuse all rows with one systematic defect

If the same serialization failure affects an entire generated family, fail the
family. Do not average its score or approve a sample. Repair the generator,
regenerate, and reverify all descendants.

## Stage H: repair without hiding lineage

Use the smallest correction that restores the declared contract. Preserve
solution and tests when only serialization is defective; change them only when
their own evidence fails.

Record:

```text
revision_of
defect_class
defect_evidence
changed_fields
repair_tool_or_editor
old_and_new_hashes
full_replay_receipt
ancestor_disposition
```

Select the corrected row and remove the defective ancestor from positive
mixtures. Retain the ancestor only in an explicitly structured critique or
repair trajectory where it cannot become the imitation target.

## Stage I: audit the combined corpus

### I1. Resolve what the artifact already contains

Read manifests and row lineage before concatenating datasets. Avoid accidentally
doubling anchors or previous augmentations.

### I2. Deduplicate at several representations

Compare raw and normalized task IDs, messages, prompts, answers, tests, symbols,
file layouts, hashes, and lineage. Inspect semantic adjacency and template
families after exact collisions are removed.

### I3. Protect the held-out surface

Exclude exact task artifacts and group task families, source lineages, templates,
and revisions across splits. Report exact contamination separately from close
semantic adjacency.

### I4. Measure composition

Report source, provenance, family, mechanism, difficulty, role, token bucket,
oracle type, revision status, and answer mode. Measure first-token or template
monoculture, repeated easy cases, and high starter-copy ratios.

### I5. Bind the eligible dataset

Create a manifest that names every selected row and hashes the JSONL bytes,
tokenizer, chat template, verifier contract, row receipts, parent datasets, and
exclusion lists.

## Stage J: run a controlled training experiment

### J1. Pin the successful control

Use the last receipt-backed successful checkpoint and training configuration as
the standard. Produce a machine-readable diff before launching.

### J2. Authorize each difference

Dataset and checkpoint names must change. Other changes require a reason tied to
the iteration contract. Pay particular attention to effective batch, sequence
length, packing, optimizer updates, epoch-to-update conversion, chat template,
reasoning mode, and resume semantics.

### J3. Use bounded canaries

Run enough data and updates to expose serialization, loss, throughput, memory,
and obvious regression problems before a costly full run. Save receipts for
step time, tokens per second, memory, hardware utilization, and checkpoint
identity.

### J4. Preserve intermediate evidence

Even if only the final production checkpoint will be retained, canary and
evaluation records should make early overfit, under-training, and checkpoint
selection diagnosable.

## Stage K: evaluate and decide promotion

### K1. Freeze comparability

Use the same harness, task and test hashes, reasoning mode, decoding, tools,
turn contract, feedback timing, and trial count as the accepted control, except
for the candidate checkpoint identity.

### K2. Report the full transition matrix

Include task-by-trial results and transitions:

```text
fail -> pass
pass -> fail
fail -> fail with changed mechanism
pass -> pass
first-turn fail -> feedback repair
first-turn fail -> repeated failure
```

### K3. Keep metrics distinct

Report first-attempt success, sampled pass@1, pass@k when valid, conditional
repair, final multi-turn success, format validity, latency, tokens, and cost.
Do not combine two settings into an unexplained mean.

### K4. Apply the predeclared gate

Promote only on the requested held-out improvement with regression, validity,
and cost constraints satisfied. Otherwise keep the data receipts, reject or
revise the training hypothesis, and preserve the previous best checkpoint.

## Code-task proof profile

Use the strongest applicable profile:

```text
strict language-version build
warnings as errors
full public and hidden behavior tests
sanitizers or memory-safety tooling
isolated header or module import
protected-file byte comparison
multi-file or multi-translation-unit integration
determinism and repeat execution
complexity or resource probes
starter rejection
direct failure mutation rejection
distinct semantic mutation rejection
```

Adapt flags and tooling to the repository. Record unavailable checks and why.

## Agent and tool-task proof profile

Verify:

```text
valid tool schema and arguments
tool-result pairing
permission and sandbox contract
state before and after every action
idempotence or rollback where required
replay under the declared environment
final-state assertions
unrequested-action detection
failure and recovery behavior
token, latency, and call limits
```

Tool-shaped prose without replay is not a proved agent trajectory.

## Human-review protocol

Use human or model review for ambiguity, relevance, naturalness, and missed
counterexamples after deterministic gates. Require verdict, confidence,
contract evidence, concrete concern, and recommended disposition. Blind the
reviewer to the desired selection decision when practical.

Escalate disagreements, weak diagnoses, high-impact rows, and suspiciously
copied targets. Do not let a judge override a deterministic counterexample.

## Final report order

Lead with:

1. accepted and invalid evaluation evidence;
2. observed failures and masked tests;
3. diagnosed mechanisms and evidence strength;
4. synthesized, repaired, rejected, and eval-only counts;
5. executable and serialization gate results;
6. duplicates, lineage, contamination, and provenance;
7. exact eligible mixture and hashes;
8. training configuration diff and canary results;
9. held-out transitions and promotion decision;
10. unresolved risks and the next falsifiable probe.

This order prevents a high aggregate score from hiding invalid evidence or
systematic row defects.
