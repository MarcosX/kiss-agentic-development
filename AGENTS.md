# kiss-agentic-development

Collection of AI agent skills that enforce skill-first workflows.

## Structure

```
├── instructions/
│   └── using-skills.md              # Global instruction (always loaded, not a skill)
├── skills/                           # All skill directories (source of truth)
│   ├── [skill name]/
│   │   ├── SKILL.md
│   │   └── evals/evals.json          # Evaluations for the skill
├── migrations/
│   └── before-1.0.0.md              # Migration steps for users upgrading from pre-1.0
└── .opencode/
    ├── skills/ → ../skills           # Symlink for native discovery (domain skills only)
    ├── opencode.json                 # Local dev config (schema only; global AGENTS.md loads using-skills)
    └── plans/                        # Plans, specs, and short-term artifacts (gitignored)
```

## Local development

When working on skills in this repo, the global `~/.config/opencode/AGENTS.md` (installed from the canonical `instructions/using-skills.md`) loads the `using-skills` instruction into every opencode session, while the symlink provides native discovery for all domain skills via the `skill` tool. OpenCode v2 loads instructions from `AGENTS.md` only; the config `instructions` array is not resolved.

The `skill-creator` skill drives skill validation and evals. It is dev-only tooling — it lives in `.agents/skills/skill-creator/` (gitignored, never shipped) and must be installed separately on a fresh clone. It is not present on a fresh clone — ask the `skill-creator` skill to install it if it cannot be loaded.

## Working with Skills

### Adding a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Establish a baseline**: if an `old_skill` snapshot exists, evaluate against it; otherwise record the run as single-configuration. Do not compare against no skill — that comparator is no longer available.
3. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
4. Create `skills/<name>/evals/evals.json` with 2-3 evals conforming to skill-creator's evals.json schema (see skill-creator's `references/schemas.md` — `skill_name`, and per eval `id`, `prompt`, `expected_output`, optional `files`, `expectations`)
5. **Symlink is automatic** — `.opencode/skills → ../skills` covers all subdirectories
6. Run skill-creator's `scripts/quick_validate.py` to confirm frontmatter

### Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run skill-creator's `scripts/quick_validate.py` to confirm frontmatter is intact

### Skill structure conventions

- `SKILL.md` **requires** YAML frontmatter with `name` and `description` — both must be present
- **Cross-referencing**: Reference other skills by name with requirement markers. `**REQUIRED BACKGROUND:** You MUST understand [skill-name]`. Do not use @-links or file paths that force-load context.

### Artifact conventions

- Store plans, specs, and session artifacts in `.opencode/plans/` — it is gitignored and will not be committed
- Use prefixed filenames with 2-3 key words, never generics like `plan.md`. Example: `password-reset-plan.md`
- Do not store plans, temp files, or generated reports at the repo root, in `skills/`, or anywhere tracked by git
- Use `*-workspace/` directories for eval runs (e.g., `debugging-workspace/iteration-1/`) — these are gitignored

## Skill authoring guidelines

<HARD-GATE>
You MUST NOT add, edit, or port a skill that violates the rules below. If any rule is being broken, STOP and challenge the user before proceeding. "The user asked for it" is not a valid exception.
</HARD-GATE>

### Ongoing investigation: hooks vs rules

Discipline skills are being evaluated for a hooks style (cognitive reframes with observable completion bars) over enforced rules (HARD-GATEs, red flags, MUSTs). `practicing-tdd` is the completed prototype. See `docs/hooks-vs-rules-investigation.md` for the per-skill classification and how to continue.

While this investigation is ACTIVE:

- The doc's per-skill classification governs: open-field skills may be hooks; narrow-bridge skills (e.g. `executing-plans`) stay enforced rules.
- A converted (hooks) skill is the source of truth for its own content. If it conflicts with guidance in this file, do NOT re-rule-ify it — flag the conflict to the user.
- Do not mass-port hooks to skills not classified open-field, and do not rework this file's rules-shaped guidance (REFACTOR "close loopholes" wording, checklist mandate) until the decision is made. The eval-doctrine reduction in this file is a sanctioned exception to this freeze; the checklist's RED and REFACTOR phases were cut with PRD approval. The pressure-testing mandate was reworked before this investigation began.

