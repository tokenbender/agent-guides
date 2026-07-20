# Claude Code Conversation Search Guide

How to search your Claude Code conversation history across all projects and sessions — built-in features first, then the raw storage format for power searches.

## Start with the Built-ins

Most "find that thing I discussed" needs are covered without touching files:

| Tool | What it does |
|------|--------------|
| `/resume` | Interactive picker over past sessions, searchable, with previews |
| `claude --resume` | Same picker, from the shell |
| `claude --continue` | Jump straight back into the most recent session in this directory |
| `/rewind` | Roll code and conversation back to a checkpoint, or summarize part of the conversation |
| `/export [filename]` | Export the current conversation as plain text |
| `/insights` | Generate a report analyzing your sessions: project areas, interaction patterns, friction points |
| `/clear [name]` | Name the conversation you're leaving so it's findable in the `/resume` picker later |

Reach for raw file search only when you need something the picker can't do: full-text search across *all* projects at once, time-range filtering, or bulk analysis.

## Where History Lives

### Session transcripts: `~/.claude/projects/`

```
~/.claude/projects/
└── -Users-you-code-my-project/     # project path with / replaced by -
    ├── 9f3a1c2e-....jsonl          # one file per session, named by session UUID
    ├── 7b21d04f-....jsonl
    └── ...
```

Each `.jsonl` file is the full transcript: **one JSON event per line**. The event types that matter for search:

| `type` | Contains |
|--------|----------|
| `user` | Your prompts (in `message.content`) |
| `assistant` | Claude's responses, including tool calls |
| `summary` | One-line session summaries (shown in the `/resume` picker) |

Every event carries `uuid`, `parentUuid` (threading), `timestamp` (ISO 8601), `sessionId`, and `cwd`. Tool calls appear as `tool_use` blocks inside assistant message content.

### Config and prompt history: `~/.claude.json`

Global config file. Under `projects.<path>.history` it keeps a list of your **recent prompt strings** per project — useful for quick keyword hits on what you *asked*, but it does not contain Claude's responses or full conversations.

## Searching the JSONL Files

Install [`jq`](https://jqlang.github.io/jq/) for structured queries; plain `rg` (ripgrep) works for quick scans.

### Quick full-text scan across every project

```bash
rg -l --no-ignore -g '*.jsonl' 'kubernetes' ~/.claude/projects/
```

### Keyword search with context and timestamps (jq)

```bash
# All user prompts mentioning a term, newest first, across all sessions
find ~/.claude/projects -name '*.jsonl' -exec cat {} + | \
  jq -rs '
    [.[] | select(.type == "user") | select(.message.content | tostring | test("memory leak"; "i"))]
    | sort_by(.timestamp) | reverse | .[:15][]
    | "\(.timestamp)  [\(.sessionId[:8])]  \(.message.content | tostring | .[:160])"
  '
```

### List recent sessions with their summaries

```bash
find ~/.claude/projects -name '*.jsonl' | while read -r f; do
  summary=$(jq -rs '[.[] | select(.type == "summary")][0].summary // empty' "$f" 2>/dev/null)
  [ -n "$summary" ] && echo "$(stat -f '%Sm' "$f")  $(basename "$f" .jsonl)  $summary"
done | sort -r | head -20
```

### Filter by time range

```bash
# Sessions active in the last 7 days
find ~/.claude/projects -name '*.jsonl' -mtime -7 | while read -r f; do
  echo "$(basename "$f" .jsonl)  $(dirname "$f" | xargs basename)"
done
```

```bash
# Events within a date range (jq)
jq -rs '
  [.[] | select(.timestamp >= "2026-07-01" and .timestamp < "2026-07-08")]
  | .[] | "\(.timestamp)  \(.type)  \(.message.content // "" | tostring | .[:120])"
' ~/.claude/projects/-Users-you-code-my-project/*.jsonl
```

### Find which project a session belongs to

The directory name encodes the project path (`-Users-you-code-my-project` → `/Users/you/code/my-project`), and every event also carries `cwd`:

```bash
jq -rs '.[0] | "\(.cwd)  \(.sessionId)"' ~/.claude/projects/*/*.jsonl 2>/dev/null | sort -u
```

### Search only what *you* typed (prompt history)

```bash
jq -r '.projects | to_entries[] | .key as $p | .value.history[]? |
  "\($p | split("/") | last): \(.)"' ~/.claude.json | grep -i 'search term'
```

## Reusing What You Find

Once you have a session ID:

```bash
# Resume it interactively
claude --resume <session-id>

# Or extract the full transcript as markdown with this repo's script
python3 scripts/extract-claude-session.py --session-id <session-id> --format markdown
```

The script walks the same JSONL files, formats messages with timestamps and tool calls, and exports markdown or cleaned JSONL. See [`scripts/extract-claude-session.py`](scripts/extract-claude-session.py).

## As a Custom Command

The [`search-prompts`](claude-commands/search-prompts.md) command packages these searches so Claude runs them for you:

```
/search-prompts "machine learning pipeline"
```

## Shell Helpers

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Find session files mentioning a term, newest first
claude-find() {
  rg -l --no-ignore -g '*.jsonl' --sort modified "$1" ~/.claude/projects/ \
    | while read -r f; do echo "$(basename "$f" .jsonl)  $(dirname "$f" | xargs basename)"; done
}

# Dump the summaries of your 15 most recent sessions
claude-sessions() {
  find ~/.claude/projects -name '*.jsonl' -exec stat -f '%m %N' {} + \
    | sort -rn | head -"${1:-15}" | cut -d' ' -f2- \
    | while read -r f; do
        s=$(jq -rs '[.[] | select(.type == "summary")][0].summary // "(no summary)"' "$f" 2>/dev/null)
        echo "$(basename "$f" .jsonl)  $s"
      done
}
```

## Search Strategy

1. **Try `/resume` first.** The picker covers "continue that conversation" and shows summaries.
2. **`rg` for breadth, `jq` for precision.** Locate candidate files with ripgrep, then query their events with jq.
3. **Filter by directory name** to scope to one project; filter by `-mtime` or `timestamp` for recency.
4. **Note valuable session IDs** somewhere durable — file mtimes shift, IDs don't.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `jq` parse errors | Some lines are metadata, not messages — add `select(.type != null)` or `?` after filters, and redirect stderr |
| No results | Session files live under the *project* directory where you launched `claude`; search all of `~/.claude/projects/` |
| garbled `message.content` | Content can be a string *or* a list of blocks — pipe through `tostring` before matching |
| Session missing from `/resume` | The picker shows sessions for the current project; `cd` to the original directory or search files directly |

## See Also

- [Claude Code Search Best Practices](claude-code-search-best-practices.md) — searching *code* with Claude, not history
- [`search-prompts` command](claude-commands/search-prompts.md) — packaged version of these searches
- [`extract-claude-session.py`](scripts/extract-claude-session.py) — full session export
- [Claude Code docs: checkpointing & rewind](https://code.claude.com/docs/en/checkpointing)
