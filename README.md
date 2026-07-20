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

## 🛠️ Ready-to-Use Skill

The [claude-skills/](claude-skills/) collection:

| Skill | Purpose |
|-------|---------|
| `/multi-mind` | Multi-specialist judgment analysis fanned out to parallel subagents, with adversarial cross-pollination rounds — for tradeoff/strategy questions where `/deep-research` (fact-finding) isn't the right tool |

## Quick Start

```bash
# Install the skill (project)
mkdir -p .claude/skills
cp -r claude-skills/multi-mind .claude/skills/

# Personal (all projects): use ~/.claude/skills/ instead
```

Then in any Claude Code session:

```
/multi-mind "Should we adopt CRDTs for our collaborative editor?" rounds=5
```

New project? Start with `/init` (set `CLAUDE_CODE_NEW_INIT=1` for the interactive flow), then `/doctor` to audit your setup.

## 🔧 Scripts

- [`extract-claude-session.py`](scripts/extract-claude-session.py) — export any session from `~/.claude/projects/` JSONL transcripts to markdown or cleaned JSONL.

## Contributing

- Add new skills (see the [Skills Guide](claude-skills-guide.md) for the format)
- Improve existing guides
- Share workflows via pull request

## License

Open source — modify and adapt for your needs. See [LICENSE](LICENSE).
