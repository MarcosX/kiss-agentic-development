---
name: writing-plans
description: Use when specs or requirements are clear and before moving to implementation
---

Write agent-executable implementation plans, assuming zero codebase context.

<IMPORTANT>
Tasks must be self-contained: file paths, code, exact commands with expected outputs, and clear definition of done.

TDD is the default. Coding tasks MUST include test-first lifecycle steps. Non-coding tasks (docs, config, CI/CD) skip TDD — use simple change→verify→commit steps.

The template below is authoritative. Merge local ticket conventions into it — do not omit Test: file or TDD steps.
</IMPORTANT>

# RULE

**Save plans before starting**: Save to `<prefix>-plan.md` (2-3 key words, never `plan.md`).

**Scope reduction**: Before extracting ACs, remove features not justified by design or requirements. Scope creep wastes effort — YAGNI is an active filter.

**AC coverage**: Extract acceptance criteria from the design, prompt, or other sources and build a coverage list.

**Vertical slices**: When slicing tickets, use `references/slicing-guide.md` to break work into thin end-to-end slices. Each slice cuts through all layers, is demoable on its own, and is typed as HITL (needs human) or AFK (agent can implement independently). Publish blockers first.

**Quiz the user**: After presenting the proposed breakdown, ask about granularity, dependency correctness, and HITL/AFK assignments. Iterate until approved.

**Each Task is self-contained**: Tasks contain clear implementation, verification, and completion steps.

**Each step is one atomic action**: No judgment required. Ambiguity means revisit the plan. Each step completes one atomic action.

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
