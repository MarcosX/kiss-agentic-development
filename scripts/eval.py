#!/usr/bin/env python3
"""
Run skill evaluations against an agent CLI and judge results.

Invoked by scripts/eval.sh. Can also be run directly.

Output is written to .opencode/evals/<skill>/ for each skill.

The judge uses the same agent CLI as the skill runner. No separate API key needed.
"""

import argparse
import json
import re
import shlex
import subprocess
import sys
from datetime import datetime
import os
import shutil
import tempfile
import time
from pathlib import Path

SKILLS_DIR = Path("skills").resolve()
OUTPUT_DIR = Path(".opencode/evals").resolve()
DEFAULT_AGENT = "opencode run"
EVAL_TIMEOUT = 300
JUDGE_TIMEOUT = 120


def parse_args():
    p = argparse.ArgumentParser(description="Run skill evaluations")
    p.add_argument("--skill", help="Skill to evaluate (default: all)")
    p.add_argument("--agent", default=DEFAULT_AGENT, help=f"Agent CLI (default: {DEFAULT_AGENT})")
    p.add_argument("--judge", default=None, help="Judge agent CLI (default: same as --agent)")
    p.add_argument("--timeout", type=int, default=EVAL_TIMEOUT, help=f"Agent timeout in seconds (default: {EVAL_TIMEOUT})")
    p.add_argument("--judge-timeout", type=int, default=JUDGE_TIMEOUT, help=f"Judge timeout in seconds (default: {JUDGE_TIMEOUT})")
    p.add_argument("--baseline", help="Compare against a previous report.json (e.g., .opencode/evals/history/report-20250101-120000.json)")
    p.add_argument("--keep-workspace", action="store_true", help="Preserve temp workspace after eval")
    p.add_argument("--dry-run", action="store_true", help="List evals without running")
    return p.parse_args()


def discover_skills(skill_name=None):
    skills = sorted(SKILLS_DIR.iterdir())
    results = []
    for d in skills:
        if not d.is_dir():
            continue
        name = d.name
        if skill_name and name != skill_name:
            continue
        evals_path = d / "evals" / "evals.json"
        if not evals_path.exists():
            continue
        results.append((name, d, evals_path))
    return results


def load_skill_content(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ""

    content = skill_md.read_text()
    parts = content.split("---", 2)
    body = parts[2].strip() if len(parts) >= 3 else content.strip()

    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        for f in sorted(refs_dir.iterdir()):
            if f.is_file():
                body += f"\n\n--- Reference: {f.name} ---\n{f.read_text().strip()}"

    return body


def load_evals(evals_path):
    data = json.loads(evals_path.read_text())
    return data.get("evals", [])


def build_eval_prompt(skill_content, eval_data):
    return f"""[SKILL INSTRUCTIONS]
{skill_content}

[USER PROMPT]
{eval_data["prompt"]}"""


def run_agent(agent_cmd, prompt, timeout=EVAL_TIMEOUT):
    parts = shlex.split(agent_cmd)
    full_cmd = parts + [prompt]

    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "error": None,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "", "returncode": -1, "error": "timeout"}
    except FileNotFoundError:
        return {"stdout": "", "stderr": "", "returncode": -1, "error": f"command not found: {agent_cmd}"}
    except Exception as e:
        return {"stdout": "", "stderr": "", "returncode": -1, "error": str(e)}


def judge_response(response_text, expectations, agent_cmd, timeout=JUDGE_TIMEOUT):
    exp_text = "\n".join(f"{i+1}. {e}" for i, e in enumerate(expectations))

    judge_prompt = f"""You are grading whether an AI agent's response meets specific expectations.

Expectations:
{exp_text}

Agent response:
{response_text}

For each expectation, answer YES or NO with a brief one-sentence justification.
Return ONLY a JSON array of objects with keys: "expectation", "passed" (boolean), "reason".
Do not include any other text before or after the JSON array.

Example:
[{{"expectation": "Problem framed before jumping to solution", "passed": true, "reason": "Agent asked clarifying questions before proposing solutions."}},
 {{"expectation": "Trade-offs discussed", "passed": false, "reason": "Agent proposed a single approach without comparing alternatives."}}]"""

    result = run_agent(agent_cmd, judge_prompt, timeout=timeout)
    if result["error"]:
        return [{"expectation": e, "passed": False, "reason": f"Judge agent error: {result['error']}"} for e in expectations]

    output = result["stdout"] or result["stderr"] or ""

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return [{"expectation": e, "passed": False, "reason": f"Judge parse error: output did not contain valid JSON"} for e in expectations]