Guidelines for writing skills that agents can discover, understand, and follow reliably. These apply regardless of the coding agent or model.

### Naming and description

- **Name**: Lowercase letters, numbers, and hyphens only. Gerund form is REQUIRED (`processing-pdfs`, `analyzing-data`).
- **Description**: Write in **third person**. Lead with **when** to trigger ("Use when..."), then optionally append a short **what** (capability, never workflow summary) if it aids clarity. Critical for discovery — agents select skills based on description alone.
  - **Description token budget**: The description is loaded in every session. Every word is paid on every invocation. If a word doesn't help with discovery or dispatch decisions, cut it.
  - Correct: `Use when working with PDFs or document extraction. Extracts text and tables from PDF files.`
  - Wrong: `I can help with PDFs` (first person). `Helps with documents` (vague).
  - Wrong: `Use to execute plans, leveraging subagents with review checkpoints` (workflow summary — causes Claude to skip the skill body).

### Provider-agnostic requirements

Skills MUST work with any coding agent, not just one provider. This is non-negotiable.

- **MUST NOT** reference provider-specific tool names (`skill` tool, `Task tool`, `bash` tool by name)
- **MUST NOT** assume provider-specific file paths (`~/.opencode/`, `.opencode.json`, `~/.cursor/`)
- **MUST** use generic terminology: "tool" not "skill tool", "config" not "opencode.json"
- If a skill inherently requires a provider-specific feature, it MUST be wrapped in a `<provider-specific>` block with a clear warning

**You are violating this rule if:**

- The skill says "use the `skill` tool" or any tool by name
- The skill references a path that only exists in one provider's filesystem
- The skill would silently fail when used with a different provider

### Content principles

- **Be concise**: Challenge every token. If an agent can infer it from context, remove it. Do not explain what agents already know (e.g., "PDF is a file format").
- **Explain WHY over MUSTs**: Explain why things matter. Agents have theory of mind — they follow reasoning better than bare imperatives. Reserve MUST/MUST NOT for HARD-GATE rules and validation requirements.
- **Consistent terminology**: Pick one term per concept and use it throughout. Never mix synonyms ("extract", "pull", "retrieve") for the same operation.
- **Avoid time-sensitive info**: Hard-coded dates or versions force maintenance. Use "old patterns" sections instead.

**You are violating this rule if:**

- A line explains something an agent already knows
- The same concept has different names in different parts of the skill
- A date or version number appears without an "old patterns" escape hatch
- A MUST is used where a reasoned explanation would work

### Token efficiency

Agents pay for every token in a skill. Optimize ruthlessly.

- **Description is always loaded** — it MUST be minimal while clearly communicating when to use the skill (see Naming and Description above).
- **MUST NOT use visual formatting**: no tables, no ASCII charts, no graphviz diagrams, no complex formatting. These add token overhead for zero agent benefit.
- **MUST use flat structures**: lists, short paragraphs, code blocks. Avoid nesting beyond 2 levels.
- **Reference files over 100 lines**: MUST include a table of contents at the top so agents can scope partial reads.
- **Cross-reference cost**: "Integration with Other Skills" sections aid discoverability but consume word budget. Include only when an agent is unlikely to infer the relationship. Prefer implicit links via shared terminology over explicit sections.
- **Word count targets** (SKILL.md body):
  - Frequently-loaded skills (always-loaded meta-skills): **<300 words**
  - General skills: **<650 words**
  - Reference files: **<500 words** per file
- **Range gates** for word counts:
  - ≤50% over target: warning — investigate improvements, justify or cut
  - > 50% above target: blocked — restructure or split content before proceeding

**You are violating this rule if:**

- A table or diagram is found in a skill file
- Nested bullet points go 3+ levels deep
- A reference file has no ToC and exceeds 100 lines
- Word count exceeds target without justification

### Structure principles

