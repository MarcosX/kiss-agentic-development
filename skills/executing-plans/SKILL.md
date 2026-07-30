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

2. **Fan-out (parallel dispatch)**: Dispatch ALL tasks in the batch simultaneously, each as a fresh subagent using `references/dispatch-agent.prompt.md` with the full task text pasted in. Do not make subagents read the plan file or inherit session context.

 3. **Fan-in (review after completion)**: Wait for all subagents to complete. For each completed task:
   a. Handle implementer status (DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED)
   b. Verify completion using `references/spec-review.prompt.md` and `references/code-review.prompt.md`
   c. **AC validation** (single-owner only): If the task has a **Satisfies** field, validate each AC that lists this task as its sole owner. Read relevant code and run tests to confirm the AC is met. Report pass/fail per AC. Skip if the task references no ACs, or no ACs it owns individually.
   d. Run review loops if issues found — fix, re-review, repeat until approved
   e. Mark task complete in TodoWrite

Proceed to the next batch. After all batches complete, go to **Complete development**.

**Complete development** — validate that the integrated result achieves the plan's intent:

1. **Global AC validation** — Dispatch a subagent to validate all remaining ACs (multi-owner and cross-cutting). Provide the full AC list from the plan and the current codebase state. The subagent reads code and runs tests to determine for each AC:
   - ✅ Pass — behavior confirmed
   - ❌ Fail — behavior not implemented or incorrect
   - ⚠️ Partial — implemented but with gaps

2. **Goal validation** — Review all AC results against the plan's **Goal** statement. Does the integrated implementation achieve the stated goal? What's missing?

3. **Decision**:
   - All ACs pass + goal achieved → report done with proof per AC
   - Any AC fails → generate remediation tasks, re-enter execution
   - Partial → report status with options for resolution

If task implementation itself failed, determine next steps:
- Review concerns and/or blockers, update the plan with what needs rework, go back to execution phase
- If implementation was not possible, propose 2-3 options for addressing the cause, report current status along with suggestions

# Red flags

- **Verification step continues to fail** — stop and ask for clarification
- **Critical gaps or blockers** — stop and present the problem, do not force through
- **Instruction unclear** — stop and ask for clarification
- **Do not skip reviews** — spec compliance first, then code quality. Both required. No exceptions.
- **Never ignore subagent questions** — answer before letting them proceed.
- **Never accept "close enough"** — reviewer found issues means not done.
