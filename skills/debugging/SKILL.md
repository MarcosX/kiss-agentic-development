---
name: debugging
description: Use when debugging any bug, error, test failure, crash, or unexpected behavior. Triggered by error output, stack traces, crash logs, failure reports, or verbal descriptions of incorrect behavior.
---

The goal is not to stop the error — it's to be able to say why the fix works.

Every bug is a claim about a system you can't see. The reliable way to a fix
that stays fixed is to make the system say what's wrong before you change
anything. Guessing looks fast; evidence is the route to a fix you can defend.

## The Loop

**Gather evidence — make the bug talk.** Read the error completely: stack
trace, line numbers, paths. Check recent changes — diff, config, dependencies,
deploys. Reproduce it if you can. When the system spans components, capture
what enters and leaves each boundary — what happens at the edge outranks what
you assume in the middle. For large or cross-component systems, a focused
investigation (see `references/gather-evidence.prompt.md`) returns a structured
report and keeps your context clean. Return an evidence report before forming
conclusions.

**Form one hypothesis — then test it cheaply.** State the suspected cause as
one specific claim, with your reasoning. Change the smallest thing that could
confirm or deny it — one variable at a time. Confirmed? Fix it. Not confirmed?
New hypothesis. Never stack fixes: each unverified fix is a second bug you
haven't seen yet.

**Fix the root cause — prove it with a test that failed first.** Write the
reproduction before the fix (see practicing-tdd): a test that shows the wrong
behavior, watched to fail for the expected reason. Then fix. A fix verified by
a failing-then-passing test is done; a fix verified by hope is a hypothesis.

**Close the loop.** The test passes, no regressions, issue gone. Record
reproduction, root cause, fix, and prevention (see `reference/debug-report.md`)
so the next bug doesn't start from zero.

## The user's suspected cause

The user offers "I think it's X" — often confidently. Treat it as the first
hypothesis, not a lead. Do not endorse or restate it until evidence exists;
restating an unchecked guess makes it look confirmed.

## When you're stuck

Three fixes with the bug still present means you're not iterating on evidence.
Stop changing things. Question the fundamentals — the architecture, the pattern,
the inherited assumption. Bring your partner in before a fourth attempt.

## Why evidence first is the fast path

The evidence-first loop is the shortest route to "I'm sure this is fixed." The
failing run names exactly what's missing; the passing run confirms you're done.
Without it, every fix is a fresh guess and the bug keeps finding you. The loop
pays for itself the moment anything changes.