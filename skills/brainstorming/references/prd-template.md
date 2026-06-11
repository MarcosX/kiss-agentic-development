# PRD Template

Use when writing the PRD after user approval of the approach. Scale sections to complexity — simple projects need a sentence per section, not paragraphs.

## Problem Statement

The problem the user is facing, from their perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories. Each in format:

```
1. As an <actor>, I want <feature>, so that <benefit>
```

Be extensive — cover all aspects of the feature.

## Implementation Decisions

Architectural choices, modules to build/modify, API contracts, schema changes, interface shapes. Do NOT include specific file paths or code snippets — they go stale. Exception: prototype-produced decision-rich snippets (state machine, reducer, schema, type shape) that encode decisions more precisely than prose. Inline them and note they came from a prototype.

## Testing Decisions

- What makes a good test (external behavior, not implementation details)
- Which modules to test
- Prior art for tests (similar test patterns in the codebase)
- Seam-first: identify the highest seam possible for testing

## Out of Scope

What is deliberately not covered by this design.

## Further Notes

Any additional context or considerations.
