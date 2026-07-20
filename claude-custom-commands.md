# Custom Commands & Skills in Claude Code

Claude Code's custom slash commands are files you write once and invoke with `/name`. As of the current releases, **custom commands have been merged into skills**: a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Existing `.claude/commands/` files keep working and support the same frontmatter.

Skills add a few things plain command files can't do: a directory for supporting files (templates, scripts, examples), automatic invocation by Claude when relevant, and subagent execution. Prefer skills for anything new.

## Where Commands & Skills Live

| Location | Path | Applies to |
|----------|------|------------|
| Personal | `~/.claude/commands/*.md` or `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/commands/*.md` or `.claude/skills/<name>/SKILL.md` | This project (commit to share with your team) |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Wherever the plugin is enabled, namespaced as `/plugin:name` |

If a skill and a command share a name, the skill wins. Whatever the location, you invoke it as `/name` — the old `/project:` and `/user:` prefixes are gone.

### Quick start

```bash
# Command (single file)
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations." > .claude/commands/optimize.md

# Skill (directory, recommended)
mkdir -p .claude/skills/optimize
```

```yaml
# .claude/skills/optimize/SKILL.md
---
description: Analyze code for performance issues and suggest optimizations. Use when the user asks to speed something up or profile hot paths.
argument-hint: "[file-or-function]"
allowed-tools: Read, Grep, Glob, Bash
---

Analyze $ARGUMENTS for performance issues: allocation patterns, hot loops,
unnecessary copies, async blocking. Suggest concrete optimizations with
expected impact.
```

Test both ways: type `/optimize src/parser.ts`, or just ask "make the parser faster" and let Claude load the skill automatically.

## Frontmatter Reference

All fields optional; `description` is strongly recommended — Claude uses it to decide when to load the skill on its own.

| Field | Purpose |
|-------|---------|
| `description` | What it does and when to use it. Front-load the key use case (listing is truncated at 1,536 chars) |
| `when_to_use` | Extra trigger phrases/examples appended to the description |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` |
| `arguments` | Named positional args, e.g. `[issue, branch]` → `$issue`, `$branch` |
| `disable-model-invocation` | `true` = only runs when you type `/name` |
| `user-invocable` | `false` = hidden from the `/` menu (background knowledge only) |
| `allowed-tools` | Tools pre-approved while the skill runs (`Read, Grep, Bash`) |
| `disallowed-tools` | Tools removed while the skill is active |
| `model` | Model override for the turn (`sonnet`, `opus`, `haiku`, `inherit`) |
| `effort` | Effort override: `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` = run in an isolated subagent context |
| `agent` | Which subagent type to use with `context: fork` |
| `hooks` | Lifecycle hooks scoped to this skill |
| `paths` | Globs limiting auto-activation to matching files |

## Arguments & Dynamic Content

### Positional and named arguments

```yaml
---
description: Create a fix branch for a GitHub issue
arguments: [issue, branch]
---

Fix issue #$issue following our coding standards. Work on branch $branch.
```

```
/fix-issue 123 bug/login-loop
```

- `$ARGUMENTS` — everything passed after the command name
- `$0`, `$1`, `$2` — positional (0-based; `$ARGUMENTS[0]` also works)
- `$name` — named, mapped to positions by the `arguments` list

### Dynamic context injection

Lines of the form `` !`command` `` execute *before* Claude sees the skill; the output is inlined into the prompt. Perfect for grounding in live state:

```markdown
## Current changes

!`git diff HEAD --stat`

## Recent commits

!`git log --oneline -5`

