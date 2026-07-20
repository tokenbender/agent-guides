---
name: technical-writing-workflow
description: "Use for planning, researching, drafting, revising, or auditing technical write-ups, textbooks, papers, reports, READMEs, research notes, PR narratives, and public technical prose. Applies a full workflow, not only style rules: reader need, source audit, ontology, outline contracts, parallel research packets, serial synthesis, claim-boundary checks, plain-English rewrite, anti-LLM prose audit, citation audit, and final render or publication readiness."
---

# Technical writing workflow

Use this skill when the user asks to write, rewrite, improve, audit, explain, teach, document, or publish technical material. Treat it as a workflow with checks, not as a prose vibe.

## Core rule

Open the subject up without making it shallow.

Every important explanation must name:

1. the object or behavior being described
2. the method, mechanism, or actor that changes it
3. the evidence that supports the claim
4. the boundary the claim is allowed to cover

## Serial before parallel

Serialize meaning. Parallelize collection.

Do these serially before drafting:

1. Define the reader and use case.
2. Define scope and exclusions.
3. Build the ontology table.
4. Decide the argument order.
5. Write chapter or section contracts.
6. Resolve source contradictions.

Then parallelize:

- source packets
- paper cards
- glossary entries
- examples
- diagrams
- exercises
- tables
- reference checks
- local fact checks
- counterexamples and failure modes

Return to serial work for:

- synthesis
- final claim strength
- voice and terminology
- cross-references
- final layout or render inspection

## The workflow

### 1. Intake

Write a short brief before drafting:

- audience
- task the reader should perform after reading
- source surface
- deliverable format
- deadline or depth target
- claim-risk level

If any of these are unknown, make a conservative assumption and state it briefly.

### 2. Source audit

Separate sources into evidence classes:

- primary paper or official documentation
- benchmark or measurement artifact
- code or reproducibility artifact
- technical blog or explainer
- social post or pointer
- local note or capture

Do not let a pointer carry a claim that belongs to a paper, code artifact, or measurement.

### 3. Ontology table

For each major topic, create this table before drafting:

```text
Topic:
Object:
Method:
Resource or behavior changed:
Evidence:
Boundary:
Common beginner mistake:
Best example:
```

This table is the backbone. If it is confused, the prose will be confused.

### 4. Outline contracts

Each section needs a job:

```text
Section:
Reader outcome:
Core sources:
Example:
Warning:
What not to include:
```

Do not write full prose until the contracts are stable.

### 5. Draft

Write from the reader's next question.

- Start with the familiar.
- Introduce one new idea per paragraph.
- Name the concept after the intuition lands.
- Use concrete examples before abstraction when possible.
- Keep implementation runbook detail out of main prose unless implementation is the contribution.

### 6. Rigor pass

Check every claim:

- what changed
- what stayed fixed
- what evidence supports it
- what the claim does not prove
- whether examples are examples rather than definitions
- whether setup details affect validity, comparability, or reproducibility

### 7. Plain-English pass

Use active voice. Prefer short sentences. Use everyday words where they preserve precision.

Replace:

- utilise with use
- leverage with use
- facilitate with help
- in order to with to
- with regard to with about
- commence with start
- sufficient with enough

Keep technical terms when they are needed, but earn them before using them heavily.

### 8. Anti-LLM prose pass

Remove patterns that make prose feel generated unless the user explicitly wants that register:

- em dashes as default punctuation
- "not only X but also Y"
- "in conclusion", "moreover", "furthermore", "it is worth noting"
- "delve", "landscape", "robust", "seamless", "holistic", "unlock", "empower"
- vague hype such as groundbreaking, revolutionary, transformative
- generic title forms such as "The power of X", "Ultimate guide", "X, explained"

### 9. Citation and source pass

Check that citations support the exact claim nearby. Prefer primary sources. Use descriptive link text when writing web prose. For PDFs or papers, include enough source detail to let another reader recover the artifact.

### 10. Final readiness

Before delivering:

- run applicable scripts in `scripts/`
- verify links or local file paths when practical
- for PDF/DOCX/HTML deliverables, render or preview the final artifact
- state any checks that could not be completed

## Scripts

The bundled scripts are optional but preferred for non-trivial prose:

```bash
python scripts/prose_audit.py path/to/file.md
python scripts/heading_audit.py path/to/file.md
python scripts/citation_audit.py path/to/file.md
python scripts/anti_llm_pattern_audit.py path/to/file.md
```

Use script output as a review surface, not as an automatic rewrite command.
