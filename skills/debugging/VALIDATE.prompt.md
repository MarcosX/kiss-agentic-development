# Debugging Skill Validation

## Content Checks

```bash
grep -q "^---" skills/debugging/SKILL.md && echo "✓ Front matter present"
grep -q "^name: debugging" skills/debugging/SKILL.md && echo "✓ Name defined"
grep -q "^description:" skills/debugging/SKILL.md && echo "✓ Description present"
grep -q "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST" skills/debugging/SKILL.md && echo "✓ Iron Law present"
grep -q "HARD-GATE" skills/debugging/SKILL.md && echo "✓ Hard gate enforces root cause first"
grep -q "Phase 1:" skills/debugging/SKILL.md && echo "✓ Phase 1 documented"
grep -q "Phase 2:" skills/debugging/SKILL.md && echo "✓ Phase 2 documented"
grep -q "Phase 3:" skills/debugging/SKILL.md && echo "✓ Phase 3 documented"
grep -q "Phase 4:" skills/debugging/SKILL.md && echo "✓ Phase 4 documented"
grep -q "3-Fix Rule" skills/debugging/SKILL.md && echo "✓ 3-fix architectural rule present"
grep -q "Multi-Component" skills/debugging/SKILL.md && echo "✓ Multi-component tracing covered"
grep -q "single hypothesis" skills/debugging/SKILL.md && echo "✓ Scientific method covered"
grep -q "Red Flags" skills/debugging/SKILL.md && echo "✓ Red flags section present"
grep -q "Verification Checklist" skills/debugging/SKILL.md && echo "✓ Verification checklist present"
grep -q "practicing-tdd" skills/debugging/SKILL.md && echo "✓ Cross-references practicing-tdd"
grep -q "brainstorming" skills/debugging/SKILL.md && echo "✓ Cross-references brainstorming"
grep -q "reference/debug-report.md" skills/debugging/SKILL.md && echo "✓ Links to debug report reference"
```

## Reference File Check

```bash
test -f skills/debugging/reference/debug-report.md && echo "✓ Debug report template exists"
grep -q "Root Cause" skills/debugging/reference/debug-report.md && echo "✓ Root cause section in template"
grep -q "Prevention" skills/debugging/reference/debug-report.md && echo "✓ Prevention section in template"
```

## Integration Test

```bash
echo "✓ Debugging skill validation complete"
```

---

**Prompt for AI Assistants:**

> Run the validation commands in `debugging/VALIDATE.prompt.md` and report any issues found with the debugging skill.

## Test Scenarios

### Scenario 1: Fix Proposed Without Investigation
**Input**: "The login is broken, let me just check the token expiration"
**Expected**: Iron Law blocks this — root cause investigation required first
**Red Flag**: proposing fix before investigation, "it's probably X"

### Scenario 2: Emergency Pressure
**Input**: "Production is down, no time for process, just try something"
**Expected**: Skill triggers, notes systematic debugging is faster than thrashing
**Red Flag**: "no time for process", "just try something"

### Scenario 3: Multiple Simultaneous Fixes
**Input**: "Let me update the config, fix the timeout, and add logging all at once"
**Expected**: Phase 3 blocks this — one variable at a time
**Red Flag**: multiple fixes at once, cannot isolate what worked

### Scenario 4: 3 Failed Fixes
**Input**: After 3 attempts, "Let me try one more thing"
**Expected**: 3-Fix Rule stops the cycle, questions architecture
**Red Flag**: 3+ fixes without architectural discussion

### Scenario 5: Symptom Fix
**Input**: "The error goes away if I retry 3 times, let me just add a retry loop"
**Expected**: Skill requires root cause of the failure, not masking it
**Red Flag**: symptom fix, masking instead of solving

### Scenario 6: Skipping the Test
**Input**: "The fix is obvious, no need to write a reproduction test"
**Expected**: Phase 4 requires failing test first via practicing-tdd
**Red Flag**: skipping test, "obvious fix"
