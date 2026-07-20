# Claude Code Subagents Guide

Subagents are specialized AI workers that run in their own context window with their own system prompt, tool access, and permissions. Claude delegates to them based on their `description`, they work independently, and only the summary returns to your main conversation.

Use one when a side task would flood your context with search results, logs, or file contents you won't reference again — or when you want the same kind of worker with the same instructions every time.

## Built-in Subagents

| Agent | Model | Tools | Used for |
|-------|-------|-------|----------|
| **Explore** | Inherits session (capped at Opus) | Read-only | File discovery, code search, codebase Q&A |
| **Plan** | Inherits session | Read-only | Research during plan mode |
| **general-purpose** | Inherits session | All | Complex multi-step tasks needing both exploration and edits |

Explore and Plan skip your CLAUDE.md and git status to stay fast. You don't invoke these directly — Claude routes to them automatically. Override `Explore` by defining your own agent named `Explore` (e.g. with `model: haiku` to cut exploration cost).

## Creating a Custom Subagent

Subagents are Markdown files with YAML frontmatter. The fastest way is to ask Claude: *"Create a project subagent that reviews migrations for safety."* Or write the file yourself:

```markdown
---
name: migration-reviewer
description: Reviews database migrations for safety — locks, reversibility, data loss risk. Use after writing or modifying a migration.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a database migration specialist. For each migration, check:
- Lock duration on large tables (rewrite as concurrent/batched if needed)
- Reversibility — every up must have a working down
- Data loss risk in column drops/type changes
- Index creation strategy (CONCURRENTLY on Postgres)

Report findings by severity with file:line. Do not modify files.
```

Save to `.claude/agents/migration-reviewer.md`, then:

```
Use the migration-reviewer agent to check db/migrations/
```

Files are watched live — edits apply within seconds (a newly created `agents/` directory needs a restart). Since v2.1.198 `/agents` no longer opens a wizard; it reminds you to ask Claude or edit the files directly.

## Frontmatter Reference

| Field | Purpose |
|-------|---------|
| `name` | Unique ID, lowercase + hyphens (required) |
| `description` | When Claude should delegate — write it for the router (required) |
| `tools` | Allowed tools; inherits all if omitted |
| `disallowedTools` | Tools to remove from the inherited/specified set |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, full model ID, or `inherit` (default) |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Turn cap before the subagent stops |
| `skills` | Skills preloaded into its context at startup |
| `mcpServers` | MCP servers available to it (names or inline definitions) |
| `hooks` | Lifecycle hooks scoped to this subagent |
| `memory` | `user` / `project` / `local` — persistent cross-session learning |
| `background` | `true` = always run as a background task (default since v2.1.198 anyway) |
| `effort` | Effort override: `low`…`max` |
| `isolation` | `worktree` = run in a temporary git worktree with an isolated repo copy |
| `color` | Display color in the task list |
| `initialPrompt` | Auto-submitted first turn when run as the main agent |

## Scopes & Priority

| Location | Scope | Priority |
|----------|-------|----------|
| Managed settings | Organization | 1 (highest) |
| `--agents '<json>'` CLI flag | Current session only | 2 |
| `.claude/agents/` | Project — commit for your team | 3 |
| `~/.claude/agents/` | All your projects | 4 |
| Plugin `agents/` | Plugin users | 5 |

Directories are scanned recursively (organize into `agents/review/`, `agents/research/`). Keep `name` values unique across a tree — duplicates resolve by filesystem read order, and `/doctor` flags them. In nested monorepo directories, the definition closest to the working directory wins.

## Key Capabilities

### Worktree isolation

```yaml
isolation: worktree
```

The subagent gets its own checkout of the repo (branched from the default branch) — parallel agents can edit code without colliding with your working tree or each other. Auto-cleaned if it makes no changes. This is what powers the bundled `/batch` skill: decompose a large change into units, one worktree-isolated subagent per unit, one PR each.

### Background execution

Subagents run in the background by default (v2.1.198+). Launch several in one message for true parallelism; collect results with `/tasks`. Detach the *whole session* with `/background` when you want your terminal back.

### Persistent memory

```yaml
memory: project
```

The subagent accumulates learnings across sessions (per repository, shared across worktrees) — e.g. a reviewer that remembers which findings you rejected.

### Skills in subagents

`skills: [api-conventions]` injects the full skill content at startup. Subagents can also invoke other skills on demand. Going the other direction, a skill with `context: fork` runs its body inside a subagent.

## Orchestration Patterns

**Fan-out research** — launch N read-only subagents in one message, each on a different question; synthesize their summaries. (This repo's [`multi-mind`](claude-commands/multi-mind.md) command is a worked example.)

**Pipeline** — explorer → implementer → reviewer, passing each stage's output to the next. Keep each stage's context clean.

**Isolated implementation** — `isolation: worktree` + `background: true` for parallel feature branches; review each worktree's diff before merging.

**Cheap routing** — set `model: haiku` on mechanical agents (formatting, boilerplate generation), keep Opus for judgment calls.

For many independent *sessions* monitored from one place, see background agents (`/background`, `claude agents`); for sessions that communicate with each other, see agent teams in the Claude Code docs.

## Gotchas

- Subagents get **only their system prompt + environment basics** — not your conversation, not the main system prompt. Put everything they need in the prompt or delegate via a detailed Task description.
- Write the `description` for the router, same discipline as skills: "Use when…" phrasing.
- `cd` doesn't persist between a subagent's Bash calls; use absolute paths in instructions.
- Plugin subagents ignore `hooks`, `mcpServers`, and `permissionMode` — copy the file into `.claude/agents/` if you need those.
- Deny the `Agent` tool in `permissions.deny` to disable delegation entirely; `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` removes built-in Explore/Plan.

## See Also

- [Skills Guide](claude-skills-guide.md) — `context: fork`, preloading skills
- [Hooks Guide](claude-hooks-guide.md) — `SubagentStart/Stop` events
- [`multi-mind` command](claude-commands/multi-mind.md) — multi-specialist orchestration
- [Claude Code docs: subagents](https://code.claude.com/docs/en/sub-agents)
