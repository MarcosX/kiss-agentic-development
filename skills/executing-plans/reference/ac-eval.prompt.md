---
name: ac-eval-agent
description: prompt to dispatch subagent to evaluate an acceptance criterion against the running application
---

Use the following template to dispatch a subagent to evaluate an AC.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are evaluating "AC-N: [AC title]" to confirm the feature works as specified.

# Acceptance criterion:

[FULL TEXT of the AC from the plan]

# Eval procedure:

[FULL TEXT of the eval procedure from the AC Evals section of the plan]

# Expected evidence:

[FULL TEXT of the expected evidence from the plan]

# Your goal

Follow the eval procedure exactly. Stand up what is needed (app, stubs, seed data),
exercise the behavior, and capture runtime evidence.

**DO NOT:**
- Skip steps in the procedure
- Substitute test output, git diff, type-check, or lint for runtime evidence
- Infer behavior from code — you must observe it from the running system
- Accept "it should work" — either the evidence shows it or it doesn't

**DO:**
- Follow each step in the procedure precisely
- Capture raw output from each step (HTTP responses, logs, screenshots, query results)
- Compare captured evidence against the expected evidence
- Report exactly what you observed, not what you expected to observe

**Report:**
- ✅ Eval passed: evidence matches expected outcome, AC is validated
- ❌ Eval failed: describe the discrepancy — what the evidence actually shows
  vs. what was expected, with the raw output attached
- ⚠️ Partial: some evidence matches, some doesn't — list what passed and what failed
```
