---
name: code-review-agent
description: prompt to dispatch subagent to review code implementation
---

Use the following template to dispatch a subagent to review code implementation.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are a set of commits looking for use of best practices, code maintenability and architecture.

# Task description:

[FULL TEXT of task from plan]

# What was implemented:

[FULL TEXT of execution report]

# Your goal

Use `git diff` to review the code implemented, considering the base and head commits:

**Base:** [commit SHA for latest changes made by the agent]
**Head:** [commit SHA for head commit where the agent started]

If more context is needed, explore related files outside of the commit, but do not consider them as part of your review.

## What to check

**Code quality**

- Clean separation of responsibilities/concerns
- Error handling with proper actions
- DRY
- Premature optimizations/abstractions
- Edge cases
- Type safety (when applicable)

**Testing**

- Tests validate behavior, not mocked implementation
- Edge cases are covered by dedicated tests
- Integration points are tested, using mocks or stubs when needed
- New tests do not overlap with existing tests cases
- All tests pass and no regression issues are found

**Architecture**

- Design decisions can reasonably scale and perform well
- Existing patterns and conventions are followed
- No security concerns
```
