---
description: Run skill evals via the skill-creator workflow for one or more skills.
---

Evaluate skills using the skill-creator eval workflow. Run exactly ONE full cycle per skill, stopping at the review viewer. Do not auto-iterate or modify any skill.

## Step 1: Select target skills

Parse $ARGUMENTS:

- If empty: ask the user which skills to evaluate. Use the question tool with multiple selection. Offer only skills under skills/ that have an evals/evals.json file.
- If it is "all" or "all skills": target every skill under skills/ that has an evals/evals.json.
- Otherwise: treat $ARGUMENTS as a space-separated list of skill names.

Validate each target: it must exist at skills/<name>/ with an evals/evals.json file. Drop invalid names with a warning. If no valid targets remain, list the valid skills and stop.

If 3 or more skills are targeted, warn about the duration and token cost, then get explicit confirmation before continuing.

## Step 2: Verify skill-creator

Load the skill-creator skill. If it cannot be loaded, print instructions for installing it and stop.

## Step 3: Evaluate each skill, one at a time

For each target skill, in order, run skill-creator's eval workflow for exactly one cycle:

1. Use workspace <skill>-workspace/ at the repo root. Use the lowest positive N such that iteration-N does not already exist in that workspace.
2. For each eval in skills/<name>/evals/evals.json, spawn two subagents in the SAME turn: one with the skill (with_skill) and one baseline without it (without_skill). Save to eval-<id>-<name>/with_skill/run-1/outputs/ and eval-<id>-<name>/without_skill/run-1/outputs/ respectively, where <name> is a short descriptive eval name. Baseline is always without_skill (no skill).
3. Write an eval_metadata.json per eval directory (eval_id, eval_name, prompt, expectations used as assertions).
4. While runs execute, draft assertions from each eval's expectations, update eval_metadata.json (and evals/evals.json if assertions change), and explain them to the user.
5. Capture timing.json for each run from the subagent task notification, saved to <run-dir>/timing.json with fields total_tokens, duration_ms, total_duration_seconds — it is not persisted elsewhere.
6. When all runs finish, grade each run against its expectations with a grader subagent that reads skill-creator's agents/grader.md. Save grading.json per run.
7. From the skill-creator base directory, run `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` to produce benchmark.json and benchmark.md in the iteration directory.
8. Launch the review viewer in the background:
   `nohup python <skill-creator>/eval-viewer/generate_review.py <workspace>/iteration-N --skill-name <name> --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &`
   For iteration-N where N > 1, also pass --previous-workspace pointing at iteration-(N-1). In a headless environment use `--static <workspace>/iteration-N/review.html` instead of the background server.

## Step 4: Summarize

After all skills are evaluated, report per skill: pass-rate delta vs baseline, time and token deltas, and the viewer URL.
