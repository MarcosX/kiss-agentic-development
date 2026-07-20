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

After testing, run the full eval pipeline using the skill-creator framework to measure behavioral deltas between with-skill and without-skill runs.

```bash
npx skills eval . --skill <name>
```

This produces a workspace directory (`<name>-workspace/iteration-1/`) with:

| Artifact | What it tells you |
|----------|-------------------|
| `review.html` | Visual side-by-side: with-skill vs without-skill, per expectation |
| `benchmark.json` | Per-expectation pass/fail with evidence, per-config pass rates, variance, delta |
| `benchmark.md` | Summary in markdown |
| `grading.json` | Raw grader reasoning for each pass/fail call |
| `eval_metadata.json` | The exact prompt and expectation list for each eval |

### Reading results

Three numbers matter:

- **pass rate** (with-skill) — how reliably the agent follows the skill. 100% means the skill is enforced consistently.
- **baseline** (without-skill) — what the agent does naturally. A high baseline means the agent already behaves this way; the skill may not be needed.
- **delta** (with minus without) — the skill's measurable improvement. This is your primary signal.

### Thresholds

| Delta | Verdict | Action |
|-------|---------|--------|
| >= +0.50 | Strong | Skill is working well. Consider trimming word count. |
| +0.30 to +0.49 | Good | Worth keeping. Review failing expectations for tightening. |
| +0.15 to +0.29 | Marginal | Keep only if variance is low or it's a critical discipline rule. |
| < +0.15 | Weak | Consider removing. The token cost likely outweighs the benefit. |
| Negative | Harmful | Remove or redesign immediately. |

Exception: Discipline skills (HARD-GATE, security rules) can justify a lower delta — preventing even one rationalization pays for the token cost.

### Code smells

| Smell | What it looks like | Likely cause |
|-------|-------------------|--------------|
| Zero delta | Delta ~0.00 | Evals test common knowledge; skill doesn't differentiate; or agent already does the right thing. Redesign evals or remove skill. |
| Ceiling effect | Baseline >= 90% | Little room to improve. Skill may still reduce variance. |
| Sinking delta | Delta drops after edit | Your change made the skill worse. Revert and investigate which section caused it. |
| High variance | Stddev >= 30pp | Instructions are ambiguous or model-dependent. Works sometimes, not reliably. |
| Reliably bad | Low with-skill, low variance | Skill is consistently ignored. Redesign the structure — agents are skipping it. |
| Negative delta | With < without | Skill is actively harmful. Remove it. |

### Iterating on results

After each edit, delta should increase (or at minimum stay flat). If it decreases, the change is harmful regardless of intent — revert and analyze which section caused the regression.

Don't rely on aggregates alone. A skill that passes 5/5 on process expectations but fails 0/3 on security has a dangerous blind spot. Read the per-expectation evidence in `grading.json` — it shows exactly what the agent did and why the grader passed or failed it.

See [AGENTS.md](AGENTS.md#evaluation-and-iteration) for the full eval-driven development cycle.
