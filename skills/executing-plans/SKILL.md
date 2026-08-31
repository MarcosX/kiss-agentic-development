---
name: executing-plans
description: Use when executing implementation plans with independent tasks in the current session.
---

Execute the plan by dispatching fresh subagents per task, then run spec compliance and code quality reviews after completion.

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

**Core principle:** Fresh subagent per task + three-stage review (spec, runtime proof, quality) = high quality, fast iteration

**Continuous execution:** Do not pause to check in with your human partner between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete. "Should I continue?" prompts and progress summaries waste their time — they asked you to execute the plan, so execute it.

<IMPORTANT>
Development should happen in isolation and using fresh subagents for each task.

Ensure a dedicated git worktree is used before making changes.

ALWAYS inspect agent completion report, to ensure implementation met task specification, and code, to ensure quality concerns are addressed early. Verify runtime proof independently before accepting a task as done.
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
   b. Verify completion using `references/spec-review.prompt.md`, `references/proof-review.prompt.md`, and `references/code-review.prompt.md` in that order — spec, then runtime proof, then code quality. Proof before code so you never review code that won't run, and rework loops fail cheapest.

   Proof review: dispatch a fresh validation subagent with `references/proof-review.prompt.md`, the task's Proof step (with expected outcome), and the implementer's proof manifest. It re-runs the reproduction command against current code and verifies artifacts match the expected outcome — it must not trust the implementer's claim.

   Proof loop-back: if proof review fails, the task is NOT done. Re-dispatch a subagent with the specific gap ("the Proof claimed the endpoint returns line items, but the response was empty") to fix and re-capture proof, then re-run proof review. AC validation runs only on proven-running code.
   c. **AC validation** (single-owner only): If the task has a **Satisfies** field, validate each AC that lists this task as its sole owner. Read relevant code and run tests to confirm the AC is met. Report pass/fail per AC. Skip if the task references no ACs, or no ACs it owns individually.
   d. Run review loops if issues found — fix, re-review, repeat until approved
   e. Mark task complete in TodoWrite

Proceed to the next batch. After all batches complete, go to **Complete development**.

**Complete development** — validate that the integrated result achieves the plan's intent:

1. **Validation task** — Run the plan's final Validation task: dispatch a subagent to run the integrated system with realistic/mock data, confirm it starts and runs, and capture the specified artifacts to SESSION_SCRATCH. Verify its proof against each AC's expected outcome. On failure, generate remediation tasks and re-enter execution.

2. **Global AC validation** — Dispatch a subagent to validate all remaining ACs (multi-owner and cross-cutting). Provide the full AC list from the plan, the current codebase state, and the Validation evidence. The subagent reads code and runs tests to determine for each AC:
   - ✅ Pass — behavior confirmed
   - ❌ Fail — behavior not implemented or incorrect
   - ⚠️ Partial — implemented but with gaps

3. **Goal validation** — Review all AC results against the plan's **Goal** statement. Does the integrated implementation achieve the stated goal? What's missing?

4. **Decision**:
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
- **Do not skip reviews** — spec compliance first, then runtime proof, then code quality. All three required. No exceptions.
- **Do not trust "it runs"** — a Proof step must be independently re-run and its artifacts matched against the expected outcome before a task is done. A claim without examined runtime evidence is not done.
- **Never ignore subagent questions** — answer before letting them proceed.
- **Never accept "close enough"** — reviewer found issues means not done.
