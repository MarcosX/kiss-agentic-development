---
name: brainstorming
description: Use when exploring ideas, diagnosing behavior, discussing approaches, or before any creative work. Covers analysis, design exploration, and requirements discovery.
---

Help turn ideas into complete design and specs through collaborative conversation.

Start by understanding the current context, then come up with questions and ask them one at a time.

Once you are confident in your understanding, present the design to request feedback and approval.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

# RULE

**No task is too simple**: Simple projects lead to unchecked assumptions, which leads to wasted work

**Simple design for simple projects**: If the project is straightforward, present a simple design and get approval first

**Brainstorming workflow**: You MUST create tasks for the following items and complete them:

1. **Explore context** - check for files, documents, CONTEXT.md/ADRs, references, recent commits
2. **Stress-test understanding** - one question at a time. Interview relentlessly, walk decision tree branches, sharpen domain language against existing glossary and code. When domain terms need capturing, use `references/CONTEXT-FORMAT.md`. When a hard decision emerges, use `references/ADR-FORMAT.md`.
3. **Propose 2-3 approaches** - including trade-offs along with your recommendation for the user
4. **Present the design** - use sections, based on the complexity, and get user approval after each of them
5. **Write design doc** - when writing the design doc, use `references/prd-template.md` as the structure. Write to a file, then:
   1. **Spec self-review**: scan for placeholders (TBD/TODO), contradictions, ambiguity, scope bloat. Fix inline.
   2. **User review gate**: ask the user to review the written spec before proceeding. Wait for approval or changes.
   3. **Create implementation plan**: only after user approves the spec, invoke `writing-plans` to create the plan.

**Always end with creating implementation plan**: Ensure an implementation plan is created based on the proposed design

**Terminal state**: `writing-plans` is the ONLY skill to invoke after brainstorming. Do NOT invoke any implementation skill (e.g. `executing-plans`) from within this skill.

# The Process

## Explore context

- Check out the current state (files, docs, CONTEXT.md/ADRs, references, recent commits)
- Note existing domain language in CONTEXT.md to catch conflicts later
- Understand existing recommendations, conventions and patterns

## Stress-test understanding

Interview relentlessly about every aspect until shared understanding is reached. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Prefer multiple choice.

During this phase, also sharpen domain language:
- When the user uses a term that conflicts with CONTEXT.md or code, call it out immediately
- Propose precise canonical terms for vague/overloaded ones
- Discuss concrete scenarios that probe edge cases and force precision about boundaries
- Cross-reference claims against code — when the user states how something works, check if the code agrees
- When domain terms need capturing, use `references/CONTEXT-FORMAT.md`
- When a hard decision emerges, use `references/ADR-FORMAT.md` to check if an ADR is warranted

**Assess scope first**: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately. Help the user decompose into sub-projects before diving into details. Each sub-project gets its own brainstorm → spec → plan → implementation cycle.

## Explore approaches

- Come up with 2 or 3 different approaches and their trade-offs
- Present all options with your recommendation and reasoning
- Always lead with your recommendation

## Present the design

- Scale design sections based on their complexity, keep it straightforward but add nuances when needed
- Check with the user after presenting each section to ensure the design is in the right path
- Ask clarifying questions and go back if something doesn't make sense

## Design for isolation and clarity

Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently. For each unit, be able to answer: what does it do, how do you use it, and what does it depend on? Smaller, well-bounded units are easier to implement reliably — agents reason better about code they can hold in context at once, and edits are more reliable when files are focused. When a file grows large, that's often a signal it's doing too much.

## Working in existing codebases

Explore the current structure before proposing changes. Follow existing patterns. Where existing code has problems that affect the work (e.g., a file grown too large, unclear boundaries), include targeted improvements as part of the design. Do not propose unrelated refactoring — stay focused on what serves the current goal.

## Write documentation

- When writing the design doc, use `references/prd-template.md` as the structure — includes problem statement, user stories, implementation decisions, testing decisions (seam-first), and out of scope
- Adopt the anti-stale principle — avoid file paths and code snippets in the output. Exception: prototype-produced decision-rich snippets (state machines, schemas, type shapes) can be inlined
- Use `writing-plans` to turn the design into an implementation plan
- Do NOT commit design documents or plans to git (they are session artifacts only)

# Guidelines

- **Do not overwhelm the user**: always ask one question at a time, present choices and recommendations
- **YAGNI**: Unnecessary scope should be removed from all design proposals
- **Always explore alternatives**: Always propose 2-3 approaches before moving on
- **Incremental feedback**: Request approval as part of the process to ensure understanding
- **When in doubt, ask**: Go back and ask clarifying questions if something doesn't make sense - unchecked assumptions are not tolerated
