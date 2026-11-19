---
name: tokenbending-worklog
description: >-
  Issue-led atomic work logging ("tokenbending-worklog"). Use whenever the user
  says "worklog" or "tokenbending-worklog", or asks to start, maintain, update,
  summarize, or close an issue-led ledger with master/child GitHub issues, atomic
  issue-scoped commits, closeout summaries, linked journal sync, and residual-work
  audits so no cleanup or risk is left hanging.
---

# Tokenbending Worklog

Use GitHub issues as the durable source of truth for a body of work: one master issue for routing/rollups, one child issue per concrete unit of work, atomic issue-scoped commits, and resume-ready milestone comments.

## Core Contract
- **Zero unrequested comments or documentation.** Do not add code comments, docstrings, README files, architecture notes, changelogs, or other repo docs unless explicitly requested. Issue bodies, issue comments, and response summaries are the worklog ledger.
- **Master issue = ledger & router:** overall goal, child issue checklist, current state, unresolved decisions, concise rollups.
- **Child issue = one executable unit:** one bug, feature, experiment, refactor, explicitly requested docs change, or operational change.
- **Atomic commits:** one coherent, issue-scoped commit per child issue (or independently reviewable step). Stage narrowly; never mix unrelated fixes and generated outputs.
- **Durable milestone comments:** record diagnosis, material discoveries, commits, verification evidence, artifacts, and blockers—never vague status chatter.
- **No implicit hanging work:** before closing any issue, run a residual-work audit. Any remaining compatibility shim, temporary fallback, manual workaround, unverified surface, cleanup, or known risk must get a linked follow-up issue.

## Before Touching GitHub
Verify the actual repo and issue surface first:

```bash
git remote -v
gh repo view --json nameWithOwner,url
gh issue list --state all --limit 50
```

If the target repo or public/private boundary is ambiguous, confirm before creating, commenting, editing, or closing issues. Prefer the user's repo/fork unless told to post upstream.

## Starting a Worklog
1. Inspect existing issues (`gh issue list --state all`) and `git status` / `git diff` before drawing issue boundaries.
2. Reuse an existing master issue if one owns the effort; otherwise create one.
3. Open a child issue for each distinct unit of work and link it from the master issue.

**Master template:**
```markdown
## Goal
<overall goal>

## Child issues
- [ ] #N - <title>

## Current state
<short status>
```

**Child template:**
```markdown
## Scope
<one concrete unit of work>

## Why
<user-visible or engineering rationale>

## Acceptance criteria
- <verifiable outcome>

## Notes
Tracked under #<master-issue>.
```

## During Work
- Post child comments only at durable milestones (diagnosis, scope-changing discovery, commit/implementation progress, verification with exact commands/receipts/paths, blockers).
- For paid compute profiling and verification rules, follow `tokenbending-experimenting` (record throughput/memory/profile *only* when profiling a genuinely novel hardware/topology/config).

## Atomic Commits
Inspect `git status --short` and `git diff` before staging. Name the issue and reason:

```text
Promote SpliceProbeBuilder and /dev/shm auto-scratch (#5)

Cuts solo probe latency from ~25s to ~0.5s with bit-exact tensor parity.
```

## Closing a Child Issue & Syncing Journals
1. **Residual-work audit:** Check for temporary configs, local-only workarounds, unpromoted speedups, missing cleanup, flaky eval variance, or documented caveats. Open/link follow-up issue(s) for anything left open.
2. **Post closeout comment, then close:**
```markdown
## Resolution
<what changed>

## Evidence
- Commit(s): <hashes or PR>
- Verification: <exact commands and real-artifact results>
- Artifacts: <links or paths>

## Follow-up
<none, or linked issue numbers>
```
Only write `none` when the residual-work audit found zero remaining tracked work.
3. **Update master issue** with a 3-line rollup (`Resolved #N`, `Evidence`, `Follow-up`).
4. **Sync linked external journals** (e.g., an associated Google Doc or local mirror) whenever a milestone closes if one is tracking the effort.

## Offline / No-`gh` Fallback
If `gh` is unavailable or blocked, draft the exact issue body/comment locally, preserve the master/child structure, never claim it was posted, and state the exact command remaining.