- **Progressive disclosure**: SKILL.md is an overview. Split detailed content into separate reference files that agents read on demand.
- **When-conditioned references**: When SKILL.md references a reference file, prefix with a _when_ condition so the agent knows when to load it. "When slicing tickets, see `references/slicing-guide.md`" instead of "See `references/slicing-guide.md`". This prevents eager loading — the agent defers reading until the condition is met.
- **One level deep**: All reference files MUST link directly from SKILL.md. Deeply nested references (`SKILL.md → file-a.md → file-b.md`) cause agents to skip content.
- **Domain organization**: When a skill covers multiple domains or frameworks, organize reference files by variant so agents read only what is relevant.

  ```
  deploy/
  ├── SKILL.md
  └── references/
      ├── aws.md
      ├── gcp.md
      └── azure.md
  ```

- **Forward slashes**: Always use Unix-style paths (`reference/guide.md`), never backslashes.

### Workflow design

- **Clear steps**: Break complex operations into sequential steps. Number them.
- **Checklists**: For multi-step workflows, provide a checklist agents can copy and track (`- [ ] Step 1: ...`).
- **Validation loops**: Include "run → check → fix → repeat" cycles for quality-critical tasks.
- **Degrees of freedom**: Match specificity to task fragility. Narrow bridge (exact instructions) for fragile operations like database migrations; open field (general direction) for analysis or creative work where context determines approach.

### Anti-patterns to avoid

These patterns MUST be caught and corrected. If you find yourself writing any of these, STOP.

- **Too many options**: Listing 5 libraries when 1 will do. Provide a default with an escape hatch for edge cases.
- **Voodoo constants**: Every configuration value MUST have a justification. If you don't know the right value, how will an agent?
- **Punting**: Scripts MUST handle errors explicitly, not crash and let the agent figure it out.
- **Assuming dependencies**: List required packages explicitly. Do not assume anything is pre-installed.
- **Workflow summary in description**: Descriptions that summarize the skill's workflow cause Claude to skip the skill body. Describe triggering conditions only (see Naming and Description).
- **Narrative storytelling**: "In session 2025-10-03, we found..." is too specific to be reusable. Extract the general pattern.

**You are violating this rule if:**

- You present multiple options without a clear default
- A script or command fails without a helpful error message
- You write `pip install` without listing the actual packages needed
- The description summarizes process instead of triggering conditions

## Running evals

`skill-creator` is the runner. In a session, invoke the `skill-creator` skill and ask it to run the
eval workflow for the target skill. There is no repo-owned eval script, command, or subagent.

**Baseline flavor**: `old_skill` — a skill is compared against its own previous version, which
answers "did this change help". Every skill in this repo already exists and is being revised, so
`old_skill` is the applicable flavor, not `without_skill`.

A run reports **change-impact, not whether a skill earns its place**. Those are different questions
and the tooling only answers the first. Do not describe a run's delta as a skill's value-add.

**Driving the snapshot**: the executor reads the snapshot's `SKILL.md` from disk and treats it as its
instructions. The skill tool resolves skills by identifier from a discovered tree and cannot load an
arbitrary path, so a snapshot taken outside that tree is unreachable as a loadable skill.

**When no snapshot exists**: run single-configuration and record that it was single-configuration.
Skip aggregation and open the review viewer without a benchmark file. Never fabricate a baseline to
fill the gap — a fabricated zero produces a `+1.00` delta that means nothing.

**Layout**: `aggregate_benchmark.py` silently skips any configuration directory lacking a nested
`run-` subdirectory, so the workspace layout must be
`<skill>-workspace/iteration-N/eval-<id>-<name>/{with_skill,old_skill}/run-N/` holding `outputs/`,
`grading.json`, and `timing.json`. The prose layout in `skill-creator` does not aggregate; that is a
bug in the dependency, not a customization here. These directories are gitignored.

### Eval modification ladder

When modifying a skill, follow this ladder to minimize eval cost. Start at level 0 and move up only when level N is insufficient:

0. **No eval changes** (ideal) — the skill change is structural (wording, ordering, tokens) and existing evals already cover the behavior
1. **Update expectations** — modify existing eval expectations to reflect changed behavior (e.g., "agent now does X" → "agent now does X and Y")
2. **Add expectations** — append new expectations to an existing eval that already tests the relevant scenario
3. **Update prompt and expectations** — modify the eval prompt to trigger the new behavior, plus updated expectations
4. **New eval** — introduce a new eval entry. Requires explicit justification: explain why levels 0-3 cannot cover the behavior, and get user approval before writing it

