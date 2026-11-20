---
name: paper-ocr-notes-pipeline
description: Create a durable, teachable paper-notes package from a PDF or paper URL, preserving source identity, equations, evidence, and extraction provenance. Use when the user asks for saved paper notes or an ingestion package; do not turn an ordinary paper question or short summary into a file-producing pipeline.
---

# Paper notes pipeline

Produce the requested notes package from the actual paper. Keep it self-contained, source-grounded, and readable. User-specified scope, sections, output format, and existing authorization take precedence over this skill's defaults within the app's instruction hierarchy.

## Intake and identity

Resolve the paper's title, authors, identifier, and version from the source. Use the user's output root; otherwise follow the workspace's deliverable convention, or use `./papers-articles/<paper-slug>/` when none exists. Infer a sensible slug without asking.

A title, author, or version mismatch means the extraction is not yet trustworthy. Recheck the source once using a different available route. If the correct source remains inaccessible, report exactly what is missing and finish any independent work that does not depend on it. Do not retry the same failure indefinitely or write plausible notes from a different paper.

## Choose extraction by evidence

Prefer official HTML/source or an intact PDF text layer. Inspect relevant equations, tables, figures, and reading order visually when their correctness matters. OCR is a fallback for scanned or materially defective regions, not a mandatory ritual for every paper.

When OCR needs refinement, use `pdf-ocr-feedback` if available. Otherwise preserve page boundaries, mark uncertain spans, and repair only the disputed regions with available tools. Never claim OCR was performed when the text came from native extraction.

For the default package, save:

- the source PDF when available and appropriate, or a source link with identifier/version;
- `notes.md`, the primary deliverable;
- a compact provenance/index file when useful to navigate multiple artifacts;
- page-delimited extraction text and a repair report only when those artifacts were produced or requested.

If a canonical OCR package is explicitly requested, keep its requested filenames and document extraction method and replaced pages accurately. Do not fabricate an OCR comparison report for an operation that never ran.

## Build the notes

Use `technical-writing-workflow` when available for substantial notes. Otherwise follow the same core approach: explain the mechanism, give evidence, and state its boundary.

For full teaching notes, this is the default structure; adjust to the user's requested form and omit inapplicable sections:

1. Paper title and source/version.
2. Short summary: problem, central idea, main result, decisive limitation.
3. Beginner's guide: prerequisites, terms, one useful concrete example.
4. Paper summary: contributions and experimental context.
5. Deep dive: method, definitions, relevant equations, derivation or implementation details.
6. Critical analysis: assumptions, failure modes, evidence gaps, and a discriminating follow-up when useful.
7. Learning path when the user wants teaching material.
8. Key equations when the paper has equations worth explaining.
9. References.

Collect source-backed facts before inference: objectives, setup, datasets, baselines, metrics, results, and author-stated limitations. Keep a compact claim-to-source map while drafting; expose it only when useful or requested. Label your interpretations and distinguish proposed follow-up experiments from experiments the authors ran. Do not invent an experiments table for a theory-only paper.

## Review and finish

Check identity, important numbers and symbols, definitions before use, baseline comparisons, and the strongest supported limitation. Review clarity and correctness together for short notes; use separate passes for a substantial package. Preserve page/section/table pointers for material claims.

Inspect only unresolved regions rather than repeatedly rescanning the whole paper. Deliver after relevant checks pass and disclose unresolved source defects. Lack of an optional tool or companion skill is not a reason to abandon reachable work; lack of source evidence is a reason to narrow an unsupported claim.

Independent extraction or reference checks may be delegated only when permitted, useful, and accompanied by concurrent local work. Keep final synthesis and claim scope coherent.
