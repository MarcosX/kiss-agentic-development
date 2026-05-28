---
name: executing-plans
description: Use to execute and verify writen plans, leveraging subagents with review checkpoints.
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

**Execute plan**: Identify what tasks can be executed independently and what tasks have dependencies, then for each task:

1. **Read the plan once**: Extract all tasks with full text and context. Save to TodoWrite.
2. **Dispatch a fresh subagent** using `dispatch-agent.prompt.md` with the full task text pasted in — do not make the subagent read the plan file.
3. **Handle implementer status**:
   - **DONE**: Proceed to spec compliance review.
   - **DONE_WITH_CONCERNS**: Read concerns before proceeding. If about correctness, address first. If observations, note and proceed.
   - **NEEDS_CONTEXT**: Provide missing context and re-dispatch.
   - **BLOCKED**: Assess the blocker — provide context, upgrade model, split task, or escalate.
4. **Verify completion**: Review subagent report and inspect implementation.
   - Use `spec-review.prompt.md` to validate task goals against implementation
   - Use `code-review.prompt.md` to ensure code quality concerns are addressed early on
5. **Run review loops**: If reviewer finds issues, have implementer fix them, then re-review until approved. Do not skip re-review.
6. **Mark task complete** in TodoWrite and proceed to the next task.

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

## Model Selection

Use the least powerful model that can handle each role to conserve cost and increase speed.

- **Mechanical implementation tasks** (isolated functions, clear specs, 1-2 files): use a fast, cheap model.
- **Integration and judgment tasks** (multi-file coordination, pattern matching, debugging): use a standard model.
- **Architecture, design, and review tasks**: use the most capable available model.

**Task complexity signals:**
- Touches 1-2 files with a complete spec → cheap model
- Touches multiple files with integration concerns → standard model
- Requires design judgment or broad codebase understanding → most capable model

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)
- Subagent can ask questions before AND during work

**Quality gates:**
- Self-review catches issues before handoff
- Two-stage review: spec compliance, then code quality
- Review loops ensure fixes actually work
- Spec compliance prevents over/under-building
- Code quality ensures implementation is well-built

# Red flags

Do not rely on guessing and do not force through blockers.

**Verification step continues to fail**: stop and ask for clarification to ensure the verification step is actually correct.

**Critical gaps are found**: when implementing, even though the plan was reviewed, stop and ask for clarification when needed.

**Previous steps prevent proper implementation**: when an implementation decision made earlier impacts the next tasks, stop and present the problem to ask for clarification.

**Instruction isn't clear or can't be performed**: when actions on a step can't be executed, due to environment or any other limitation, stop and present the problem to ask for clarification.

**Do not dispatch multiple implementation subagents in parallel** — they will conflict.

**Do not skip reviews** (spec compliance OR code quality).

**Do not proceed with unfixed issues** — reviewer found issues = implementer fixes = review again.

**Do not skip re-review** after fixes are applied.

**Do not let implementer self-review replace actual review** — both are needed.

**Do not start code quality review before spec compliance is ✅** — wrong order.

**Never ignore subagent questions** — answer before letting them proceed.

**Never accept "close enough" on spec compliance** — spec reviewer found issues = not done.
