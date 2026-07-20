# Claude Code Memory Guide

How Claude Code carries knowledge across sessions — and how to structure it so instructions actually get followed.

Two mechanisms:

- **CLAUDE.md files** — instructions *you* write (facts, conventions, standards)
- **Auto memory** — notes *Claude* writes itself from your corrections and preferences

Both load at the start of every session, and both are *context, not enforcement*. To guarantee a behavior, use a [PreToolUse hook](claude-hooks-guide.md) instead.

## CLAUDE.md Locations

Loaded in this order, broadest to most specific:

| Scope | Location | Use for |
|-------|----------|---------|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Org-wide standards, deployed by IT |
| User | `~/.claude/CLAUDE.md` | Your personal preferences across all projects |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared project instructions — commit it |
| Local | `./CLAUDE.local.md` | Personal per-project prefs — gitignore it |

Files above the working directory load fully at launch; files in subdirectories load on demand when Claude reads files there. All discovered files concatenate (they don't override); more specific files appear later in context.

## Setup & Maintenance

- **`/init`** — generates a starter CLAUDE.md by analyzing the repo (suggests improvements if one exists). Set `CLAUDE_CODE_NEW_INIT=1` for the interactive flow that also walks through skills, hooks, and personal memory.
- **`/memory`** — edit memory files, toggle auto memory, view auto-memory entries.
- **`/doctor`** — deduplicates local vs. checked-in CLAUDE.md content and can trim files by moving always-loaded guidance into on-demand skills and nested files.

Add an entry when: Claude makes the same mistake twice, a code review catches something Claude should have known, or you re-type a correction from last session.

## Writing Instructions That Stick

- **Under ~200 lines per file.** Every line costs context every session; long files reduce adherence.
- **Concrete and verifiable.** "Use 2-space indentation", "Run `npm test` before committing", "API handlers live in `src/api/handlers/`" — not "write clean code".
- **Structured.** Headers and bullets; Claude scans structure like a reader does.
- **Facts, not procedures.** A multi-step procedure belongs in a [skill](claude-skills-guide.md); file-specific conventions belong in path-scoped rules.
- **No contradictions.** Conflicting rules get resolved arbitrarily — audit periodically, especially in monorepos (`claudeMdExcludes` setting skips other teams' files).

Block-level HTML comments (`<!-- maintainer notes -->`) are stripped before injection — free documentation for humans.

## Imports

`@path/to/file` anywhere in CLAUDE.md inlines that file at launch (recursive, max depth 4):

```markdown
See @README for the project overview.

# Git Workflow
@docs/git-instructions.md
```

Relative paths resolve from the importing file. Wrap in backticks (`` `@README` ``) to mention without importing. External imports (outside the project) trigger a one-time approval dialog. To share personal instructions across git worktrees, import from home: `@~/.claude/my-project-instructions.md`.

## AGENTS.md Interop

Claude Code reads CLAUDE.md, not AGENTS.md. If your repo already has AGENTS.md for other coding agents, share one source:

```markdown
@AGENTS.md

## Claude Code specifics
Use plan mode for changes under src/billing/.
```

…or symlink: `ln -s AGENTS.md CLAUDE.md` (on Windows use the import; symlinks need admin/Developer Mode). `/init` in a repo with AGENTS.md (or `.cursorrules`, `.windsurfrules`, …) incorporates them automatically.

## Path-Scoped Rules: `.claude/rules/`

Split instructions into topic files that load **only when relevant**:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md      # no frontmatter → always loaded
    ├── testing.md
    └── api.md             # frontmatter below → loads only for matching files
```

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/**/*.{ts,tsx}"
---

# API Development Rules
- All endpoints include input validation
- Standard error response format
```

Rules trigger when Claude *reads* matching files. Globs support `**`, brace expansion; escape literal `[` as `\[`. Symlinks work — maintain a shared rule set and link it into every project (`ln -s ~/shared-rules .claude/rules/shared`). Personal rules live in `~/.claude/rules/` and load before project rules.

## Auto Memory

Claude takes notes from your corrections and preferences, per repository (shared across worktrees). Manage via `/memory`. It's loaded every session (first 200 lines / 25KB), best for build commands, debugging insights, and discovered preferences — the things you'd never write down yourself. Subagents can keep their own auto memory (`memory:` frontmatter, see the [Subagents Guide](claude-subagents-guide.md)).

## Decision Table

| Content | Put it in |
|---------|-----------|
| "API handlers live in src/api/" | CLAUDE.md |
| "Run npm test before committing" (should always hold) | CLAUDE.md **+ a hook if it must be enforced** |
| Conventions for one part of the tree | `.claude/rules/` with `paths:` |
| Multi-step deploy/release procedure | Skill with `disable-model-invocation` |
| Domain knowledge needed only sometimes | Skill (auto-invoked) |
| Personal editor/tool quirks | `~/.claude/CLAUDE.md` or CLAUDE.local.md |
| Things Claude learned from your corrections | Auto memory (automatic) |

## See Also

- [Skills Guide](claude-skills-guide.md) — procedures and on-demand knowledge
- [Hooks Guide](claude-hooks-guide.md) — actual enforcement
- [Search Best Practices](claude-code-search-best-practices.md) — memory files that improve search
- [Claude Code docs: memory](https://code.claude.com/docs/en/memory)
