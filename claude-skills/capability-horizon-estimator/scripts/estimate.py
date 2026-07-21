#!/usr/bin/env python3
"""Capability & time-horizon estimator (METR-style logistic model).

Computes single-attempt success probability, best-of-N uplift, and wall-clock
estimate for an agent task, given a human-equivalent task time and a model
horizon.

Examples:
    # Direct horizon lookup (h50 in minutes)
    python estimate.py --h50 719 --task-min 240

    # Extrapolate horizon from a reference model + release-date gap
    python estimate.py --ref-h50 1045 --ref-date 2026-04-07 --model-date 2026-07-21 --task-min 480

    # Messy real-world task, push with 6 attempts
    python estimate.py --h50 719 --task-min 240 --messiness 4 --attempts 6 --scaffold-boost 1.75
"""

import argparse
import math
from datetime import date


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def verdict(p: float) -> str:
    for lo, name in [(0.80, "CONFIDENT"), (0.60, "LIKELY"), (0.35, "COIN-FLIP"), (0.15, "STRETCH")]:
        if p >= lo:
            return f"{name} (p={p:.0%})"
    return f"OUT OF REACH (p={p:.0%})"


def fmt_time(minutes: float) -> str:
    if minutes < 1:
        return f"{minutes * 60:.0f} s"
    if minutes < 60:
        return f"{minutes:.1f} min"
    if minutes < 60 * 24:
        return f"{minutes / 60:.1f} h"
    return f"{minutes / (60 * 24):.1f} days"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task-min", type=float, required=True, help="human-equivalent task time in minutes")
    ap.add_argument("--h50", type=float, help="model 50%% horizon in minutes (from references/horizon-data.md)")
    ap.add_argument("--ref-h50", type=float, help="reference model h50 for extrapolation")
    ap.add_argument("--ref-date", help="reference model release date YYYY-MM-DD")
    ap.add_argument("--model-date", help="target model release date YYYY-MM-DD")
    ap.add_argument("--doubling-days", type=float, default=150, help="horizon doubling time (default 150; range 90-190)")
    ap.add_argument("--beta", type=float, default=0.8, help="logistic slope (default 0.8; range 0.6-0.9)")
    ap.add_argument("--messiness", type=float, default=1.0, help="difficulty multiplier on t: 1 clean, 2 proprietary codebase, 4 messy/underspecified, 50-100 GUI")
    ap.add_argument("--scaffold-boost", type=float, default=1.0, help="horizon multiplier from good scaffold/elicitation (1.5-2 typical)")
    ap.add_argument("--attempts", type=int, default=1, help="independent attempts (best-of-N)")
    ap.add_argument("--speedup", type=float, default=5.0, help="agent speed vs human on successful tasks (3-8 typical for SWE)")
    args = ap.parse_args()

    # Resolve h50
    if args.h50:
        h50 = args.h50
        h_src = "direct lookup"
    elif args.ref_h50 and args.ref_date and args.model_date:
        d0 = date.fromisoformat(args.ref_date)
        d1 = date.fromisoformat(args.model_date)
        days = (d1 - d0).days
        h50 = args.ref_h50 * 2 ** (days / args.doubling_days)
        h_src = f"extrapolated: {args.ref_h50:.0f} min @ {args.ref_date}, D={args.doubling_days:.0f}d, +{days} days"
    else:
        ap.error("provide --h50 or all of --ref-h50/--ref-date/--model-date")

    h_eff = h50 * args.scaffold_boost
    t_eff = args.task_min * args.messiness

    p = sigmoid(args.beta * math.log(h_eff / t_eff))
    p_n = 1.0 - (1.0 - p) ** args.attempts

    # Wall clock: base duration at agent speed, scaled by expected attempts (capped)
    expected_attempts = min(1.0 / max(p, 1e-6), args.attempts)
    wall = args.task_min / args.speedup * expected_attempts

    # Sensitivity band: beta 0.6-0.9
    p_lo = sigmoid(0.6 * math.log(h_eff / t_eff))
    p_hi = sigmoid(0.9 * math.log(h_eff / t_eff))

    print(f"TASK:               {fmt_time(args.task_min)} human-equivalent"
          + (f" (x{args.messiness:g} difficulty -> {fmt_time(t_eff)} effective)" if args.messiness != 1 else ""))
    print(f"MODEL HORIZON h50:  {fmt_time(h50)} [{h_src}]"
          + (f" (x{args.scaffold_boost:g} scaffold -> {fmt_time(h_eff)})" if args.scaffold_boost != 1 else ""))
    print(f"SINGLE ATTEMPT:     {p:.1%}  (beta band 0.6-0.9: {min(p_lo, p_hi):.1%} - {max(p_lo, p_hi):.1%})")
    if args.attempts > 1:
        print(f"BEST-OF-{args.attempts}:         {p_n:.1%}  -> {verdict(p_n)}")
    else:
        print(f"VERDICT:            {verdict(p)}")
    print(f"WALL-CLOCK EST:     ~{fmt_time(wall)}  (t/{args.speedup:g} speedup x {expected_attempts:.1f} expected attempts)")
    if t_eff > 960:
        print("WARNING: effective task time > 16 h — beyond METR suite ceiling; extrapolation only.")
    if args.messiness >= 50:
        print("NOTE: GUI/computer-use tasks sit in a separate capability cluster (~40-100x shorter horizons); treat this estimate as very rough.")


if __name__ == "__main__":
    main()
