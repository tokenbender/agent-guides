---
name: paper-ocr-notes-pipeline
description: Canonical end-to-end workflow for turning a paper PDF or URL into grounded OCR artifacts and a teachable notes.md.
---

# Paper OCR Notes Pipeline

This skill is a reusable policy for paper ingestion and note production. It must stay self-contained and work in any workspace.

Do not require any companion `README.md` or local notes file to run this workflow. If one exists, treat it only as supplemental context.

## Objective

Generate a self-contained notes package from a paper source while preserving provenance, factual grounding, OCR quality, and teachability.

## Inputs

- One of: a PDF path, a paper URL, or an arXiv abs URL.
- Optional: preferred folder slug.
- Optional: output root directory.

## Output Root Resolution

Use this priority order:
1. If the user provides an output root, use it.
2. Else create and use `./papers-articles` in the current working directory.

## Output Contract

Create a dedicated folder:

```text
<output-root>/<paper-slug>/
```

Required files:
- source file: `<paper>.pdf` or `link.txt` for URL-only sources,
- `notes.md` as the primary deliverable,
- `README.md` as a paper-local artifact and provenance index,
- `<paper>.ocr.feedback-loop.txt` as the final OCR output,
- `<paper>.ocr.feedback-loop-comparison.md` as the OCR replacement report.

`notes.md` must be sufficient for a new reader to learn the paper without opening extra files.

## Canonical Notes Sections

Use these headings in order:
1. `# <Paper Title>`
2. `## TL;DR`
3. `## Beginner's Guide`
4. `## Paper Summary`
5. `## Deep Dive`
6. `## Critical Analysis`
7. `## Learning Path`
8. `## Key Equations Summary`
9. `## References`

## Nested Skills

- Use `pdf-ocr-feedback` for pagewise OCR refinement.
- Use `technical-writing-workflow` while drafting and revising `notes.md`.

## Core Principles

1. Reader intuition comes before technical detail.
2. Do not blur distinct concepts.
3. Evidence-first writing: claims point to table, figure, section, or page evidence.
4. Revision is mandatory.
5. Identity verification is mandatory before trusting extracted content.
6. Uncertainty and limitations must be stated explicitly.

## Workflow

Follow the phases in order.

### Phase 0 - Intake and setup

1. Resolve canonical identity: title, authors, date/version, identifier (arXiv/DOI when available).
2. Create output folder and store source.
3. Initialize `notes.md` skeleton with required section order.
4. Create paper-local `README.md` listing source and produced artifacts.

### Phase 1 - Extraction and OCR feedback loop

Use nested skill `pdf-ocr-feedback` for pagewise OCR refinement.

Required OCR behavior:
1. Pass-1 extraction across all pages.
2. Per-page quality scoring and weak-page detection.
3. Pass-2 retries only on weak pages.
4. Merge pages in original order.

Required OCR format:
- Preserve `===== PAGE N =====` delimiters.
- Preserve page order.
- Record replaced pages and rationale in comparison report.

### Phase 1.5 - Identity gate (mandatory)

Before trusting extracted content, verify anchors:
- title matches target,
- author block matches reasonably,
- identifier/date lines are consistent when available.

If any anchor mismatches:
1. reject extraction,
2. rerun extraction,
3. revalidate before proceeding.

### Phase 2 - Ground-truth extraction (facts only)

Collect source-backed facts only (no interpretation yet):
- problem statement and failure mode,
- contributions as stated by authors,
- method overview,
- key equations and definitions,
- experimental setup: tasks, datasets, models, baselines, metrics, ablations/stress tests,
- headline quantitative results,
- limitations stated by authors.

Stop condition: answer "what did they do" without guessing.

### Phase 3 - Compose `notes.md` in strict order

1. TL;DR (problem, key idea, 1-2 evidence numbers, caveat)
2. Beginner's Guide (college-level, define symbols once, one concrete toy example)
3. Paper Summary (problem recap, contributions, results, experiments table)
4. Deep Dive (definitions, derivation steps, implementation sketch, optional pseudocode)
5. Critical Analysis (assumptions, objections, failure modes, validation/refutation experiments)
6. Learning Path (prereqs, next study steps, diagnostics)
7. Key Equations Summary (equation + one-line meaning)

While drafting, apply `technical-writing-workflow`:
- anchor explanations in familiar ground,
- define terms at point of need,
- keep ontology and score ownership clear,
- cut implementation-operator detail unless it matters scientifically,
- keep claims tied to evidence.

### Phase 4 - Exploration and consistency checks

While reading and drafting, run these checks:

Problem framing checks:
- what exactly breaks and under what conditions,
- where boundary conditions are stated.

Method checks:
- what estimator/objective is actually optimized,
- which terms are additive vs multiplicative,
- what comes from probabilities vs gradients vs external signals.

Claims checks:
- theoretical vs empirical claims separation,
- strongest evidence source for each major claim,
- missing ablations/OOD/calibration/compute analyses.

Consistency checks:
- terminology consistency across sections,
- equation-to-implementation narrative alignment,
- baseline independence assumptions where claimed,
- proxy computability with stated costs.

### Phase 5 - Revision passes (non-negotiable)

1. Clarity pass:
   - remove duplicates,
   - ensure definitions appear before equations,
   - soften overconfident wording where uncertainty exists.
2. Correctness pass:
   - detect concept conflations,
   - remove unsupported claims,
   - fix misleading pseudocode assumptions.
3. Objection stress test:
   - state strongest objection,
   - provide rebuttal conditions,
   - propose falsifiable tests.
4. Update TL;DR caveat after all revisions.

### Phase 6 - Quality gates (must pass all)

- Accuracy: symbols and claims are correct and evidence-backed.
- Completeness: experiments table includes tasks, baselines, metrics.
- Teachability: beginner section is understandable by a college-level reader.
- Critical rigor: at least one strong objection and a test plan.
- Implementation sanity: pseudocode and grouping assumptions are coherent.

## Inference and process optimization defaults
- Prefer source-of-truth hierarchy:
  1) official source text (arXiv source/HTML when available),
  2) OCR feedback-loop output,
  3) targeted visual rechecks for disputed pages.
- Use selective rereads: only revisit sections needed for unresolved claims.
- Maintain a claim-to-evidence ledger while writing to reduce drift.
- Minimize full-document rescans unless identity gate or consistency checks fail.
- Keep output deterministic: fixed section order and explicit caveats.

## Common pitfalls to avoid

- Over-summarizing without experimental context.
- Concept conflation (baseline vs weighting, confidence vs correctness).
- Pseudocode that violates grouping assumptions.
- Omitting caveats/limitations.

## Must not do

- Do not depend on external README files for policy.
- Do not rely on memory summaries over source evidence.
- Do not finalize if identity gate fails.
- Do not skip revision passes or quality gates.
