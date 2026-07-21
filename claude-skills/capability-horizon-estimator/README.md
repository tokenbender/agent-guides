# Capability & Time Horizon Estimator

Estimate whether a frontier AI model can complete a task — and how long it will take — using the METR time-horizon framework.

Every task has a human-equivalent duration $t$; every model has a 50% time horizon $h_{50}$; success probability follows a logistic curve in $\log(h/t)$. This skill packages the model, the data, and a calculator.

## Contents

| File | What it is |
|------|-----------|
| [`SKILL.md`](SKILL.md) | The 6-step estimation workflow: anchor human time → get $h_{50}$ → logistic $p$ → difficulty multipliers → scaffold/best-of-N uplift → wall-clock |
| [`references/horizon-data.md`](references/horizon-data.md) | METR TH v1.1 per-model p50/p80 table (GPT-2 → Claude Mythos, May 2026), doubling stats, methodology caveats, projection table |
| [`references/benchmark-catalog.md`](references/benchmark-catalog.md) | 20+ SWE/MLE/math benchmarks with human task times and July 2026 SOTA — the anchoring table |
| [`scripts/estimate.py`](scripts/estimate.py) | Dependency-free calculator: success probability, β sensitivity band, best-of-N, wall-clock |

## Quick use

```bash
# 4-hour task on a 12-hour-horizon model (Claude Opus 4.6)
python3 scripts/estimate.py --h50 719 --task-min 240
# → SINGLE ATTEMPT: 70.6%  VERDICT: LIKELY  WALL-CLOCK: ~48 min

# Extrapolate an unlisted model from a reference point
python3 scripts/estimate.py --ref-h50 1045 --ref-date 2026-04-07 \
    --model-date 2026-07-21 --task-min 480

# Messy real-world task, pushed with scaffold + retries
python3 scripts/estimate.py --h50 293 --task-min 480 \
    --messiness 4 --scaffold-boost 1.75 --attempts 6
# → 26% single attempt → 83% best-of-6
```

## The model in one breath

$$p_{\text{success}} = \sigma\!\big(\beta \ln(h_{50}/t)\big), \quad \beta \approx 0.8$$

Horizons double every ~130–190 days (METR: 129 days since 2023). Difficulty multipliers adjust $t$: ×1 clean/verifiable, ×2 proprietary codebase, ×4 messy, ×50–100 GUI. Agents run 3–8× faster than the human baseline on tasks they can do.

## Data sources

- [METR Time Horizons](https://metr.org/time-horizons/) (raw: `benchmark_results_1_1.yaml`, May 2026)
- [METR: How Does Time Horizon Vary Across Domains?](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/)
- [Measuring AI Ability to Complete Long Tasks](https://arxiv.org/abs/2503.14499) (Kwa & West et al.)
- Benchmark SOTA from public leaderboards, July 2026

## Honest limits

- METR's suite saturates at 16 h human-equivalent — estimates beyond that are extrapolation
- Horizons are calibrated on low-context contractors, not resident experts
- Near the horizon, per-task outcomes vary wildly (⅓ always pass, ⅓ always fail, ⅓ mixed)
- GUI/computer-use is a separate capability cluster, ~40–100× behind SWE
