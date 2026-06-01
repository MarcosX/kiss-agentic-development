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

### 2. Review Tests First

Tests reveal intent and coverage before you see the implementation. Check that they test behavior not internals, cover edge cases, and would catch regressions.

### 3. The Five-Axis Review

Evaluate every change across all five dimensions:

- **Correctness**: Does the code do what it claims? Are edge cases and error paths handled? Do tests pass and test the right things?
- **Readability and Simplicity**: Can someone understand this without the author? Clear names, straightforward control flow, no clever tricks. Could this be fewer lines? Are abstractions earning their complexity?
- **Architecture**: Does the change fit the system? Does it follow existing patterns? Clean module boundaries, no circular dependencies, appropriate abstraction level?
- **Security**: Is user input validated and sanitized? Secrets kept out of code? Auth checked? SQL parameterized? External data treated as untrusted?
- **Performance**: N+1 queries? Unbounded loops? Missing pagination? Sync ops that should be async? Large objects in hot paths?

### 4. Categorize Findings

Label every comment so the author knows what is required versus optional:

- **Critical:** Blocks merge — security vulnerability, data loss, broken functionality
- **Required (no prefix):** Must address before merge
- **Nit:** Minor — formatting, style preferences, optional
- **Optional:** Suggestion worth considering but not required
- **FYI:** Informational only, no action needed

### 5. The Approval Standard

Approve when a change improves overall code health, even if not perfect. Do not block because you would have written it differently.

### 6. Handling Disagreements

Resolve disputes in this order:
1. Technical facts and data override opinions
2. Style guides are absolute on style matters
3. Software design evaluated on engineering principles
4. Codebase consistency acceptable if it does not degrade health

Do not accept "I will clean it up later" — deferred cleanup rarely happens.

### 7. Change Sizing

~100 lines changed is good. ~300 lines is acceptable for a single logical change. ~1000+ lines is too large — split it. Separate refactoring from feature work into different changes.

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


