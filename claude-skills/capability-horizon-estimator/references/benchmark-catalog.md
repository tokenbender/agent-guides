# SWE / MLE / Math Benchmark Catalog — Task Times & SOTA (July 2026)

Benchmarks that measure frontier capability, ordered by human task duration. Use the task-time columns as anchors when estimating human-equivalent $t$.

## Software engineering

| Benchmark | What it tests | Human task time | Agent time budget | SOTA (July 2026) |
|---|---|---|---|---|
| **SWAA** (METR) | Atomic software actions (clicks, commands) | 1 s – 1 min | seconds | Saturated for frontier models |
| **SWE-bench Verified** | 500 real GitHub issues, human-validated | 7 min – 2 h per issue (OpenAI annotations, *engineer familiar with codebase*) | minutes–1 h per issue | ~88–95% (GPT-5.5 88.7%, Opus 4.8 88.6%; Fable 5 95% suspended) — **saturating + contamination found** (verbatim gold patches reproducible) |
| **SWE-bench Pro** | Harder, contamination-resistant repo tasks | hours per task | hours | ~80% top (Mythos 5, 80.3%) — note: OpenAI audit flagged ~30% broken tasks on public split |
| **HCAST** (METR) | 189 tasks: ML eng, cyber, SWE, general reasoning | 1 s – 8+ h (human-baselined) | up to hours per task | Core of METR horizon suite |
| **RE-Bench** (METR) | 7 ML research-engineering tasks (optimize kernel, fix embedding, scale law, etc.) | 8 h expert budget | 8 h per attempt (vs humans head-to-head) | Agents beat humans on some, lose on hard-open-ended; core of horizon suite |
| **SWE-Lancer** (OpenAI) | 1,400+ real Upwork tasks, $1M total payouts | hours–days per task (freelance) | per-task runs | Early 2025: best ~40% of $ (Claude 3.5S); IC tasks ~26%. **Task $ value is a poor difficulty proxy** (METR) |
| **Terminal-Bench** | Terminal/CLI agent tasks | minutes–hours | minutes–hours | Active leaderboard 2026 |
| **LiveCodeBench** | Competitive programming, contamination-controlled | 4 min – 1.5 h per problem | single attempts | Strong time↔difficulty correlation (β high); good horizon proxy |

## ML engineering & research

| Benchmark | What it tests | Human task time | Agent time budget | SOTA (July 2026) |
|---|---|---|---|---|
| **MLE-bench** (OpenAI) | 75 Kaggle competitions, medal rate | days–weeks of human Kaggle effort per comp | ~24 h per comp (typical agent setups) | ~56% medal rate (ML-Master 2.0); frontier agents medal on majority of easy comps, few hard ones |
| **RE-Bench** | See above | 8 h | 8 h | — |
| **AI R&D automation suites** (METR risk reports) | End-to-end research tasks | 8–40+ h | hours–days | Tracked in METR risk reports; suite saturation above ~16 h |

## Math & long-horizon reasoning

| Benchmark | What it tests | Human task time | Agent time | SOTA (July 2026) |
|---|---|---|---|---|
| **MATH / MATH-500** | High-school competition math | 2 s – 30 min | seconds–minutes | Saturated (97%+) |
| **AIME / Mock AIME** | Top-5% HS contest, 15 problems / 3 h | 5 min – 4 h per problem | minutes with reasoning | Near-saturated for frontier; **fastest-rising horizon domain (~3-month doubling)** |
| **GPQA Diamond** | PhD-level science MCQ | 5 min – 3 h per question | minutes | Saturating at top; time↔difficulty correlation weakens at saturation |
| **FrontierMath T1–T3** (Epoch) | Research-level unpublished problems | hours–days for expert mathematicians | hours (tool-use allowed) | Frontier models solve meaningful fractions; GPT-5.4 Pro solved hard problems via literature search |
| **FrontierMath T4** (v2) | 43 private extreme problems | days–weeks for experts | hours–days | Hardest standing math eval; low solve rates; v1 audit flagged ~⅓ problems with errors — v2 corrected |
| **Humanity's Last Exam** | Expert-level cross-domain QA | minutes–hours per item | minutes | Frontier ~30–50% and climbing |
| **Cybench** (Stanford) | 40 professional CTF challenges | minutes–11 h (human CTF players) | per-challenge agent runs | Used in METR cyber evaluations |

## Cross-domain horizon summary (METR, Jul 2025)

| Domain cluster | 50% horizon (Mar 2025) | Doubling | Notes |
|---|---|---|---|
| SWE / reasoning (METR-HRS, LCB, AIME, GPQA) | 50–200+ min | 2–6 months | The "intellectual" cluster |
| Agentic GUI (OSWorld, WebArena) | ~1–5 min (40–100× shorter) | similar rate, ~2 yrs behind | 75% of OSWorld failures = mouse-click inaccuracy |
| Video QA (VideoMME) | >60 min (weak length↔difficulty link) | n/a | Horizon metric not appropriate |
| Self-driving (Tesla FSD) | mean time to disengagement | ~20 months | Slowest measured domain |

## Using this catalog for anchoring

1. Find the row whose "Human task time" bracket contains your task.
2. Read off $t$ (use geometric mean of the bracket).
3. If the benchmark is noted as *saturating*, that tells you frontier $h$ exceeds the suite ceiling — treat as floor, not measurement.
4. Benchmark tasks are cleaner than real work — apply the SKILL.md messiness multiplier when your task is not self-contained and auto-verifiable.