Summarize the state of the working tree above.
```

### File references

`@path/to/file` inlines a file's content into the skill prompt.

### Environment substitutions

`${CLAUDE_SESSION_ID}`, `${CLAUDE_SKILL_DIR}` (the skill's own directory — use it to call bundled scripts), `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_EFFORT}`.

## Namespacing

Subdirectories under `.claude/commands/` create namespaced commands: `.claude/commands/frontend/component.md` → `/frontend:component`. Nested `.claude/skills/` directories in monorepo packages are discovered on demand when Claude works in those directories.

## Built-in Commands & Bundled Skills You'll Use Daily

Type `/` for the full list. Highlights:

| Command | Purpose |
|---------|---------|
| `/init` | Generate a starter `CLAUDE.md` (set `CLAUDE_CODE_NEW_INIT=1` for the interactive flow that also sets up skills and hooks) |
| `/memory` | Edit memory files, manage auto-memory |
| `/compact [focus]` | Summarize the conversation to free context |
| `/context` | Visualize what's filling the context window |
| `/rewind` | Roll code/conversation back to a checkpoint |
| `/resume`, `/branch`, `/fork` | Reopen, branch, or copy conversations |
| `/plan` | Plan mode before large changes |
| `/model`, `/effort` | Switch model / reasoning effort |
| `/tasks`, `/background` | Manage background agents |
| `/permissions` | Approval rules |
| `/usage` | Token usage breakdown (alias: `/cost`) |
| `/doctor` | Setup checkup — diagnoses *and fixes* config issues |
| `/export` | Export the conversation as text |

Bundled **skills** (prompt-based, overridable by your own same-name skill): `/code-review`, `/security-review`, `/debug`, `/batch` (parallel large-scale changes in worktrees), `/loop` (scheduled prompts), `/run`, `/verify`, `/deep-research`, `/fewer-permission-prompts`, `/claude-api`.

## Best Practices

1. **Write the description for the router.** "Use when the user asks X, Y, Z" gets auto-invoked correctly; vague descriptions never fire.
2. **One job per skill.** Compose with skill chaining (`/skill-a /skill-b rest of prompt`) instead of building mega-skills.
3. **Keep the body lean.** Once loaded, skill content stays in context for the rest of the session — every line is a recurring token cost.
4. **Pre-approve narrowly.** `allowed-tools: Read, Grep` beats blanket access; use `disable-model-invocation: true` for destructive or deploy-type workflows.
5. **Ground with injection.** Prefer `` !`git status` `` over asking Claude to check — the fact arrives in the prompt.
6. **Commit project skills.** `.claude/skills/` in the repo = shared team capability, versioned like code.
7. **Move procedures out of CLAUDE.md.** Facts stay in CLAUDE.md; multi-step procedures belong in skills.

## Examples

### Release notes from live git state

```yaml
---
description: Draft release notes from commits since the last tag. Use when preparing a release or changelog.
argument-hint: "[since-tag]"
allowed-tools: Bash
---

## Commits since last release

!`git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD`

## Changed files

!`git diff --stat $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD | tail -5`

Group the commits above into Features / Fixes / Internal. Write user-facing
release notes: one line per item, no commit hashes, flag breaking changes.
```

This pattern — `` !`injection` `` grounding the prompt in live repo state — is what makes skills beat pasted prompts. (For diff review, use the bundled `/code-review` instead of writing your own.)

### Bug triage

```yaml
---
description: Triage a bug report into root cause, severity, and fix plan
argument-hint: "<bug description>"
disable-model-invocation: true
---

Analyze this bug report and provide:
1. Root cause hypothesis with evidence from the codebase
2. Severity assessment (blocker / high / medium / low)
3. Recommended fix approach
4. Test that would have caught it

Bug: $ARGUMENTS
```

## See Also

- [Agent Skills Guide](claude-skills-guide.md) — skills in depth: supporting files, subagent execution, distribution
- [Subagents Guide](claude-subagents-guide.md) — `context: fork` and `.claude/agents/`
- [Hooks Guide](claude-hooks-guide.md) — deterministic automation around the agent loop
- [Skills Collection](claude-skills/) — ready-to-use skills from this repo
- [Claude Code docs: skills](https://code.claude.com/docs/en/skills) · [commands reference](https://code.claude.com/docs/en/commands)
