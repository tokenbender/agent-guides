---
name: tokenbending-preflight
description: >-
  Run a zero-dollar, line-by-line spec-vs-code audit ("Preflight") before writing
  implementation code or spinning up paid compute. Use when the user asks to
  "preflight" or "tokenbending-preflight" an issue, spec, plan, or run, or asks
  how solid a spec is and what blindspots exist before execution.
---

# Tokenbending Preflight

Preflight is a zero-dollar, line-by-line engineering gate run **before** writing implementation code or launching paid compute. Never accept an issue or architecture spec from prose summaries alone.

## Protocol

### 1. Read Every Touched File & Binary Boundary
Read the target spec alongside **every concrete file, binary layout, C++/CUDA kernel, CLI interface, and downstream consumer** it touches:
- Check exact tensor shapes, memory strides, block alignment, and dtype/quantization invariants.
- Check path conventions, resume/cache keys, and host/container constraints (`noexec` `/dev/shm`, FUSE vs NVMe, overlay disk stalls, PEP 668, NUMA/MPS).
- Check downstream milestones in the queue so a local shortcut today does not plant a landmine for the next issue.

### 2. Score the Spec Honestly (`1–10`)
Assign a candid readiness score to the spec *as currently written*:
- `< 7`: Missing critical mechanics or contains silent correctness/eval blockers.
- `7–8.5`: Right high-level design, but concrete codebase, math, or infra blindspots will fail or degrade results mid-run.
- `9–10`: Interfaces, invariants, controls, edge cases, and verification gates are locked.

### 3. Surface Concrete Blindspots + Minimal Fixes
List every blindspot with **exact `file:line` references**, stating:
1. **The blindspot:** What fails, drifts, leaks memory, or degenerates (e.g., broken negative controls, shared quantization blocks, wrong cache keys, single-stream I/O bottlenecks).
2. **The fix:** The smallest clean engineering change that eliminates the failure mode without breaking backward compatibility on saved receipts.

### 4. Lock the Spec & Exhaust \$0 Real-Artifact Proof First
- Always present preflight design forks and sign-off choices via the interactive questionnaire tool (`ask_question`) rather than plain-text bullets; wait for user alignment before editing implementation files or spending compute (unless pre-authorized).
- Once approved, tighten the spec/issue first, then verify **everything possible locally at \$0 against real artifacts** (real C++ compilation, real tiny checkpoints, exact byte/SHA256 parity on real files, dry-runs over saved receipts). Do **not** invent synthetic/mock unit tests or add unrequested docs/comments.
- When paid hardware is required, design for full hardware saturation, per-stage durable artifact sync, and an automatic `EXIT` teardown trap so zero idle compute is billed.
