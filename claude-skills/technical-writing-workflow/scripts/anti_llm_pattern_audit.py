#!/usr/bin/env python3
"""Scan prose for common generated-writing tells."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS: list[tuple[str, str]] = [
    ("em dash", r"—"),
    ("not only / but also", r"\bnot only\b.+\bbut also\b"),
    ("in conclusion", r"\bin conclusion\b"),
    ("in summary", r"\bin summary\b"),
    ("moreover", r"\bmoreover\b"),
    ("furthermore", r"\bfurthermore\b"),
    ("it is worth noting", r"\bit'?s worth noting\b|\bit is worth noting\b"),
    ("delve", r"\bdelve(?:s|d|ing)?\b"),
    ("landscape", r"\blandscape\b"),
    ("robust", r"\brobust\b"),
    ("seamless", r"\bseamless\b"),
    ("holistic", r"\bholistic\b"),
    ("unlock", r"\bunlock(?:s|ed|ing)?\b"),
    ("empower", r"\bempower(?:s|ed|ing)?\b"),
    ("groundbreaking", r"\bgroundbreaking\b"),
    ("revolutionary", r"\brevolutionary\b"),
    ("transformative", r"\btransformative\b"),
    ("game-changing", r"\bgame[- ]changing\b"),
    ("ultimate guide", r"\bultimate guide\b"),
    ("x explained title", r"\bexplained\b"),
]


def iter_lines(path: Path):
    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        yield lineno, line


def audit(path: Path) -> int:
    hits = 0
    print(f"# Anti-LLM pattern audit: {path}")
    for lineno, line in iter_lines(path):
        lower = line.lower()
        for label, pattern in PATTERNS:
            if re.search(pattern, lower, flags=re.IGNORECASE):
                hits += 1
                print(f"{path}:{lineno}: {label}: {line.strip()}")
    if hits == 0:
        print("No flagged patterns found.")
    else:
        print(f"\nFlagged patterns: {hits}")
    return 1 if hits else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    status = 0
    for path in args.paths:
        if not path.exists():
            print(f"{path}: missing")
            status = 1
            continue
        status = max(status, audit(path))
    return status


if __name__ == "__main__":
    raise SystemExit(main())

