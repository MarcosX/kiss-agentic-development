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

## Versioning

Version `0.0.1`. Bump using git tags with semver:

```bash
# Current
git tag v0.0.1

# New patch
git tag v0.0.2

# New minor
git tag v0.1.0

# New major
git tag v1.0.0
```

Push tags after tagging:

```bash
git push --tags
```

## Commit convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add code-review skill
fix: correct brainstorming frontmatter
docs: update installation instructions
refactor: simplify validate.mjs
chore: clean up stale test artifacts
```

## Validation

```bash
node test/validate.mjs
```

## Red flags (skill development)

- **Editing `.opencode/skills/` instead of `skills/`**: The symlink is a mirror — edit the source at `skills/`
- **Missing frontmatter**: `name` and `description` are required for discovery
- **Forgetting to run validation**: Always run `node test/validate.mjs` after skill changes
