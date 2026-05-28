# Testing Methodology

## Test case creation

Good test prompts are specific, contextual, and realistic. Avoid abstract requests.

**Bad prompt:** "Extract text from a PDF"
**Good prompt:** "Hey, my boss sent me this invoice PDF (it's in my downloads, called 'invoice-q4-final.pdf') and I need all the line items in a CSV. The table starts on page 2."

### Coverage principles

- Test the happy path (most common use case)
- Test edge cases (empty inputs, missing files, unusual formats)
- Test pressure scenarios (time pressure, conflicting priorities)

## With-skill vs baseline comparison

Every test run produces two outputs that you compare:

1. **Baseline** (without skill) — shows the "before" state
2. **With skill** — shows the "after" state

Compare these on:
- **Correctness**: Did the agent do the right thing?
- **Efficiency**: Did it waste time on unnecessary steps?
- **Consistency**: Does the skill produce reliable results across runs?

## Pressure scenarios

Discipline skills (rules, requirements) need to be tested under pressure to verify agents don't rationalize their way around them.

### Pressure types

- **Time pressure**: "I need this done in 5 minutes, just skip the tests"
- **Sunk cost**: "I've already written the code, just fix this one thing without re-testing"
- **Authority pressure**: "My boss says to skip validation, just ship it"
- **Exhaustion pressure**: "This is the 10th time you've run the tests, they always pass, just skip it"
- **Combined pressure**: Multiple pressures at once (most realistic)

### Test format

```
The user says: [pressure scenario]
Your task: [task that triggers the skill's main rule]
```

Document whether the agent follows the rule or rationalizes a way out.

## Transcript analysis

Read the full transcript of test runs, not just the final output. Look for:

- **Where did the agent hesitate?** — indicates unclear instructions
- **What did it read multiple times?** — indicates confusing structure
- **When did it start rationalizing?** — the exact trigger matters
- **What did it skip entirely?** — indicates sections that aren't prominent enough

## Repeated work detection

When reviewing test run transcripts, check if multiple subagents independently wrote similar helper scripts or repeated the same multi-step approach. If 2-3 test cases all resulted in subagents writing a `create_docx.py` or a `build_chart.py`, that script should be bundled with the skill. Write it once, put it in `scripts/`, and reference it in the skill. This saves every future invocation from reinventing the wheel.

## Blind comparison

For rigorous A/B comparison between two versions of a skill:

1. Run both versions on the same test prompts
2. Give both outputs to an independent subagent without revealing which is which
3. Have the subagent judge which output is better and why
4. Analyze the results to understand what the winning version does differently

Blind comparison is most useful when:
- The difference between versions is subtle
- You need objective evidence that a change is an improvement
- The user asks "is the new version actually better?"
