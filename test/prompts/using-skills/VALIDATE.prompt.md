# Using Skills Validation

Validate the `using-skills` global instruction file.

## Content Checks

```bash
test -f instructions/using-skills.md && echo "✓ Instructions file exists"
grep -q "ABSOLUTELY MUST invoke skills" instructions/using-skills.md && echo "✓ Critical rule: ABSOLUTELY MUST invoke skills"
grep -q "Announce what skill" instructions/using-skills.md && echo "✓ Skill announcement requirement"
grep -q "Red Flags" instructions/using-skills.md && echo "✓ Red flags section present"
grep -q 'This is just a simple question' instructions/using-skills.md && echo "✓ Red flag: simple question"
grep -q "I'll quickly check files" instructions/using-skills.md && echo "✓ Red flag: quickly check files"
grep -q "I need more context first" instructions/using-skills.md && echo "✓ Red flag: need more context"
grep -q "I'll just do this thing first" instructions/using-skills.md && echo "✓ Red flag: just do this thing"
grep -q "Let me explore the codebase first" instructions/using-skills.md && echo "✓ Red flag: explore codebase first"
grep -q "Let me gather information first" instructions/using-skills.md && echo "✓ Red flag: gather information first"
grep -q "I know what that means" instructions/using-skills.md && echo "✓ Red flag: know what that means"
grep -q "This doesn't need a skill" instructions/using-skills.md && echo "✓ Red flag: doesn't need a skill"
grep -q "The skill is overkill" instructions/using-skills.md && echo "✓ Red flag: skill is overkill"
grep -q "Signal Scan" instructions/using-skills.md && echo "✓ Signal Scan section present"
grep -q "bug, error, crash" instructions/using-skills.md && echo "✓ Signal scan: debugging triggers"
grep -q "idea, approach, explore" instructions/using-skills.md && echo "✓ Signal scan: brainstorming triggers"
grep -q "plan, implement, build" instructions/using-skills.md && echo "✓ Signal scan: writing-plans triggers"
grep -q "Let me investigate this" instructions/using-skills.md && echo "✓ Red flag: investigate this"
grep -q "Let me understand the problem first" instructions/using-skills.md && echo "✓ Red flag: understand problem first"
grep -q "I already know what skill I need" instructions/using-skills.md && echo "✓ Red flag: already know skill"
```

---

**Prompt for AI Assistants:**

> Validate that `instructions/using-skills.md` exists, contains no YAML frontmatter, no recursion guard ("DO NOT re-invoke"), and no preamble text beyond the header. All red flags from the original must be present.

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
