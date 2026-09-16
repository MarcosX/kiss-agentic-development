---
name: reviewing-code
description: Use when reviewing code from any source (your own, another agent, or a human), before merging.
---

# The task

The task is to produce findings worth acting on — verified against the actual code.

# Why

The review subagent sees only the diff. Its findings can be mis-scoped: real issues downplayed, noise inflated. Verifying against the actual code is how you produce findings worth acting on.

# The Loop

1. **Understand intent** — read the PR description or context before reading the diff.
2. **Subagent reviews five axes** — dispatch using `references/code-review.prompt.md`. The subagent returns findings per severity (Critical, Required, Nit, Optional, FYI) across Correctness, Readability, Architecture, Security, and Performance.
3. **Challenge findings** — verify each finding against the actual code. See "Challenge findings" below.
4. **Present surviving findings** — each finding carries axis, severity, and file:line.
5. **Decide** — approve, request changes, or comment.

# Challenge findings

For each finding, in order:

1. **Verify** — Read the actual code. Confirm the finding is real: the flagged path exists, is reachable, and is genuinely a problem in this codebase. Do not rely on the diff alone.
2. **Decide** — Critical and Required: keep unless concrete codebase evidence refutes them. Over-dismissal is the failure mode this step prevents. Nit, Optional, FYI: keep only when verified or clearly valuable. These face harder scrutiny.
3. **Recalibrate** — Adjust severity to codebase reality. Promote issues the subagent could not see (callers in other files, failing tests, documented behavior the change breaks). Demote inflated ones.
4. **Merge** — Collapse duplicate findings to one root cause. One issue, one finding.

Dismissal requires explicit codebase evidence, never "seems fine." When evidence is ambiguous, lean toward the higher severity for Critical and Required findings. Apply the disagreement ladder: technical facts override opinions, style guides are absolute on style, design is judged on engineering principles, codebase consistency is acceptable if it does not degrade health.

# Approval

Approve when the change improves code health, even if imperfect. Do not block because it could have been written differently.

# Change sizing

~100 lines changed is good. ~300 lines is acceptable for a single logical change. ~1000+ lines is too large — flag it and suggest splitting. Separate refactoring from feature work.

# Done when

Each finding was verified against actual code with axis, severity, and file:line. You can point to the code behind each one.
