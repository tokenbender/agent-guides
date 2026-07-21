# METR Time Horizon Data (TH v1.1, updated May 8, 2026)

Source: [metr.org/time-horizons](https://metr.org/time-horizons/) — raw data `benchmark_results_1_1.yaml`. Horizons in **minutes** of human-expert-equivalent task time. Task suite: HCAST + RE-Bench + SWAA + shorter novel software tasks (SWE, ML, cybersecurity; self-contained, auto-scored).

> Measurements above 16 h (960 min) are unreliable — the task suite saturates.

## Frontier model table

| Model | Release | p50 horizon (min) | p50 ≈ | p80 horizon (min) | CI on p50 (min) |
|---|---|---|---|---|---|
| GPT-2 | 2019-02 | 0.05 | 3 s | 0.01 | — |
| davinci-002 | 2020-05 | 0.14 | 8 s | 0.06 | — |
| GPT-3.5 Turbo | 2022-03 | 0.6 | 36 s | 0.26 | — |
| GPT-4 | 2023-03 | 4.0 | 4 min | 0.9 | 1.9–8.0 |
| GPT-4o | 2024-05 | 7.0 | 7 min | 1.3 | 4.0–12.9 |
| Claude 3.5 Sonnet (Oct) | 2024-10 | 20.5 | 21 min | 2.6 | 10.1–40.8 |
| o1 | 2024-12 | 38.8 | 39 min | 7.1 | 21.2–65.0 |
| Claude 3.7 Sonnet | 2025-02 | 60.4 | 1 h | 12.1 | 33.0–104.2 |
| o3 | 2025-04 | 119.7 | 2 h | 30.0 | 74.6–190.9 |
| Claude Opus 4 | 2025-05 | 100.4 | 1.7 h | 20.4 | 60.0–163.5 |
| GPT-5 | 2025-08 | 203 | 3.4 h | 38.3 | 112.6–405.6 |
| Claude Opus 4.5 | 2025-11 | 293 | 4.9 h | 49.4 | 161.7–623.7 |
| Gemini 3 Pro | 2025-11 | 224 | 3.7 h | 54.1 | 139.6–379.2 |
| GPT-5.1 Codex Max | 2025-11 | 224 | 3.7 h | 50.6 | 134.3–396.2 |
| GPT-5.2 | 2025-12 | 352 | 5.9 h | 66.0 | 198.1–815.2 |
| Claude Opus 4.6 | 2026-02 | 719 | 12 h | 69.9 | 316.7–3633.8 |
| GPT-5.3-Codex | 2026-02 | 350 | 5.8 h | 54.7 | 194.9–816.4 |
| Gemini 3.1 Pro | 2026-02 | 384 | 6.4 h | 89.8 | 233.5–694.8 |
| GPT-5.4 | 2026-03 | 342 | 5.7 h | 53.9 | 186.6–768.8 |
| Claude Mythos Preview (early) | 2026-04 | 1045 | 17.4 h ⚠️ | 185.9 | 508.9–3304.3 |

⚠️ Above the 16 h reliability ceiling.

Not yet measured by METR as of May 2026: Claude Opus 4.7, Grok 4.3, GPT-5.5.

## Doubling-time statistics (from the same dataset)

| Fit window | Doubling time | Notes |
|---|---|---|
| All-time (2019–2026, stitched) | ~188 days (~6.2 mo) | — |
| From 2023 onward | ~129 days (~4.3 mo), CI 104–158 | Excludes p50 > 16 h points |
| Post-2024 (secondary sources) | ~90–130 days | Acceleration cited by METR and others |

## Methodology notes that matter for estimation

- **The logistic model**: $p = \sigma(\beta(\log h - \log t))$. Average $\beta \approx 0.6$ across the original suite; recent models fit $\beta \approx 0.8$ (p80 ≈ p50/5.7). Use 0.8, sanity-check against the table's p80 column.
- **Horizon ≠ runtime.** Horizon is a *difficulty* measure in human-time units. Agents finish successful tasks several times faster than the human baseline (fewer actions, one-shot code).
- **Low-context calibration.** Human baselines are skilled contractors (~5 yrs experience, top-100 universities) with *no prior context* on the task. Treat "2-hour task" as "2 hours for a capable new hire," not for the resident expert.
- **Near-horizon variance is huge.** A model with 2 h horizon on 1.5–3 h tasks: 100% success on ~⅓ of tasks, 0% on ~⅓, mixed on the rest. p is a population average, not a per-task guarantee.
- **Messiness penalty.** Models do worse on underspecified/messy tasks and under holistic vs algorithmic scoring (METR Aug 2025 follow-up). This is the basis for the ×2–8 difficulty multipliers.
- **Scaffold matters.** Different scaffolds (ReAct, Triframe, Claude Code, Codex) move measured horizons; elicitation quality is worth roughly ×1.5–2.
- **Domain jaggedness** (METR Jul 2025, 9 benchmarks): SWE/math/QA cluster at 50–200+ min horizons doubling every 2–6 months; agentic GUI (OSWorld/WebArena) ~40–100× shorter; self-driving doubling ~20 months. No domain shows sub-exponential progress.
- **Suite saturation.** TH v1.1 can't measure beyond ~16 h. Mythos Preview's 17.4 h is an extrapolated fit, flagged by METR itself.

## Trend projection table (for unlisted models)

Anchor: Claude Mythos Preview, p50 ≈ 1045 min, April 2026.
With D = 130 days (fast) / 150 days (default) / 190 days (slow):

| Months after Apr 2026 | D=130 | D=150 | D=190 |
|---|---|---|---|
| +3 (Jul 2026) | ~1700 min | ~1600 min | ~1450 min |
| +6 (Oct 2026) | ~2800 min | ~2450 min | ~2050 min |
| +12 (Apr 2027) | ~7600 min | ~5800 min | ~3900 min |

Cap confidence at 16 h (960 min) unless the task suite caveat is stated.
