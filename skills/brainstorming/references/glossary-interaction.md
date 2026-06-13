# Glossary Interaction

How to interact with CONTEXT.md — the project's domain glossary — during a brainstorming session.

## Load before questioning

Before step 2 questioning begins, read `CONTEXT.md` if it exists. Internalize every term. These are constraints you challenge against, not documentation you write to. If no CONTEXT.md exists yet, proceed — creation is lazy (first resolved term).

## Challenge against the glossary

When the user introduces or uses a term:

- If it matches an existing entry, confirm alignment
- If it conflicts with an existing entry, call it out: "Your glossary defines X as Y, but you seem to mean Z — which is it?"
- If it is vague or overloaded, propose a precise canonical term with an `_Avoid_` list
- Push for concrete scenarios that force boundaries between terms

## Cross-reference all three directions

Maintain continuous awareness across three sources:

| Direction | Question to ask |
|-----------|----------------|
| Conversation ↔ Glossary | Does the user's language match established terms? |
| Conversation ↔ Code | Does the stated behavior match what the code does? |
| Glossary ↔ Code | Does the code use terms consistently with the glossary? |

Surface every contradiction immediately. Let the user resolve — do not assume which source is correct.

## Update inline, do not batch

When a term is resolved, update `CONTEXT.md` immediately. Use `references/CONTEXT-FORMAT.md` for structure. Do not batch updates — each resolution is a separate edit. This keeps the glossary precise and prevents unresolved terms from being forgotten.

## Purity rules

CONTEXT.md is a glossary and nothing else:

- **Domain terms only.** General programming concepts (timeout, cache, retry) do not belong.
- **No implementation details.** Do not describe how something works — define what it IS.
- **No specs or ADRs.** Implementation decisions go in `docs/adr/`. Behavioral specs go in the PRD.
- **No scratch pad.** Do not use CONTEXT.md for notes, open questions, or temporary labels.

## Lazy creation

Create CONTEXT.md only when the first term is resolved. Do not pre-create it. If no domain-specific terminology emerges during the session, no file is needed.

## Edge cases

- **Empty glossary (no CONTEXT.md)**: Proceed normally. Create when first term resolves.
- **Stale glossary**: Terms may be outdated. If code contradicts the glossary, surface it as a conflict to resolve — do not silently update the glossary.
- **Multiple contexts**: If CONTEXT-MAP.md exists, read it to find the relevant CONTEXT.md. If the topic spans contexts, note term differences between them.
- **Repo without domain language**: Not every project needs a glossary. If all terms are general programming concepts, skip creation entirely.
