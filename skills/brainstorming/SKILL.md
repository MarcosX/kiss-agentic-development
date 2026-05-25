---
name: brainstorming
description: MUST be used for ideation prompts or creative work. Use this skill to explore intent for modifying or adding new features, components, or functionality. Load this skill before checking or exploring the current project.
---

Help turn ideas into complete design and specs through collaborative conversation.

Start by understanding the current context, then come up with questions and ask them one at a time.

Once you are confident in your understanding, present the design to request feedback and approval.

<IMPORTANT>
No implementation skill should be invoked before presenting the design and receiving approval! Do not write any code or take any action until user has approved it, regardless of how simple the idea might be.
</IMPORTANT>

# RULE

**No task is too simple**: Simple projects lead to unchecked assumptions, which leads to wasted work

**Simple design for simple projects**: If the project is straightforward, present a simple design and get approval first

**Brainstorming workflow**: You MUST create tasks for the following items and complete them:

1. **Explore context** - check for files, documents, references, recent commits
2. **Ask clarifying questions** - one question at a time to understand purpose, goals, constraints, and success criteria
3. **Propose 2-3 approaches** - including trade-offs along with your recommendation for the user
4. **Present the design** - use sections, based on the complexity, and get user approval after each of them
5. **Write design doc** - create a plan (using `writing-plans` if available)

**Always end with creating implementation plan**: Ensure an implementation plan is created based on the proposed design

# The Process

## Explore context

- Check out the current state (files, docs, references, recent commit)
- Understand existing recommendations, conventions and patterns

## Explore understanding

- Ask questions, one at a time, to refine the idea
- Prefer multiple choice questions over open-ended
- Ensure you understand purpose, constraints and success criteria

## Explore approaches

- Come up with 2 or 3 different approaches and their trade-offs
- Present all options with your recommendation and reasoning
- Always lead with your recommendation

## Present the design

- Scale design sections based on their complexity, keep it straightforward but add nuances when needed
- Check with the user after presenting each section to ensure the design is in the right path
- Ask clarifying questions and go back if something doesn't make sense

## Write documentation

- Use `writing-plans` to turn the design into an implementation plan
- Do NOT commit design documents or plans to git (they are session artifacts only)

# Guidelines

- **Do not overwhelm the user**: always ask one question at a time, present choices and recommendations
- **YAGNI**: Unnecessary scope should be removed from all design proposals
- **Always explore alternatives**: Always propose 2-3 approaches before moving on
- **Incremental feedback**: Request approval as part of the process to ensure understanding
- **When in doubt, ask**: Go back and ask clarifying questions if something doesn't make sense - unchecked assumptions are not tolerated
