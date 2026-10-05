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
the ask. A test is your intent made checkable: one behavior per test, and one value
per test — two tests reading the same value are one test wearing two names.

A dependency you did not write — a network, a clock, a filesystem — gets a double,
because reaching what happens when it fails is the point of the test and a live call
cannot be told to fail. Replacing something you did write is the design signal: it
marks a seam the code should have had.

**Watch it fail — earn your proof.** Run it now, and see it fail for the expected
reason: the behavior missing, not a typo. A module that does not exist yet gives a
collection error, not a failure: no assertion ran, so nothing was proven. Stand up
the smallest thing that lets the test execute and still fail, then run it again.
This failing run is the receipt for everything after. A test that never failed is
hollow — it proves the code you have, not the code you wrote, so it can't be your
proof of done.

**Make it pass — write the simplest thing that turns the failure green.** No
extras means not going beyond what was needed, and the signals around you set
what was needed. A dependency that stalls or rate-limits is a signal that failure
handling belongs in the contract, not an extra to defer; a circuit breaker nothing
asked for is the extra. Handling you add is behavior like any other, so it earns
its own failing test first. Even a hardcoded answer counts, if it satisfies the
contract. The test is your "enough" detector — green means the contract is met,
nothing more is asked. Green on one test is not the end: run the whole suite,
because a change that satisfies its own contract can still break someone else's.

**Refactor — the code you just wrote is unproven too.** Green says the contract
holds; it says nothing about whether the code is any good, exactly as a test
that never failed proves nothing about your intent. Read the change back as if
someone else wrote it: a hardcoded answer that satisfies the contract is still
hardcoded, a name that hides what it does still hides it. Take the seams your
own tests had to work around. Change no behavior here — this is the shape of the
code, not what it does. Remove duplication, sharpen names, extract helpers. Each
change is verified by the next run, so cleanup is confident.

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
