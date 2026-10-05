---
name: reviewing-code
description: Use when reviewing code from any source (your own, another agent, or a human), before merging.
---

# The task

Produce findings worth acting on — each one grounded in code you actually read.

# Why

Severity is a claim about this codebase, not about the diff: whether the flagged path is reachable, whether a test already documents the contract, whether a caller elsewhere depends on the behavior. A review that starts and ends with the diff cannot support that claim, so it inflates noise into Critical findings and downplays real ones. Reading the changed files together with their surroundings is where severity comes from.

# The Loop

1. **Understand intent** — read the PR description or context before reading the diff.
2. **Get the code** — work in the repository root and switch to the branch under review, named in the request or in the PR. A branch that exists only on the remote needs no switch: fetch it and read its files from the fetched ref. For a local branch, run the switch even when the working tree looks dirty — the remedies below only exist once a failure is real. If the switch fails, report the reason, name the remedies (stash, force, or review the already-checked-out branch), and ask which to use, because a review makes no changes and stopping costs only a round trip. Never discard uncommitted work to get past a failed switch.
3. **When the repository is absent** — clone or fetch it into a scratch location outside the user's tree, and say that the review will be slower.
4. **Read what the diff hides** — read each changed file whole rather than its hunks, then follow the links that decide whether a finding is real: the callers of a changed function, the tests covering it, and any place the behavior is documented.
5. **Review five axes** — Correctness (does the change do what it claims, are edge cases and error paths handled, do the tests check behavior rather than internals?), Readability (can someone follow it without the author, are abstractions earning their complexity?), Architecture (does it fit the system and follow existing patterns, are module boundaries clean?), Security (is user input validated, are secrets kept out of code, is auth checked, is external data untrusted?), Performance (N+1 queries, unbounded loops, missing pagination, sync work in an async path?).
6. **Label every finding** — axis; severity, one of Critical (blocks merge: security vulnerability, data loss, broken functionality), Required (must address before merge), Nit (minor, formatting or style), Optional (worth considering, not required), FYI (informational, no action needed); the file and line; what is wrong; the fix or the question for the author.
7. **Decide** — approve, request changes, or comment.

# Approval

Approve when the change improves code health, even if imperfect. Do not block because it could have been written differently. Severity describes the code; the verdict describes the change. A defect the change did not introduce is a follow-up, not a block, whatever its severity.

# Change sizing

~100 lines changed is good. ~300 lines is acceptable for a single logical change. ~1000+ lines is too large — flag it and suggest splitting. Separate refactoring from feature work.

# Done when

Every finding you present cites a file and line you read, and its severity reflects what that code shows. You can point to the code behind each one.
