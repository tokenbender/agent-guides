---
name: tokenbending-etl
description: >-
  Deliver an Executive Tech Lead ("tokenbending-etl") update combining top-line
  wall-clock and unit-economics impact with a measured stage-by-stage bottleneck
  table and an ROI-ranked engineering action plan. Use when the user asks for an
  Executive Tech Lead update, "tokenbending-etl", or whether scaling hardware or
  changing architecture will speed things up.
---

# Tokenbending ETL (Executive Tech Lead Update)

Answer engineering, scaling, or status questions at two altitudes at once: leadership gets immediate clarity on time, cost, and readiness at the top; engineers get a measured bottleneck table and ROI-ranked action plan right below.

## Step 0: Ground in Real Code & Receipts First
Never answer from generic systems intuition alone:
1. Read the actual run receipts, timing breakdowns, and hardware utilization logs in the repo or artifacts.
2. Read the exact concurrency, topology, batching, and launcher files that govern throughput so you distinguish what is **already built/allowlisted** from what requires new code or hits a pinned dependency limit.

## Required Structure

### 1. Executive View (Verdict, Turnaround & Unit Economics)
Open with a decisive heading stating the answer and headline impact up front, followed by 2–3 tight bullets:
- **Already proven vs. net-new:** State clearly whether the target setup already exists in code.
- **Wall-clock impact:** Compare baseline vs. target wall time and throughput (episodes/min, tokens/sec, minutes per gate) using measured numbers.
- **Unit economics:** Compare hourly burn vs. total cost per outcome (e.g., why `8x` at `2.7x` hourly cost halves total run cost at `6x` throughput).

### 2. Tech-Lead View (Stage-by-Stage Bottleneck Table)
Separate stages that scale linearly from stages bottlenecked by design, with clickable file links:

| Pipeline Stage | Scaling Status | Measured Timing / Busy % | Bottleneck Diagnosis |
| :--- | :--- | :--- | :--- |
| Name + `[file.py](file:///...)` | `Solved (~Nx linear)` / `Bottleneck #1` / `Operational limit` | Exact seconds, min, or GPU/CPU % | Exact mechanical cause (Amdahl barrier, straggler tail, idle VRAM, fixed sleep, I/O contention) |

Call out hard external or pinned-framework constraints in one crisp note beneath the table.

### 3. Concrete Action Plan (Ranked by ROI & Risk)
List 3–4 numbered actions ordered strictly from **highest speedup-per-hour / lowest risk** to **higher-effort or recipe-changing**:
1. **Zero-code config flips or existing-machinery wiring:** Exact config keys, effort (`config-only` or `~0.5 day`), and expected wall-clock savings.
2. **Pure dead-time / I/O / sleep removals:** Separate safe training/probe speedups from eval fidelity settings that must stay untouched.
3. **Recipe-altering scale levers (flagged explicitly):** Whenever a throughput knob alters optimization math or semantics (effective batch size, staleness, precision), flag it as a recipe decision rather than a free infra win.

## Tone & Anti-LLM-ism Rules
- **Cut operational housekeeping:** Never pad updates with operator chores ("logs saved", "GPUs shut down", "tests pass") unless explicitly asked.
- **Write direct human prose:** Prefer concrete clauses with real numbers over participial filler ("...while seamlessly ensuring...") and throat-clearing transitions.
- **Separate measured from projected:** Cite measured run timings as facts; state unmeasured speedups as bounded estimates tied to the exact bottleneck removed.
