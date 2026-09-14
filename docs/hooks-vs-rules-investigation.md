# Hooks vs Rules: Ongoing Investigation

Status: **ACTIVE — no final decision yet.** This is the handoff point for the
investigation into replacing rules-style discipline skills with hooks-style
skills. Read this before touching any skill under investigation.

## What this is

Whether discipline skills (TDD, debugging, reviewing, planning, execution) should
be written as **hooks** — cognitive reframes that show the agent why a behavior
is in its own interest and give it a clear way to complete the task — instead of
**rules** — HARD-GATEs, red flags, MUSTs that try to restrain the agent.

- **Rule / blocker**: "Always write a test first", "never X", red-flag catalogs,
  verification checklists. Obeyed by prohibition. A wall between the agent and
  what it was asked to do.
- **Hook**: "A failing test is the fastest way to know you've successfully
  completed the task." Reframes the task so the violation is no longer part of
  the task's definition, and aligns the behavior with what agents already want
  (done, confident, fast). Uses the agent's theory of mind instead of fighting it.

Both produce the same outward behavior; they differ in mechanism. A rule is
obeyed cautiously, a hook is adopted.

The core observation that started this: agents are driven to be helpful, fast,
and "done", so under pressure they rationalize **around** walls instead of
through them. Rules only "work" while a gate fires and punishes; the design is
fighting the agent rather than working with it.

## The prototype: practicing-tdd rework (Sep 2026)

The pattern was built and validated on `skills/practicing-tdd/`. Reference
implementation, current state on `main`.

- **SKILL.md**: HARD-GATE, Red Flags list, and Verification Checklist removed.
  Spine is the task reframe — "The task is to make a failing test pass" — plus
  The Loop (write the failing test → watch it fail → make it pass → refactor).
  Bug fixes reframed: the bug IS the failing test (reproduction test).
- **Intentional strictness reduction**: "pre-written code must be deleted" became
  "delete, adapt, or keep is the agent's choice" — the observable bar is a
  witnessable failing run BEFORE the implementation is accepted. This loosening
  was deliberate, so the skill works with the agent.
