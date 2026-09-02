---
name: proof-review-agent
description: prompt to dispatch subagent to verify runtime proof after implementation
---

Use the following template to dispatch a subagent to verify that a task's Proof step produces evidence matching the expected outcome.

Ensure information is pasted in the prompt, do not reference files:

```markdown
You are verifying the runtime proof for "Task N: [task title]" to confirm the
feature actually runs and produces the expected outcome.

# Original task spec:

[FULL TEXT of task from plan, including its Proof step with expected outcome]

# What was claimed:

[FULL TEXT of the implementer's proof manifest]

# CRITICAL: Do Not Trust the Report

The implementer claims the feature works. Their proof may be missing, staged,
mislabeled, or optimistic. You MUST verify the runtime behavior yourself.

**DO NOT:**
- Take their word that the feature runs
- Accept an artifact that does not match its stated reproduction command
- Assume a captured log or response demonstrates the claimed behavior
- Accept test output, git diff, type-check, or lint as runtime proof — these prove code exists, not that it works

**DO:**
- Run the reproduction command yourself against the current codebase state
- Check the app actually starts and stays alive (no crash at startup)
- Compare each artifact against the stated expected outcome
- Confirm the reproduction command is plausible and was actually run

If the task has no Proof step (pure static change), report "No proof required".

# Your goal

Run the reproduction command and verify:

**Execution:** does the slice actually start and run, or does it crash or hang?

**Outcome match:** does each artifact show what the expected outcome requires
(e.g. response contains the line items, DB row exists, error logged with context)?

**Coverage limit:** the Proof declares which dependencies are real vs. stubbed.
If a dependency is stubbed or external, is the evidence scoped to the behavior
the slice owns rather than silently implying full integration?

**Proof validity:** reject any evidence that is not runtime observation:

REJECT (never valid as proof):
- `git diff` or commit content — shows code changes, not behavior
- Test framework output (pass/fail) — shows tests pass, not app behaves
- Type checker or linter output — shows code is valid, not runtime correct
- Agent-written narrative ("the feature should work because...")
- Screenshots of code editors or terminal showing code
- Any artifact not produced by actually running the application

ACCEPT (valid runtime proof):
- Raw application logs from a running instance
- HTTP request/response pairs from actual calls to a running server
- DB query results (SELECT output) after operations on a running database
- Screenshots of the running application UI (not code editors)
- Process stdout/stderr from actual execution
- File system state (ls, cat of output files) after execution

**Report:**
- ✅ Proof confirmed: artifacts match expected outcome, feature runs
- ❌ Proof failed: describe the discrepancy (artifact missing, app crashes,
  output differs from expected outcome) with what the evidence actually shows
- ⚠️ Partial: feature runs but some expected outcomes aren't demonstrated
```
