---
name: capability-horizon-estimator
description: Estimate whether an AI model can complete a task and how long it will take, using METR-style time-horizon modeling. Use when scoping agent work, deciding if a task is within reach, planning retries/parallelism, estimating wall-clock time for SWE/MLE/math tasks, or answering "can you do this" / "how long will this take" for autonomous work.
---

# Capability & Time Horizon Estimator

Estimate what a model can do and how long it takes using the METR time-horizon framework: every task has a human-equivalent duration $t$, every model has a 50% time horizon $h_{50}$, and success probability follows a logistic curve in $\log(h/t)$.

## When to use

- "Can you do X autonomously?" — give a calibrated yes/maybe/no instead of vibes
- "How long will this agent run take?" — wall-clock estimate with retry overhead
- Scoping: should this be one task, or decomposed?
- Deciding attempt budget (best-of-N) for a stretch task

## The core model

**Step 1 — Estimate human-equivalent task time $t$ (minutes).**
Anchor against known reference points (full table in `references/benchmark-catalog.md`):

| Reference task | Human time |
|---|---|
| SWE-bench Verified issue | 7 min – 2 h |
| HCAST task bands | 15 min / 1 h / 4 h / 8 h |
| RE-Bench ML research task | 8 h |
| Small bug fix, clear repro | 15–60 min |
| Multi-file feature | 2–8 h |
| Cross-repo refactor | 4–16 h |
| Kaggle competition (MLE-bench) | days of human effort |
| FrontierMath T4 problem | days–weeks of expert time |

Estimate for a *low-context* professional (new hire, contractor), not the resident expert — that is what the horizons are calibrated against.

**Step 2 — Get the model's horizon $h_{50}$ (minutes).**
Look it up in `references/horizon-data.md` (METR TH v1.1, May 2026). If the model isn't listed, extrapolate from release date:

$$h_{50}(\text{date}) = h_{50}(\text{ref}) \times 2^{(\text{date} - \text{ref}) / D}, \quad D \approx 130\text{–}190 \text{ days}$$

Use $D = 150$ days as default; state the range. Post-2024 data supports faster ($\sim$90–130 days); all-time average is $\sim$190.

**Step 3 — Success probability.**

$$p = \sigma\!\big(\beta \cdot \ln(h_{50}/t)\big), \quad \beta \approx 0.8 \text{ (range 0.6–0.9)}, \quad \sigma(x) = \frac{1}{1+e^{-x}}$$

Sanity anchors with $\beta = 0.8$: $t = h_{50} \Rightarrow p = 50\%$ · $t = h_{50}/5.7 \Rightarrow p = 80\%$ · $t = 2h_{50} \Rightarrow p \approx 36\%$ · $t = 4h_{50} \Rightarrow p \approx 25\%$.

**Step 4 — Difficulty adjustments (multiply $t$ before Step 3).**

| Condition | Multiplier on $t$ |
|---|---|
| Well-specified, auto-verifiable (benchmark-like) | ×1 |
| Proprietary/large codebase, high prior context needed | ×2 |
| Messy, underspecified, human-judged success | ×4 (range ×2–8) |
| GUI/computer-use (no API/DOM) | ×50–100 — different capability cluster |
| Parallelizable/additive work (N independent items) | Not one task — split, apply model per piece |

Rationale: METR's suite is clean and self-contained; models do measurably worse on messy tasks and under holistic (vs algorithmic) scoring. GUI horizons measured ~40–100× shorter than SWE/reasoning.

**Step 5 — "Pushed itself" uplift.**
- Better scaffold/elicitation: ×1.5–2 on $h_{50}$ (scaffold choice moves measured horizons ~2×)
- Best-of-N independent attempts: $P(\geq 1 \text{ success}) = 1 - (1-p)^N$
- Both compose. A $p = 0.25$ task with a good scaffold ($\times 1.75 h$) and 6 attempts: $p \to \sigma(0.8 \ln(1.75 \cdot h/t)) \approx 0.37$ per attempt, $1-(1-0.37)^6 \approx 94\%$.

**Step 6 — Wall-clock time.**
Agents complete tasks they *can* do several times faster than the human baseline:

$$\text{wall-clock} \approx \frac{t_{\text{human}}}{S} \times \text{expected attempts}, \quad S \approx 3\text{–}8\times \text{ for SWE (default 5)}$$

Expected attempts $= 1/p$ for independent retries (cap at 3–5 in practice; if it fails 3×, the plan is wrong, not the luck). Report a range, not a point.

## Output format

```
TASK: <one line>
HUMAN-EQUIVALENT TIME (t): <estimate> (anchor: <reference task>)
MODEL HORIZON (h50): <value> (source: table / extrapolated from <date>, D=150d)
DIFFICULTY: ×<mult> (<reason>)  → effective t = <value>
SINGLE-ATTEMPT SUCCESS: <p> → <verdict>
PUSHED (scaffold ×1.75, N=<n>): <p_eff> per attempt, <P> overall
WALL-CLOCK ESTIMATE: <range> (t/S × attempts, S=5)

VERDICT: CONFIDENT (≥80%) | LIKELY (60–80%) | COIN-FLIP (35–60%) | STRETCH (15–35%) | OUT OF REACH (<15%)
CAVEATS: <extrapolation flags, messiness, jagged-domain warnings>
DECOMPOSITION ADVICE: <if stretch/out-of-reach: where to split>
```

## Calibration rules

- **Always state the anchor.** Every $t$ estimate names the reference task it was derived from. No anchor, no number.
- **Report ranges.** Horizons have wide CIs (Opus 4.6 p50: 317–3634 min). Give the interval, pick the geometric mean for the headline.
- **Above 16 h human-equivalent, say so.** METR's suite saturates at 16 h; estimates beyond it are extrapolation, not measurement.
- **Jaggedness is real.** A model strong in SWE may be 50–100× weaker on GUI work, and different on math research. Never transfer a horizon across domains without the multiplier.
- **Long ≠ hard, hard ≠ long.** The model applies to *coherent, non-parallelizable* tasks. 1000 independent 1-hour problems is a 1-hour task done 1000 times.
- **Failure mode asymmetry.** Near the horizon, models fail by derailing (repeating failed approaches, losing state), not by slow progress. If $p < 50\%$, recommend decomposition over retries.

## Reference files

- `references/horizon-data.md` — METR TH v1.1 per-model p50/p80 table (2019 → May 2026), doubling-time stats, methodology caveats
- `references/benchmark-catalog.md` — SWE/MLE/math benchmark inventory with task times, human budgets, and July-2026 SOTA
- `scripts/estimate.py` — calculator for Steps 3–6 (logistic p, best-of-N, wall-clock)
