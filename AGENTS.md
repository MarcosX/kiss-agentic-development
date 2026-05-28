# kiss-agentic-development

Collection of AI agent skills that enforce skill-first workflows.

## Structure

```
├── skills/                           # All skill directories (source of truth)
│   ├── [skill name]/
│   │   ├── SKILL.md
│   │   └── VALIDATE.prompt.md
├── test/
│   └── validate.mjs                  # Frontmatter + VALIDATE.prompt.md checks
└── .opencode/
    ├── skills/ → ../skills           # Symlink for native discovery
    └── opencode.json                 # Local dev config (loads using-skills)
```

## Local development

When working on skills in this repo, the local config (`.opencode/opencode.json`) loads `using-skills` into every opencode session, while the symlink provides native discovery for all 4 skills via the `skill` tool.

## Working with Skills

### Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Create `skills/<name>/VALIDATE.prompt.md` (optional, for AI-driven validation)
3. **Symlink is automatic** — `.opencode/skills → ../skills` covers all subdirectories
4. Run `node test/validate.mjs` to confirm frontmatter and symlink

### Modifying an existing skill

1. Edit `skills/<name>/SKILL.md` only
2. Run `node test/validate.mjs` to verify frontmatter is intact

### Skill structure conventions

- `SKILL.md` **requires** YAML frontmatter with `name` and `description` — both must be present
- `VALIDATE.prompt.md` provides AI agents with self-check instructions for the skill
- Prompt files (`.prompt.md`) under `executing-plans/` are loaded by the skill itself, not auto-discovered

## Skill authoring guidelines

<HARD-GATE>
You MUST NOT add, edit, or port a skill that violates the rules below. If any rule is being broken, STOP and challenge the user before proceeding. "The user asked for it" is not a valid exception.
</HARD-GATE>

Guidelines for writing skills that agents can discover, understand, and follow reliably. These apply regardless of the coding agent or model.

### Naming and description

- **Name**: Lowercase letters, numbers, and hyphens only. Gerund form is REQUIRED (`processing-pdfs`, `analyzing-data`).
- **Description**: Write in **third person**. Include BOTH what the skill does AND when to use it. Critical for discovery — agents select skills based on description alone.
  - **Description token budget**: The description is loaded in every session. Every word is paid on every invocation. If a word doesn't help with discovery or dispatch decisions, cut it.
  - Correct: `Extract text and tables from PDF files. Use when working with PDFs or document extraction.`
  - Wrong: `I can help with PDFs` (first person). `Helps with documents` (vague).

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
- **Consistent terminology**: Pick one term per concept and use it throughout. Never mix synonyms ("extract", "pull", "retrieve") for the same operation.
- **Avoid time-sensitive info**: Hard-coded dates or versions force maintenance. Use "old patterns" sections instead.

**You are violating this rule if:**
- A line explains something an agent already knows
- The same concept has different names in different parts of the skill
- A date or version number appears without an "old patterns" escape hatch

### Token efficiency

Agents pay for every token in a skill. Optimize ruthlessly.

- **Description is always loaded** — it MUST be minimal while clearly communicating when to use the skill (see Naming and Description above).
- **MUST NOT use visual formatting**: no tables, no ASCII charts, no graphviz diagrams, no complex formatting. These add token overhead for zero agent benefit.
- **MUST use flat structures**: lists, short paragraphs, code blocks. Avoid nesting beyond 2 levels.
- **Reference files over 100 lines**: MUST include a table of contents at the top so agents can scope partial reads.
- **SKILL.md body**: MUST stay under 500 lines.

**You are violating this rule if:**
- A table or diagram is found in a skill file
- Nested bullet points go 3+ levels deep
- A reference file has no ToC and exceeds 100 lines

### Structure principles

- **Progressive disclosure**: SKILL.md is an overview. Split detailed content into separate reference files that agents read on demand.
- **One level deep**: All reference files MUST link directly from SKILL.md. Deeply nested references (`SKILL.md → file-a.md → file-b.md`) cause agents to skip content.
- **Forward slashes**: Always use Unix-style paths (`reference/guide.md`), never backslashes.

### Workflow design

- **Clear steps**: Break complex operations into sequential steps. Number them.
- **Checklists**: For multi-step workflows, provide a checklist agents can copy and track (`- [ ] Step 1: ...`).
- **Validation loops**: Include "run → check → fix → repeat" cycles for quality-critical tasks.

### Anti-patterns to avoid

These patterns MUST be caught and corrected. If you find yourself writing any of these, STOP.

- **Too many options**: Listing 5 libraries when 1 will do. Provide a default with an escape hatch for edge cases.
- **Voodoo constants**: Every configuration value MUST have a justification. If you don't know the right value, how will an agent?
- **Punting**: Scripts MUST handle errors explicitly, not crash and let the agent figure it out.
- **Assuming dependencies**: List required packages explicitly. Do not assume anything is pre-installed.

**You are violating this rule if:**
- You present multiple options without a clear default
- A script or command fails without a helpful error message
- You write `pip install` without listing the actual packages needed

## Versioning

Version `0.0.1`. Bump with `git tag v<semver>` and `git push --tags`.

## Commit convention

Use [Conventional Commits](https://www.conventionalcommits.org/):
`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`

## Validation

```bash
node test/validate.mjs
```

## Red flags (skill development)

- **Editing `.opencode/skills/` instead of `skills/`**: The symlink is a mirror — edit the source at `skills/`
- **Missing frontmatter**: `name` and `description` are REQUIRED for discovery
- **Forgetting to run validation**: RUN `node test/validate.mjs` after every skill change. Do not skip.

### Quality red flags — STOP if any of these are true

- **Over-explaining**: Explaining what agents already know — CUT IT. Agents know what PDFs, APIs, and files are.
- **Deeply nested references**: `SKILL.md → file-a.md → file-b.md` — FLATTEN to one level.
- **Too many options**: Presenting multiple approaches without a default — PICK ONE.
- **Voodoo constants**: Undocumented magic numbers — JUSTIFY or PARAMETERIZE.
- **Punting**: Scripts that fail instead of handling errors — HANDLE EXPLICITLY.
- **Time bombs**: Hard-coded dates or version references — USE "old patterns" INSTEAD.
- **Inconsistent terminology**: Mixing synonyms for the same concept — PICK ONE.
- **Provider-specific references**: Tool names, file paths, or config that only works with one provider — FLAG or REMOVE.
