# Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether an agent invokes a skill. A well-written description means the skill triggers when needed and stays quiet when not.

## Trigger eval queries

Create a set of eval queries — a mix of should-trigger and should-not-trigger cases — to test whether the description correctly dispatches the skill.

### Query structure

```json
[
  {"query": "realistic user prompt here", "should_trigger": true},
  {"query": "another user prompt", "should_trigger": false}
]
```

- **Should-trigger queries (8-10)**: Cover different phrasings, casual and formal. Include cases where the user doesn't name the skill explicitly but clearly needs it. Include edge cases and uncommon use cases.
- **Should-not-trigger queries (8-10)**: Focus on near-misses — queries that share keywords with the skill but need something different. Avoid obvious negatives (e.g., "write fibonacci" for a PDF skill is too easy — it doesn't test anything).

### Realistic queries

Queries should be substantive enough that an agent would actually benefit from consulting the skill. Include file paths, personal context, company names, casual speech, typos.

**Bad:** "Format this data", "Extract text from PDF"
**Good:** "ok so my boss just sent me this xlsx file (its in my downloads, called 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage"

## Optimization criteria

A good description:

- Starts with "Use when..." (trigger conditions)
- Uses third person throughout
- Includes keywords the agent would search for (error messages, symptoms, tool names)
- Never summarizes the skill's process or workflow
- Uses concrete triggers, not abstract concepts
- Describes the problem, not the language-specific symptoms
- Keeps under 100 words if possible

## CSO (Claude Search Optimization)

Agents discover skills by matching descriptions against task context. Optimize for this:

### Keywords

Include words the agent would naturally search for:
- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Tool names: Actual commands, library names, file types

### Active naming

Name skills with active, verb-first phrasing:
- `creating-skills` not `skill-creation`
- `condition-based-waiting` not `async-test-helpers`
- `root-cause-tracing` not `debugging-techniques`
