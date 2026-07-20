---
name: tokenbending
description: Use when planning, launching, tracking, or preserving experiments across projects, especially to separate deterministic operating rules from fuzzy experiment-defining variables that require clarification before costly or irreversible work, and to ensure any residual compatibility, migration, cleanup, or risk is tracked rather than left hanging.
---

Yes. Examples would make it much more usable because they turn the rule from taste into a decision boundary.

**Deterministic Rules With Examples**

Use the project's canonical tracking surface as the experiment log.
Example: If the project uses GitHub issues, update the issue when a run starts, when a stage completes, when a failure occurs, and when artifacts are uploaded.
Example: If the project uses a lab notebook or `runs/README.md`, append the command, config, result summary, and artifact path there.

Keep changes atomic and reviewable.
Example: Commit "add experiment spec" separately from "fix distributed launcher."
Example: Do not mix README cleanup, runner code, and generated data into one commit.

Verify before reporting completion.
Example: Do not say "uploaded" until the destination lists the expected files.
Example: Do not say "training is distributed" until process/GPU state or logs confirm multiple workers.

Do not leave hanging work implicit.
Example: If a temporary compatibility endpoint, migration alias, fallback script, manual workaround, unresolved verification, or cleanup step remains, create or link a follow-up issue before calling the work done.
Example: Do not write "follow-up: none" when any known duct tape, residual risk, or future cleanup still exists; make the remaining work durable in the project's tracking surface.

Preserve reproducible state before deleting compute resources.
Example: Upload configs, logs, checkpoints, summaries, and command history before terminating a pod.
Example: If upload fails, keep the machine alive or create a smaller fallback bundle before cleanup.

Do not upload secrets, tokens, caches, or third-party base assets unless explicitly authorized.
Example: Upload adapter weights and run logs, but exclude API keys and model cache directories.
Example: Preserve a manifest saying which external base model must be re-downloaded instead of copying the full base model.

Clean up costly resources after preservation is verified.
Example: Delete an experiment VM after artifact upload is listed and checksummed.
Example: Leave unrelated shared infrastructure alone unless the user asked to clean it too.

If the user says stop at first failure, stop at the first substantive failure.
Example: A syntax check failure means stop, report it, and do not launch the long run.
Example: If stage 2 crashes after stage 1 succeeds, preserve stage 1 outputs and do not proceed to stage 3.

Honor exact named constraints.
Example: If the user specifies a particular GPU type, verify the actual GPU model before running.
Example: If the user specifies a held-out dataset, do not silently swap in a convenient alternative.

Prefer resumability.
Example: Save the exact command line, config, environment notes, logs, and output manifest.
Example: Make the artifact bundle sufficient for a new machine to continue from the last valid checkpoint.

Gate paid or long accelerator runs with a full-load profile smoke.
Example: Before launching full training on paid GPU/TPU compute, sweep the viable batch, gradient accumulation, packing, compile, checkpointing, and logging settings on a realistic smoke run; record step time, tokens/sec, memory, estimated MFU, and the chosen profile.
Example: Do not spend the full run on a low-utilization profile unless the user explicitly accepts the efficiency tradeoff or the controlled experiment forbids changing the profile.

**Fuzzy Clarification Rules With Examples**

Clarify the exact research question when ambiguous.
Example: "Are we testing whether the smaller subsystem alone performs the task, or whether the full system works after replacing that subsystem?"
Example: "Is the goal best absolute score, smallest viable subsystem, or a clean comparison to a prior method?"

Clarify fixed variables versus allowed variables.
Example: "Should dataset, model, metric, and evaluation mode stay fixed while only the training method changes?"
Example: "Can I change batch size and launcher details for stability, or are those part of the controlled experiment?"

Clarify the comparison baseline.
Example: "Which prior result is the baseline: best known score, most recent run, or same-budget run?"
Example: "Should this compare against the unmodified base, an earlier trained variant, or a manually selected region?"

Clarify the success metric.
Example: "Is success judged by accuracy, judge score, recovery percentage, latency, cost, or Pareto frontier?"
Example: "If two candidates tie on score, should smaller size or lower training cost win?"

Clarify the evaluation mode.
Example: "Should we evaluate the modified component inside the full system or isolated from the rest?"
Example: "Should non-selected components be zeroed, mean-ablated, patched from a baseline, or left untouched?"

Clarify data roles.
Example: "Which split is training, which is calibration/attribution, and which is held out?"
Example: "Can seed examples overlap with training data, or must they be separated?"

Clarify mandatory versus discretionary methods.
Example: "Is this method required, or can I choose a stronger equivalent?"
Example: "Should I reproduce the previous method exactly before adding the new variant?"

Clarify failure policy.
Example: "If training crashes, should I stop and preserve state, retry with the same spec, or make an engineering fix and continue?"
Example: "If the judge service is down, should I pause or fall back to a secondary metric?"

Clarify run grade.
Example: "Is this a quick probe where partial data is acceptable, or a benchmark-grade run requiring full provenance?"
Example: "Should I optimize for fastest signal or publishable reproducibility?"

Clarify artifact policy.
Example: "Should checkpoints be uploaded, or only logs and summaries?"
Example: "Should failed-run artifacts be preserved, deleted, or marked as partial?"

Clarify residual-work policy.
Example: "If we keep a compatibility shim or temporary fallback after this change, should I open a follow-up issue now or complete the cleanup before closeout?"
Example: "Can this risk remain as documented debt, or is the acceptance bar that all migration/cleanup work is complete before the issue closes?"

Clarify resource authority.
Example: "May I create new cloud compute, or must I reuse existing machines?"
Example: "May I terminate only resources created for this run, or also older matching resources?"

That would make the guidance both general and enforceable.
