---
name: audit-sft-data-quality
description: Audit supervised fine-tuning datasets against the behavior and task they are meant to teach. Use when inspecting SFT JSONL, chat messages, instruction-response pairs, tool or agent trajectories, code corpora, synthetic examples, revised datasets, base-model evals, pass@k skill maps, train-validation-test splits, benchmark contamination, duplicate lineage, answer correctness, token limits, data mixtures, or train-readiness claims. Produce an evidence-backed row catalog, quality gates, duplicate and contamination report, corpus composition analysis, and a train, review, replace, reject, or eval-only decision.
---

# Audit SFT Data Quality

## Core rule

Judge every row against the target task. A polished answer is not high-quality
supervision if it teaches the wrong behavior, violates the task contract, leaks
the evaluator, or cannot be verified.

Apply hard correctness and integrity gates before diversity scores, confidence
scores, or aesthetic judgments.

For base-eval diagnosis, capability planning, synthesis, augmentation, and
iterative dataset design, read
[iterative-sft-data-design.md](references/iterative-sft-data-design.md).

## 1. Define the behavior contract

Write the contract before reading candidate answers:

| Field | Required description |
| --- | --- |
| Task | What the model must accomplish |
| Inputs | Allowed data, context, tools, and state |
| Output | Required schema, format, files, actions, or response style |
| Invariants | Facts that must remain true |
| Failure behavior | Rejection, abstention, rollback, or recovery rules |
| Resource limits | Context, tokens, latency, memory, calls, or complexity |
| Evaluation | Oracle, tests, rubric, benchmark, and sampling policy |
| Generalization target | Novel domains, templates, difficulty, or workflows |

Do not infer train readiness while any contract-critical field is unknown. Record
assumptions explicitly when the source does not define them.

## 2. Freeze the source inventory

Preserve immutable evidence before transforming data:

- source path, repository, revision, archive member, or URL;
- file and member SHA-256;
- row counts and unique task counts;
- schema version and split;
- synthetic, human, model-generated, repaired, or imported provenance;
- license, privacy, consent, and secret-handling constraints;
- parent row or revision lineage.

Never overwrite raw inputs. Put normalized, selected, repaired, and rejected
rows in separately identified artifacts.

## 3. Validate structure and conversation semantics

Check every row, not a sample:

- parseability and required keys;
- stable task identity and label consistency;
- legal role order and nonempty assistant target;
- output-format compliance;
- tool-call and tool-result pairing;
- referenced files, attachments, schemas, and environments;
- absence of accidental test, reference-answer, private-state, or system-prompt
  content;
- tokenizer-measured length under the actual model revision;
- loss masking and target boundaries when the training loader uses them.

Reject malformed rows rather than silently coercing them unless the repair is
deterministic, recorded, and reverified.

## 4. Categorize and tag every row

Use tags that support balancing, diagnostics, and regression analysis. Include:

- task family and domain;
- target capability;
- output mode and interaction mode;
- algorithm, tool, or reasoning pattern;
- stateful versus stateless behavior;
- edge-case and failure-mode tags;
- difficulty and resource profile;
- source, split, revision, and synthetic status;
- verification status and oracle type;
- safety, privacy, or contamination risk.

Prefer explicit tags such as `mutation-atomicity`, `boundary-conditions`,
`tool-repair`, `deterministic-ordering`, or `calibrated-abstention` over vague
labels such as `hard` or `quality`.

## 5. Detect duplicates and lineage

Compare within the candidate set and against all existing sets at multiple
levels:

1. exact row hash;
2. exact task ID or label;
3. normalized prompt and answer;
4. prompt-only and answer-only matches;
5. revision suffixes and explicit parent metadata;
6. source slug and source hash;
7. template, paraphrase, or semantic overlap;
8. equivalent tests, APIs, or solution contracts under different names.

Classify matches instead of calling all of them duplicates:

| Relation | Default action |
| --- | --- |
| Exact duplicate | Keep one canonical row |
| Same-ID correction | Replace the ancestor after verification |
| Versioned revision | Keep the newest verified version; preserve lineage |
| Paraphrase with identical target | Down-weight or keep one representative |
| Shared concept, distinct contract | Keep if it adds measurable coverage |
| Conflicting answers | Quarantine and adjudicate |
| Collision-qualified variants | Review APIs and tests before keeping both |

Do not train an ancestor and its correction as independent examples unless the
training format explicitly teaches critique and correction.

## 6. Audit contamination and split integrity

Check more than exact task IDs:

- benchmark names and public exercise IDs;
- prompt, title, filename, symbol, and test similarity;
- answer or reference-code similarity;
- shared templates and generated variants;
- parent-child lineage across splits;
- hidden labels, expected outputs, tests, rubrics, or judge feedback;
- near-duplicate domains that preserve the same executable contract.