- **Evals**: rewritten to positive observable expectations ("a failing test is
  written first and watched to fail for the expected reason") instead of
  internal-state checks ("HARD-GATE fires"). Later converted to `Plan task:`
  format mirroring executing-plans dispatch context. A deviation eval was added:
  the plan predicts `ModuleNotFoundError` but an existing `app.py` causes a
  `NameError`; the agent must reconcile the real cause rather than force green.
- **Executing-plans integration**: coding tasks now route to practicing-tdd by
  name ("Coding tasks follow practicing-tdd's loop...").

Design intent (from the original PRD, `.opencode/plans/tdd-hooks-refactor-prd.md`):

- Two mechanisms: (1) **cognitive reframe** — redefine the task so done means
  "a test I wrote first, and watched fail, now passes", not "code exists"; no
  rule to violate because the violation is excluded from the task. (2) **drive
  alignment** — frame the desired behavior as the fast path to what agents want
  ("the failing run is your receipt", "the loop pays for itself").
- **Purist stance was deliberate**: no residual rules, so evals can measure
  whether the reframe alone carries the discipline. If it fails, rules can be
  reintroduced as a measured backstop — a later decision, not this design.
- The original plan intended to convert the other five skills in subsequent
  cycles once the pattern was proven.

Findings and decisions so far:

- Chosen mostly as experimentation, but proved better at avoiding rationalization
  than the rules version.
- The pressure eval (added with the rework as AC-7) was later removed to lighten
  tests: agents mostly work WITHIN the skill framework, not against an angry user
  pushing past a skill. See the tension note below — this contradicts a current
  AGENTS.md mandate.
- Word count dropped ~40% (≈230 words vs the ~650 general-skill target) — hooks
  are leaner by construction.

## Compatibility with authoring guidance

AGENTS.md and skill-creator largely endorse hooks. Most tension lives in AGENTS.md.

### Aligned

- "Explain WHY over MUSTs: agents have theory of mind — they follow reasoning
  better than bare imperatives" (AGENTS.md) IS the hooks principle.
- skill-creator: all-caps ALWAYS/NEVER and rigid structures are "a yellow flag —
  reframe and explain the reasoning"; warns against "oppressively constrictive
  MUSTs".
- Evals must be behavior-observable (both docs agree); hooks evals comply.
- "Degrees of freedom: match specificity to task fragility" is the vocabulary for
  the narrow-bridge vs open-field split.
- Token efficiency / lean skills align with hooks (the rework cut words).

### Tension — candidates to rework if hooks win

- **AGENTS.md is itself rules-shaped**: HARD-GATEs, "STOP if true" red flags,
  mandated checklists, and a REFACTOR phase that says "close loopholes → add
  explicit counters → update red flags". practicing-tdd's fix was to DELETE red
  flags — the opposite move.
- **Pressure-testing mandate**: AGENTS.md requires pressure scenarios for
  discipline skills. Practice has moved away from it (pressure eval removed).
  Nothing yet distinguishes when pressure testing still applies.
- **Iron Law** ("no skill without a failing test first") presumes a concrete
  failure baseline. Philosophy-driven reworks have a murkier RED: baseline = the
  old skill version, proof = `compare` (with/without) runs.
- **Eval schema blind spot**: grading is behavior-only. "The task is to make a
  failing test pass" is unfalsifiable as a mechanism — the grader can't tell a
  hooked agent from a compiled one. "Hooks reduce rationalization" is exactly
  the claim current evals can't directly verify; detecting it needs adversarial
  prompts or with/without baselines.
- **Checklist guidance**: AGENTS.md prescribes copyable checklists for
  multi-step workflows; hooks skills may prefer prose completion bars. Keep
  checklists where they help; don't force them onto hooks.
- **skill-creator** says "prefer the imperative form" — mild, resolved by framing
  the completion bar as the instruction.

## Assessment: narrow-bridge vs open-field (per skill)

Decision rule: **the artifact a downstream actor depends on is narrow (rules,
structured); the discipline a single agent applies is open (hooks).**

- **practicing-tdd** — open-field → **hooks (DONE)**. Reference implementation.
  Narrow contract (the test) + open loop (the why).
- **debugging** — open-field → **hook candidate**. Natural next experiment:
  closest twin of practicing-tdd (method discipline; root-cause "proof" ≈
  failing-test "proof"). Current shape: HARD-GATE + red flags + phases. Failure
  driver is motivational (jump-to-fix), not hazardous. Rewrite why-before-gate.
- **reviewing-code** — open-field → **hook candidate**. Failure modes (LGTM
  without review, rubber-stamping, skipping the challenge step) are shortcut
  failures. Human-in-the-loop catches mistakes → low irreversibility. Convert
  red flags to a "done when" bar.
- **brainstorming** — open-field with one guarded boundary → **hook candidate**.
  Content is open-context work and already argues its own why. The one
  load-bearing rule — no implementation before user approval — is human-reinforced
  anyway (the user approves the design). Rewrite the HARD-GATE as a why-framed
  lead; keep the approval-gate behavior.
- **writing-plans** — **hybrid**: narrow on the FORMAT, open on the JUDGMENT.
  The plan is a downstream contract for executing-plans (self-contained tasks,
  exact commands, AC mapping, eval procedures) — ambiguity costs a dispatch
  round-trip. Keep the template/checklist; convert the judging parts (YAGNI,
  atomic steps, quiz-the-user) to reasoning. Already splits contract vs loop
  correctly.
- **executing-plans** — narrow-bridge → **keep enforced**. Structural, not
  stylistic: worktree isolation is an irreversibility guard ("uncommitted changes
  in main → stop and assess damage" protects main from damage the skill can't
  undo); cross-agent orchestration means a skipped step cascades. Hooks may
  explain WHY the lifecycle exists; the lifecycle steps stay imperative.

## Experimental suspension of AGENTS.md rules

This conversion is an experiment run under the active investigation. AGENTS.md
rules that would block a hooks conversion are deliberately NOT enforced while
the investigation is active — but they stay in AGENTS.md, and the plan is to
rework them once the decision is made. Currently suspended for the experiment:

- **Pressure-testing mandate** (Coverage principles + the "Pressure scenarios"
  section). Scope stays, form changes: only cooperative pressure survives (a
  stressed user asking for advice), not adversarial "push past the skill" tests.
- **REFACTOR phase "close loopholes → add explicit counters → update red
  flags"**. The operator for escaping old machinery is reversed: delete red
  flags rather than extend them.
- **Checklist mandate** for multi-step workflows. Prose completion bars (The
  Loop) may replace copyable checklists.
- **The authoring HARD-GATE** to the extent it would forbid a hooks conversion
  on a skill this doc classifies as open-field (debugging, reviewing-code,
  brainstorming).
- **The Iron Law's implied baseline**. For a philosophy rework, "no skill
  without a failing test first" is fulfilled by with-skill vs without-skill
  evals (`compare`), not by a bug-fix reproduction.

Status: the first conversion under this suspension is the `debugging` hook
conversion (plan: `.opencode/plans/debugging-hooks-conversion-plan.md`).

## Open decisions

- Apply hooks to all open-field skills, or keep some as enforced guidance/rules
  (the standing question; classification above is a proposal, not a decision).
- Whether to rework AGENTS.md's rules-shaped guidance (REFACTOR "close loopholes"
  wording, pressure-testing mandate, checklist mandate) to match hooks — currently
  AGENTS.md is the source of most tension.
- Verify "hooks reduce rationalization" empirically via `compare` baselines.

## How to continue this work

1. Read this doc, then read `skills/practicing-tdd/SKILL.md` as the reference
   implementation.
2. Decide (with the user) whether executing-plans and writing-plans' format stay
   enforced guidance — the classification above is a proposal.
3. Natural next experiment: convert `debugging` (or `reviewing-code`) to hooks,
   snapshotting the current version as baseline and running `compare`.
4. If hooks win: convert remaining open-field skills, then rework AGENTS.md
   tension points, then update this doc to "DECIDED".

## Handling conflicts while incomplete

- This doc's per-skill classification is provisional and advisory, not a gate.
- For an unconverted skill, AGENTS.md authoring rules remain the governing
  process (RED/GREEN/REFACTOR, quick_validate, eval ladder).
- For a converted (hooks) skill, the converted skill is the source of truth for
  its own content. If it conflicts with AGENTS.md guidance, do NOT silently
  re-rule-ify it — flag the conflict to the user.
- Do NOT mass-port the hooks style to any skill not classified open-field.
- Do NOT rewrite AGENTS.md tension points until the decision is made.
- When a decision is made, update this doc from ACTIVE to the decided outcome,
  remove the AGENTS.md note's "while active" caveats, and update any guidance
  that the decision supersedes.

## Changelog

- 2026-09-12: Created from the practicing-tdd rework learnings, the AGENTS.md /
  skill-creator compatibility analysis, and the per-skill narrow/open assessment.
- 2026-09-12: Documented the experimental suspension of AGENTS.md rules for the
  hooks experiment, and the `debugging` conversion (first conversion; plan
  drafted in `.opencode/plans/debugging-hooks-conversion-plan.md`).