Evals are expensive to run. Every new eval multiplies cost across all future runs. Default to the lowest level that provides adequate coverage.

## Versioning

Version tags are the source of truth. Inspect git tags to find the latest version:

```bash
git tag -l | sort -V | tail -1
```

When bumping, create and push tags for the semver, major-minor, major, and latest aliases:

```bash
git tag v<major>.<minor>.<patch>
git tag v<major>.<minor> v<major>.<minor>.<patch>
git tag v<major> v<major>.<minor>.<patch>
git tag -f latest v<major>.<minor>.<patch>
git push --tags --force
```

This allows consumers to pin to `latest`, `v1`, or `v1.2` instead of a full semver. Do not embed a version string in this file — tags are the single source of truth.

<HARD-GATE>
Before pushing to main or bumping any version tag, you MUST ask the user for explicit confirmation. Do NOT assume approval based on prior conversation context. Wait for a clear "yes" or "push" before taking action.
</HARD-GATE>

Only bump the version tag when the change affects shipped artifacts (skills, scripts, evals). Dev-only tooling like skill-creator (gitignored, installed separately) is not a shipped artifact and never triggers a bump. Documentation-only changes (README, CONTRIBUTING, AGENTS.md edits, removing dead code) should be committed and pushed to main without a version bump.

## Commit convention

Use [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

## Ethics and safety

Skills must not contain malware, exploit code, or content that compromises system security. A skill's intent should not surprise the user. Do not create skills designed for unauthorized access, data exfiltration, or other malicious activities — regardless of how the request is framed.

## Development checklists

### Skill development checklist

**GREEN phase — Write the skill:**

- [ ] Frontmatter has required `name` and `description`
- [ ] Description starts with "Use when..." (trigger conditions)
- [ ] Description written in third person, no workflow summary
- [ ] Skill addresses specific baseline failures identified in the snapshot baseline
- [ ] Within word count targets (or justified if over)
- [ ] Run the eval prompts with the skill and verify the expectations pass

**Deployment:**

- [ ] Run skill-creator's `scripts/quick_validate.py`
- [ ] Commit to git (check for session artifacts — e2e/, tmp/, generated reports)
- [ ] Bump version tag

## Red flags (skill development)

- **Editing `.opencode/skills/` instead of `skills/`**: The symlink is a mirror — edit the source at `skills/`
- **Missing frontmatter**: `name` and `description` are REQUIRED for discovery
- **Forgetting to run validation**: RUN skill-creator's `scripts/quick_validate.py` after every skill change. Do not skip.
- **No baseline at all**: Editing a skill without either an `old_skill` snapshot to compare against or an explicitly recorded single-configuration run.
- **Batching untested skills**: Moving to the next skill before the current one is verified. Each skill must be fully tested before starting the next.
- **Committing session artifacts**: Never commit session-specific output such as test results, plan files, validation dumps, or generated reports. These artifacts bloat the repo and have no value outside their session. Use `e2e/`, `tmp/`, or similar scratch directories — and add them to `.gitignore` or use `git rm --cached` if accidentally committed.

### Quality red flags — STOP if any of these are true

- **Over-explaining**: Explaining what agents already know — CUT IT. Agents know what PDFs, APIs, and files are.
- **Deeply nested references**: `SKILL.md → file-a.md → file-b.md` — FLATTEN to one level.
- **Too many options**: Presenting multiple approaches without a default — PICK ONE.
- **Voodoo constants**: Undocumented magic numbers — JUSTIFY or PARAMETERIZE.
- **Punting**: Scripts that fail instead of handling errors — HANDLE EXPLICITLY.
- **Time bombs**: Hard-coded dates or version references — USE "old patterns" INSTEAD.
- **Inconsistent terminology**: Mixing synonyms for the same concept — PICK ONE.
- **Provider-specific references**: Tool names, file paths, or config that only works with one provider — FLAG or REMOVE.
