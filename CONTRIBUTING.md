# Contributing

## Local development

Clone the repo and work from it. The repo includes:

- `.opencode/skills → ../skills` — symlink for native OpenCode skill discovery (domain skills only)
- `.opencode/opencode.json` — local dev config (schema only; the config `instructions` array is not resolved). The global `~/.config/opencode/AGENTS.md` (installed from `instructions/using-skills.md`) loads the `using-skills` instruction into every session

Skill validation runs through skill-creator's `scripts/quick_validate.py <skill>`, which checks SKILL.md frontmatter (`name`, `description`). Run it after every skill change.

## Adding a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Establish a baseline**: follow skill-creator's baseline selection — `without_skill` for a new skill, `old_skill` (a snapshot of the current version) for a revision
3. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
4. Create `skills/<name>/evals/evals.json` with evals conforming to skill-creator's schema (`skill_name`, and per eval `id`, `prompt`, `expected_output`, optional `files`, `expectations`)
5. Run skill-creator's `scripts/quick_validate.py <name>` to confirm frontmatter
6. Run the eval workflow (invoke the `skill-creator` skill and ask it to run the eval workflow for the target skill)
7. Test the skill with the same prompts — verify the skill now produces better output
8. Re-run the eval workflow to confirm the final pass rate

## Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run skill-creator's `scripts/quick_validate.py <name>` to confirm frontmatter is intact
5. Re-run the eval workflow to confirm the change didn't regress expectations

## Testing workflow

Skill development is iterative: draft, evaluate, review the results, improve. `skill-creator` is the runner — invoke the skill and ask it to run the eval workflow for the target skill. See [AGENTS.md](AGENTS.md) for the eval modification ladder and for how evals are run.

## Evaluation

Evals run through the `skill-creator` workflow, which is the runner.

**Layout**: `<skill>-workspace/iteration-N/eval-<id>-<name>/{with_skill,without_skill,old_skill}/run-N/` with `outputs/`, `grading.json`, and `timing.json` per run. These directories are gitignored.

See [AGENTS.md](AGENTS.md#running-evals) for the full evaluation documentation.
