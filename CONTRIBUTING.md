# Contributing

## Local development

Clone the repo and work from it. The repo includes:

- `.opencode/skills → ../skills` — symlink for native OpenCode skill discovery (domain skills only)
- `.opencode/opencode.json` — loads `instructions/using-skills.md` into every session via `instructions`

Skill validation runs through skill-creator's `scripts/quick_validate.py <skill>`, which checks SKILL.md frontmatter (`name`, `description`). Run it after every skill change.

## Adding a new skill

1. **Capture intent**: Interview the user to understand what the skill should do, when it should trigger, expected output, and edge cases.
2. **Test baseline first**: Run representative prompts WITHOUT the skill — document what the agent gets wrong or misses. This is your "RED" phase.
3. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
4. Create `skills/<name>/evals/evals.json` with 2-3 evals conforming to skill-creator's schema (`skill_name`, and per eval `id`, `prompt`, `expected_output`, optional `files`, `expectations`)
5. Run skill-creator's `scripts/quick_validate.py <name>` to confirm frontmatter
6. Run the eval workflow (via the `eval-skills` command or by invoking the `skill-creator` skill) — it spawns with-skill runs per eval prompt, grades them, and aggregates the benchmark (without-skill baselines are opt-in for comparison)
7. Test the skill with the same prompts — verify the skill now produces better output
8. Re-run the eval workflow to confirm the final pass rate

## Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run skill-creator's `scripts/quick_validate.py <name>` to confirm frontmatter is intact
5. Re-run the eval workflow to confirm the change didn't regress expectations

## Testing workflow

Skill development follows the RED-GREEN-REFACTOR cycle. See [AGENTS.md](AGENTS.md) for the full testing methodology including test case creation, pressure scenarios, transcript analysis, and blind comparison.

In the GREEN phase, after writing or editing a skill, run the skill-creator eval workflow to validate the skill produces the expected agent behavior against its eval prompts.

## Evaluation

Evals run through the skill-creator workflow — the skill is the runner, there is no custom eval script. Invoke the `skill-creator` skill in a session and ask it to run the eval workflow for `skills/<name>`.

The workflow:

1. Spawns a with-skill subagent per prompt in `skills/<name>/evals/evals.json` (with-skill only is the default; without-skill baselines are opt-in for comparison)
2. Grades each run against the eval's expectations via skill-creator's grader agent (`agents/grader.md`), writing `grading.json` per run
3. Aggregates results with skill-creator's `scripts/aggregate_benchmark.py` into `benchmark.json` and `benchmark.md`
4. Opens skill-creator's `eval-viewer/generate_review.py` for review (use `--static` in headless environments)

**Layout**: `<skill>-workspace/iteration-N/eval-<id>-<name>/{with_skill,without_skill}/run-N/` with `outputs/`, `grading.json`, and `timing.json` per run (`without_skill` present only in comparison mode). These directories are gitignored.

See [AGENTS.md](AGENTS.md#evaluation) for the full evaluation documentation.
