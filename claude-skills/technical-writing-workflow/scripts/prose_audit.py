#!/usr/bin/env python3
"""Run lightweight prose checks for technical writing drafts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LONG_SENTENCE_WORDS = 32
SHORT_SENTENCE_WORDS = 5
JARGON_RE = re.compile(
    r"\b(utili[sz]e|leverage|facilitate|commence|sufficient|with regard to|"
    r"in order to|pivotal|crucial|meticulous|multifaceted|underscore|showcase)\b",
    re.IGNORECASE,
)
PASSIVE_RE = re.compile(r"\b(is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", re.IGNORECASE)


def strip_markup(line: str) -> str:
    line = re.sub(r"`[^`]*`", "", line)
    line = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", "", line)
    line = re.sub(r"https?://\S+", "", line)
    return line


def sentence_spans(text: str):
    cleaned = "\n".join(strip_markup(line) for line in text.splitlines())
    for match in re.finditer(r"[^.!?\n][^.!?\n]*(?:[.!?]|$)", cleaned):
        sentence = re.sub(r"\s+", " ", match.group(0)).strip()
        if sentence:
            lineno = cleaned.count("\n", 0, match.start()) + 1
            yield lineno, sentence


def audit(path: Path) -> int:
    text = path.read_text(errors="replace")
    print(f"# Prose audit: {path}")
    hits = 0

    for lineno, sentence in sentence_spans(text):
        words = re.findall(r"[A-Za-z0-9_'-]+", sentence)
        count = len(words)
        if count > LONG_SENTENCE_WORDS:
            hits += 1
            print(f"{path}:{lineno}: long sentence ({count} words): {sentence[:220]}")
        elif 0 < count <= SHORT_SENTENCE_WORDS:
            hits += 1
            print(f"{path}:{lineno}: very short sentence ({count} words): {sentence}")

    for lineno, line in enumerate(text.splitlines(), 1):
        if JARGON_RE.search(line):
            hits += 1
            print(f"{path}:{lineno}: jargon/default phrasing: {line.strip()}")
        if PASSIVE_RE.search(line):
            hits += 1
            print(f"{path}:{lineno}: possible passive voice: {line.strip()}")

    if hits == 0:
        print("No prose issues flagged.")
    else:
        print(f"\nFlagged prose issues: {hits}")
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

