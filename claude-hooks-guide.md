# Claude Code Hooks Guide

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. They are the **deterministic** layer: the model doesn't decide whether they run — when the event fires and the matcher hits, the hook runs. Use hooks for anything that must happen every time: guardrails, linting, logging, secret scanning, environment setup.

> If a rule should *always* be enforced, don't put it in CLAUDE.md (context, not enforcement) — put it in a `PreToolUse` hook.

## How a Hook Resolves

```
Event fires  →  matcher matches?  →  if condition matches?  →  handler runs  →  optional JSON decision
(tool call,     (tool name,           (permission-rule syntax     (command/http/      (allow / deny /
 prompt, etc.)    session source,      on tool input, e.g.         prompt handler)      inject context)
                  agent type, …)       "Bash(git *)")
```

Three levels of config nesting: **event** → **matcher group** → **handlers**.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

The handler receives event JSON on **stdin** and answers on **stdout**:

```bash
#!/bin/bash
# .claude/hooks/block-rm.sh — deny destructive rm, pass everything else
COMMAND=$(jq -r '.tool_input.command')
if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0   # no decision → normal permission flow
fi
```

Exit 0 with no output = no opinion. A hook can *deny*; staying silent does not approve.

## Events

| Cadence | Events |
|---------|--------|
| Once per session | `SessionStart`, `SessionEnd` |
| Once per turn | `UserPromptSubmit`, `Stop`, `StopFailure` |
| Every tool call | `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch` |
| Subagents & tasks | `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted` |
| Context lifecycle | `PreCompact`, `PostCompact`, `InstructionsLoaded` |
| Environment | `Notification`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove` |
| MCP | `Elicitation`, `ElicitationResult` |

What the `matcher` filters depends on the event: tool name for tool events (`Bash`, `Edit|Write`, `mcp__memory__.*`), session source for `SessionStart` (`startup`, `resume`, `clear`, `compact`), agent type for `SubagentStart/Stop`, `manual|auto` for compaction events. Matchers are exact strings (or `|`/`,`-separated lists) unless they contain regex characters, which makes them unanchored JavaScript regexes.

The `if` field on a handler narrows further using permission-rule syntax: `"Bash(git *)"` (any git subcommand), `"Edit(*.ts)"` (only TypeScript files). Use it — it avoids spawning a process for calls the handler would ignore anyway.

## Where Hooks Live

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All your projects | No |
| `.claude/settings.json` | One project | Yes — commit it |
| `.claude/settings.local.json` | One project | No (gitignored) |
| Managed policy settings | Organization | Admin-controlled |
| Plugin `hooks/hooks.json` | Plugin users | Yes |
| Skill/agent frontmatter `hooks:` | While that skill/agent is active | Yes (bundled with the component) |

## Recipes

### 1. Lint after every edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/lint.sh" }]
      }
    ]
  }
}
```

```bash
#!/bin/bash
FILE=$(jq -r '.tool_input.file_path')
case "$FILE" in
  *.py) ruff check --fix "$FILE" 2>&1 | head -20 ;;
  *.ts|*.tsx) npx eslint --fix "$FILE" 2>&1 | head -20 ;;
esac
exit 0
```

PostToolUse stdout is shown to Claude, so lint errors feed straight back into the loop for self-correction.

### 2. Block commands touching production config

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "if": "Bash(*prod*)", "command": "~/.claude/hooks/guard-prod.sh" }]
      }
    ]
  }
}
```

### 3. Log every session for searchability

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [{ "type": "command", "command": "jq -r '.session_id + \" \" + .cwd' >> ~/.claude/session-log.txt" }]
      }
    ]
  }
}
```

### 4. Snapshot context before compaction

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [{ "type": "command", "command": "cp ~/.claude/projects/*/$(jq -r .session_id).jsonl ~/claude-backups/ 2>/dev/null; exit 0" }]
      }
    ]
  }
}
```

(Or use the [`page`](claude-commands/page.md) command proactively instead.)

### 5. Skill-scoped hook

Hooks in skill frontmatter run only while that skill is active — e.g. force a test run after every edit *during a TDD skill*:

```yaml
---
description: Strict TDD workflow
hooks:
  PostToolUse:
    - matcher: Edit|Write
      hooks:
        - type: command
          command: ${CLAUDE_PROJECT_DIR}/run-tests.sh
---
```

## Handler Types

- **`command`** — shell command; JSON in on stdin, decision JSON on stdout. Covered above.
- **`http`** — POST the event JSON to an endpoint; the response body is the decision. Good for centralized org policy.
- **`prompt`** / **`agent`** — an LLM evaluates the event (e.g. "is this change consistent with our API conventions?"). Powerful but non-deterministic and slower — reserve for judgment calls that regex can't express.

## Gotchas

- **Hooks run with your credentials.** Review any hook you install from the internet like you'd review code you run.
- `jq` is the de-facto parser for command hooks — keep it on `PATH`.
- Matchers with hyphens/commas have version nuances (comma lists need v2.1.191+, hyphens in exact sets v2.1.195+); when in doubt use `|` or a regex.
- `UserPromptSubmit`, `Stop`, `PostToolBatch`, and several others ignore `matcher` entirely — it is silently dropped.
- Slow hooks slow every tool call. `/doctor` flags slow hooks; keep handlers fast and use `if` to skip irrelevant invocations.
- MCP tools match like normal tools: `mcp__<server>__<tool>`; append `.*` for a whole server (`mcp__memory__.*`). Plugin-bundled servers get scoped names (`mcp__plugin_<plugin>_<server>__<tool>`).
- Enterprises can force `allowManagedHooksOnly` — user/project hooks are then ignored by design.

## See Also

- [Skills Guide](claude-skills-guide.md) — skill-scoped hooks, and when a hook is the wrong tool
- [Subagents Guide](claude-subagents-guide.md) — `SubagentStart/Stop` events, agent frontmatter hooks
- [Claude Code docs: hooks reference](https://code.claude.com/docs/en/hooks) · [hooks guide](https://code.claude.com/docs/en/hooks-guide)
