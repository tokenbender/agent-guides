---
name: technical-writing-workflow
description: Draft, revise, and review technical explanations, reports, papers, READMEs, and PR narratives with clear mechanisms, source-backed claims, and proportionate verification. Use for substantive technical writing; handle a small wording edit directly without a research or planning workflow.
---

# Technical writing workflow

Open the subject up without making it shallow. Preserve the user's audience, purpose, format, length, terminology, and requested scope.

## Choose the scale

- **Small edit or short explanation:** revise directly. Check meaning, terminology, and any factual claim you change. No intake questionnaire, ontology table, outline, script run, or extra artifact is required.
- **Substantial technical draft:** establish the reader's next question, main claim, evidence, and argument order. Keep planning internal unless the user requests it or a decision materially affects the result.
- **Paper, long report, or synthesis:** use the source audit, concept map, section contracts, and claim checks below where they help. Resolve contradictory sources before merging their conclusions.

Infer routine missing details from context. Ask a focused question only when a missing fact or decision would materially change the deliverable and cannot be recovered. Continue independent authorized work while waiting. A writing request authorizes preparing the writing; it does not by itself authorize sending or publishing it.

## Evidence before claim strength

For each material claim identify the object, the mechanism or intervention, the supporting evidence, and its scope. Prefer primary papers, official documentation, measurements, code, and reproducibility artifacts. A social post or local note may point to evidence but cannot stand in for it.

Preserve denominators, baselines, units, dates, uncertainty, and distinctions between measured results and inference. Do not invent a mechanism for an empirical correlation. Verify current or uncertain facts when they matter; do not launch external research for a self-contained rewrite unless factual correction is needed or requested.

For a complex explanation, a working concept map can contain:

```text
Object / method / behavior changed / evidence / boundary / likely misunderstanding / example
```

For a long document, give each section a reader outcome, core evidence, and example. These are planning aids, not mandatory output sections.

## Draft and revise

Lead with the result or central claim, then answer the reader's next question. Introduce one idea at a time; explain unfamiliar terms at their point of use. Use concrete examples before abstraction when helpful. Keep runbook details out of conceptual prose unless they affect the contribution or the reader's decision.

Use concise, connected paragraphs, active voice, and familiar words. Retain technical vocabulary that earns its place. Match the requested genre: a PR description, paper, tutorial, and chat explanation need different levels of detail. Use headings, tables, and lists for real structure rather than as a default wrapper around every answer.

Avoid stock phrases, vague hype, invented compound labels, repeated conclusions, and automatic adversarial contrasts such as "This is not X; it is Y." Use a contrast when it explains an actual distinction. Preserve the user's intentional voice; a linter's preference is not a reason to flatten it.

For technical edits, keep identifiers, equations, code, numbers, citations, and qualifications intact unless the task calls for changing them. If a supplied claim is unsupported, flag or qualify that claim instead of quietly strengthening it.

## Review proportionately

1. Check that the requested content is present and the argument is coherent.
2. Check high-impact facts, definitions, quantitative comparisons, and claim boundaries against the source.
3. Remove duplication and unclear wording without dropping unique requirements.
4. Check that each citation supports its nearby claim; distinguish sources read directly from inaccessible references.
5. Preview or render layout-sensitive deliverables with an available suitable tool. Do not render an unrelated format merely to satisfy this skill.

Once the relevant checks pass, deliver. Repeat checks only after a material change or to resolve an actual issue. Report material verification gaps; do not imply that a script pass proves factual accuracy.

## Tools and collaboration

Use the current harness's available tools; resolve supporting paths relative to this skill directory. When permitted and useful, delegate independent source packets, examples, reference checks, or counterarguments while doing useful local work. Keep argument design, source reconciliation, final claim strength, and prose synthesis with the parent. Do not delegate a small edit or fan out merely because this skill mentions parallel work.

Apply applicable user instructions ahead of advisory skill conventions, within the app's instruction hierarchy. If another instruction file causes a pause, identify the path and exact relevant instruction rather than inventing an approval requirement.

The existing scripts are optional review aids for substantial file-backed prose:

```bash
python scripts/prose_audit.py path/to/file.md
python scripts/heading_audit.py path/to/file.md
python scripts/citation_audit.py path/to/file.md
python scripts/anti_llm_pattern_audit.py path/to/file.md
```

Inspect a script's usage before running it. Its findings require judgment; do not automatically rewrite or expand the task to eliminate every match.

Guidance basis: [OpenAI Astra prompting guidance](https://developers.openai.com/api/docs/guides/latest-model). This skill contains writing workflow guidance, not model or API configuration.
