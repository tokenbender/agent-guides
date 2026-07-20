---
description: Search across all Claude Code conversation history (session JSONL files) for a keyword or topic, and return resumable session IDs
argument-hint: "<search term>"
allowed-tools: Bash, Read, Grep
---

# Search Prompts - Conversation History Search

Search across all Claude Code conversation history for: **$ARGUMENTS**

## Where the history lives

Claude Code stores every session as a JSONL transcript (one JSON event per line):

```
~/.claude/projects/<project-slug>/<session-id>.jsonl
```

- `<project-slug>` is the project path with `/` replaced by `-`
- Events with `type: "user"` hold prompts, `type: "assistant"` holds responses, `type: "summary"` holds session summaries
- Every event has `timestamp`, `sessionId`, `cwd`, and `uuid`

Run the searches below with the Bash tool. Never interpolate the search term directly into SQL or unquoted shell — pass it via an environment variable or `jq --arg` to avoid quoting/injection bugs.

## Step 1: Broad file scan

Locate candidate transcripts with ripgrep:

```bash
rg -l --no-ignore -g '*.jsonl' --sort modified "$TERM" ~/.claude/projects/
```

## Step 2: Structured search with jq

Pull matching user prompts with timestamps and session IDs:

```bash
find ~/.claude/projects -name '*.jsonl' -exec cat {} + | \
  jq -rs --arg term "$TERM" '
    [.[] | select(.type == "user")
        | select(.message.content | tostring | test($term; "i"))]
    | sort_by(.timestamp) | reverse | .[:15][]
    | "\(.timestamp)  session:\(.sessionId[:8])  \(.message.content | tostring | .[:160])"
  '
```

Also search assistant responses (solutions, explanations) the same way with `.type == "assistant"`.

## Step 3: Session summaries and recency

```bash
# Summaries matching the term
find ~/.claude/projects -name '*.jsonl' | while read -r f; do
  jq -rs --arg term "$TERM" '
    [.[] | select(.type == "summary") | select(.summary | test($term; "i"))][0]
    | "\(.sessionId)  \(.summary)"' "$f" 2>/dev/null
done

# Sessions active in the last 7 days
find ~/.claude/projects -name '*.jsonl' -mtime -7
```

## Step 4: Prompt history in ~/.claude.json

Recent prompt strings per project (fast, shallow):

```bash
jq -r --arg term "$TERM" '
  .projects | to_entries[] | .key as $p | .value.history[]?
  | select(test($term; "i"))
  | "\($p | split("/") | last): \(.)"' ~/.claude.json
```

## Output format

Present results as:

```
🔍 SEARCH RESULTS for: "$ARGUMENTS"

🎯 TOP MATCHES (newest first)
- 2026-07-14  session:9f3a1c2e  "how do I fix the memory leak in..."
  project: my-ml-project

📋 MATCHING SESSION SUMMARIES
- 9f3a1c2e-...  "Debugging GPU OOM in training loop"

▶️ RESUME WITH
  claude --resume 9f3a1c2e-...

💡 SUGGESTED FOLLOW-UPS
- related terms worth searching next
```

## Notes

- The built-in `/resume` picker covers simple cases natively — mention it when the user just wants to reopen a recent session.
- To export a found session as markdown, use `scripts/extract-claude-session.py --session-id <id>` from the agent-guides repo.
- Content fields can be strings or lists of blocks; always pipe through `tostring` before matching.
