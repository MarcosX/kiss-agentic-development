---
name: explore-context
description: Prompt template for dispatching a subagent to explore codebase context during brainstorming
---

Paste into the subagent prompt, filling in bracketed sections:

You are exploring a codebase to surface existing context relevant to a project.

# Project domain/goal:

[Brief description of what the user is building or designing]

# Codebase location

[Repository path]

Only explore files relevant to the domain/goal above. Skip node_modules, .git, build artifacts.

# What to explore

1. **CONTEXT.md / CONTEXT-MAP.md** — read any domain language definitions, check for term conflicts
2. **ADRs** (docs/adr/) — read last 5, note architectural decisions constraining the project
3. **Recent commits** — last 10, summarize changes relevant to the domain
4. **Relevant file structure** — which directories/files are most relevant
5. **Existing patterns** — conventions, architecture, code organization to preserve
6. **References/docs** — any other documentation informing the design

# Edge cases

- **Empty/new repo**: If nothing exists or is relevant, say so clearly.
- **Giant codebase**: Focus on the 3-5 most relevant files/directories, then stop.
- **No CONTEXT.md or ADRs**: Report that none were found.

# Report format

Return a structured report:

## Domain Language
Terms found relating to the project. Note conflicts with the project's language.

## Relevant Changes
Summary of recent commits touching related areas.

## File Structure
Key files/directories relevant to the domain.

## Patterns
Existing conventions, architecture decisions, or ADRs that constrain or inform the design.

## References
Any docs, specs, or templates discovered.

If nothing relevant was found, report "Nothing relevant found" per section.
