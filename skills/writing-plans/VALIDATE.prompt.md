# Writing Plans Skill Validation

Run these commands to validate the writing-plans skill.

## Syntax Check

```bash
grep -q "^---" skills/writing-plans/SKILL.md && echo "✓ Front matter present"
grep -q "^name: writing-plans" skills/writing-plans/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/writing-plans/SKILL.md && echo "✓ Description present"
grep -q "self-contained" skills/writing-plans/SKILL.md && echo "✓ Self-contained requirement"
grep -q "<prefix>-plan.md" skills/writing-plans/SKILL.md && echo "✓ prefix-plan.md naming convention"
grep -q "AC coverage" skills/writing-plans/SKILL.md && echo "✓ AC coverage required"
grep -q "Done when" skills/writing-plans/SKILL.md && echo "✓ Done when section in template"
grep -q "YAGNI" skills/writing-plans/SKILL.md && echo "✓ YAGNI principle mentioned"
grep -q "atomic action" skills/writing-plans/SKILL.md && echo "✓ Atomic step requirement"
grep -q "Write failing test" skills/writing-plans/SKILL.md && echo "✓ TDD: write failing test step"
grep -q "Verify test fails" skills/writing-plans/SKILL.md && echo "✓ TDD: verify test fails step"
grep -q "Write minimal implementation" skills/writing-plans/SKILL.md && echo "✓ TDD: implementation step"
grep -q "Verify test pass" skills/writing-plans/SKILL.md && echo "✓ TDD: verify test passes step"
```

## Integration Test

```bash
# Test plan creation with proper naming
echo "Test: Write a plan for adding user authentication"

# Verify plan:
# 1. Uses prefix-plan.md naming (not generic plan.md)
# 2. Includes Goal, Architecture sections
# 3. Tasks have Files (Create/Modify/Test)
# 4. Steps follow TDD pattern (fail test → implement → pass → commit)
# 5. Each step is atomic and unambiguous
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `writing-plans/VALIDATE.prompt.md` and report any issues found with the writing-plans skill.

## Test Scenarios

### Scenario 1: Generic Plan Name
**Input**: "Write a plan for adding a feature"
**Expected**: 
- Plan named `feature-name-plan.md` (with actual prefix)
- NOT just `plan.md`
- Prefix should be 2-3 key words

### Scenario 2: Missing AC Coverage
**Input**: "Write a plan based on this spec" (with partial acceptance criteria)
**Expected**:
- AI identifies missing ACs before writing plan
- Builds AC coverage list
- Ensures no AC is left without task mapping

### Scenario 3: Non-Atomic Step
**Input**: "Write a plan with step 'Implement the feature'"
**Expected**:
- Skill detects non-atomic step
- Breaks into: failing test, verify fails, implementation, verify passes, commit

### Scenario 4: TDD Enforcement
**Input**: "Write a plan for a new feature"
**Expected**:
- Every task starts with "Write failing test"
- Followed by "Verify test fails"
- Then implementation, then verify pass, then commit

### Scenario 5: Self-Contained Requirement
**Input**: "Write a plan assuming you know nothing about the codebase"
**Expected**:
- All file paths are explicit
- All commands include expected outputs
- Done criteria are clear and verifiable

### Scenario 6: DRY/YAGNI Principle
**Input**: "Write a plan that includes all possible features"
**Expected**:
- Skill applies YAGNI to reduce scope
- Focuses on minimal viable implementation
- Identifies unnecessary scope

### Scenario 7: Plan Document Structure
**Input**: "Write a plan"
**Expected document structure**:
```
# [Feature] Implementation Plan
**Goal**: ...
**Architecture**: ...
---
## Task N: [Name]
**Files:**
- Create:
- Modify:
- Test:
**Steps:**
1. Write failing test: [code]
2. Verify test fails: [instructions]
3. Write minimal implementation: [code]
4. Verify test pass: [instructions]
5. Commit
**Done when**: ...
```

### Scenario 8: Ambiguity Detection
**Input**: Plan with vague step like "check the code"
**Expected**:
- Identifies ambiguity
- Revises plan to make step unambiguous
- Provides clear commands and expected outputs

### Scenario 9: AC to Task Mapping
**Input**: Plan with ACs left without tasks
**Expected**:
- Skill identifies gaps in coverage
- Adds tasks to cover all ACs
- Reports any duplication

### Scenario 10: Context Assumptions
**Input**: "Write a plan" without any context
**Expected**:
- Assumes zero codebase context
- All file paths and commands are explicit
- No assumptions about existing code structure