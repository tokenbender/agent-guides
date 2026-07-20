# Agent Skills Guide

Skills are the 2026 extension primitive for Claude Code: a `SKILL.md` file with instructions that Claude loads when relevant, or that you invoke directly with `/skill-name`. Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, so a well-written skill ports to other tools that implement the spec.

Custom commands have been merged into skills: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. Commands keep working; skills add supporting files, automatic invocation, and subagent execution.

## When to Write a Skill

- You keep pasting the same instructions, checklist, or procedure into chat
- A section of CLAUDE.md has grown into a *procedure* rather than a *fact*
- You want Claude to apply domain knowledge automatically, only when relevant
- You need a prompt plus supporting files (templates, scripts, examples)

Unlike CLAUDE.md content (loaded every session), a skill's body loads only when used — long reference material costs almost nothing until needed.

## Which Surface When

Claude Code has five extension mechanisms. Pick by trigger:

| Surface | Triggered by | Use for |
|---------|-------------|---------|
| **CLAUDE.md / rules** | Always loaded (or path-scoped) | Facts, conventions, standards |
| **Skill** | You type `/name`, or Claude decides it's relevant | Procedures, checklists, domain knowledge |
| **Subagent** | Claude delegates by description | Isolated context, parallel work, tool restrictions |
| **Hook** | Lifecycle event fires (deterministic — the model can't skip it) | Guardrails, linting, logging, enforcement |
| **MCP server** | Tool call | External systems and data sources |

A skill can bundle the others: `context: fork` runs it in a subagent, `hooks:` scopes hooks to its lifecycle, and a plugin wraps skills + agents + hooks + MCP servers for distribution.

## Anatomy

```
my-skill/
├── SKILL.md           # required — frontmatter + instructions
├── template.md        # optional: template for Claude to fill in
├── examples/
│   └── sample.md      # optional: example outputs
└── scripts/
    └── validate.sh    # optional: scripts Claude can run
```

```yaml
---
description: Summarizes uncommitted changes and flags risks. Use when the user asks what changed or wants a commit message.
argument-hint: "[path]"
allowed-tools: Bash, Read
---

## Current changes

!`git diff HEAD`

Summarize the changes above in 2-3 bullets, then list risks (missing error
handling, hardcoded values, stale tests). Empty diff = say so.
```

The directory name becomes the command (`/my-skill`). The `` !`git diff HEAD` `` line is **dynamic context injection**: it executes before Claude reads the skill and the output is inlined — the prompt arrives grounded in live state.

## Frontmatter Reference

All optional except `description` (effectively required — it's what Claude routes on).

| Field | Purpose |
|-------|---------|
| `description` | What + when. Front-load the use case; the listing truncates description+when_to_use at 1,536 chars |
| `when_to_use` | Extra trigger phrases appended to the description |
| `name` | Display label (doesn't change the `/command` — that's the directory name) |
| `argument-hint` | Autocomplete hint: `[issue-number]` |
| `arguments` | Named positional args: `[issue, branch]` → `$issue`, `$branch` |
| `disable-model-invocation` | `true` = manual `/name` only (deploys, destructive ops) |
| `user-invocable` | `false` = hidden from `/` menu (pure background knowledge) |
| `allowed-tools` | Tools pre-approved while the skill runs |
| `disallowed-tools` | Tools removed while active (e.g. `AskUserQuestion` in a background loop) |
| `model` | Model override for the turn |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` |
| `context` | `fork` = run in an isolated subagent (see below) |
| `agent` | Subagent type to use with `context: fork` |
| `hooks` | Lifecycle hooks scoped to this skill |
| `paths` | Globs — auto-load only when working with matching files |
| `shell` | `bash` (default) or `powershell` for injections |

### Substitutions

`$ARGUMENTS` · `$0`/`$1`/… (0-based) · `$name` from `arguments:` · `${CLAUDE_SESSION_ID}` · `${CLAUDE_EFFORT}` · `${CLAUDE_SKILL_DIR}` (reference bundled scripts portably) · `${CLAUDE_PROJECT_DIR}` · `@path/to/file` (inline file content) · `` !`cmd` `` (inline command output).

## Locations & Precedence

| Location | Path | Scope |
|----------|------|-------|
| Enterprise | managed settings | Whole org |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This repo (commit it) |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Plugin users, namespaced `/plugin:name` |

Precedence: enterprise > personal > project; any of them overrides a bundled skill of the same name (ship your own `code-review` to replace `/code-review`). A skill beats a same-name flat command. Nested `.claude/skills/` in monorepo packages are discovered on demand; name clashes get directory-qualified (`/apps/web:deploy`).

Skill directories are **watched live** — edits take effect mid-session (a brand-new top-level `skills/` dir needs a restart).

## Running Skills in Subagents

`context: fork` executes the skill body in a forked subagent with its own context window — the main conversation only receives the result. Use for heavy analysis (audits, large refactors) that would otherwise flood your context. Pair with `agent:` to pick a subagent type and `allowed-tools` to restrict it.

```yaml
---
description: Deep security audit of the auth subsystem
context: fork
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---
```

## Bundled Skills (Know Before You Rebuild)

`/code-review` (diff review, `--fix`, `--comment`, `ultra` for cloud) · `/simplify` · `/security-review` · `/debug` · `/doctor` (setup checkup, fixes config) · `/batch` (fan a large change across worktree-isolated subagents, one PR each) · `/loop` (scheduled prompts) · `/run` + `/verify` + `/run-skill-generator` (launch and verify your app) · `/deep-research` (cited web research) · `/fewer-permission-prompts` · `/claude-api` · `/dataviz` · `/design-sync`.

Override any of them per-project by creating a same-name skill.

## Writing Skills That Work

1. **Description = routing.** Write "Use when the user asks X or Y." Vague descriptions never auto-fire; overly broad ones fire constantly.
2. **Lean body.** Loaded skill content stays in context all session. State what to do, not essays about why. Push reference material into supporting files the skill tells Claude to read on demand.
3. **Ground with injection.** `` !`git status` ``, `` !`npm ls --depth=0` `` — facts beat guesses.
4. **Procedures, not facts.** Facts belong in CLAUDE.md/rules; multi-step procedures belong here.
5. **Minimal tools.** `allowed-tools` is a pre-approval grant — keep it tight.
6. **Examples beat adjectives.** An `examples/` file showing ideal output improves quality more than paragraphs of description.
7. **Test both paths.** Invoke `/name` explicitly *and* phrase a natural request that should auto-trigger it.

## Distribution

- **Git repo**: commit `.claude/skills/` — the team gets them on clone
- **Plugin**: add `.claude-plugin/plugin.json` to bundle skills + agents + hooks + MCP servers; share via a marketplace
- **Symlink**: a `<skill-name>` symlink in `~/.claude/skills/` pointing at a central checkout works for personal reuse across machines
- **Cloud/Cowork sessions** don't read `~/.claude/skills/` — commit skills to the repo or enable them for your claude.ai account

## See Also

- [Custom Commands Guide](claude-custom-commands.md) — quick-start version of this material
- [Subagents Guide](claude-subagents-guide.md) — `context: fork` in depth
- [Hooks Guide](claude-hooks-guide.md) — skill-scoped hooks
- [Memory Guide](claude-memory-guide.md) — facts vs. procedures
- [Claude Code docs: skills](https://code.claude.com/docs/en/skills)
