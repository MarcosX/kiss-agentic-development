# Contributing

## Local development

Clone the repo and work from it. The repo includes:

- `.opencode/skills → ../skills` — symlink for native OpenCode skill discovery (domain skills only)
- `.opencode/opencode.json` — loads `instructions/using-skills.md` into every session via `instructions`

Run validation after making changes:

```bash
node test/validate.mjs
```

Temp directories for per-skill validation are created under `test/tmp/` and cleaned up automatically.

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Create `test/prompts/<name>/VALIDATE.prompt.md` (optional, for AI-driven validation)
3. Run `node test/validate.mjs` to confirm frontmatter is valid
4. Install from the repo to test: `npx skills add . --agent opencode --skill <name>`

## Adding tests for a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Test baseline first**: Run representative prompts WITHOUT the skill — document what the agent gets wrong or misses.
3. Create the skill following the guidelines in [AGENTS.md](AGENTS.md).
4. **Test with same prompts**: Verify the skill now produces better output.
5. Run `node test/validate.mjs` to verify frontmatter is intact.

## Validation

See [AGENTS.md](AGENTS.md) for the full VALIDATE.prompt.md strategy, including automated bash checks and manual AI-review scenarios.
