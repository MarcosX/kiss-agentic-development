---
name: practicing-tdd
description: Use when implementing any feature, fixing any bug, refactoring, or changing behavior.
---

The task is to make a failing test pass.

Every feature, bug fix, refactor, or behavior change is this task. The test is
the contract: it defines "done" in a form the computer checks for you. You
finish when a test you wrote first, and watched fail, now passes — never when
code exists alone.

Exceptions: throwaway prototypes, generated code, configuration files. These
aren't behavior tasks — when one applies, state it in a line before proceeding.

## The Loop

**Write the failing test — define done.** This is the actual ask, not a step before
the ask. A test is your intent made checkable: describe one behavior per test,
with real code over mocks.

**Watch it fail — earn your proof.** Run it now, and see it fail for the expected
reason: the behavior missing, not a typo. This failing run is the receipt for
everything after. A test that never failed is hollow — it proves the code you
have, not the code you wrote, so it can't be your proof of done.

**Make it pass — write the simplest thing that turns the failure green.** No
extras; even a hardcoded answer counts, if it satisfies the contract. The test
is your "enough" detector — green means the contract is met, nothing more is
asked. Green on one test is not the end: run the whole suite, because a change
that satisfies its own contract can still break someone else's.

**Refactor — improve while the test stays green.** Remove duplication, sharpen
names, extract helpers. Each change is verified by the next run, so cleanup is
confident.

## Bug fixes

The bug is your failing test. Write the reproduction — a test that shows the
wrong behavior — and watch it fail. That failing run captures the bug in a
checkable form. Then fix the code and watch it pass: now you have proof the bug
is gone and a guard against it returning.

## Why the loop is the fast path

The fail-then-pass loop is the shortest route to "I'm sure it works." The
failing run names exactly what's missing; the passing run confirms you're done.
Without it, every verification is guessing, and each future change forces you
to re-verify by hand. The loop pays for itself the moment anything changes.
