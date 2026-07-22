# Claude Code Skills Collection

Production-ready skills in the standard `.claude/skills/<name>/SKILL.md` layout.

## Installation

```bash
# Project (shared via version control)
mkdir -p .claude/skills
cp -r claude-skills/<skill-name> .claude/skills/

# Personal (all your projects)
cp -r claude-skills/<skill-name> ~/.claude/skills/

# Everything at once
cp -R claude-skills/*/ ~/.claude/skills/
```

Skill directories are watched live — files take effect in a running session within seconds (a newly created top-level `skills/` directory needs a restart).

## Available Skills

### Orchestration \u0026 analysis
| Skill | Purpose |
|-------|---------|
| `/multi-mind` | Multi-specialist judgment analysis via parallel subagents — for tradeoff/strategy questions where `/deep-research` (fact-finding) isn't the right tool |
| `epistemic-libido` | Filter and rank ideas for high-entropy mechanistic insight, underpriced leverage, and evidence-backed nerdsniping |
| `capability-horizon-estimator` | Estimate whether a model can complete a task and how long it takes — METR time-horizon model, benchmark anchors, best-of-N and wall-clock calculator |
| `audit-sft-data-quality` | Audit SFT datasets against the behavior they teach: contracts, hard gates, duplicates, contamination, train/review/reject dispositions |

### Research & experiment operations
| Skill | Purpose |
|-------|---------|
| `tokenbending` | Experiment discipline: deterministic contract vs fuzzy choices, preserve-before-delete, stop-on-first-substantive-failure |
| `worklog` | Issue-led atomic work logging: one issue per unit of work, comment journal, closeout checklist |

### Documents & OCR
| Skill | Purpose |
|-------|---------|
| `paper-ocr-notes-pipeline` | Paper PDF/URL → grounded OCR artifacts + teachable `notes.md` (orchestrates `pdf-ocr-feedback` + `technical-writing-workflow`) |
| `pdf-ocr-feedback` | High-accuracy OCR with self-scoring rubric and Maj@K consensus voting |

### Writing
| Skill | Purpose |
|-------|---------|
| `technical-writing-workflow` | Full writing workflow: ontology tables, outline contracts, rigor/plain-English/anti-LLM passes, audit scripts |
| `blade-and-contract` | Provocative-but-defensible rhetoric: lead with the blade, anchor with the contract |

### Tools & platforms
| Skill | Purpose |
|-------|---------|
| `playwright` | Browser automation from the terminal via `playwright-cli` (includes wrapper script + command reference) |
| `manim-math-explainer` | Manim Community math explainer scenes: style rules, templates, render loop |
| `x-thread-reader` | Full X/Twitter threads via twitter-thread.com mirror + fallbacks |

## Writing Your Own

See the [Agent Skills Guide](../claude-skills-guide.md) for the full format: frontmatter reference, dynamic context injection, supporting files, subagent execution, and distribution.

## License

Same license as the agent-guides repository. Modify and adapt freely.
