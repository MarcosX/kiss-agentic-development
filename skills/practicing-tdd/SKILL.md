---
name: practicing-tdd
description: Use when implementing any feature, fixing any bug, refactoring, or changing behavior.
---

<HARD-GATE>
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

Production code written before a test must be deleted. Not kept as reference, not adapted while writing tests, not looked at. Implement fresh from tests.
</HARD-GATE>

## When to Use

Always: new features, bug fixes, refactoring, behavior changes.

Exceptions (ask your human partner first): throwaway prototypes, generated code, configuration files.

## RED — Write a Failing Test

Write one minimal test showing desired behavior. One behavior per test — if the name has "and", split it. Use a clear name describing the behavior, not the implementation. Use real code; avoid mocks unless the dependency is too slow, non-deterministic, or has uncontrollable side effects.

## Verify RED — Watch It Fail

Mandatory. Run the test now — fresh output only. Confirm it fails because the feature is missing, not because of typos or errors. A test that passes immediately proves nothing — you tested existing behavior or the wrong thing.

## GREEN — Write Minimal Code

Write the simplest code to pass the test. No extra features, no refactoring, no improvements beyond the test. Cheating is acceptable here: hardcode return values, duplicate code, skip edge cases. Refactor will clean it up.

## Verify GREEN — Watch It Pass

Mandatory. Run the test now — previous runs do not count. Confirm it passes. Then run the full suite and check for regressions. Fix any broken tests immediately.

## REFACTOR — Clean Up

Only after GREEN. Remove duplication, improve names, extract helpers. Keep tests green throughout. If a test fails during refactor, undo immediately and take smaller steps. Do not add behavior.

## Prove-It Pattern (Bug Fixes)

Bug reported? Write a reproduction test first. Watch it fail (confirming the bug). Then fix the code. Watch it pass (proving the fix). Never fix bugs without a test — the test proves the fix and prevents regression.

## Red Flags — STOP and Start Over

- Code before test
- Test passes on first run
- Cannot explain why the test failed
- Tests added "later" or "after"
- "I already manually tested it"
- "This is too simple to test"
- "Deleting X hours of work is wasteful" — sunk cost fallacy
- "TDD is dogmatic, I am being pragmatic"
- "I will keep the code as reference" — delete means delete

Any of these means: delete the code, restart with TDD.

## Verification Checklist

Before marking work complete:

- [ ] Every new function has a test that failed first
- [ ] Each test failed for the expected reason (feature missing, not typo)
- [ ] Minimal code was written to pass each test
- [ ] All tests pass, output pristine
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors are covered
- [ ] Bug fixes include a reproduction test

## Integration with Other Skills

This skill pairs with `brainstorming` (design before building) and `writing-plans` (implementation plans with built-in TDD steps).
