# Claude Code Custom Commands Collection

Production-ready commands and skills for Claude Code. Every file includes YAML frontmatter (tool pre-approval, argument hints, invocation control) — see the [Custom Commands & Skills Guide](../claude-custom-commands.md) for what each field does.

## Installation

Commands work from either layout — pick one:

```bash
# As commands (single files)
mkdir -p .claude/commands
cp claude-commands/*.md .claude/commands/

# As skills (recommended; one directory per skill)
mkdir -p .claude/skills
for f in claude-commands/*.md; do
  name=$(basename "$f" .md)
  mkdir -p ".claude/skills/$name"
  cp "$f" ".claude/skills/$name/SKILL.md"
done
```

- **Project install** (`.claude/`): shared with your team via version control
- **Personal install** (`~/.claude/`): available across all your projects
- Invoke as `/name` from either location (the old `/project:` / `/user:` prefixes are gone)

## Available Commands

### 🔍 `/search-prompts`
Search across all Claude Code conversation history (session JSONL files) for a keyword.
Returns matching prompts, session summaries, and resumable session IDs (`claude --resume <id>`).

```
/search-prompts "machine learning pipeline"
```

### 📝 `/analyze-function`
Deep line-by-line analysis of any function: implementation details, performance implications, edge cases, and architectural context. Read-only tools pre-approved.

```
/analyze-function train.py:detect_words_gpu
```

### 🧠 `/multi-mind`
Multi-specialist collaborative analysis using parallel subagents. Dynamically assigns 4-6 decorrelated specialists, runs research and cross-pollination rounds, and synthesizes without flattening disagreement.

```
/multi-mind "Should we adopt CRDTs for our collaborative editor?"
/multi-mind "Postgres vs. FoundationDB for multi-tenant SaaS" rounds=5
```

### 📄 `/page`
OS-style paging for Claude's context: saves the complete session history (with full citations) to a `-full.md` file plus a `-compact.md` executive summary, then hands off to `/compact` to free context. Built-in alternatives: `/export` (plain text) and `/rewind` (checkpoints).

```
/page                                  # session-dump files in cwd
/page feature-implementation           # custom prefix
/page bug-fix ./docs/sessions/         # custom location
```

### 🔧 `/crud-claude-commands`
Manage the command/skill collection itself — create, read, update, delete, list — generating files with correct modern frontmatter.

```
/crud-claude-commands create git-flow "automate feature branches, PRs, merges"
/crud-claude-commands list
```

## Writing Your Own

Use this template (works for both `.claude/commands/<name>.md` and `.claude/skills/<name>/SKILL.md`):

```yaml
---
description: What it does and when to use it — Claude routes on this
argument-hint: "<expected args>"
allowed-tools: Read, Grep, Glob
---

# Command Name

Instructions for Claude. Use $ARGUMENTS, $0/$1, named arguments,
!`shell injection`, and @file references as needed.

## Examples
/command-name example input
```

Frontmatter quick reference: `description`, `when_to_use`, `argument-hint`, `arguments`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable`, `model`, `effort`, `context: fork`, `agent`, `hooks`, `paths`. Full details in the [Custom Commands & Skills Guide](../claude-custom-commands.md).

## Related Guides

- [Custom Commands & Skills Guide](../claude-custom-commands.md)
- [Agent Skills Guide](../claude-skills-guide.md) — supporting files, subagent execution, distribution
- [Subagents Guide](../claude-subagents-guide.md) — what powers `/multi-mind`
- [Conversation Search Guide](../claude-conversation-search-guide.md) — the storage format behind `/search-prompts`
- [Claude Code docs](https://code.claude.com/docs/en/skills)

## License

Same license as the agent-guides repository. Modify and adapt freely.
