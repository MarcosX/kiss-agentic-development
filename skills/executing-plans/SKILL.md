---
name: executing-plans
description: Use to execute and verify writen plans, leveraging subagents with review checkpoints.
---

Execute the plan by dispatching subagents per task, then run spec compliance and code quality reviews after completion.

<IMPORTANT>
Development should happen in isolation and using fresh subagents for each task.

Ensure a dedicated git worktree is used before making changes.

ALWAYS inspect agent completion report, to ensure implementation met task specification, and code, to ensure quality concerns are addressed early.
</IMPORTANT>

# RULE

If no plan is provided, use `brainstorming` before proceeding.

**Understand plan**: Load and review plan to identify questions, concerns and assumptions.
If there are concerns, raise them and do not proceed. If the plan is clear, proceed with execution of each task.

**Execute plan**: Identify what tasks can be executed independently and what tasks have dependencies, then for each them:

1. If the task is independent
   - use `dispatch-agent.prompt.md` to dispatch a fresh subagent to implement the task
2. If the task has dependencies
   - wait until the previous task is completed successfully and use `dispatch-agent.prompt.md` to dispacth an agent
3. Verify completion
   - review the subagent report and inspect implementation to ensure the task was successfully completed
   - use `spec-review.prompt.md` to validate task goals against implementation
   - use `code-review.prompt.md` to ensure code quality concerns are addressed early on

**Complete development**: Review execution output to determine if the plan was completed successfully.
If it is, report status and provide proof of completion.
If not, determine next steps:

- if task implementation failed
  - review concerns and/or blockers
  - update the plan with what needs rework
  - go back to execution phase
- if task implementation was not possible
  - review concerns and/or blockers
  - propose 2-3 options for addressing the cause
  - report current status of plan along with suggestions

# Red flags

Do not rely on guessing and do not force through blockers.

**Verification step continues to fail**: stop and ask for clarification to ensure the verification step is actually correct.

**Critical gaps are found**: when implementing, even though the plan was reviewed, stop ans ask for clarification when needed.

**Previous steps prevent proper implementation**: when an implementation decision made earlier impacts the next tasks, stop and present the problem to ask for clarification.

**Instruction isn't clear or can't be performed**: when actions on a step can't be executed, due to environment or any other limitation, stop and present the problem to ask for clarification.