def main():
    args = parse_args()
    skills = discover_skills(args.skill)

    if not skills:
        print(f"No skills found{f' matching {args.skill!r}' if args.skill else ''}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_results = {}
    total_passed = 0
    total_evals = 0
    any_failures = False

    for skill_name, skill_dir, evals_path in skills:
        print(f"\n{'=' * 60}")
        print(f"Skill: {skill_name}")
        print(f"{'=' * 60}")

        skill_content = load_skill_content(skill_dir)
        evals = load_evals(evals_path)

        if not evals:
            print("  No evals found")
            continue

        print(f"  Evals: {len(evals)}")

        skill_out = OUTPUT_DIR / skill_name
        skill_out.mkdir(parents=True, exist_ok=True)

        skill_results = []
        skill_passed = 0
        skill_total = 0

        for i, ev in enumerate(evals):
            prompt_text = ev.get("prompt", "")
            expectations = ev.get("expectations", [])

            label = prompt_text[:80].replace("\n", " ")
            print(f"\n  [{i + 1}] {label}...")

            if args.dry_run:
                for j, exp in enumerate(expectations):
                    print(f"       expect: {exp[:70]}...")
                continue

            # Create isolated workspace
            workspace = Path(tempfile.mkdtemp(prefix="kiss-eval-"))
            original_cwd = Path.cwd()
            try:
                # Copy fixtures into workspace
                fixt_dir = skill_dir / "evals" / "fixtures"
                if fixt_dir.exists():
                    dest = workspace / fixt_dir.relative_to(SKILLS_DIR.parent)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.copytree(fixt_dir, dest, dirs_exist_ok=True)
                    except (OSError, shutil.Error) as e:
                        print(f"       ERROR copying fixtures from {fixt_dir}: {e}")

                # Run agent from workspace
                os.chdir(str(workspace))
                combined = build_eval_prompt(skill_content, ev)
                t0 = time.time()

                print(f"       running agent...", end=" ", flush=True)
                response = run_agent(args.agent, combined, timeout=args.timeout)
                elapsed = time.time() - t0
                print(f"({elapsed:.1f}s / timeout: {args.timeout}s)")

                (skill_out / f"response-{i}.json").write_text(json.dumps(response, indent=2))

                if response["error"]:
                    print(f"       ERROR: {response['error']}")
                    grades = [{"expectation": e, "passed": False, "reason": f"Agent error: {response['error']}"} for e in expectations]
                else:
                    output = response["stdout"] or response["stderr"] or ""
                    judge_cmd = args.judge if args.judge else args.agent
                    print(f"       judging ({len(output)} chars)...", end=" ", flush=True)
                    t0 = time.time()
                    grades = judge_response(output, expectations, judge_cmd, timeout=args.judge_timeout)
                    elapsed = time.time() - t0
                    print(f"({elapsed:.1f}s / timeout: {args.judge_timeout}s)")

                (skill_out / f"grade-{i}.json").write_text(json.dumps(grades, indent=2))

                n_pass = sum(1 for g in grades if g.get("passed"))
                n_total = len(grades)
                skill_passed += n_pass
                skill_total += n_total
                total_passed += n_pass
                total_evals += n_total

                if n_pass < n_total:
                    any_failures = True

                print(f"       {n_pass}/{n_total} passed")
                for g in grades:
                    mark = "PASS" if g.get("passed") else "FAIL"
                    print(f"         [{mark}] {g.get('expectation', '?')[:70]}")

                skill_results.append({
                    "eval_index": i,
                    "prompt": prompt_text[:100],
                    "passed": n_pass,
                    "total": n_total,
                    "grades": grades,
                })
            finally:
                os.chdir(str(original_cwd))
                if args.keep_workspace:
                    print(f"       workspace preserved: {workspace}")
                else:
                    shutil.rmtree(workspace, ignore_errors=True)

        if not args.dry_run and skill_total > 0:
            summary = {
                "skill": skill_name,
                "results": skill_results,
                "passed": skill_passed,
                "total": skill_total,
                "pass_rate": round(skill_passed / skill_total, 3),
            }
            (skill_out / "summary.json").write_text(json.dumps(summary, indent=2))
            all_results[skill_name] = summary

    if not args.dry_run and total_evals > 0:
        rate = (total_passed / total_evals) * 100
        print(f"\n{'=' * 60}")
        print(f"OVERALL: {total_passed}/{total_evals} expectations met ({rate:.1f}%)")
        print(f"{'=' * 60}")

        # Archive previous report before overwriting
        history_dir = OUTPUT_DIR / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        if (OUTPUT_DIR / "report.json").exists():
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.copy(OUTPUT_DIR / "report.json", history_dir / f"report-{timestamp}.json")

        (OUTPUT_DIR / "report.json").write_text(json.dumps(all_results, indent=2))

        # Baseline comparison
        if args.baseline:
            baseline_path = Path(args.baseline)
            if not baseline_path.exists():
                print(f"WARNING: baseline file not found: {args.baseline}")
            else:
                baseline = json.loads(baseline_path.read_text())
                print(f"\nBaseline comparison against {args.baseline}:")
                regressions = False
                for skill_name, current in sorted(all_results.items()):
                    if skill_name in baseline:
                        prev_rate = baseline[skill_name]["pass_rate"]
                        curr_rate = current["pass_rate"]
                        delta = curr_rate - prev_rate
                        marker = " *** REGRESSION ***" if delta < -0.1 else ""
                        if delta < -0.1:
                            regressions = True
                        print(f"  {skill_name}: {prev_rate*100:.0f}% \u2192 {curr_rate*100:.0f}% ({delta*100:+.0f}pp){marker}")
                    else:
                        print(f"  {skill_name}: (new, no baseline)")
                if regressions:
                    print("WARNING: One or more skills regressed by more than 10pp")

    sys.exit(1 if any_failures else 0)


if __name__ == "__main__":
    main()
