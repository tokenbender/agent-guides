#!/usr/bin/env python3
"""Scan Markdown and LaTeX headings for weak or generated-sounding forms."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


WEAK_PATTERNS: list[tuple[str, str]] = [
    ("generic conclusion", r"^(conclusion|final thoughts|key takeaways|tl;dr|wrapping up)$"),
    ("ultimate guide", r"\bultimate guide\b|\beverything you need to know\b"),
    ("power/art/science/state of", r"^the (power|art|science|state|future|rise) of\b"),
    ("beyond/towards/rethinking", r"^(beyond|towards|rethinking)\b"),
    ("inside x", r"^inside\b"),
    ("x explained", r"\bexplained$"),
    ("comma-pair title", r"^[^,]{2,60}, [^,]{2,60}$"),
    ("colon subtitle", r".+:.+"),
    ("from x to y", r"^from .+ to .+"),
]


def extract_headings(path: Path):
    for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        stripped = line.strip()
        md = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if md:
            yield lineno, md.group(2).strip()
            continue
        tex = re.match(r"\\(?:chapter|section|subsection|subsubsection)\*?\{(.+)\}", stripped)
        if tex:
            yield lineno, tex.group(1).strip()


def audit(path: Path) -> int:
    hits = 0
    print(f"# Heading audit: {path}")
    for lineno, heading in extract_headings(path):
        normalized = re.sub(r"\s+", " ", heading).strip().lower()
        for label, pattern in WEAK_PATTERNS:
            if re.search(pattern, normalized):
                hits += 1
                print(f"{path}:{lineno}: {label}: {heading}")
    if hits == 0:
        print("No weak heading patterns found.")
    else:
        print(f"\nFlagged headings: {hits}")
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

