---
description: Create, read, update, delete, and list Claude Code custom commands and skills
argument-hint: "<operation> <name> [instructions]"
disable-model-invocation: true
---

# CRUD Claude Commands - Dynamic Command & Skill Management

Manage Claude Code custom commands and skills through Create, Read, Update, and Delete operations.

**Usage**: `/crud-claude-commands <operation> <name> [instructions]`

Note: custom commands and skills are the same mechanism now. Default to the **skill layout** (`.claude/skills/<name>/SKILL.md`) for anything new; use the flat command layout (`.claude/commands/<name>.md`) only for simple single-file prompts.

## Operations

| Operation | Usage | Example |
|-----------|-------|---------|
| CREATE | `/crud-claude-commands create <name> "what it should do"` | `create git-flow "automate feature branches, PRs, merges"` |
| READ | `/crud-claude-commands read <name>` | `read multi-mind` |
| UPDATE | `/crud-claude-commands update <name> "changes"` | `update page "add JSON export format"` |
| DELETE | `/crud-claude-commands delete <name>` | `delete old-command` |
| LIST | `/crud-claude-commands list` | — |

## Implementation

Parse the operation from $ARGUMENTS and execute:

### CREATE
1. Parse name and description.
2. Choose layout: skill (default) or flat command if trivially simple.
3. Write the file with proper frontmatter:

   **Skill** — `.claude/skills/<name>/SKILL.md`:
   ```yaml
   ---
   description: <what it does + when to use it — this drives auto-invocation>
   argument-hint: "<expected args>"
   allowed-tools: <minimal tool set>
   ---

   # <Name>

   <concise instructions for Claude>

   ## Examples
   /<name> <example usage>
   ```

   **Command** — `.claude/commands/<name>.md`: same frontmatter, same body, no directory.

4. Frontmatter guidance:
   - `description`: front-load the use case; it's what Claude routes on
   - `allowed-tools`: pre-approve the minimum (`Read, Grep` for read-only; add `Bash, Write, Edit` only when needed)
   - `disable-model-invocation: true` for deploy/destructive workflows
   - `context: fork` for heavy analysis that shouldn't fill the main context
   - Use `$ARGUMENTS`, `$0`/`$1`, named `arguments:`, `` !`cmd` `` injection, and `@file` references as appropriate
5. Confirm with the file path and a one-line summary.

### READ
1. Check `.claude/skills/<name>/SKILL.md` first, then `.claude/commands/<name>.md`, then the `~/.claude/` equivalents.
2. Display the full content with its location.

### UPDATE
1. Read the existing file (skill first, as above).
2. Apply the requested changes, preserving valid frontmatter.
3. Show a before/after summary of what changed.

### DELETE
1. Locate the file (skill directory or command file).
2. Show its content, then delete (remove the whole directory for skills).
3. Confirm deletion.

### LIST
1. Enumerate `.claude/skills/*/SKILL.md`, `.claude/commands/*.md`, and `~/.claude/` equivalents.
2. For each: name, layout, description (from frontmatter), and scope (project/personal).
3. Also list relevant bundled skills (`/code-review`, `/debug`, `/batch`…) so users don't recreate them.

## Syncing to agent-guides

This collection lives at `https://github.com/tokenbender/agent-guides` (`claude-commands/` directory). After CREATE/UPDATE/DELETE:

1. Show the user the final file content for easy copying.
2. If the agent-guides repo is checked out locally, offer to copy the file into `claude-commands/` and update `claude-commands/README.md`.
3. Suggest a PR for generally useful commands.

## Error Handling

- **Not found**: fuzzy-match against existing names and suggest the closest
- **Ambiguous name** (both skill and command exist): show both, ask which
- **Invalid operation**: list valid operations
- **Permission errors**: report the path that failed

## Quality Bar for Generated Commands

- Reusable across projects, not one-off
- `description` written for the auto-invocation router
- Minimal `allowed-tools`
- Concise body — loaded content stays in context for the session
- At least one usage example

Execute the requested operation now.
