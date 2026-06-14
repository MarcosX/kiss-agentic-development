---
name: brainstorming
description: Use when exploring ideas, diagnosing behavior, discussing approaches, or before any creative work. Covers analysis, design exploration, and requirements discovery.
---

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Workflow

Create TODOs to track each step. Complete them in order.

1. **Explore context** — dispatch an explore subagent using `references/explore-context.prompt.md`. Paste the project domain/goal into the template. The subagent returns structured context covering domain language, relevant changes, file structure, patterns, and references. Note domain language conflicts and relevant patterns. Targeted file reads are still fine for specific questions the report raises.

2. **Stress-test understanding** — one question at a time. Provide your recommended answer with each question. Prefer multiple choice. Interview relentlessly, walk decision tree branches, sharpen domain language against existing context and code.

   **Load the glossary first.** Read `CONTEXT.md` if it exists. Existing terms are constraints to question against — challenge conflicts immediately, sharpen vague language, probe edge cases with concrete scenarios.

   **Cross-reference all three** — code, conversation, glossary. Surface every contradiction between them. When a term is resolved, update `CONTEXT.md` inline (don't batch) using `references/CONTEXT-FORMAT.md`. When resolving domain terminology, see `references/glossary-interaction.md`.

   **Assess scope first**: if the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this. Help the user decompose into sub-projects before diving into details. Each sub-project gets its own brainstorm → spec → plan → implementation cycle.

3. **Propose 2-3 approaches** — present all options with trade-offs and your recommendation with reasoning. Always lead with your recommendation. Apply YAGNI: remove scope not justified by requirements.

4. **Present the design** — scale sections based on complexity. Check with the user after each section. Ask clarifying questions and go back if something does not make sense.

   Break the system into smaller units with one clear purpose, well-defined interfaces, and independent testability. Smaller units are easier to implement reliably — agents reason better about code they can hold in context. When a file grows large, it is often doing too much.

   Explore the existing structure before proposing changes. Follow existing patterns. Where existing code has problems that affect the work, include targeted improvements. Do not propose unrelated refactoring.

5. **Write PRD** — use `references/prd-template.md` (problem statement, user stories, implementation decisions, testing decisions, out of scope). Adopt the anti-stale principle — avoid file paths and code snippets. Exception: prototype-produced decision-rich snippets (state machines, schemas, type shapes) can be inlined. Do NOT commit PRD documents to git.

   After writing:
   1. **Spec self-review**: dispatch a subagent to scan for placeholders (TBD/TODO), contradictions, ambiguity, and scope bloat. Apply fixes in the main session. Skip if spec is under 50 lines.
   2. **User review gate**: ask the user to review and approve before proceeding.
   3. **Create implementation plan**: after approval, invoke `writing-plans`.

**Terminal state**: `writing-plans` is the ONLY skill to invoke after brainstorming. Do NOT invoke any implementation skill (e.g. `executing-plans`) from within this skill.
