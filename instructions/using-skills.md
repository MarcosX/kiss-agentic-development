# Using Skills

<HARD-GATE>
Before responding to any user message, check the available skills. If any skill applies, you MUST load it and follow it. Responding without loading an applicable skill — or loading it and then not following it — is a violation. Stop and do it properly.
</HARD-GATE>

## Every response

Begin every response with exactly one line, then continue:

- "Using [skill] to [goal]." — when a skill applies (load and follow it)
- "No applicable skill." — only when none does

A response without this line is non-compliant; rewrite it before sending.

## When to load

Load a skill whenever there is any chance it applies, not only when you're sure. The signal scan is the floor, not the ceiling.

- bug, error, crash, fail, unexpected → `debugging`
- idea, approach, explore, design → `brainstorming`
- plan, implement, build, add, feature → `writing-plans`

Process skills first (`brainstorming`, `debugging`), implementation skills after.

## After loading

1. Restate the skill's key rules in your own words in that response. If you can't, re-read it.
2. Create TODOs for each step the skill prescribes.
3. Follow the skill's workflow. User instructions define WHAT; the skill defines HOW.
4. Before sending, check your work against the skill's gates and checklists. If a step is missing, do it — don't ship around it.

## Rationalizing

These thoughts are how agents skip skills. If you catch yourself thinking one, stop and load the skill:

- "This is just a simple question" / "I'll quickly check files"
- "Just a high-level answer is fine" / "Keep it short" / "Quick question"
- "Let me explore the codebase first" / "Let me gather information first"
- "I know what that means" / "This doesn't need a skill" / "The skill is overkill"
- "I'll just do this thing first" / "Let me investigate this" / "Let me understand the problem first"
- "I already know what skill I need"
