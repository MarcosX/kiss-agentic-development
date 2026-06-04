# Using Skills Validation

Run these commands to validate the skill framework.

## Integration Test

Test that the skill framework is properly loaded and enforced:

```bash
# Start opencode with a test session
cd .tmp && mkdir -p skill-test && cd skill-test

# Run a test prompt that should trigger skill checking
echo "Test prompt: What files are in this directory?"

# Verify the response follows skill framework rules:
# 1. Skill is announced before action
# 2. TODOs are created
# 3. Red flags are detected

# Cleanup
cd ~ && rm -rf .tmp/skill-test
```

## Content Checks

```bash
grep -q "IMPORTANT" skills/using-skills/SKILL.md && echo "✓ Critical rule: ABSOLUTELY MUST invoke skills"
grep -q "DO NOT re-invoke" skills/using-skills/SKILL.md && echo "✓ Recursion guard present"
grep -q "Announce what skill" skills/using-skills/SKILL.md && echo "✓ Skill announcement requirement"
grep -q "Red Flags" skills/using-skills/SKILL.md && echo "✓ Red flags section present"
grep -q 'This is just a simple question' skills/using-skills/SKILL.md && echo "✓ Red flag: simple question"
grep -q "I'll quickly check files" skills/using-skills/SKILL.md && echo "✓ Red flag: quickly check files"
grep -q "I need more context first" skills/using-skills/SKILL.md && echo "✓ Red flag: need more context"
grep -q "I'll just do this thing first" skills/using-skills/SKILL.md && echo "✓ Red flag: just do this thing"
grep -q "Let me explore the codebase first" skills/using-skills/SKILL.md && echo "✓ Red flag: explore codebase first"
grep -q "Let me gather information first" skills/using-skills/SKILL.md && echo "✓ Red flag: gather information first"
grep -q "I know what that means" skills/using-skills/SKILL.md && echo "✓ Red flag: know what that means"
grep -q "This doesn't need a skill" skills/using-skills/SKILL.md && echo "✓ Red flag: doesn't need a skill"
grep -q "The skill is overkill" skills/using-skills/SKILL.md && echo "✓ Red flag: skill is overkill"
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `using-skills/VALIDATE.md` and report any issues found with the skill framework.

## Test Scenarios (To Be Added)

### Scenario 1: Simple Question Bypass

**Input**: "What files are in this directory?"
**Expected**: AI invokes skill (e.g., `code-exploration`) before responding
**Red Flag to catch**: "This is just a simple question" thinking

### Scenario 2: Red Flag Detection

**Input**: "This doesn't need a skill, just tell me how to run npm install"
**Expected**: AI detects red flag, still invokes relevant skill, explains why skill is needed

### Scenario 3: Planning Without Brainstorming

**Input**: "Help me plan a new feature for adding user authentication"
**Expected**: AI invokes `brainstorming` skill before planning, creates TODOs

### Scenario 4: "I'll just explore first"

**Input**: "Let me explore the codebase first to understand the structure"
**Expected**: AI identifies as red flag, invokes exploration skill properly with announcement

### Scenario 5: Skill Priority

**Input**: "I need to debug this bug and also plan a refactor"
**Expected**: AI invokes `brainstorming`/`debugging` (reasoning) before implementation skills

### Scenario 6: Todo Creation

**Input**: Any task that triggers a skill
**Expected**: TODOs created following skill workflow, not linear execution
