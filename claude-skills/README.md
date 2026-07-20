# Claude Code Skills Collection

Production-ready skills in the standard `.claude/skills/<name>/SKILL.md` layout.

## Installation

```bash
# Project (shared via version control)
mkdir -p .claude/skills
cp -r claude-skills/multi-mind .claude/skills/

# Personal (all your projects)
cp -r claude-skills/multi-mind ~/.claude/skills/
```

Skill directories are watched live — files take effect in a running session within seconds (a newly created top-level `skills/` directory needs a restart).

## Available Skills

### 🧠 `/multi-mind`
Multi-specialist collaborative analysis for **judgment questions** — architecture tradeoffs, strategy, design decisions. Dynamically assigns 4-6 decorrelated specialists, fans them out to parallel subagents for research and adversarial cross-pollination, then synthesizes across rounds without flattening disagreement.

```
/multi-mind "Should we adopt CRDTs for our collaborative editor?"
/multi-mind "Postgres vs. FoundationDB for multi-tenant SaaS" rounds=5
```

Use `/deep-research` (bundled) for factual questions; use this when the answer depends on weighing expert perspectives.

## Writing Your Own

See the [Agent Skills Guide](../claude-skills-guide.md) for the full format: frontmatter reference, dynamic context injection, supporting files, subagent execution, and distribution.

## License

Same license as the agent-guides repository. Modify and adapt freely.
