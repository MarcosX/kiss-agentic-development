---
name: spec-review-agent
description: prompt to dispatch subagent to check spec compliance after implementation
---

Use the following template to dispatch a subagent to review specification against implementation.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are reviewing the implementation for "Task N: [task title]" to ensure it matches what was specified

# Original task spec:

[FULL TEXT of task from plan]

# What was implemented:

[FULL TEXT of execution report]

# Your goal

**Do not blindly trust the report**: everything MUST be verified independently, the report is optimistic and may be inaccurate. Read the code implemented and verify:

**Missing requirements:**

- Did they implement everything that was requested?
- Did they claim something works but didn't actually implement it?

**Extra/unneeded work:**

- Did they build things that weren't requested?
- Did they over-engineer or add unnecessary features?

**Misunderstandings:**

- Did they interpret requirements differently than intended?
- Did they solve the wrong problem?
- Did they implement the right feature but wrong way?

**Report:**

- When the implementation matches the spec: ✅ Spec compliant
- When issues are found: ❌ Issues found: [list what is missing/extra, with task, file an line references]

# Guidelines to ALWAYS keep in context

- Review the entire code, do not take their word for what was implemented
- Compare implementation to requirements, do not trust what they claim to have completed
- Check for extra implementation that was not mentioned in the report
```
