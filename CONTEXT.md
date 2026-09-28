# Skill Development

The vocabulary for authoring, measuring, and governing agent skills in this repo. This context
exists because the terms below are routinely conflated, and conflating them is what makes eval
results and skill-engineering decisions misleading.

Avoid lists are scoped to this context. The repo also uses evidence (a claim's recorded support
in grading.json), compliance (conforming to a schema), and re-running (running evals again
operationally) in distinct, legitimate senses — those homonyms are noted in their entries.

## Language

### What an eval measures

**Skill value-add**:
The difference in outcome between an agent holding a skill and an agent without it.
_Avoid_: skill value, impact, skill effectiveness, skill works, conformance

**Conformance**:
Whether an agent followed a skill's stated procedure. Distinct from value-add: an agent can
conform perfectly and change nothing, or skip the procedure and reach the same outcome.
_Avoid_: compliance, adherence, following the skill (the eval sense; schema conformance is a
different homonym)

**Discriminating expectation**:
An expectation where the with-skill and without-skill configurations reach different verdicts.
An expectation that passes in both configurations measures nothing about the skill.
_Avoid_: useful, valuable, good expectation

**Saturated eval**:
An eval where every expectation passes in both configurations, so its pass rate cannot separate
them. Usually means the scenario is too easy or the prompt supplies the answer.
_Avoid_: easy eval, passing eval, green eval

**Strengthened round**:
The adversarial re-run required before a skill may be removed for showing no value-add: the
fixture holds a real defect, the prompt carries no scripted procedure, a decoy makes the naive
path visibly fail, and mechanism expectations were re-plumbed to outcomes.
_Avoid_: retry, rerun, second attempt (when naming this procedure; re-running evals
operationally is a different sense)

### What an expectation grades

**Expectation**:
The graded unit in an eval: one leaf-level, falsifiable observable defined in evals.json. A
grader returns a verdict per expectation.
_Avoid_: assertion, check

**Claim**:
A grader-recorded assertion in grading.json, typed (factual, quality, process), flagged with a
verified verdict and its evidence. The recorded outcome of grading an expectation, not the
expectation itself.
_Avoid_: expectation, result

**Outcome claim**:
An assertion about the state of the world after the run — a file's contents, a captured HTTP
response, a decision recorded in an artifact. The default and preferred target for expectations.
_Avoid_: artifact check, result check

**Process claim**:
An assertion about how the agent got there — that it read before concluding, wrote a test before
the implementation, explored context before proposing. Checkable only with tool-call evidence,
and unreliable without it.
_Avoid_: behavior check, discipline check

**Mechanism expectation**:
An expectation grading the skill's own machinery — that a named gate fired, that a specific
section exists, that a workflow stage was announced — rather than the outcome the skill exists
to produce.
_Avoid_: process expectation, structural expectation

**Vacuous expectation**:
An expectation an output can satisfy by doing nothing relevant: an absence-form check, a check
gated on a conditional that can be absent, or a prohibition over a section the agent never
created.
_Avoid_: weak expectation, soft expectation, negative expectation

### Why measurement breaks

**Evidence channel**:
The artifact a claim is checked against — an output file, a captured log, a tool-call record. A
claim's strength is bounded by its channel; a process claim read from an executor-authored prose
summary is a self-report regardless of how confident it sounds.
_Avoid_: evidence, source (in the channel sense — evidence also names the recorded support in
grading.json claims)

**Self-report**:
Evidence authored by the party being measured — typically an executor-authored prose summary
with no tool-call record. A claim backed only by self-report is not independently checkable.
_Avoid_: transcript (the specific self-report artifact), note, summary

### Eval workflow mechanics

**Configuration**:
One of the two executor groups in a comparison eval, named in the workspace layout:
with_skill (skill available) or without_skill (skill tool disabled). Distinct from config, the
agent's tool configuration.
_Avoid_: arm, side, group

**Baseline**:
Two senses: the without-skill configuration of a comparison eval, and the recorded behavior of
the current skill before a change (the RED phase).
_Avoid_: control (the eval sense), old version (the pre-change sense)

**Run / iteration / cycle**:
Nesting, not synonyms: a run is one executor execution under a configuration; an iteration is
one full eval pass over a skill; a cycle is a campaign across skills.
_Avoid_: interchangeable use; "round" for anything but a strengthened round

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

**Removal bar**:
A strengthened round that still shows zero value-add is grounds to remove a skill. Structural
guards are exempt: their value is damage prevention, never visible in graded artifacts, so they
carry substitute validation — the guard fires when the hazard is present.
_Avoid_: exemption, exception (bleed into eval-level vocabulary)

**skill-creator**:
The external dev-only skill that drives skill validation, evals, and grading (scripts, grader
agent, review viewer). Not shipped; install separately. The /eval-skills command reports when it
is missing.
_Avoid_: the eval tooling, "the skill" (ambiguous with domain skills)

**Shipped artifact**:
Skills (their SKILL.md, references, evals, and scripts) — what version tags track and consumers
install. Dev-only tooling (.opencode/, .agents/, plans, workspaces) is never shipped and does
not trigger version bumps.
_Avoid_: tooling, the framework (reserved for the whole repo)