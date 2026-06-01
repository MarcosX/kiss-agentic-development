---
name: writing-plans
description: Use when specs or requirements are clear and before moving to implementation
---

Write agent-executable implementation plans, assuming zero codebase context.

<IMPORTANT>
Tasks must be self-contained: file paths, code, exact commands with expected outputs, and clear definition of done.

TDD is the default. Coding tasks MUST include test-first lifecycle steps. Non-coding tasks (docs, config, CI/CD) skip TDD — use simple change→verify→commit steps.

The template below is authoritative. If the project has local ticket conventions (e.g. `project-management.md`), merge them INTO this template — do not omit the Test: file section or TDD lifecycle steps.
</IMPORTANT>

# RULE

**Save plans before starting**: Save plans to `<prefix>-plan.md`, where prefix is 2-3 key words, never use generic names, like `plan.md`.

**Scope reduction**: Before extracting ACs, identify features not justified by the design or requirements and remove them. Scope creep wastes implementation effort — YAGNI is an active filter, not a footnote.

**AC coverage**: Extract acceptance criteria from the design, prompt, or other sources and build a coverage list.

**Vertical slices**: When slicing tickets, use `references/slicing-guide.md` to break work into thin end-to-end slices. Each slice cuts through all layers, is demoable on its own, and is typed as HITL (needs human) or AFK (agent can implement independently). Publish blockers first.

**Quiz the user**: After presenting the proposed breakdown, ask about granularity, dependency correctness, and HITL/AFK assignments. Iterate until approved.

**Each Task is self-contained**: Tasks contain clear steps to implement them, along with verification steps and completion steps.

**Each step is one atomic action**: No judgment is required to complete a step. Any ambiguity should be addressed by revisting the plan. Steps should be minimalistic bite-sized actions to complete just one part of a task.

**Ensure all ACs are covered**: Map every AC to tasks as they are created. If ACs are left with no task assigned, review the plan to identify gaps/duplication.

**Plan handover**: Once the plan is in place, use `executing-plans` to transition to implementation.

# Plan document

**The following outline should be used for plans**

````markdown
# [Feature name] Implementation Plan

**Goal**: [One sentence on what and why]

**Architecture**: [2-3 sentences with approach, key components and patterns]

---

## Task N: [Task Name]

**Category:** Coding | Non-coding

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

**Done when**:

- All tests pass
- Lint shows no errors or warning
- Application builds locally

---

**Non-coding template** — use when Category is Non-coding (docs, config, CI/CD, dependency bumps):

1. Make change

[description of what to change, with exact values]

2. Verify

[how to confirm — read output, parse file, dry run, etc.]

3. Commit

```bash
git add path/to/files
git commit -m 'chore: description'
```

**Done when**:

- Change is confirmed correct
````
