# Challenge Findings

The review subagent sees only the diff and lacks codebase context. Its findings can be mis-scoped: genuine issues downplayed or dismissed, noise inflated. The main session holds the codebase context, so it challenges every finding before anything is presented.

## Process

For each finding, in order:

1. **Verify** — Read the actual code. Confirm the finding is real: the flagged path exists, is reachable, and is genuinely a problem in this codebase. Do not rely on the diff alone.
2. **Decide** — Severity-scaled default:
   - Critical and Required: keep unless concrete codebase evidence refutes them. Over-dismissal is the failure mode this step prevents.
   - Nit, Optional, FYI: keep only when verified or clearly valuable. These face harder scrutiny.
3. **Recalibrate** — Adjust severity to codebase reality. Promote issues the subagent could not see: callers in other files, failing tests, documented behavior the change breaks. Demote inflated ones.
4. **Merge** — Collapse duplicate findings to one root cause. One issue, one finding.

## Rules

- Dismissal requires explicit codebase evidence, never "seems fine". Record the reason.
- When evidence is ambiguous, lean toward the higher severity for Critical and Required findings.
- Apply the disagreement ladder from SKILL.md: technical facts override opinions, style guides are absolute on style, design is judged on engineering principles.
- The surviving findings are the final output. Presentation format is unchanged: each finding keeps its axis and severity.
