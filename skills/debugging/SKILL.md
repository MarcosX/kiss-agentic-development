---
name: debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
---

<HARD-GATE>
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

Root cause must be identified and confirmed before any fix is implemented. Symptom fixes without root cause are not allowed.
</HARD-GATE>

## When to Use

Use for any technical issue: test failures, production bugs, unexpected behavior, build failures, performance problems, integration issues. Do not skip because the issue seems simple or there is time pressure — systematic debugging is faster than guess-and-check.

## Phase 1: Reproduce and Investigate

Before attempting any fix:

- **Read error messages** — Read stack traces completely. Note line numbers, file paths, error codes. Do not skip past warnings.
- **Reproduce consistently** — Determine exact steps. Does it happen every time? If not reproducible, gather more data instead of guessing.
- **Check recent changes** — Git diff, recent commits, new dependencies, config changes, environmental differences.

### Trace Multi-Component Systems

When a system spans multiple components, add diagnostic instrumentation at each component boundary before proposing fixes. Log what enters and exits each component. Verify environment and config propagation. Run once to gather evidence showing where it breaks, then investigate that specific component.

## Phase 2: Compare and Analyze

Find the pattern before fixing:

- **Find working examples** — Locate similar working code in the same codebase. What works that is similar to what is broken?
- **Compare against references** — If implementing a pattern, read the reference implementation completely. Do not skim or adapt from partial understanding.
- **Identify differences** — List every difference between working and broken code. Do not assume something cannot matter.
- **Understand dependencies** — What other components, config, or environment does this depend on? What assumptions does it make?

## Phase 3: Hypothesize and Test

Apply the scientific method:

- **Form a single hypothesis** — State clearly what you think the root cause is and why. Be specific.
- **Test minimally** — Make the smallest possible change to test the hypothesis. One variable at a time. Do not fix multiple things at once.
- **Verify before continuing** — If the test confirms the hypothesis, proceed to Phase 4. If not, form a new hypothesis. Do not stack fixes on top of each other.
- **When stuck** — Say "I do not understand X" rather than pretending. Ask for help or research more.

## Phase 4: Fix and Verify

Fix the root cause, not the symptom:

- **Create a failing test first** — Write the simplest reproduction test. Use the `practicing-tdd` skill. The test MUST fail before the fix.
- **Implement a single fix** — Address the root cause identified. One change at a time. No bundled refactoring or "while I am here" improvements.
- **Verify the fix** — The test passes. No other tests broken. The issue is actually resolved.
- **Document the outcome** — Fill in `reference/debug-report.md` with the reproduction, root cause, fix, and prevention steps.

## The 3-Fix Rule

If you have tried 3 fixes and none worked:

1. STOP. Do not attempt a 4th fix.
2. Consider that the architecture itself may be the problem.
3. Question fundamentals: Is this pattern sound? Are we fixing symptoms of a wrong design?
4. Discuss with your human partner before attempting more fixes.

This is not a failed hypothesis — this is a signal that the approach needs revisiting.

## Red Flags — STOP and Follow Process

- Proposing fixes before root cause is identified
- "Quick fix for now, investigate later"
- Multiple fixes applied at once
- Skipping the reproduction test
- "It is probably X, let me fix that" without verification
- Stacking fixes when previous ones did not work
- 3+ failed fixes without questioning architecture
- "I do not fully understand but this might work"

## Verification Checklist

Before marking debugging complete:

- [ ] Root cause identified and confirmed
- [ ] Reproduction test written and failing before fix
- [ ] Single fix implemented (no bundled changes)
- [ ] Fix verified (test passes, no regressions)
- [ ] Debug report filed in `reference/debug-report.md`

## Integration with Other Skills

This skill pairs with `practicing-tdd` for creating failing tests during Phase 4 and `brainstorming` when debugging reveals a design problem worth rethinking.
