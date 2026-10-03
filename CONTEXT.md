# Skill Development

The vocabulary for authoring, measuring, and governing agent skills in this repo. This context
exists because the terms below are routinely conflated, and conflating them is what makes eval
results and skill-engineering decisions misleading.

Avoid lists are scoped to this context. The repo also uses compliance (conforming to a schema) in a
distinct, legitimate sense — that homonym is noted in its entry.

## Language

### What an eval measures

**Skill value-add**:
The difference in outcome between an agent holding a skill and an agent without it. It names the
question the maintainer asks, not a figure the tooling reports. An `old_skill` baseline compares a
skill to its own previous version and so returns change-impact, not this number; only the
`without_skill` comparator measures value-add directly.
_Avoid_: skill value, impact, skill effectiveness, skill works, conformance

**Conformance**:
Whether an agent followed a skill's stated procedure. Distinct from value-add: an agent can
conform perfectly and change nothing, or skip the procedure and reach the same outcome.
_Avoid_: compliance, adherence, following the skill (the eval sense; schema conformance is a
different homonym)

### Discipline and governance

**Hook vs rule**:
A hook is a discipline presented as a reframe that aligns with the agent's own incentives —
adopted, not obeyed. A rule is an enforced directive (HARD-GATE, red flag, MUST). Open-field
skills may run on hooks; narrow-bridge skills keep enforced rules.
_Avoid_: guideline, principle, best practice (used loosely for both)

**Open-field vs narrow-bridge**:
Whether a skill's discipline is a single agent's judgment (open-field, hook-eligible) or a
contract a downstream actor depends on (narrow-bridge, enforced rules).
_Avoid_: strict vs lenient, hard vs soft

**Decoy**:
An element in a fixture or prompt that makes the wrong path the easy read, so a naive agent
visibly fails. The general pattern behind the debugging red herring.
_Avoid_: red herring (one specific decoy for debugging misdirection)

**skill-creator**:
The external dev-only skill that drives skill validation, evals, and grading (scripts, grader
agent, review viewer). Not shipped; install separately.
Not shipped; install it separately before running evals.
_Avoid_: the eval tooling, "the skill" (ambiguous with domain skills)

**Shipped artifact**:
Skills (their SKILL.md, references, evals, and scripts) — what version tags track and consumers
install. Dev-only tooling (.opencode/, .agents/, plans, workspaces) is never shipped and does
not trigger version bumps.
_Avoid_: tooling, the framework (reserved for the whole repo)