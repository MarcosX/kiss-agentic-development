---
name: writing-plans
description: Use when specs or requirements are clear and before moving to implementation
---

Write agent-executable implementation plans, assuming zero codebase context.

<IMPORTANT>
Tasks must be self-contained: file paths, code, exact commands with expected outputs, and clear definition of done.

TDD prevents regressions — coding tasks follow test-first lifecycle steps below. Non-coding tasks (docs, config, CI/CD) skip TDD — use simple change→verify→commit steps.

The template below guarantees every task is agent-executable. Merge local ticket conventions into it — keep Test: file and TDD steps.
</IMPORTANT>

# RULE

**Save plans before starting**: Save to `<prefix>-plan.md` (2-3 key words, never `plan.md`).

**Scope reduction**: Before extracting ACs, remove features not justified by design or requirements. Scope creep wastes effort — YAGNI (You Ain't Gonna Need It) is an active filter.

**AC coverage**: Extract acceptance criteria from the design, prompt, or other sources and build a coverage list.

**Vertical slices**: Break work into thin end-to-end slices. Each slice cuts through ALL layers (schema → API → logic → tests → UI), is demoable on its own. Type each as HITL (needs human) or AFK (agent can implement independently). Publish blockers first. Only load `references/slicing-guide.md` for the full template and edge cases around ordering — do not read it proactively.

**Quiz the user**: After presenting the proposed breakdown, ask about granularity, dependency correctness, and HITL/AFK assignments. Iterate until approved.

**Each Task is self-contained**: Tasks contain clear implementation, verification, and completion steps.

**Each step is one atomic action**: No judgment required. Ambiguity means revisit the plan. Each step completes one atomic action.

**Ensure all ACs are covered**: Map every AC to tasks as they are created. If ACs are left with no task assigned, review the plan to identify gaps/duplication.

**Proof & Validation**: Tests and code review prove code matches spec — they don't prove it runs. Every runtime-behavior task gets a Proof step capturing observable evidence, and every plan ends with a Validation task running the integrated system. This closes the gap where agents claim "done, matches spec, passes review" yet the feature fails once running.

**Plan handover**: Once the plan is in place, transition to implementation. **REQUIRED BACKGROUND:** You MUST understand executing-plans.

# Plan document

**The following outline should be used for plans**

````markdown
# [Feature name] Implementation Plan

**Goal**: [One sentence on what and why]

**Architecture**: [2-3 sentences with approach, key components and patterns]

**Acceptance Criteria:**

- AC-1: [testable statement] [owned by: Task N, Task M]
- AC-2: [testable statement] [owned by: Task N]

---

## Task N: [Task Name]

**Category:** Coding | Non-coding
**Satisfies:** AC-1, AC-2

**Files:**

- Create: [path to files that need to be created]
- Modify: [path to files that should be modified]
- Test: [path to test files — REQUIRED for Coding tasks]

**Coding template** — use when Category is Coding:

1. Write failing test:

[code block with test that should be created]

2. Verify test fails:

[instructions to run tests and expected failures]

3. Write minimal implementation

[code block with code to be added]

4. Verify test pass

[instructions to run tests and expected output]

5. Commit

```bash
git add path/to/files path/to/test/files
git commit -m 'feat: add feature'
```

6. Proof (required for runtime-behavior tasks: server, endpoint, UI, job, migration)

Prove the feature runs in a realistic isolated environment, not just that tests pass. State the **expected outcome** so evaluation is objective — without it the artifact is self-serving. Declare which dependencies are real vs. stubbed; if a dependency is external/blocked, capture behavior up to that boundary and log the stub. Expected-outcome kinds:
- Execution trace: process stays alive, health check 200
- Output capture: API/CLI/page output matches expected shape
- State inspection: DB row, cache, or queue entry has expected value
- Failure evidence: error logged with context, graceful degradation

```
Run the isolated slice, capture artifacts (log, response, query result) to
SESSION_SCRATCH, record the reproduction command and the expected outcome.
```

**Done when**:

- All tests pass
- Lint shows no errors or warning
- Application builds locally
- Proof artifacts captured matching the expected outcome

---

**Non-coding template** — use when Category is Non-coding (docs, config, CI/CD, dependency bumps):

1. Make change

[description of what to change, with exact values]

2. Verify

[how to confirm — read output, parse file, dry run, etc.]

3. Proof (only if the change has runtime behavior; otherwise skip)

4. Commit

```bash
git add path/to/files
git commit -m 'chore: description'
```

**Done when**:

- Change is confirmed correct
- Proof captured (if applicable)

---

**Final task: Validation** — every plan ends with this. Runs the integrated system with realistic (stub or mock) data, captures end-to-end artifacts, and writes a validation report mapping each AC to its evidence.

- Repro: exact commands to run the full app and exercise each AC
- Dependencies: which are real vs. stubbed for this run
- Artifacts: logs, responses, query dumps, screenshots captured to SESSION_SCRATCH
- Expected outcome per AC: what the evidence must show for each AC to be considered validated

Non-coding-only plans (no runtime) may collapse this into a single final Verify step.
````

## Plan Self-Review

Before finalizing, dispatch a subagent to review the plan against the checklist below. Include the checklist categories and ask the subagent to report any AC coverage gaps, ambiguous steps, incomplete specs, or HITL tasks missing human instructions. Apply all fixes in the main session.

## Checklist

- Every AC maps to a named task (via **Satisfies** field)
- Each task has a **Satisfies** field referencing its ACs
- Each task has a Category and Type
- Exact file paths always
- Complete code (never "add code here")
- Exact commands with expected output
- Every task has a "Done when:" statement
- Every runtime-behavior task has a Proof step with an expected outcome
- Plan ends with a Validation task that maps each AC to its evidence
