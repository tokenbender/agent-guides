---
name: ncert-textbook
description: Write, revise, or typeset NCERT-style technical textbooks and chapters combining warm NCERT Class IX-XI pedagogy, Feynman discovery-before-explanation rigor, real traces/experiments, and the 4-bit lossless A4 WeasyPrint visual aesthetic. Use for any deep technical topic, model, paper, or repository, as well as chapters of "In the Praise of The Word" (see references/in-the-praise-of-the-word.md).
---

# NCERT-Style Technical Textbook

Write technical material that teaches like the best NCERT school textbooks—warm, visual, grounded in real observations, and unafraid of real arithmetic—while maintaining frontier-lab honesty and accuracy.

If the user is writing or revising a chapter of **"In the Praise of The Word"** (the Qwen3-0.6B textbook), also read [references/in-the-praise-of-the-word.md](references/in-the-praise-of-the-word.md) for the exact chapter plan, metaphor vocabulary, and real-trace browser/local workflow.

## Two Anchors: Voice and Aesthetic

1. **Writing & teaching voice — NCERT Class IX/XI style** (modelled on NCERT Class IX *Democratic Politics*, `https://www.drishtiias.com/images/pdf/social%20science%20demo%20part%201.pdf`):
   - **Direct, warm address ("you")**: start from the familiar before moving to abstraction; prefer causal prose (*because, therefore, so*) and short paragraphs over bullet dumps.
   - **Spiral structure**: open with a big-picture overview that picks up from the previous chapter, then numbered sections (`N.1`, `N.2`, …) that each open with a concrete puzzle, case, or everyday scenario.
   - **NCERT pedagogical boxes**:
     - Recurring cartoon children in the margin asking the naive, pointed question the reader is secretly wondering.
     - **Activity** boxes the student can genuinely do with pen, spreadsheet, or plain Python (no GPU required).
     - **Check Your Progress** (2–4 focused questions) and **"Read the graph / cartoon"** prompts.
     - **Comparison cases** (as NCERT compares countries, compare two real models, architectures, or regimes).
     - **Discuss / Debate** dialogues where reasonable people disagree, intentionally left open.
     - **Common Misconception** and **Where This Stops Working (Boundary)** notes.
     - **Let's Revisit / What We Have Learnt**, **Glossary**, graded **Exercises** (MCQ, match the columns, numerical, short/long answer, implementation/debugging, open-ended), and a **Group Project**.
   - **Real "aha" moments**: let a surprising measured fact overturn the reader's default assumption.
   - **No fake framing**: never invent fake chapter numbers, fake parent book titles, or fictional citations. Match Indian English spellings (*quantisation, colour, behaviour*) when the user prefers NCERT flavour; otherwise match the user's locale.

2. **Look & print layout — the 4-bit lossless A4 aesthetic** (reference: `~/Downloads/Is-4-bit-the-new-lossless-textbook.pdf` when present):
   - **A4 page built with WeasyPrint** (HTML/CSS → PDF) with a wide right margin dedicated to margin asides, callouts, and cartoon questions. (If the user explicitly requests Pandoc/Markdown/LaTeX source instead, use clean fenced-div boxes and numbered `$$ ... $$` equations.)
   - **Typography**: Libre Baskerville body; Marcellus title caps and Marcellus SC red section heads; Barlow Condensed orange sub-heads; Roboto Condensed labels; Noto Sans Mono for code/tokens (show space as `·`, newline as `↵`); Noto Sans CJK when non-Latin scripts appear.
   - **Page furniture**: yellow page-number circles; clean running footers bearing the author/book title (adapt to the current book/project).
   - **Data-driven figures**: generate SVGs or high-DPI plots directly from saved data files. Keep text readable (≥ 9 pt at final print size), avoid overlap or clipped labels, and never rely on colour alone (must remain legible in black-and-white).

## Non-Negotiable Principles

1. **Real system, real data only.** Ground every chart, table, trace, and quotation in real runs, real measurements, or verified repository/paper artifacts. Never use a fictional "pocket" toy model as the main teaching vehicle. A tiny hand-worked arithmetic example is welcome as a stepping stone—and should immediately be reconciled against the real system.
2. **Feynman: discovery before explanation.** Follow the arc: *puzzle or case → experiment/measurement → explanation → technical term (highlighted, only after the idea is earned)*. Show why a component exists by removing or ablating it and watching what breaks. Ask the reader to predict before revealing the result.
3. **Educational, not a spec sheet.** A number appears only if it reveals something. For each major concept, answer in flowing text: what observation motivates it, why the problem arises, what fails without it, how the mechanism works step by step, why each step makes sense, what the answer means, where it stops being valid, and how it hands off to the next idea.
4. **Radical honesty.**
   - Say **"nobody knows"** wherever true.
   - State method caveats plainly (single run, single prompt, numerical precision, logit-lens limits, crude zero-ablation, small sample sizes, reused test sets).
   - Keep **claim status** crystal clear—never blur proven held-out results, previews, failed experiments, and unbuilt plans.
   - Report failures as plainly as successes; failures are often the clearest teaching material.
   - Never fabricate numbers, quotes, or sources.
5. **Consistent concrete imagery.** Choose a coherent set of everyday images early (and stick to them across chapters). Give the proper technical name once when earned, then use the plain image alongside it—and explicitly say where an analogy breaks.
6. **Complete mapping.** Do not wave hands past the hard parts. By the end of the chapter or book, map every essential component down to its actual arithmetic, backed by worked examples using real numbers.

## Workflow

1. **Plan the chapter.** List the reader's starting assumptions, the central questions, the experiments or data artifacts that answer them, the earlier sections being deepened, and the concrete worked examples.
2. **Gather & save real data / traces.** Run the real model, script, or analysis first (or read the primary experiment artifacts). Save compact structured data files and generate all figures/tables programmatically from them—never hand-copy numbers loosely.
3. **Write in the NCERT voice.** Warm, direct "you", short paragraphs, questions before answers, earned jargon, and NCERT pedagogical boxes. Provide worked answers that *teach* (not merely state final answers) whenever exercises are included.
4. **Verify every derived number.** Write and run a small check script (assertions in plain Python) that recomputes every derived value in worked examples, tables, code blocks, and exercises against the saved data files. Every code block shown to the reader must actually run and produce the claimed output.
5. **Build the PDF / deliverable.** Render via WeasyPrint in the 4-bit lossless A4 aesthetic (or the user's requested toolchain) with data-driven SVG/vector figures.
6. **Inspect every single page visually.** Convert pages to images and inspect every page before delivering: catch text overflow, stranded margin notes, half-empty pages, broken glyphs/fonts, clipped figure labels, or unbalanced columns, and fix them. Cross-check displayed figures/numbers against the data files one final time.
7. **Deliver cleanly.** Present the artifact to the user and save it to their requested output path (or `~/Downloads` for standalone PDFs when appropriate), keeping earlier versions intact rather than silently clobbering them.

## Quality Bar

Before calling a chapter done, ask three questions:
- Could a curious 15-year-old explain this section accurately to a friend?
- Would a frontier researcher find nothing false or misleading in it?
- Does it feel like a genuine piece from a beloved NCERT textbook rather than a dry spec sheet?

If the chapter only describes instead of making the reader discover, it is not done.
