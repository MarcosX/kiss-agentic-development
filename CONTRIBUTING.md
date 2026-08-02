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
6. Run `scripts/eval.sh --skill <name>` to run the end-to-end eval — the agent (with the skill loaded) is tested against each eval prompt, and responses are graded against expectations
7. Test the skill with the same prompts — verify the skill now produces better output
8. Run `scripts/eval.sh --skill <name>` again to confirm final pass rate

## Modifying an existing skill

1. **Snapshot baseline**: Before editing, save the current skill version and test it on representative prompts to document current behavior
2. Edit `skills/<name>/SKILL.md` only
3. **Test with same prompts**: Verify the skill now produces better output
4. Run `scripts/validate.sh` to confirm frontmatter is intact
5. Run `scripts/eval.sh --skill <name>` to confirm the change didn't regress expectations

## Testing workflow

Skill development follows the RED-GREEN-REFACTOR cycle. See [AGENTS.md](AGENTS.md) for the full testing methodology including test case creation, pressure scenarios, transcript analysis, and blind comparison.

In the GREEN phase, after writing or editing a skill, run `scripts/eval.sh --skill <name>` to validate the skill produces the expected agent behavior against its eval prompts.

## Evaluation

### Local eval runner (fast, with-skill only)

Use `scripts/eval.sh` for quick iteration — it tests the skill's end-to-end behavior by running each eval prompt against the configured agent CLI and grading responses with an LLM judge.

```bash
scripts/eval.sh --skill brainstorming                        # single skill
scripts/eval.sh --skill debugging --dry-run                   # list evals without running
scripts/eval.sh --skill reviewing-code --judge "opencode run" # independent judge
scripts/eval.sh --skill practicing-tdd --timeout 600          # override agent timeout
scripts/eval.sh --judge-timeout 180                            # override judge timeout
scripts/eval.sh --baseline .opencode/evals/report.json        # compare with previous run
scripts/eval.sh --keep-workspace                              # preserve temp dirs for debugging
scripts/eval.sh                                               # all 6 skills
```

Output is written to `.opencode/evals/<skill>/` with per-eval responses, grades, and a summary. Previous reports are automatically archived to `.opencode/evals/history/`. Each eval runs in an isolated temp directory with relevant fixtures copied in, preventing cross-contamination. The exit code is non-zero when any expectation fails, making it suitable for CI gating. Agent errors (timeouts, crashes, non-zero exits) are tracked separately in the summary's `errors` field and do not count against the pass rate.

See [AGENTS.md](AGENTS.md#eval-runner) for the full eval runner documentation.
