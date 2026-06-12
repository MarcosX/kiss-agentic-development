---
name: debugging
description: Use when given error output, stack traces, crash logs, or any failure report from commands or tests. Use before proposing any fix or making any code change.
---

<HARD-GATE>
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

Root cause must be identified and confirmed before any fix is implemented. Symptom fixes without root cause are not allowed.
</HARD-GATE>

## When to Use

Use for any technical issue: test failures, production bugs, unexpected behavior, build failures, performance problems. Do not skip because of time pressure — systematic debugging is faster than guess-and-check.

## Phase 1: Gather Evidence

When investigating a bug or failure, dispatch a subagent using `references/gather-evidence.prompt.md`, providing: the error message, relevant file paths, and recent git diff. The subagent returns a structured evidence report. Bring the report back to the main session before forming hypotheses.

If subagent dispatch is not avialable, follow the prompt directly. Bring findings into the next phase before forming hypotheses.

When a system spans multiple components, instruct the subagent to add diagnostic instrumentation at each component boundary and run once to gather boundary-level evidence before returning.

## Phase 2: Hypothesize and Test

Apply the scientific method:

- **Form a single hypothesis** — State the suspected root cause and why. Be specific.
- **Test minimally** — Smallest possible change to test the hypothesis. One variable at a time.
- **Verify before continuing** — Confirmed? Proceed to Phase 4. Not confirmed? Form a new hypothesis. Do not stack fixes.
- **When stuck** — Acknowledge uncertainty and research more.

## Phase 3: Fix and Verify

Fix the root cause, not the symptom:

- **Create a failing test first** — Write the simplest reproduction test using `practicing-tdd`. The test MUST fail before the fix.
- **Implement a single fix** — Address the root cause. One change at a time. No bundled improvements.
- **Verify the fix** — Test passes. No regressions. Issue resolved.
- **Document the outcome** — Fill in `reference/debug-report.md` with reproduction, root cause, fix, and prevention.

## The 3-Fix Rule

If you have tried 3 fixes and none worked:

1. STOP. Do not attempt a 4th fix.
2. Consider the architecture itself may be the problem.
3. Question fundamentals: Is this pattern sound? Are we fixing symptoms of a wrong design?
4. Discuss with your human partner before attempting more fixes.

## Red Flags — STOP and Follow Process

- Proposing fixes before root cause is identified
- "Quick fix for now, investigate later"
- Multiple fixes applied at once
- Skipping the reproduction test
- "It is probably X, let me fix that" without verification
- Stacking fixes when previous ones did not work
- 3+ failed fixes without questioning architecture
- "I do not fully understand but this might work"
