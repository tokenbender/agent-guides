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

`molab-gpu` is maintained here as a portable, single-file skill. On this Mac,
`~/.agents/skills/molab-gpu`, `~/.codex/skills/molab-gpu`, and
`~/.claude/skills/molab-gpu` link to that source directory. Grok Bot has a copy in
its shared cloud library. The existing Grok Bot CLI's `skills add` imports a new
entry rather than updating one. After saving the source, remove only the previous
`molab-gpu` library entry by its exact ID, import the source again, and verify
there is exactly one matching skill. Cloud updates are explicit; no background
synchronizer is installed.

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
| `tokenbending-preflight` | Zero-dollar line-by-line spec-vs-code audit (`1–10` score, `file:line` blindspots, real-artifact verification) |
| `tokenbending-experimenting` | Trust-region & causal-delta operating rules, real-artifact & control checks, preemption-safe sync, clarify-before-spend gate |
| `tokenbending-worklog` | Issue-led atomic work logging: master/child GitHub issues, atomic commits, residual-work audit, linked journal sync |
| `tokenbending-etl` | Executive Tech Lead update: verdict + unit economics, measured stage-by-stage bottleneck table, ROI-ranked action plan |

### Documents & OCR
| Skill | Purpose |
|-------|---------|
| `paper-ocr-notes-pipeline` | Paper PDF/URL → grounded OCR artifacts + teachable `notes.md` (orchestrates `pdf-ocr-feedback` + `technical-writing-workflow`) |
| `pdf-ocr-feedback` | High-accuracy OCR with self-scoring rubric and Maj@K consensus voting |

### Writing
| Skill | Purpose |
|-------|---------|
| `ncert-textbook` | NCERT Class IX–XI + Feynman discovery-before-explanation technical textbook writing & 4-bit lossless A4 WeasyPrint typesetting grounded in real traces/data |
| `technical-writing-workflow` | Full writing workflow: ontology tables, outline contracts, rigor/plain-English/anti-LLM passes, audit scripts |
| `blade-and-contract` | Provocative-but-defensible rhetoric: lead with the blade, anchor with the contract |

### Tools & platforms
| Skill | Purpose |
|-------|---------|
| `playwright` | Browser automation from the terminal via `playwright-cli` (includes wrapper script + command reference) |
| `manim-math-explainer` | Manim Community math explainer scenes: style rules, templates, render loop |
| `x-thread-reader` | Full X/Twitter threads via twitter-thread.com mirror + fallbacks |
| `molab-gpu` | Run experiments on Molab's remote GPU through marimo pair; portable across Codex, Claude Code, and Grok Bot |

## Writing Your Own

See the [Agent Skills Guide](../claude-skills-guide.md) for the full format: frontmatter reference, dynamic context injection, supporting files, subagent execution, and distribution.

## License

Same license as the agent-guides repository. Modify and adapt freely.
