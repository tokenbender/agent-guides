---
description: Multi-specialist collaborative analysis — fans a topic out to parallel specialist subagents, cross-pollinates findings, and synthesizes across rounds
argument-hint: "<topic> [rounds=3]"
disable-model-invocation: true
---

# Multi-Mind - Subagent-Based Collaborative Analysis

Execute a multi-specialist collaborative analysis on: **$ARGUMENTS**

Parse an optional `rounds=N` parameter (default 3).

## How this maps to Claude Code's agent system

- Launch each specialist as a **parallel subagent** via the Task tool — they run concurrently, each in its own context window, and return only their analysis.
- For one-off runs, inline subagent prompts (below) are enough. For topics you revisit, make the specialists persistent by writing definitions to `.claude/agents/<role>.md` (see the [Subagents Guide](../claude-subagents-guide.md)) — Claude will then route to them by description automatically.
- Subagents run in the background by default; launch all specialists for a round in a single message so they execute in parallel.
- If the question needs codebase-wide changes (not just analysis), the bundled `/batch` skill is a better fit. For long-running collaborative sessions, see agent teams in the Claude Code docs.

**When to use this vs. `/deep-research`:** the bundled `/deep-research` workflow fans out web searches and synthesizes a cited report — use it for factual questions. Use multi-mind for *judgment* questions (architecture tradeoffs, strategy, design decisions) where decorrelated expert perspectives and adversarial cross-pollination matter more than citation coverage.

## Phase 1: Specialist Assignment & Research

Analyze the topic and determine 4-6 specialist roles with maximally decorrelated perspectives. Then launch them all in parallel, e.g.:

```
Task tool, subagent_type: general-purpose — run all in one block:

1. "You are a technical specialist. Research [topic] focusing on implementation
   details, architecture, performance, and technical risk. Use web search for
   current documentation and case studies. Return ≤500 words of findings."

2. "You are a business strategy specialist. Analyze [topic] from market dynamics,
   competitive landscape, ROI, and strategic positioning. Use web search for
   current market reports. Return ≤500 words."

3. "You are a user experience / adoption specialist. Investigate [topic] for
   user needs, usability concerns, and adoption barriers. Return ≤500 words."

[... additional specialists as the topic demands — security, regulatory,
 ethics, operations, contrarian/red-team ...]
```

**Specialist selection criteria**:
- Unique domain expertise relevant to the topic
- Different methodologies (quantitative/qualitative, theoretical/practical)
- Varied temporal perspectives (historical, current, future-focused)
- Distinct risk/opportunity sensitivities
- Independent information sources

Cap each subagent's output (~500 words) so synthesis stays tractable.

## Phase 2: Cross-Pollination Round

After all specialist reports return, launch a second parallel wave. Each subagent receives **all** first-round reports and must:

1. Identify where other specialists' findings intersect its domain
2. Challenge assumptions from its perspective
3. Build on insights while keeping its distinct viewpoint
4. Flag blind spots in the other analyses

## Phase 3: Synthesis & Iteration

For each round (default 3):
- Collect all subagent outputs
- Synthesize without homogenizing perspectives
- Identify emerging patterns and unresolved gaps
- Choose the next round's focus
- Launch the next wave with refined prompts that include prior synthesis

## Anti-Repetition Mechanisms

**You (the orchestrator) are the moderator**:
- Track what's been thoroughly covered vs. what needs depth
- Redirect specialists away from rehashing prior points
- Push for new angles, deeper analysis, or broader implications
- Synthesize without flattening disagreement

**Specialist instructions** (include in every round-2+ prompt):
- Build on previous insights; never restate them
- Contribute only what your unique expertise adds
- Search for information others likely missed
- Challenge emerging consensus from your perspective

## Output Protocol

```
=== MULTI-MIND ANALYSIS: [Topic] ===
Rounds: [X] | Specialists: [roles]

--- ROUND 1 ---
🔍 KNOWLEDGE ACQUISITION   [per-specialist research findings]
🎯 SPECIALIST ANALYSIS     [unique perspectives]
🔄 CROSS-POLLINATION       [engagement with each other's findings]
⚖️ MODERATOR SYNTHESIS     [progress, key insights, next-round focus]

--- ROUND 2..N ---
[same structure, deeper]

--- FINAL SYNTHESIS ---
🧠 COLLECTIVE INTELLIGENCE OUTCOME
🎯 KEY INSIGHTS
⚠️ REMAINING UNCERTAINTIES
🔮 IMPLICATIONS
```

## Success Metrics
- Each round produces genuinely new insights (not repetition)
- Specialists maintain distinct valuable perspectives throughout
- Cross-pollination yields insights no single specialist would reach
- The collective outcome exceeds the sum of individual contributions
- Different error types are caught by different specialists

Begin with dynamic specialist assignment based on the topic's complexity and domains.
