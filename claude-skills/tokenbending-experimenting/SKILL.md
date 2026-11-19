---
name: tokenbending-experimenting
description: >-
  Core engineering and experimentation operating rules ("tokenbending-experimenting").
  Use when planning, launching, debugging, verifying, or promoting ML experiments
  and framework changes—especially to operate from the highest-trust region, keep
  deltas causally atomic, avoid unrequested docs/comments and mock unit tests,
  verify on real artifacts, protect against preemption/idle burn, and clarify
  fuzzy experiment variables before spend.
---

# Tokenbending Experimenting

Deterministic operating rules for fast, honest, high-trust ML engineering—plus the fuzzy variables that must be clarified before costly or irreversible work.

## 1. Trust Region, Causal Deltas & Clean Promotion
- **Zero unrequested comments or documentation.** Do not add code comments, docstrings, README updates, architecture notes, or changelogs unless explicitly requested. Keep verification and tracking in issue comments or the response, never as automatic repo docs.
- **Operate from the highest-trust region.** Rank paths by direct live evidence for the same job: exact proven recipe first, proven components + one necessary delta second, new wrappers/shims/ports last. Never swap a working evaluator for a "cleaner" wrapper mid-experiment.
- **Make deltas causally atomic, not merely commit-sized.** State the one behavioral difference, smallest surface that produces it, expected effect, and rollback point before changing code.
- **Keep unproven code local.** Never commit or push an experiment path just to get a SHA; prove it live on the real image, hardware, model, and output path first.
- **Return to trust after failure.** When a new delta fails, restore the last proven state and isolate one cause instead of stacking shims on top.
- **Promote live-proven wins into the clean framework.** Once a speedup or control fix proves itself in a throwaway runner, promote the minimal, declarative, config-driven delta into the core library so future runs inherit it cleanly.

## 2. Real Verification, Zero Mock Anxiety
- **Verify on real artifacts, not synthetic unit tests.** Do not write ceremonial mock/stub unit tests out of anxiety. Prove correctness against real binaries, real checkpoints, exact byte/SHA256 parity, and real receipts.
- **Audit negative controls before trusting a win.** Confirm `empty` / no-op controls are bit-identical to `base`, shuffled labels are non-constant (balanced fallback on single-class feedback), and contrastive shuffles permute paired trajectories together.
- **Verify before claiming completion.** Never report "uploaded", "distributed", "closed", or "zero cost" until listings, GPU/process state, checksums, or billing queries confirm it.
- **Honor exact named constraints & stop-on-first-failure.** Verify the exact GPU model, dataset split, or budget requested. If the user says stop at first failure, halt at the first substantive error, preserve outputs, and report.

## 3. Compute, Durability & Cleanup Discipline
- **Reuse live-proven paid configs without ceremonial re-gating.** Run a realistic full-load profile smoke *only* when hardware, image, model, distributed topology, or material perf settings (batch, seq len, parallelism, checkpointing) are genuinely new.
- **Sync artifacts per stage to durable storage.** Write/upload masks, checkpoints, configs, and receipts to persistent storage (volume, Drive, local mirror) after *each* cell or stage—never wait until the end of a multi-GPU sweep where preemption can wipe outputs.
- **Preserve before teardown; then verify zero burn.** Confirm remote/local artifacts are listed and checksummed before terminating compute, then verify `0` active sessions / `\$0/hr`. Leave unrelated shared infra untouched.
- **Never upload secrets, caches, or third-party base weights** unless explicitly authorized; record pinned repo/commit/SHA256 manifests instead.

## 4. Clarify Fuzzy Variables Once Before Spend
Before launching costly or irreversible work, clarify any of these that are still ambiguous (ask once, concisely):

| Variable | Clarify if unclear |
| :--- | :--- |
| **Research question** | Best absolute score, smallest budget, subsystem-alone, or clean comparison to a prior method? |
| **Fixed vs. allowed** | Which knobs stay locked (model, split, metric, decode) vs. free for stability/speed? |
| **Baseline & metric** | Which baseline counts, primary metric, and tie-breaker (size, latency, cost)? |
| **Eval & data roles** | Full-system vs. isolated eval; exact train / calibration / select / sealed-exam boundaries. |
| **Method freedom** | Exact reproduction required, or stronger equivalent allowed? |
| **Failure & run grade** | Stop/preserve vs. fix-and-continue on crash; quick probe vs. benchmark-grade provenance? |
| **Artifacts & debt** | What to upload/keep; whether residual cleanup/risks can be tracked as follow-up issues. |
| **Resource authority** | May spin up new paid compute vs. reuse existing; what may be terminated. |

## 5. Style, Visuals & Reporting Honesty
- **Lead with truth, including caveats.** Never hide partial ties, eval variance, or compression floors behind green headlines.
- **Obvious visuals only.** Use unmistakable semantic encodings (e.g., Green = Built / Yellow = Partial / Red = Missing with a 1-line legend) rather than decorative multi-color pastels.
- **Cut housekeeping fluff.** Be terse and concrete; defer issue tracking and residual-work ledgers to `tokenbending-worklog`.
