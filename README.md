# Agent Guides

Guides and production-ready commands for Claude Code: skills, subagents, hooks, memory, custom commands, and conversation-history tooling. Current as of July 2026 (skills-merged commands, native subagents, hooks, Agent Skills open standard).

## 📚 Guides

| Guide | What it covers |
|-------|----------------|
| [Agent Skills Guide](claude-skills-guide.md) | The 2026 extension primitive: SKILL.md, frontmatter, dynamic context injection, subagent execution, distribution |
| [Custom Commands & Skills](claude-custom-commands.md) | Quick-start for `/commands` — arguments, frontmatter, built-ins |
| [Subagents Guide](claude-subagents-guide.md) | `.claude/agents/`, worktree isolation, background execution, orchestration patterns |
| [Hooks Guide](claude-hooks-guide.md) | Deterministic automation: events, matchers, decision JSON, recipes |
| [Memory Guide](claude-memory-guide.md) | CLAUDE.md, `.claude/rules/`, auto memory, AGENTS.md interop |
| [Search Best Practices](claude-code-search-best-practices.md) | Finding things in your codebase with natural language |
| [Conversation Search Guide](claude-conversation-search-guide.md) | Searching your session history (JSONL storage, `/resume`, jq recipes) |

**Which one do I need?** Facts → [memory](claude-memory-guide.md). Procedures → [skills](claude-skills-guide.md). Isolated/parallel work → [subagents](claude-subagents-guide.md). Guaranteed enforcement → [hooks](claude-hooks-guide.md). External systems → MCP.

## 🛠️ Ready-to-Use Commands

The [claude-commands/](claude-commands/) collection — every command ships with modern frontmatter (tool pre-approval, argument hints, invocation control):

| Command | Purpose |
|---------|---------|
| `/search-prompts` | Full-text search across all conversation history, with resumable session IDs |
| `/analyze-function` | Line-by-line function deep dive with performance and edge-case analysis |
| `/multi-mind` | Multi-specialist analysis fanned out to parallel subagents with cross-pollination rounds |
| `/page` | Save full session history with citations, then hand off to `/compact` |
| `/crud-claude-commands` | Create/read/update/delete your command & skill collection |

## Quick Start

```bash
# Install as skills (recommended)
mkdir -p .claude/skills
for f in claude-commands/*.md; do
  name=$(basename "$f" .md)
  mkdir -p ".claude/skills/$name"
  cp "$f" ".claude/skills/$name/SKILL.md"
done

# Or as flat commands
mkdir -p .claude/commands
cp claude-commands/*.md .claude/commands/

# Personal (all projects): use ~/.claude/ instead of .claude/
```

Then in any Claude Code session:

```
/multi-mind "Should we adopt CRDTs for our collaborative editor?" rounds=5
/search-prompts "database optimization"
/analyze-function train.py:detect_words_gpu
/page feature-work
```

New project? Start with `/init` (set `CLAUDE_CODE_NEW_INIT=1` for the interactive flow), then `/doctor` to audit your setup.

## 🔧 Scripts

- [`extract-claude-session.py`](scripts/extract-claude-session.py) — export any session from `~/.claude/projects/` JSONL transcripts to markdown or cleaned JSONL. Powers the `/page` command.

## Contributing

- Add new commands/skills (use the [template](claude-commands/README.md#writing-your-own))
- Improve existing guides
- Share workflows via pull request

## License

Open source — modify and adapt for your needs. See [LICENSE](LICENSE).