Use group-aware splits by underlying task, template, source family, and revision
lineage. If a row teaches an evaluation answer directly, remove it from training
or move the evaluation surface.

## 7. Verify correctness with the strongest oracle

Prefer deterministic evidence. Use the strongest applicable method:

| Task type | Preferred evidence |
| --- | --- |
| Code | Build, tests, hidden tests, sanitizers, static checks, complexity probes |
| Math or logic | Exact solver, symbolic check, property tests, counterexamples |
| Extraction | Source-grounded field comparison and span provenance |
| Transformation | Round-trip, invariant, and property-based checks |
| Tool or agent task | Sandboxed replay, final-state assertions, action constraints |
| Structured output | Schema validation plus semantic field checks |
| Open-ended response | Explicit rubric, independent judges, factual grounding |
| Safety behavior | Adversarial cases, policy rubric, false-positive audit |

Run tests answer-blind where possible. A compile pass proves syntax, not semantic
correctness. A reward, confidence score, or judge approval does not override a
deterministic counterexample.

### Use model judges carefully

- Give the judge the task contract and candidate, not the desired verdict.
- Require a verdict, confidence, evidence, and concrete counterexample.
- Use independent judges or adjudication for uncertain and high-impact rows.
- Separate specification ambiguity from answer failure.
- Send disagreements and low-confidence rows to review.
- Never make judge approval the sole hard gate when executable evidence exists.

## 8. Evaluate signal density and teaching value

Apply soft scoring only after hard gates pass. Score each survivor for:

- directness of the desired behavior;
- correctness coverage, including failure behavior;
- clarity and absence of contradictory prose;
- realism of inputs, tools, and state;
- novelty relative to the retained corpus;
- rare capability or failure-mode coverage;
- answer concision and token efficiency;
- difficulty appropriate to the target model;
- usefulness for the declared evaluation and deployment distribution.

Do not reward length, stylistic polish, or exotic difficulty by default.

## 9. Audit corpus composition

Report counts by family, capability, source, difficulty, verification method,
token bucket, and revision status. Detect:

- dominant templates or families;
- repeated easy examples;
- rare but critical behaviors with too little coverage;
- synthetic-source monocultures;
- answer-length and difficulty skew;
- conflicting style or tool contracts;
- distribution mismatch with evaluation and deployment.

Balance by underlying behavior, not merely topic name. Preserve a verified
anchor set and add the smallest tranche that tests the next hypothesis.

## 10. Assign a row disposition

Give every row one terminal or actionable status:

- `train`: all hard gates pass;
- `replace-ancestor`: verified correction or revision;
- `review`: ambiguity, weak evidence, or unresolved overlap;
- `repair-and-reverify`: deterministic defect with recoverable source evidence;
- `reject`: wrong, leaked, unverifiable, conflicting, or malformed;
- `eval-only`: useful diagnostic that must not enter training.

Do not call a dataset train-ready while selected rows still have unresolved hard
gates.

## 11. Validate with training and held-out execution

Treat dataset audit and model validation as separate evidence tiers:

1. train a bounded canary or short checkpoint sequence;
2. keep model, optimizer, inference, and evaluation contracts fixed;
3. evaluate first-attempt success, repair success, and best-of-N separately;
4. run multiple seeds when sampling is stochastic;
5. report per-task gains, retained tasks, and regressions;
6. measure format validity, tokens, latency, and context exhaustion;
7. promote only on held-out task success, not training loss alone.

## Required outputs

Produce these artifacts or their equivalents:

- immutable source manifest and hashes;
- row-level audit catalog with categories, tags, evidence, and disposition;
- duplicate and revision-lineage report;
- contamination and split audit;
- tokenizer and length audit;
- verification receipt with oracle versions and test outcomes;
- category, tag, source, and token summaries;
- selected train and validation manifests;
- rejected and review queues with reasons;
- train-readiness decision and explicit limitations.

Lead the final report with confirmed counts, unresolved risks, and the next gate.
Keep structural validity, executable correctness, and completed training as
separate claims.

## Non-negotiable failures

Reject or quarantine a row when any of these is true:

- the target answer is known wrong or contradicted by a valid counterexample;
- evaluation labels, hidden tests, or private references leak into the input;
- the row exceeds the actual training context after official tokenization;
- the answer violates the required action or output contract;
- source or revision lineage is unknown where contamination matters;
- an ancestor and correction conflict without an explicit teaching structure;
- privacy, licensing, secret, or policy constraints prohibit use.

Do not convert absence of a discovered defect into proof of quality.
