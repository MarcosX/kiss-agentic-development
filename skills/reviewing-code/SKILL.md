---
name: reviewing-code
description: Use when reviewing code from any source (your own, another agent, or a human), before merging, or when receiving review feedback.
---

## When to Use

- Before merging any change
- When another agent or model produced code you need to evaluate
- When receiving review feedback from a human or peer

## Giving Review

### 1. Determine Target and Prepare

- **Local changes**: Check `git status` and `git diff`. Run preflight checks (tests, lint).
- **Remote PR**: Fetch context — PR description, existing comments, diff. Run preflight.
- **Always**: Understand what the change is trying to accomplish before reading code.

### 2. Dispatch Review Subagent

When reviewing, dispatch a subagent using `references/code-review.prompt.md`, providing the diff, PR description and any existing review comments. The subagent returns structured findings per severity. Bring those findings back into the main session for the next steps.

The subagent reviews across five axes: Correctness, Readability and Simplicity, Architecture, Security, and Performance. It returns findings per severity (Critical, Required, Nit, Optional, FYI).

### 3. Challenge Findings

The subagent works from the diff alone and lacks codebase context, so its findings can be mis-scoped — genuine issues downplayed, noise inflated. Before presenting, challenge every finding against the actual code. When challenging findings, see `references/challenge-findings.md`.

When presenting findings, always include the axis and severity.

### 4. The Approval Standard

Approve when a change improves overall code health, even if not perfect. Do not block because it could have been written differently.

### 5. Handling Disagreements

Resolve disputes in this order:

1. Technical facts and data override opinions
2. Style guides are absolute on style matters
3. Software design evaluated on engineering principles
4. Codebase consistency acceptable if it does not degrade health

Do not accept "I will clean it up later" — deferred cleanup rarely happens.

### 6. Change Sizing

~100 lines changed is good. ~300 lines is acceptable for a single logical change. ~1000+ lines is too large — split it. Separate refactoring from feature work into different changes.

## Exit Gate

Before you call a review complete, check each box:

- [ ] Change intent understood before reading code
- [ ] Findings presented with axis and severity
- [ ] Every finding challenged against the actual code
- [ ] Approval standard applied — health improvement, not perfection
- [ ] No red flag present (LGTM without review, tests-only check, unread diff)

## Receiving Review Feedback

### The Response Pattern

When receiving feedback, follow this sequence:

1. **READ** — Complete feedback without reacting or planning responses
2. **UNDERSTAND** — Restate the requirement or ask for clarification
3. **VERIFY** — Check the suggestion against codebase reality
4. **EVALUATE** — Is it technically sound for this codebase?
5. **RESPOND** — Technical acknowledgment or reasoned pushback
6. **IMPLEMENT** — One item at a time, test each

### Clarify Before Implementing

If any item is unclear, stop and ask before implementing anything. Items may be related — partial understanding leads to wrong implementation.

### YAGNI on Suggestions

If a reviewer suggests productionizing code that is not currently used, grep for actual usage. If the code is not called anywhere, flag it rather than building it out.

### Push Back When Wrong

Push back when a suggestion breaks existing functionality, the reviewer lacks full context, it violates YAGNI, or it is technically incorrect. Use technical reasoning backed by code and tests.

## Red Flags

- Merging without any review
- "LGTM" without evidence of actual review
- Reviews that only check whether tests pass
- Large PRs that should have been split
- Bug fixes without reproduction tests
- Accepting "I will fix it later"
- Implementing unclear feedback without clarification
