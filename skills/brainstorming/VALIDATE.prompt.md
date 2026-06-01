# Brainstorming Skill Validation

Run these commands to validate the brainstorming skill.

## Syntax Check

```bash
grep -q "^---" skills/brainstorming/SKILL.md && echo "✓ Front matter present"
grep -q "^name: brainstorming" skills/brainstorming/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/brainstorming/SKILL.md && echo "✓ Description present"
grep -q "Do NOT invoke any implementation skill" skills/brainstorming/SKILL.md && echo "✓ Critical rule: blocks implementation before approval"
grep -q "Explore context" skills/brainstorming/SKILL.md && echo "✓ Workflow step 1: explore context"
grep -q "Ask clarifying questions" skills/brainstorming/SKILL.md && echo "✓ Workflow step 2: clarifying questions"
grep -q "Propose 2-3 approaches" skills/brainstorming/SKILL.md && echo "✓ Workflow step 3: propose approaches"
grep -q "Present the design" skills/brainstorming/SKILL.md && echo "✓ Workflow step 4: present design"
grep -q "Create implementation plan" skills/brainstorming/SKILL.md && echo "✓ Workflow step 5: creates implementation plan"
grep -q "writing-plans" skills/brainstorming/SKILL.md && echo "✓ References writing-plans for plan creation"
grep -q "YAGNI" skills/brainstorming/SKILL.md && echo "✓ YAGNI principle enforced"
grep -q "one at a time" skills/brainstorming/SKILL.md && echo "✓ One question at a time rule"
grep -q "explore-context.prompt.md" skills/brainstorming/SKILL.md && echo "✓ References explore-context.prompt.md for subagent dispatch"
test -f skills/brainstorming/references/explore-context.prompt.md && echo "✓ explore-context.prompt.md reference file exists"
grep -q "dispatch a subagent to scan" skills/brainstorming/SKILL.md && echo "✓ Spec self-review uses subagent dispatch"
```

## Integration Test

```bash
# Start opencode with test session
mkdir -p .tmp/brainstorm-test && cd .tmp/brainstorm-test

# Test prompt that should trigger brainstorming
echo "Test: Design a user notification system"

# Verify workflow:
# 1. Context exploration announced
# 2. Questions asked one at a time
# 3. 2-3 approaches presented with recommendation
# 4. Design sections reviewed with user
# 5. Plan file created

cd ~ && rm -rf .tmp/brainstorm-test
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `brainstorming/VALIDATE.prompt.md` and report any issues found with the brainstorming skill.

## Test Scenarios

### Scenario 1: Bypass Attempt
**Input**: "Just add a login button, it's obvious"
**Expected**: Skill detects bypass attempt, still runs full brainstorming workflow
**Red Flag**: "it's obvious", "no need to overthink"

### Scenario 2: Missing Exploration
**Input**: "Help me add caching to the API"
**Expected**: 
- Context exploration phase runs (check files, patterns, existing cache implementations)
- Questions asked before proposing approaches
- NOT jumping straight to implementation

### Scenario 3: Multiple Approaches
**Input**: "We need to handle file uploads"
**Expected**:
- At least 2-3 approaches presented with trade-offs
- Recommendation provided with reasoning
- User approval sought before design finalization

### Scenario 4: Premature Implementation
**Input**: "Actually, I already know what to do - let me just write the code"
**Expected**:
- Skill stops implementation attempt
- Redirects back to brainstorming workflow
- Explains why design approval is required first

### Scenario 5: Simple Project Workflow
**Input**: "Just a simple hello world endpoint"
**Expected**:
- Still follows brainstorming workflow (condensed)
- Presents simple design and gets approval
- No implementation until approved

### Scenario 6: Todo Tracking
**Input**: "Plan adding search functionality"
**Expected**:
- TODOs created for: context explore, questions, approaches, design review, plan doc
- TODOs completed in order
- Implementation plan created at end

### Scenario 7: Clarifying Questions
**Input**: "Build a dashboard"
**Expected**:
- Asks one question at a time
- Covers: purpose, constraints, success criteria, existing patterns
- Multiple choice questions preferred

### Scenario 8: Design Review Feedback
**Input**: "Actually, I prefer option 2 from your proposal"
**Expected**:
- Incorporates feedback into design
- Updates approach accordingly
- Gets final approval before proceeding

### Scenario 9: YAGNI Enforcement
**Input**: "And while we're at it, add admin panel, real-time sync, and export to PDF"
**Expected**:
- Identifies scope creep
- Proposes minimal viable approach
- Requests user approval on reduced scope

### Scenario 10: Plan Document Creation
**Input**: Any brainstorming session that reaches approval
**Expected**:
- Plan file created (prefix-something-plan.md)
- Follows existing conventions
- Not committed to git (session artifact only)