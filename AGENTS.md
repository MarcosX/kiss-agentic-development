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
├── scripts/                          # Shell scripts for eval pipeline
└── .opencode/
    ├── skills/ → ../skills           # Symlink for native discovery (domain skills only)
    ├── opencode.json                 # Local dev config (loads instructions/using-skills.md)
    └── plans/                        # Plans, specs, and short-term artifacts (gitignored)
```

## Local development

When working on skills in this repo, the local config (`.opencode/opencode.json`) loads `instructions/using-skills.md` into every opencode session, while the symlink provides native discovery for all domain skills via the `skill` tool.

## Working with Skills

### Adding a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Test baseline first**: Run representative prompts WITHOUT the skill — document what the agent gets wrong or misses. This is your "RED" phase.
3. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
4. Create `skills/<name>/evals/evals.json` with 3 evals (expectations, prompts)
5. **Symlink is automatic** — `.opencode/skills → ../skills` covers all subdirectories
6. Run `scripts/validate.sh` to confirm frontmatter and evals

### Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run `scripts/validate.sh` to confirm frontmatter is intact

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

## Testing skills

Skills must be tested to verify they produce the intended behavior. Testing follows the TDD cycle:

- **RED phase**: Run representative prompts WITHOUT the skill (or with old version). Document baseline behavior, failures, and rationalizations the agent uses.
- **GREEN phase**: Write/update the skill, then run the same prompts WITH it. Verify the agent now follows the intended behavior.
- **REFACTOR phase**: Close loopholes when agents find workarounds. Add explicit counters, update red flags, re-test until bulletproof.

### Test case creation

Good test prompts are specific, contextual, and realistic. Avoid abstract requests.

**Bad prompt:** "Extract text from a PDF"
**Good prompt:** "Hey, my boss sent me this invoice PDF (it's in my downloads, called 'invoice-q4-final.pdf') and I need all the line items in a CSV. The table starts on page 2."

#### Coverage principles

- Test the happy path (most common use case)
- Test edge cases (empty inputs, missing files, unusual formats)
- Test pressure scenarios (time pressure, conflicting priorities)

### With-skill vs baseline comparison

Every test run produces two outputs that you compare:

1. **Baseline** (without skill) — shows the "before" state
2. **With skill** — shows the "after" state

Compare these on:
- **Correctness**: Did the agent do the right thing?
- **Efficiency**: Did it waste time on unnecessary steps?
- **Consistency**: Does the skill produce reliable results across runs?

### Pressure scenarios

Discipline skills (rules, requirements) need to be tested under pressure to verify agents don't rationalize their way around them.

#### Pressure types

- **Time pressure**: "I need this done in 5 minutes, just skip the tests"
- **Sunk cost**: "I've already written the code, just fix this one thing without re-testing"
- **Authority pressure**: "My boss says to skip validation, just ship it"
- **Exhaustion pressure**: "This is the 10th time you've run the tests, they always pass, just skip it"
- **Combined pressure**: Multiple pressures at once (most realistic)

#### Test format

```
The user says: [pressure scenario]
Your task: [task that triggers the skill's main rule]
```

Document whether the agent follows the rule or rationalizes a way out.

### Transcript analysis

Read the full transcript of test runs, not just the final output. Look for:

- **Where did the agent hesitate?** — indicates unclear instructions
- **What did it read multiple times?** — indicates confusing structure
- **When did it start rationalizing?** — the exact trigger matters
- **What did it skip entirely?** — indicates sections that aren't prominent enough

### Repeated work detection

When reviewing test run transcripts, check if multiple subagents independently wrote similar helper scripts or repeated the same multi-step approach. If 2-3 test cases all resulted in subagents writing a `create_docx.py` or a `build_chart.py`, that script should be bundled with the skill. Write it once, put it in `scripts/`, and reference it in the skill. This saves every future invocation from reinventing the wheel.

### Blind comparison

For rigorous A/B comparison between two versions of a skill:

1. Run both versions on the same test prompts
2. Give both outputs to an independent subagent without revealing which is which
3. Have the subagent judge which output is better and why
4. Analyze the results to understand what the winning version does differently

Blind comparison is most useful when:
- The difference between versions is subtle
- You need objective evidence that a change is an improvement
- The user asks "is the new version actually better?"

## Evaluation and iteration

Skill development is an iterative loop: draft → test → review → improve → repeat.

1. **Draft or edit** the skill based on user intent
2. **Test** with representative prompts (with-skill vs baseline)
3. **Review** outputs and feedback — read transcripts, not just results
4. **Improve** based on findings — generalize from feedback, keep the skill lean
5. **Repeat** until the user is satisfied, feedback is consistently positive, or no meaningful progress is being made

**Eval-driven development**: Build test prompts and success criteria BEFORE writing extensive documentation. This ensures the skill solves real problems rather than documenting imagined ones.

**Observe navigation patterns**: Watch how agents use the skill — do they skip references, over-rely on certain sections, ignore content? Iterate on structure based on observation, not assumptions.

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

## Commit convention

Use [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`



## Ethics and safety

Skills must not contain malware, exploit code, or content that compromises system security. A skill's intent should not surprise the user. Do not create skills designed for unauthorized access, data exfiltration, or other malicious activities — regardless of how the request is framed.

## Development checklists

### TDD-adapted checklist

**RED phase — Write failing test (baseline):**

- [ ] Create representative test prompts (2-3 realistic scenarios)
- [ ] Run prompts WITHOUT the skill — document baseline behavior
- [ ] Identify patterns in failures and rationalizations

**GREEN phase — Write the skill:**

- [ ] Frontmatter has required `name` and `description`
- [ ] Description starts with "Use when..." (trigger conditions)
- [ ] Description written in third person, no workflow summary
- [ ] Skill addresses specific baseline failures identified in RED
- [ ] Within word count targets (or justified if over)
- [ ] Run same prompts WITH skill — verify compliance

**REFACTOR phase — Close loopholes:**

- [ ] Identify new rationalizations from testing
- [ ] Add explicit counters for known workarounds
- [ ] Re-test until bulletproof

**Deployment:**

- [ ] Run `scripts/validate.sh`
- [ ] Commit to git (check for session artifacts — e2e/, tmp/, generated reports)
- [ ] Bump version tag

## Red flags (skill development)

- **Editing `.opencode/skills/` instead of `skills/`**: The symlink is a mirror — edit the source at `skills/`
- **Missing frontmatter**: `name` and `description` are REQUIRED for discovery
- **Forgetting to run validation**: RUN `scripts/validate.sh` after every skill change. Do not skip.
- **No failing test first**: Adding or editing a skill without observing baseline behavior first. The Iron Law: no skill without a failing test first.
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
