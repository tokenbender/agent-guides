---
name: worklog
description: Issue-led atomic work logging. Use whenever the user says "worklog" or asks to run, apply, start, maintain, update, summarize, or close a worklog; also use for issue-led development, master or umbrella issue tracking, one-issue-per-bug/feature/change workflows, atomic issue-scoped commits, GitHub issue comment journals, closeout summaries, durable engineering ledgers, and making sure no compatibility, migration, cleanup, or residual-risk work is left hanging without an issue.
---

# Worklog

Use GitHub issues as the durable source of truth for a body of work. Keep a master issue for the overall effort, a separate child issue for each bug, feature, experiment, or change, atomic commits for each logical unit, and issue comments as the running engineering ledger.

## Core Contract

- Treat the master issue as the project ledger: scope, child issue index, current status, unresolved decisions, and final rollup.
- Treat child issues as executable work units: one bug, feature, experiment, refactor, docs change, or operational change per issue.
- Keep commits atomic and issue-scoped. Prefer one coherent commit per child issue or per independently reviewable step inside that issue.
- Record important observations, commands, failures, design decisions, implementation notes, artifacts, verification, and residual risk as comments on the child issue.
- Close a child issue only after posting a detailed closeout comment with what changed, evidence, tests, commit refs, and remaining follow-up.
- Update the master issue when child issues are opened, materially change direction, resolve, or create follow-up work.
- Do not leave hanging work implicit. If any compatibility shim, migration, cleanup, temporary fallback, unresolved verification, operational risk, or "duct tape" remains, create or link a follow-up issue before saying the work is done.

## Before Touching GitHub

Verify the actual repo and target issue surface:

```bash
git remote -v
gh repo view --json nameWithOwner,url
gh issue list --state all --limit 50
```

If the repo target is ambiguous, private/public boundaries are unclear, or the action would post to someone else's upstream repo, ask for confirmation before creating, commenting, closing, or editing issues. If a user fork exists and the user did not ask to post upstream, prefer the user's repo/fork.

## Starting A Worklog

1. Inspect existing issues before creating new ones.
2. Reuse an existing master issue if it clearly owns the effort.
3. Create a new master issue when no durable parent exists.
4. For every distinct work item, create or identify a child issue and link it from the master issue.
5. If the task already has code changes in progress, inspect `git status` and diffs before deciding issue boundaries.

Master issue body should include:

```markdown
## Goal
<overall goal>

## Child issues
- [ ] #N - <title>

## Current state
<short status>

## Operating rule
Each bug, feature, experiment, or change gets its own issue. Work is recorded in issue comments. Commits stay atomic and issue-scoped. Child issues close with a detailed closeout; this master issue receives concise rollups.
```

Child issue body should include:

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

Post child issue comments at durable milestones, not for every minor thought:

- Initial diagnosis: what was observed, relevant files/issues, and the immediate plan.
- Important discoveries: new facts that change scope, risk, or approach.
- Implementation progress: atomic change made, files touched, and commit ref if available.
- Verification: exact commands run, pass/fail result, relevant output summary, and artifacts.
- Blockers: what failed, why it matters, and the proposed next move.
- Hardware profile gate for paid or long accelerator runs: before full launch, record the realistic smoke sweep, throughput, memory, estimated MFU, chosen profile, and any user-approved efficiency tradeoff.

Use comments as a journal another engineer could resume from. Include exact commands and paths when they are material. Avoid vague status updates that do not preserve new information.

## Atomic Commits

Before committing, inspect status and diffs:

```bash
git status --short
git diff
```

Stage narrowly. Do not include unrelated user changes. Commit messages should name the issue and the reason:

```text
Fix share receiver timeout handling (#42)

Preserve captures when enrichment exceeds the fast-path budget so mobile sends
return promptly while background processing continues.
```

If one diff covers multiple child issues, split it before committing when practical. If splitting would create churn or risk, explain the coupling in the issue comment and commit body.

## Closing A Child Issue

Before closing, run a residual-work audit. Look specifically for compatibility aliases, temporary configs, local-only workarounds, migration gaps, unverified runtime surfaces, missing cleanup, security loosenings, flaky tests, manual steps, and known risks. If any remain, open or link issue(s) for them first.

Post a final comment before closing:

```markdown
## Resolution
<what changed>

## Evidence
- Commit(s): <hashes or PR>
- Verification: <commands and results>
- Artifacts: <links or paths if relevant>

## Follow-up
<none, or linked issue numbers>
```

Then close the issue. If follow-up work remains, open or link separate child issues instead of hiding incomplete work inside a closed issue. Only write `none` when the residual-work audit found no remaining tracked work.

## Updating The Master Issue

When a child issue closes, post a concise master comment:

```markdown
Resolved #N: <one-sentence outcome>.

Evidence: <commit/test/artifact summary>.
Follow-up: <none or linked issue numbers>.
```

Keep the master issue useful for scanning. Detailed logs live on child issues; master comments are rollups and routing.

## If GitHub Is Not Available

If `gh` is unavailable, authentication fails, or network access blocks issue updates, continue the workflow locally:

- Draft the exact issue body or comment text in the response.
- Preserve the child/master issue structure.
- Do not claim anything was posted.
- Tell the user what command or action remains.
