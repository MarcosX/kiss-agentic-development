# Reviewing Code Skill Validation

## Content Checks

```bash
grep -q "^---" skills/reviewing-code/SKILL.md && echo "✓ Front matter present"
grep -q "^name: reviewing-code" skills/reviewing-code/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/reviewing-code/SKILL.md && echo "✓ Description present"
grep -q "Correctness" skills/reviewing-code/SKILL.md && echo "✓ Correctness axis covered"
grep -q "Readability" skills/reviewing-code/SKILL.md && echo "✓ Readability axis covered"
grep -q "Architecture" skills/reviewing-code/SKILL.md && echo "✓ Architecture axis covered"
grep -q "Security" skills/reviewing-code/SKILL.md && echo "✓ Security axis covered"
grep -q "Performance" skills/reviewing-code/SKILL.md && echo "✓ Performance axis covered"
grep -q "Categorize Findings" skills/reviewing-code/SKILL.md && echo "✓ Severity labeling present"
grep -q "Change Sizing" skills/reviewing-code/SKILL.md && echo "✓ Change sizing guidance"
grep -q "Handling Disagreements" skills/reviewing-code/SKILL.md && echo "✓ Disagreements hierarchy"
grep -q "The Response Pattern" skills/reviewing-code/SKILL.md && echo "✓ Feedback response pattern"
grep -q "Clarify Before Implementing" skills/reviewing-code/SKILL.md && echo "✓ Clarify-before-implement rule"
grep -q "YAGNI on Suggestions" skills/reviewing-code/SKILL.md && echo "✓ YAGNI on feedback"
grep -q "Push Back When Wrong" skills/reviewing-code/SKILL.md && echo "✓ Push-back guidance"
grep -q "Red Flags" skills/reviewing-code/SKILL.md && echo "✓ Red flags section present"
```

## Integration Test

```bash
echo "✓ Reviewing code skill validation complete"
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `test/prompts/reviewing-code/VALIDATE.prompt.md` and report any issues found with the reviewing-code skill.

## Test Scenarios

### Scenario 1: Merge Without Review

**Input**: "This change is tiny, just merge it"
**Expected**: Skill triggers review workflow, red flag on merging unreviewed code
**Red Flag**: "merge without review", "too small to review"

### Scenario 2: Review Only Tests

**Input**: "All tests pass, ship it"
**Expected**: Five-axis review still runs — tests are necessary but not sufficient
**Red Flag**: "tests pass = good", skipping other axes

### Scenario 3: LGTM Without Evidence

**Input**: "Looks good to me"
**Expected**: Skill requires evidence of actual review, red flags rubber-stamping
**Red Flag**: "LGTM without evidence"

### Scenario 4: Unclear Feedback

**Input**: Reviewer says "Fix this section" with vague comments
**Expected**: Skill requires clarification before implementation
**Red Flag**: implementing unclear feedback

### Scenario 5: Over-engineered Suggestion

**Input**: Reviewer says "Implement proper metrics tracking with database, filters, CSV export"
**Expected**: YAGNI check on feedback — grep for actual usage first
**Red Flag**: building features that aren't called

### Scenario 6: Wrong Suggestion

**Input**: Reviewer says "Remove this for simplicity" but it handles an edge case
**Expected**: Push back with technical reasoning backed by code
**Red Flag**: blind implementation of wrong feedback
