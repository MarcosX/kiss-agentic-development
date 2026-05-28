# TDD for Skills

Skill development follows the same RED-GREEN-REFACTOR cycle as test-driven development. The test is "will an agent follow these instructions correctly?" and the production code is the skill document itself.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills. If you wrote a skill before testing baseline behavior, delete it and restart. If you edited a skill without testing what changed, same violation.

**No exceptions:** Not for "simple additions", not for "just a section", not for "documentation updates."

## RED phase: Establish baseline

Before writing a skill, you need to know what agents do without it.

### Create test prompts

Write 2-3 realistic prompts the skill should handle. These should be things a real user would actually type — include context, file references, casual language.

### Run baseline

Execute the prompts WITHOUT the skill loaded. Use a fresh subagent per prompt so each run is independent. Document:

- What did the agent do? (step by step)
- What did it get wrong or miss?
- What rationalizations did it use?
- Which pressures caused it to violate rules?

### Identify patterns

Look for recurring failure modes. These become the core of your skill. If agents consistently skip validation steps, your skill needs to emphasize validation. If they use the wrong library, your skill needs to specify the right one.

## GREEN phase: Write the skill

Write a SKILL.md that addresses the specific failures identified in baseline testing. Follow the skill authoring guidelines in AGENTS.md.

### Test with skill

Run the same prompts WITH the skill loaded. The agent should now follow the intended behavior. If it doesn't, iterate.

## REFACTOR phase: Close loopholes

Agents are smart and will find workarounds. When they do:

### Close every loophole explicitly

Don't just state the rule — forbid specific workarounds:

```
Write code before test? Delete it. Start over.
```

### Address "spirit vs letter" arguments

Add a foundational principle early in the skill:

```
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Build a rationalization table

Capture every excuse agents make during testing:

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Testing takes seconds. |
| "I'll test after" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Academic review is enough" | Reading ≠ using. Test application scenarios. |
| "The skill is obvious" | Clear to you ≠ clear to other agents. Test it. |
| "No time to test" | Deploying untested skill wastes more time fixing it later. |

### Create a red flags list

Make it easy for agents to self-check when rationalizing:

```
## Red flags — STOP and start over

- [behavior that indicates the rule is being violated]
- [another common rationalization symptom]
- [another workaround agents try]
```

### Re-test until bulletproof

After each fix, re-run all test prompts. If the agent finds a new workaround, add it to the rationalization table and the red flags list.

## Subagent patterns for testing

When testing skills, dispatch fresh subagents for each test case. Never use your own session — you have too much context and will naturally follow instructions you wrote.

For each test prompt, run two subagents:
1. **Without skill** (baseline) — documents what goes wrong
2. **With skill** — verifies the fix

Compare both outputs side by side. The with-skill run should clearly improve over baseline.
