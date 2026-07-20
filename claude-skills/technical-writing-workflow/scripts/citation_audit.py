#!/usr/bin/env python3
"""Report URLs, citation-like markers, and paragraphs that may need sources."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s)}\\]+|file:/[^\s)}\\]+")
CLAIM_HINT_RE = re.compile(
    r"\b(show(?:s|ed)?|prove(?:s|d)?|demonstrate(?:s|d)?|report(?:s|ed)?|"
    r"state-of-the-art|outperform(?:s|ed)?|best|first|novel|"
    r"\d+(?:\.\d+)?%|\d+(?:\.\d+)?x)\b",
    re.IGNORECASE,
)


def paragraphs(text: str):
    start = 1
    buff: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip():
            if not buff:
                start = lineno
            buff.append(line)
        elif buff:
            yield start, " ".join(part.strip() for part in buff)
            buff = []
    if buff:
        yield start, " ".join(part.strip() for part in buff)


def audit(path: Path) -> int:
    text = path.read_text(errors="replace")
    urls = URL_RE.findall(text)
    print(f"# Citation audit: {path}")
    print(f"URLs found: {len(urls)}")
    for url in sorted(set(urls)):
        print(f"- {url}")

    risky = []
    for lineno, para in paragraphs(text):
        if CLAIM_HINT_RE.search(para) and not URL_RE.search(para) and "\\cite" not in para:
            risky.append((lineno, para[:180]))

    if risky:
        print("\nParagraphs with claim-like language but no nearby source:")
        for lineno, snippet in risky[:80]:
            print(f"{path}:{lineno}: {snippet}")
        if len(risky) > 80:
            print(f"... {len(risky) - 80} more")
    else:
        print("\nNo unsourced claim-like paragraphs flagged.")

    return 1 if risky else 0


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

