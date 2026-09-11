---
name: executing-plans
description: Use when executing implementation plans with independent tasks in the current session.
---

Execute the plan by dispatching fresh subagents per task, then run spec compliance and code quality reviews after completion.

**Why subagents:** You delegate tasks to specialized agents with isolated context. They never inherit your session's context — you construct what they need, preserving your own context for coordination.

**Core principle:** Fresh subagent per task + two-stage review (spec, quality) + AC evals = high quality, fast iteration

**Continuous execution:** Do not pause to check in with your human partner between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete. "Should I continue?" prompts and progress summaries waste their time — they asked you to execute the plan, so execute it.

<IMPORTANT>
Development should happen in isolation and using fresh subagents for each task.

Before making changes, follow the Worktree Lifecycle steps in the RULE section.

ALWAYS inspect agent completion report, to ensure implementation met task specification, and code, to ensure quality concerns are addressed early.
</IMPORTANT>

# RULE

If no plan is provided, use `brainstorming` before proceeding.

**Understand plan**: Load and review plan to identify questions, concerns and assumptions.
If there are concerns, raise them and do not proceed. If the plan is clear, proceed with execution of each task.

**Worktree Lifecycle:**

Before dispatching tasks, create a dedicated git worktree:

1. Derive a branch name from the plan filename: `plan/<plan-name-slug>`
2. Create the worktree: `git worktree add .worktrees/<plan-name-slug> -b plan/<plan-name-slug>`
3. Record the worktree path as a session variable — all subsequent steps reference it
4. If `git worktree add` fails (e.g., branch exists, dirty tree), resolve the conflict before proceeding — do not skip worktree creation

All work happens inside this worktree; the main repo stays untouched.

After all tasks and AC evals complete, report the worktree path to the user. Do not auto-merge or delete.

**Execute plan**: Identify what tasks can be executed independently and what tasks have dependencies. Group independent tasks into batches for parallel dispatch. Dependent tasks execute sequentially (each forms its own batch).

For each batch, follow the fan-out/fan-in pattern:

1. **Extract tasks**: Read the plan once and extract all tasks in this batch with full text and context. Save to TodoWrite.

2. **Fan-out (parallel dispatch)**: Dispatch ALL tasks in the batch simultaneously, each as a fresh subagent using `reference/dispatch-agent.prompt.md` with the full task text pasted in. Do not make subagents read the plan file.

 3. **Fan-in (review after completion)**: Wait for all subagents to complete. For each completed task:
   a. Handle implementer status:
      - DONE / DONE_WITH_CONCERNS → proceed to spec review (step 3b)
      - NEEDS_CONTEXT → provide context and re-dispatch
      - BLOCKED → **before stopping**, review all previously completed tasks for
        spec compliance using `reference/spec-review.prompt.md`. Then notify user
        with: (1) spec review results for completed tasks, (2) blocked task + reason,
        (3) tasks held back. Do not skip spec review just because a later task is blocked.
   b. Verify completion using `reference/spec-review.prompt.md` and `reference/code-review.prompt.md` — spec compliance first, then code quality.
   c. Run review loops if issues found — fix, re-review, repeat until approved
   d. Mark task complete in TodoWrite

Proceed to the next batch. After all batches complete, go to **AC Evals**.

**AC Evals** — after all tasks are complete, evaluate each acceptance criterion against the running application:

1. **Read the plan's AC Evals section** — identify which ACs have eval procedures and which are non-coding (lightweight verify).

2. **Dispatch evals sequentially** — for each AC in dependency order:
   a. If the AC has dependencies that haven't been validated yet, defer it
   b. Dispatch a FRESH subagent using `reference/ac-eval.prompt.md` with the AC's eval
      procedure pasted in. AC evals MUST run as subagents — never run them inline.
      Inline execution defeats the purpose: the eval subagent must independently verify
      evidence without seeing implementation context.
   c. The eval subagent stands up the app, runs the procedure, captures runtime evidence
   d. Compare the eval result against the expected evidence

3. **Handle eval results**:
   - ✅ Pass → mark AC as validated
   - ❌ Fail → generate specific remediation tasks targeting the failure, add them to the plan, re-enter execution
   - ⚠️ Partial → report what passed and what failed, generate tasks for failures

4. **After all ACs evaluated** — re-run any evals that were deferred (their dependencies should now be validated)

**Goal validation** — once all ACs are validated:

1. Review all AC results against the plan's **Goal** statement. Does the integrated implementation achieve the stated goal?
2. **Decision**:
   - All ACs pass + goal achieved → report done with evidence per AC
   - Any AC fails → remediation tasks already generated, continue execution
   - Partial → report status with options for resolution

If task implementation itself failed, determine next steps:
- Review concerns and/or blockers, update the plan with what needs to work, go back to execution phase
- If implementation was not possible, propose 2-3 options for addressing the cause, report current status along with suggestions

# Red flags

- **Verification step continues to fail** — stop and ask for clarification
- **Critical gaps or blockers** — stop and present the problem, do not force through
- **Instruction unclear** — stop and ask for clarification
- **BLOCKED reached without reviewing completed tasks** — spec review of all DONE tasks is required before stopping
- **Do not skip reviews** — spec compliance first, then code quality. Both required. No exceptions.
- **Never ignore subagent questions** — answer before letting them proceed.
- **Never accept "close enough"** — reviewer found issues means not done.
- **Subagent reports files changed outside the worktree** — isolation has failed, re-dispatch with explicit worktree path
- **git diff in main repo shows uncommitted changes from this session** — worktree was not used, stop and assess damage
