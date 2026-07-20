---
name: pdf-ocr-feedback
description: High-accuracy OCR refinement workflow with self-scoring, Maj@K consensus voting, and targeted repair for page-faithful transcription.
---

# PDF OCR Feedback

Use this skill when transcribing PDF pages through a vision model and a single OCR pass is not reliable enough.

## Objective

Produce page-faithful OCR with exact page boundaries, explicit uncertainty, and a practical target of at least 95/100 quality whenever the source allows it.

## When to Use

Escalate to this workflow when any of the following are true:
- equations or mathematical notation matter,
- tables have nontrivial structure,
- the page is multi-column,
- the scan is noisy, low-resolution, or artifact-heavy,
- the document mixes languages, scripts, or handwriting,
- or a single OCR pass leaves meaningful uncertainty.

## Output Contract

For every page:
1. Preserve reading order.
2. Capture all visible regions that matter: headers, footers, footnotes, captions, margin notes, table content, equation text, figure labels, and code blocks.
3. Emit exact page delimiters:

```text
===== PAGE N =====
<page text>
```

4. Keep page order unchanged.
5. Preserve equations, units, and table semantics.
6. Never silently drop unknown symbols.
7. If a tie cannot be resolved, mark the span explicitly as `[uncertain: "A" | "B"]`.

## Pipeline Overview

```text
For each page:
  1. Pass-1 OCR
  2. Self-evaluate on a 0-100 rubric
  3. If score >= 95 and no red flags -> ACCEPT
  4. Else run Maj@K escalation:
     a. Generate K-1 additional independent passes
     b. Vote at the smallest reliable unit
     c. Re-score the merged result
     d. If still weak, repair only flagged spans
  5. Stop when accepted, capped, or no longer improving
```

## Phase 1: Initial Transcription

For the first pass on every page:
1. Transcribe the full page faithfully.
2. Preserve top-to-bottom, left-to-right reading order. For multi-column pages, process column-by-column.
3. Do not skip difficult regions; capture them or mark them uncertain.
4. Keep formatting structure when it carries meaning, such as headings, lists, table rows, and code blocks.

## Phase 2: Self-Evaluation

Switch into evaluator mode. In this phase you do not edit text; you only score, flag, and decide whether the page is accepted or escalated.

### Scoring Rubric

Score each page on a 0-100 scale across five dimensions:
- Structural fidelity: 0-25
- Completeness: 0-25
- Character and numeric accuracy: 0-20
- Layout-sensitive content: 0-20
- Noise and garbling: 0-10

### What to Check

- Structural fidelity: headings, paragraph breaks, list structure, column order, and section boundaries.
- Completeness: no dropped text regions, no truncated lines, no missing footnotes or captions.
- Character and numeric accuracy: symbols, digits, citation numbers, units, and OCR confusions such as `0/O`, `1/l`, or `rn/m`.
- Layout-sensitive content: table cells, equation operators, superscripts, subscripts, code tokens, and figure labels.
- Noise and garbling: repeated fragments, hallucinated text, gibberish, or broken words.

### Red Flags

Any red flag forces escalation even if the numeric score is high:
- an acknowledged unreadable region with no transcription attempt,
- a suspected skipped column,
- an ambiguous table grid or cell assignment,
- an equation with uncertain structure or operators,
- more than two unresolved uncertainty markers on the page,
- conflicting variants that remain unresolved after voting.

### Mandatory Spot-Check

For every scored page:
1. Pick 3-5 high-risk snippets, such as equations, numbers, citations, table cells, or proper nouns.
2. Explain why each snippet is risky.
3. Record confidence for each snippet.
4. Flag any snippet below 80 percent confidence for retry or repair.

### Evaluation Format

```text
PAGE N - Score: XX/100
  Structural Fidelity: XX/25 - [notes]
  Completeness: XX/25 - [notes]
  Character/Numeric Accuracy: XX/20 - [notes]
  Layout-Sensitive Content: XX/20 - [notes]
  Noise/Garbling: XX/10 - [notes]
  Red Flags: [list or "none"]
  Spot-Check:
    1. "snippet text" - risk: [reason] - confidence: [high/medium/low]
    2. ...
  Decision: ACCEPT / ESCALATE (reason)
```

## Phase 3: Maj@K Consensus Voting

Use this phase for pages scoring below 95 or pages with any red flag.

### Additional Passes

1. Generate `K-1` additional independent passes.
2. Use `K=3` by default.
3. Use `K=5` for hard pages: equations, dense tables, multi-column layouts, handwriting, mixed scripts, or poor scans.
4. Keep the passes independent. Do not anchor later passes to the first pass.

### Voting Rules

- Default to line-level voting.
- For a disagreement, shrink the dispute to the smallest meaningful span.
- Majority wins when a clear majority exists.
- If the vote is tied, choose the most contextually consistent variant only when the evidence is strong.
- If no clear winner exists, keep the span explicit as `[uncertain: ...]`.

### Special Cases

- Numbers and equations: vote at character level when needed.
- Tables: vote per cell, not per line.
- Proper nouns and citations: cross-check against other occurrences in the document.

### Consensus Output

Produce one merged transcription per page:
- majority-agreed content passes through unchanged,
- disputed spans are either resolved or marked uncertain,
- remaining uncertain spans are queued for targeted repair.

## Phase 4: Targeted Span Repair

Only repair flagged spans. Do not regenerate accepted text.

1. Identify unresolved or low-confidence spans.
2. Re-read only those regions from the source.
3. Replace the uncertain span if the repair is clearly better.
4. Re-score the page after repair.

## Phase 5: Final Merge and Summary

Assemble the final document in original page order with exact delimiters preserved.

Append a short refinement summary:

```text
## OCR Refinement Summary

Total pages: N
Pass-1 accepted: [pages]
Maj@K escalated: [pages]
Targeted repair needed: [pages]
Final scores: [page -> score]
Remaining uncertain spans: [count and pages]
Iterations used: [count]
```

## Stopping Criteria

Stop when the first applicable rule fires:
1. Accept: score at least 95, no red flags, and output contract satisfied.
2. Diminishing returns: less than 2 points of improvement across consecutive rounds.
3. Hard cap per page: 3 total iterations.
4. Hard cap global: 5 refinement iterations across the full document.

If a page hits the cap below 95, accept it only with an explicit note about the remaining uncertain spans.

## Anti-Patterns

- Never invent text that appears in none of the OCR passes.
- Never skip reading-order validation on multi-column pages.
- Never score a page without filling the rubric and the spot-check.
- Never regenerate a whole page when only a few spans are weak.
- Never exceed `K=5`.
- Never round up uncertain work into a confident score.
