# PRD Template

Use when writing the PRD after user approval of the approach. Scale sections to complexity — simple projects need a sentence per section, not paragraphs.

## Problem Statement

The problem the user is facing, from their perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories. Each story carries a sequential ID assigned in the order written (`US-1`, `US-2`, ...). Format:

1. US-1: As an <actor>, I want <feature>, so that <benefit>

Be extensive — cover all aspects of the feature. Decisions below reference these IDs.

## Implementation Decisions

Architectural choices, modules to build/modify, API contracts, schema changes, interface shapes. Do NOT include specific file paths or code snippets — they go stale. Exception: prototype-produced decision-rich snippets (state machine, reducer, schema, type shape) that encode decisions more precisely than prose. Inline them and note they came from a prototype.

Tie each decision to the story or stories it serves, and state why the path was chosen. Format:

- US-1, US-3: <decision>. Chosen because <rationale — the rejected alternative and the trade-off that ruled it out>.

## Testing Decisions

- What makes a good test (external behavior, not implementation details)
- Which modules to test
- Prior art for tests (similar test patterns in the codebase)
- Seam-first: identify the highest seam possible for testing

Tie each decision to the story it serves with a `Chosen because` line when it maps to a specific story.

## Out of Scope

What is deliberately not covered by this design, and why — deferred, rejected, or unnecessary. A fresh reader must be able to tell a deliberate cut from an omission.

## Further Notes

Any additional context or considerations. Acceptance criteria are not written in the PRD — they are derived during plan writing from the user stories and decisions above.
