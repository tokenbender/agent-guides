# Agent Guides

Field guides and a production skill collection for Claude Code, current with the July 2026 ecosystem: commands merged into skills, native subagents with worktree isolation, lifecycle hooks, path-scoped memory, and the Agent Skills open standard.

> The repo tracks the ecosystem as it moves. Last full audit: July 2026 against `code.claude.com/docs` and METR's published time-horizon data.

## 📚 Guides

| Guide | What it covers |
|-------|----------------|
| [Agent Skills](claude-skills-guide.md) | SKILL.md anatomy, full frontmatter, dynamic context injection, `context: fork` subagent execution, precedence, distribution |
| [Custom Commands](claude-custom-commands.md) | `/commands` quick start: arguments, frontmatter, built-in command map |
| [Subagents](claude-subagents-guide.md) | `.claude/agents/`, background-by-default execution, worktree isolation, persistent memory, orchestration patterns |
| [Hooks](claude-hooks-guide.md) | Deterministic guardrails: event table, matchers, decision JSON, five production recipes |
| [Memory](claude-memory-guide.md) | CLAUDE.md, `.claude/rules/` path scoping, auto memory, AGENTS.md interop, what-goes-where table |
| [Code Search](claude-code-search-best-practices.md) | Natural-language codebase search, memory files that improve it, custom search skills |
| [Conversation Search](claude-conversation-search-guide.md) | Session history: JSONL storage format, `/resume` picker, jq/rg power recipes |

**Which surface when:** facts → [memory](claude-memory-guide.md) · procedures → [skills](claude-skills-guide.md) · isolated or parallel work → [subagents](claude-subagents-guide.md) · hard enforcement → [hooks](claude-hooks-guide.md) · external systems → MCP.

## 🛠️ Skills Collection

[claude-skills/](claude-skills/) — 16 skills in standard `SKILL.md` layout, dependencies (references, templates, scripts) included. Install one or all:

```bash
cp -r claude-skills/multi-mind ~/.claude/skills/   # one
cp -R claude-skills/*/ ~/.claude/skills/           # all
```

| Skill | What it does |
|-------|--------------|
| [multi-mind](claude-skills/multi-mind/) | Fans judgment questions out to 4-6 decorrelated specialist subagents with adversarial cross-pollination rounds |
| [capability-horizon-estimator](claude-skills/capability-horizon-estimator/) | Answers "can the model do this, and how long will it take" with METR time-horizon math: logistic success curve, doubling-rate extrapolation, best-of-N, wall-clock calculator |
| [epistemic-libido](claude-skills/epistemic-libido/) | Filters and ranks papers, posts, and ideas for high-entropy mechanistic insight and underpriced leverage — separates fertile results from hype |
| [audit-sft-data-quality](claude-skills/audit-sft-data-quality/) | Audits SFT datasets against the behavior they teach: contracts, contamination, lineage, train/review/reject dispositions |
| [tokenbending-preflight](claude-skills/tokenbending-preflight/) | Zero-dollar line-by-line spec-vs-code audit (`1–10` score, `file:line` blindspots, real-artifact verification) |
| [tokenbending-experimenting](claude-skills/tokenbending-experimenting/) | Trust-region & causal-delta operating rules, real-artifact & control checks, preemption-safe sync, clarify-before-spend gate |
| [tokenbending-worklog](claude-skills/tokenbending-worklog/) | Issue-led atomic work journal: master/child GitHub issues, atomic commits, residual-work audit, linked journal sync |
| [tokenbending-etl](claude-skills/tokenbending-etl/) | Executive Tech Lead update: verdict + unit economics, measured bottleneck table, ROI-ranked action plan |
| [paper-ocr-notes-pipeline](claude-skills/paper-ocr-notes-pipeline/) | Paper PDF/URL → grounded OCR + teachable notes.md, with identity gate and revision passes |
| [pdf-ocr-feedback](claude-skills/pdf-ocr-feedback/) | High-accuracy OCR via self-scoring rubric and Maj@K consensus voting |
| [technical-writing-workflow](claude-skills/technical-writing-workflow/) | Full technical writing pipeline: ontology tables, outline contracts, rigor and anti-slop passes, audit scripts |
| [blade-and-contract](claude-skills/blade-and-contract/) | Provocative but defensible rhetoric: lead with the blade, anchor with the contract |
| [playwright](claude-skills/playwright/) | Browser automation from the terminal via playwright-cli, wrapper script included |
| [manim-math-explainer](claude-skills/manim-math-explainer/) | Manim Community math scenes: style rules, templates, render loop |
| [x-thread-reader](claude-skills/x-thread-reader/) | Full X/Twitter threads through twitter-thread.com with fallbacks |
| [molab-gpu](claude-skills/molab-gpu/) | Run experiments in a live Molab GPU notebook through the official marimo pair CLI; shared with Codex, Claude Code, and Grok Bot |

### Try the newest one

```bash
# Can a 12-hour-horizon model do a 4-hour task? 
python3 claude-skills/capability-horizon-estimator/scripts/estimate.py --h50 719 --task-min 240
# SINGLE ATTEMPT: 70.6%  VERDICT: LIKELY  WALL-CLOCK EST: ~48 min
```

## 🔧 Scripts

- [`extract-claude-session.py`](scripts/extract-claude-session.py) — exports any session from `~/.claude/projects/` JSONL transcripts to markdown or cleaned JSONL.

## Contributing

Add a skill (format: [Agent Skills guide](claude-skills-guide.md)), fix a fact, or open a PR with a workflow worth sharing.

## License

See [LICENSE](LICENSE).
