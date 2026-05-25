# Executing Plans Skill Validation

Run these commands to validate the executing-plans skill.

## Syntax Check

```bash
grep -q "^---" skills/executing-plans/SKILL.md && echo "✓ Front matter present"
grep -q "^name: executing-plans" skills/executing-plans/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/executing-plans/SKILL.md && echo "✓ Description present"
grep -q "git worktree" skills/executing-plans/SKILL.md && echo "✓ Git worktree requirement mentioned"
grep -q "dispatch-agent" skills/executing-plans/SKILL.md && echo "✓ Subagent dispatch mentioned"
grep -q "inspect agent completion report" skills/executing-plans/SKILL.md && echo "✓ Completion report inspection required"
grep -q "brainstorming" skills/executing-plans/SKILL.md && echo "✓ Brainstorming fallback for missing plans"
grep -q "Red flags" skills/executing-plans/SKILL.md && echo "✓ Red flags section present"
```

## Prompt Files

```bash
test -f skills/executing-plans/dispatch-agent.prompt.md && echo "✓ dispatch-agent.prompt.md exists"
test -f skills/executing-plans/spec-review.prompt.md && echo "✓ spec-review.prompt.md exists"
test -f skills/executing-plans/code-review.prompt.md && echo "✓ code-review.prompt.md exists"
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `executing-plans/VALIDATE.prompt.md` and report any issues found with the executing-plans skill.

## Test Scenarios

### Scenario 1: Missing Plan
**Input**: "Execute this task for me"
**Expected**:
- Skill detects no plan provided
- Invokes `brainstorming` before proceeding
- Returns to executing after plan is created

### Scenario 2: Plan Review
**Input**: A plan with ambiguous steps
**Expected**:
- Skill reviews plan before executing
- Identifies questions, concerns, and assumptions
- Raises concerns if the plan is unclear
- Does NOT proceed with unclear plan

### Scenario 3: Task Dependencies
**Input**: A multi-task plan with dependencies
**Expected**:
- Identifies independent vs dependent tasks
- Dispatches independent tasks in parallel
- Sequences dependent tasks correctly
- Uses fresh subagent per task

### Scenario 4: Completion Review
**Input**: Plan execution completes
**Expected**:
- Reviews subagent completion report
- Runs spec review to validate task goals
- Runs code review for quality
- Reports status with proof of completion

### Scenario 5: Task Failure Recovery
**Input**: A task implementation fails
**Expected**:
- Reviews concerns/blockers
- Updates plan with rework items
- Goes back to execution phase
- Does NOT force through blockers

### Scenario 6: Blocked Implementation
**Input**: A task can't be implemented (e.g., missing dependency)
**Expected**:
- Reviews concerns/blockers
- Proposes 2-3 options for addressing the cause
- Reports current status with suggestions
- Asks for clarification before proceeding

### Scenario 7: Red Flag — Verification Loop
**Input**: Verification step continues to fail repeatedly
**Expected**:
- Stops and asks for clarification
- Questions whether the verification step is correct
- Does NOT attempt to force the implementation through

### Scenario 8: Red Flag — Critical Gap
**Input**: During implementation, a critical design gap is found
**Expected**:
- Stops and asks for clarification
- Does NOT make assumptions about the gap
- Waits for user input before proceeding

### Scenario 9: Red Flag — Previous Step Impact
**Input**: An earlier implementation decision blocks the next task
**Expected**:
- Stops and presents the problem
- Asks for clarification
- Does NOT silently work around the issue

### Scenario 10: Red Flag — Unclear Instruction
**Input**: A step can't be executed (environment limitation, missing info)
**Expected**:
- Stops and presents the problem
- Asks for clarification
- Does NOT guess or force through
