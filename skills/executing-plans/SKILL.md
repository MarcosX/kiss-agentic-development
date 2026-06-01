---
name: executing-plans
description: Use when executing implementation plans with independent tasks in the current session.
---

Execute the plan by dispatching fresh subagents per task, then run spec compliance and code quality reviews after completion.

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

**Continuous execution:** Do not pause to check in with your human partner between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete. "Should I continue?" prompts and progress summaries waste their time — they asked you to execute the plan, so execute it.

<IMPORTANT>
Development should happen in isolation and using fresh subagents for each task.

Ensure a dedicated git worktree is used before making changes.

ALWAYS inspect agent completion report, to ensure implementation met task specification, and code, to ensure quality concerns are addressed early.
</IMPORTANT>

# RULE

If no plan is provided, use `brainstorming` before proceeding.

**Understand plan**: Load and review plan to identify questions, concerns and assumptions.
If there are concerns, raise them and do not proceed. If the plan is clear, proceed with execution of each task.

**Execute plan**: Identify what tasks can be executed independently and what tasks have dependencies. Group independent tasks into batches for parallel dispatch. Dependent tasks execute sequentially (each forms its own batch).

For each batch, follow the fan-out/fan-in pattern:

1. **Extract tasks**: Read the plan once and extract all tasks in this batch with full text and context. Save to TodoWrite.

2. **Fan-out (parallel dispatch)**: Dispatch ALL tasks in the batch simultaneously, each as a fresh subagent using `dispatch-agent.prompt.md` with the full task text pasted in. Do not make subagents read the plan file or inherit session context.

3. **Fan-in (review after completion)**: Wait for all subagents to complete. For each completed task:
   a. Handle implementer status (DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED)
   b. Verify completion using `spec-review.prompt.md` and `code-review.prompt.md`
   c. Run review loops if issues found — fix, re-review, repeat until approved
   d. Mark task complete in TodoWrite

Proceed to the next batch. After all batches complete, go to **Complete development**.

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

- **Verification step continues to fail** — stop and ask for clarification
- **Critical gaps or blockers** — stop and present the problem, do not force through
- **Instruction unclear** — stop and ask for clarification
- **Do not skip reviews** — spec compliance first, then code quality. Both required. No exceptions.
- **Never ignore subagent questions** — answer before letting them proceed.
- **Never accept "close enough"** — reviewer found issues means not done.
