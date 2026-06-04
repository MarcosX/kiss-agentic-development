# Practicing TDD Skill Validation

## Content Checks

```bash
grep -q "^---" skills/practicing-tdd/SKILL.md && echo "✓ Front matter present"
grep -q "^name: practicing-tdd" skills/practicing-tdd/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/practicing-tdd/SKILL.md && echo "✓ Description present"
grep -q "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" skills/practicing-tdd/SKILL.md && echo "✓ Iron Law present"
grep -q "HARD-GATE" skills/practicing-tdd/SKILL.md && echo "✓ Hard gate enforces test-first"
grep -q "RED" skills/practicing-tdd/SKILL.md && echo "✓ RED phase documented"
grep -q "GREEN" skills/practicing-tdd/SKILL.md && echo "✓ GREEN phase documented"
grep -q "REFACTOR" skills/practicing-tdd/SKILL.md && echo "✓ REFACTOR phase documented"
grep -q "Verify RED" skills/practicing-tdd/SKILL.md && echo "✓ RED verification mandated"
grep -q "Verify GREEN" skills/practicing-tdd/SKILL.md && echo "✓ GREEN verification mandated"
grep -q "Prove-It Pattern" skills/practicing-tdd/SKILL.md && echo "✓ Prove-It Pattern for bugs"
grep -q "Red Flags" skills/practicing-tdd/SKILL.md && echo "✓ Red flags section present"
grep -q "Verification Checklist" skills/practicing-tdd/SKILL.md && echo "✓ Verification checklist present"
grep -q "must be deleted" skills/practicing-tdd/SKILL.md && echo "✓ Deletion rule enforced"
```

## Integration Test

```bash
echo "✓ Practicing TDD skill validation complete"
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `test/prompts/practicing-tdd/VALIDATE.prompt.md` and report any issues found with the practicing-tdd skill.

## Test Scenarios

### Scenario 1: Code Written Before Test
**Input**: "Here's an implementation I wrote, let me just add tests after"
**Expected**: Iron Law blocks this, requires deletion and restart
**Red Flag**: "just this once", "add tests after"

### Scenario 2: Skip TDD for Small Change
**Input**: "It's just a one-line fix, no need for TDD"
**Expected**: Skill triggers, points to "this is too simple" red flag
**Red Flag**: "too simple to test", "one-line fix"

### Scenario 3: Bug Without Reproduction Test
**Input**: "There's a bug in the login flow, let me just fix it"
**Expected**: Prove-It Pattern invoked — reproduction test required first
**Red Flag**: fix without test, "I know what the bug is"

### Scenario 4: Immediate Green
**Input**: "I wrote the test and it passed on the first run!"
**Expected**: RED verification catches this — test tested existing behavior
**Red Flag**: test passes on first run, didn't see it fail

### Scenario 5: Over-engineered GREEN
**Input**: "Let me add logging, caching, and error handling while I'm at it"
**Expected**: Skill blocks extra features in GREEN phase, points to minimal code rule
**Red Flag**: adding features in GREEN, YAGNI violation

### Scenario 6: Skipping Verification
**Input**: "I trust the test, no need to run it"
**Expected**: Skill requires mandatory verification steps
**Red Flag**: skipping test run, "I trust it"
