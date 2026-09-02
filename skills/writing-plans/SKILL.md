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

**What counts as proof — hard taxonomy**: Proof is output observed from a running system. Nothing else qualifies.

Valid proof types:
- **Log output**: application logs showing the operation executed (e.g. "POST /api/items 201 Created")
- **HTTP response**: actual request/response pair from a running server (status code, headers, body)
- **DB state**: query results showing data changed as expected (SELECT output after INSERT/UPDATE)
- **Screenshot**: image of running application UI showing expected state
- **Process output**: stdout/stderr from a running process (startup messages, job completion, error traces)
- **File system state**: directory listing or file contents after execution (generated report, exported file)
- **Queue/cache state**: message published, cache entry set, job enqueued

Invalid — these are NEVER proof of runtime behavior:
- `git diff` (shows code was written, not that it works)
- Test runner output (shows tests pass, not that the app behaves correctly in production-like conditions)
- Type checker output (shows types are valid, not runtime behavior)
- Linter output (shows style compliance, not runtime behavior)
- Agent narrative ("the feature should work because..." — inference, not observation)
- Code review findings (shows code quality, not runtime behavior)
- Screenshots of code editors or terminals showing code (not the running application)

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

Prove the feature runs in a realistic isolated environment, not just that tests pass. State the **expected outcome** so evaluation is objective — without it the artifact is self-serving. Declare which dependencies are real vs. stubbed; if a dependency is external/blocked, capture behavior up to that boundary and log the stub.

Proof must be **runtime observation from a running system** — see taxonomy above. The expected outcome must describe what the evidence will show in concrete, observable terms:

```
Proof type: [log | http-response | db-state | screenshot | process-output | file-system | queue-state]
Run the isolated slice, capture evidence from the running system.
Expected outcome: [what the evidence must show — e.g. "server log shows POST /api/items returns 201 with item ID"]
```

**Done when**:

- All tests pass
- Lint shows no errors or warning
- Application builds locally
- Proof captured from running system matching the expected outcome (not test output or git diff)

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
- Every runtime-behavior task has a Proof step with a valid proof type and observable expected outcome
- No Proof step uses test output, git diff, type-check, or lint as runtime evidence
- Plan ends with a Validation task that maps each AC to its evidence
