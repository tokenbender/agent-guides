---
name: pdf-ocr-feedback
description: Refine unreliable OCR or scanned PDF transcription with page-level checks, targeted retries, and source-grounded resolution of equations, tables, or uncertain spans. Use when extraction has meaningful defects; do not OCR a clean text document merely because it is a PDF.
---

# PDF OCR feedback

Produce page-faithful text with explicit uncertainty. Use intact source text when available; reserve OCR for the regions that need it. Respect the user's requested pages, output format, and transcription scope.

## Output contract

For requested page-faithful transcription, preserve original page order with:

```text
===== PAGE N =====
<page text>
```

Preserve reading order, column structure, captions, footnotes, equations, units, table relationships, and code where present and in scope. Mark unreadable material instead of silently dropping or inventing it. Use `[uncertain: "A" | "B"]` for unresolved alternatives.

## Initial pass and review

Transcribe each requested defective page or region once. Compare it with the source image, especially at column boundaries and around numerical or mathematical content. Inspect available high-risk spans rather than manufacturing a fixed number of examples on every page.

For a substantial transcription, the following rubric can prioritize repairs:

- structure: 25 points;
- completeness: 25 points;
- character and numeric accuracy: 20 points;
- layout-sensitive content: 20 points;
- noise and garbling: 10 points.

A score is a review heuristic, not a measured accuracy percentage or calibrated confidence. A score of 95 does not establish 95% correctness. For a small repair, direct source comparison and a concise uncertainty note are enough.

Escalate actual defects even when the score is high: skipped columns, ambiguous cell assignments, uncertain operators, missing regions, or conflicting transcriptions that affect meaning.

## Targeted repair and optional consensus

First re-read or crop the disputed source region using available tools. Cross-check recurring symbols, proper nouns, and citations within the source when useful.

If the uncertainty persists and multiple independent reads are practical, use three total OCR candidates; at most five for a genuinely difficult page. Do not describe correlated outputs as independent verification. Vote at the smallest meaningful unit: table cell, line, symbol, or equation operator.

Agreement is not proof. The visible source decides when it is legible; majority voting must not overwrite contradictory source evidence. If no supported resolution exists, retain an uncertainty marker. Do not fill a damaged region from contextual plausibility alone.

Repair only flagged spans. Preserve accepted text. Use the current harness's available OCR, vision, and local rendering tools; do not assume a particular model, API key, or callable tool exists.

## Bounded completion

Stop when the requested content is complete and material defects are resolved, or when further attempts do not improve the evidence. By default, use at most two targeted repair rounds after the initial pass and at most five OCR candidates per page. User-specified limits take precedence. Do not launch a large paid OCR batch without the required scope and authorization.

If a page remains partly unreadable, deliver the verified portion with exact page/span limitations. Ask for a better source only when the missing material prevents the requested result. Continue independent pages while awaiting it.

When a repair report is requested or useful, record actual pages processed, extraction method, replaced spans/pages, remaining uncertainties, and attempts performed. Do not generate empty comparison artifacts or claim accuracy that was not measured. Render and visually inspect only the pages/regions needed to resolve or validate the transcription.
