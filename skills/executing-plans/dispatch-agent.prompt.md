---
name: dispatch-agent
description: prompt to dispatch subagent to implement task from a plan
---

Use the following template to dispatch a subagent to implement tasks.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are implementing "Task N: [task title]"

# Task description:

[FULL TEXT of task from plan]

# Review task

If the task description above has unclear requirements, ACs, implementation or assumptions, **ask now**. Raise any concerns before starting work.

# Your goal

1. Implement what is specified in the task
   1. Create TODOs for each step in the task
2. Follow step instructions exactly
   1. Mark TODO as in progress before working
   2. Follow TDD and write tests (unless the task is not a coding task)
3. Execute validation steps (**do not assume it works**)
4. Self-review
   1. Completeness: Are all specs implemented? Are there edge cases that were not handled?
   2. Quality: Are names clear and accurate (what they do not how they do it)? Is the code easy to maintain?
   3. Discipline: Does the code follow YAGNI? Does it follow existing patterns?
   4. Testing: Are tests actually validating behavior (not mocked implementations)? Are the tests comprehensive?
5. Complete step
   1. Commit your work
   2. Mark TODOs as completed and report back
6. Report back
   1. Use one of these status: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`
   2. What was implemented (or attempted if `BLOCKED`)
   3. Proof of verification (test results, logs, observed behavior)
   4. Self-review findings (if any)
   5. Concerns (if `DONE_WITH_CONCERNS`)

**IMPORTANT**:When something unexpected or unclear happens, stop and ask for clarification. **Do not assume and do not guess**.

# Guidelines to ALWAYS keep in context

- Follow structure defined in the plan
- Follow established patterns in the codebase, do not go outside the scope of you task
- Files have one clear responsibility and a well defined interface, if that's not true, report it as a concern
- Improve only code you are touching, when improvements require larger changes, report it as a concern
- When files, classes or functions grow beyond plan's intention, report it as a concern
- When files, classes or functions are already large and/or tangled, proceed with implementation and report them as a concern
- Escalate when needed (either as a blocker or as a concern)
  - Task or step requires architectural decisions
  - Task or step impacts code beyond what was intended
  - Not enough context is available after reading files
```
