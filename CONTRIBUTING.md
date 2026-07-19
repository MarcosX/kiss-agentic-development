# Contributing

## Local development

Clone the repo and work from it. The repo includes:

- `.opencode/skills → ../skills` — symlink for native OpenCode skill discovery (domain skills only)
- `.opencode/opencode.json` — loads `instructions/using-skills.md` into every session via `instructions`

Validation: Run `scripts/validate.sh` to check frontmatter and evals.json structure.

## Adding a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Test baseline first**: Run representative prompts WITHOUT the skill — document what the agent gets wrong or misses. This is your "RED" phase.
3. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
4. Create `skills/<name>/evals/evals.json` with 3 evaluations (prompts + expectations)
5. Run `scripts/validate.sh` to confirm frontmatter and evals
6. Test the skill with the same prompts — verify the skill now produces better output
7. Install from the repo to test: `npx skills add . --agent opencode --skill <name>`

## Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run `scripts/validate.sh` to confirm frontmatter is intact

## Testing workflow

Skill development follows the RED-GREEN-REFACTOR cycle. See [AGENTS.md](AGENTS.md) for the full testing methodology including test case creation, pressure scenarios, transcript analysis, and blind comparison.

## Evaluation

After testing, run the full eval pipeline using the skill-creator framework to measure behavioral deltas between with-skill and without-skill runs. See [AGENTS.md](AGENTS.md#evaluation-and-iteration) for details on eval-driven development.
