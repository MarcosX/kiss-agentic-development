#!/usr/bin/env python3
"""
Run skill evaluations against an agent CLI and judge results.

Invoked by scripts/eval.sh. Can also be run directly.

Output is written to .opencode/evals/<skill>/ for each skill.
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

SKILLS_DIR = Path("skills")
OUTPUT_DIR = Path(".opencode/evals")
DEFAULT_AGENT = "opencode run"
DEFAULT_JUDGE_MODEL = "claude-sonnet-4-20250514"
EVAL_TIMEOUT = 180
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def parse_args():
    p = argparse.ArgumentParser(description="Run skill evaluations")
    p.add_argument("--skill", help="Skill to evaluate (default: all)")
    p.add_argument("--agent", default=DEFAULT_AGENT, help=f"Agent CLI (default: {DEFAULT_AGENT})")
    p.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL, help=f"Judge model (default: {DEFAULT_JUDGE_MODEL})")
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


def call_anthropic(prompt, model, max_tokens=2000):
    api_key = os.environ.get("OPENCODE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = Request(
        ANTHROPIC_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )

    try:
        resp = urlopen(req, timeout=30)
        data = json.loads(resp.read())
        content = data.get("content", [])
        return content[0]["text"] if content else None
    except URLError as e:
        return None


def judge_response(response_text, expectations, model):
    api_key = os.environ.get("OPENCODE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return [{"expectation": e, "passed": False, "reason": "Set OPENCODE_API_KEY or ANTHROPIC_API_KEY for judging"} for e in expectations]

    exp_text = "\n".join(f"{i+1}. {e}" for i, e in enumerate(expectations))

    judge_prompt = f"""You are grading whether an AI agent's response meets specific expectations.

Expectations:
{exp_text}

Agent response:
{response_text}

For each expectation, answer YES or NO with a brief one-sentence justification.
Format your response as a JSON array of objects with keys: "expectation", "passed" (boolean), "reason".

Example:
[
  {{"expectation": "Problem framed before jumping to solution", "passed": true, "reason": "Agent asked clarifying questions before proposing solutions."}},
  {{"expectation": "Trade-offs discussed", "passed": false, "reason": "Agent proposed a single approach without comparing alternatives."}}
]"""

    result = call_anthropic(judge_prompt, model)
    if not result:
        return [{"expectation": e, "passed": False, "reason": "Judge API call failed"} for e in expectations]

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", result, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return [{"expectation": e, "passed": False, "reason": f"Judge parse error"} for e in expectations]


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

            # Run agent
            combined = build_eval_prompt(skill_content, ev)
            t0 = time.time()

            print(f"       running agent...", end=" ", flush=True)
            response = run_agent(args.agent, combined)
            elapsed = time.time() - t0
            print(f"({elapsed:.1f}s)")

            (skill_out / f"response-{i}.json").write_text(json.dumps(response, indent=2))

            if response["error"]:
                print(f"       ERROR: {response['error']}")
                grades = [{"expectation": e, "passed": False, "reason": f"Agent error: {response['error']}"} for e in expectations]
            else:
                output = response["stdout"] or response["stderr"] or ""
                print(f"       judging ({len(output)} chars)...", end=" ", flush=True)
                t0 = time.time()
                grades = judge_response(output, expectations, args.judge_model)
                elapsed = time.time() - t0
                print(f"({elapsed:.1f}s)")

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
        (OUTPUT_DIR / "report.json").write_text(json.dumps(all_results, indent=2))

    sys.exit(1 if any_failures else 0)


if __name__ == "__main__":
    main()
