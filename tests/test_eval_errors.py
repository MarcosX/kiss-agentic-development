import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import eval


def test_run_agent_marks_nonzero_exit_as_error():
    result = eval.run_agent("python3 -c 'import sys; sys.exit(3)'", "", timeout=5)
    assert result["returncode"] == 3
    assert result["error"], "non-zero exit should be recorded as an error"


def test_run_agent_marks_timeout_as_error():
    result = eval.run_agent("python3 -c 'import time; time.sleep(5)'", "", timeout=1)
    assert result["returncode"] == -1
    assert result["error"] == "timeout"


def test_run_agent_success_has_no_error():
    result = eval.run_agent("python3 -c 'print(\"ok\")'", "", timeout=5)
    assert result["returncode"] == 0
    assert result["error"] is None
    assert "ok" in result["stdout"]


def test_run_agent_uses_cwd_for_child_and_pwd_env(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    env = os.environ.copy()
    env["PWD"] = "/some/stale/root"
    result = eval.run_agent(
        "python3 -c 'import os; print(os.getcwd()); print(os.environ.get(\"PWD\"))'",
        "",
        timeout=5,
    )
    cwd_line, pwd_line = result["stdout"].strip().splitlines()
    assert cwd_line == str(tmp_path), "child process must run in the eval workspace"
    assert pwd_line == str(tmp_path), "PWD env must match the eval workspace, not the stale repo root"


def test_run_agent_pwd_env_matches_workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = eval.run_agent(
        "python3 -c 'import os; print(os.environ[\"PWD\"])'",
        "",
        timeout=5,
    )
    assert result["stdout"].strip() == str(tmp_path)


@pytest.fixture
def fake_skill(tmp_path):
    skill_dir = tmp_path / "skills" / "demo"
    (skill_dir / "evals").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Use when testing.\n---\nbody"
    )
    (skill_dir / "evals" / "evals.json").write_text(
        json.dumps(
            {
                "evals": [
                    {"prompt": "Do the thing", "expectations": ["Agent completes it"]}
                ]
            }
        )
    )
    return tmp_path, skill_dir


def run_pipeline(tmp_path, agent_cmd, monkeypatch):
    monkeypatch.setattr(eval, "SKILLS_DIR", tmp_path / "skills")
    out_dir = tmp_path / "out"
    monkeypatch.setattr(eval, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(
        sys,
        "argv",
        ["eval.py", "--skill", "demo", "--agent", agent_cmd, "--timeout", "2", "--judge-timeout", "5"],
    )
    with pytest.raises(SystemExit) as exc:
        eval.main()
    return exc.value.code, out_dir


def test_crash_is_reported_as_error_not_eval_failure(tmp_path, fake_skill, monkeypatch, capsys):
    code, out_dir = run_pipeline(
        tmp_path,
        "python3 -c 'import sys; sys.exit(3)'",
        monkeypatch,
    )
    captured = capsys.readouterr()
    summary = json.loads((out_dir / "demo" / "summary.json").read_text())

    assert code == 1
    assert "ERROR" in captured.out, "error should be visibly displayed in console"
    assert summary["errors"] == 1, "crash should be tracked separately"
    assert summary["total"] == 0, "errored eval must not pollute pass-rate total"
    assert summary["pass_rate"] == 0.0


def test_timeout_is_reported_as_error_not_eval_failure(tmp_path, fake_skill, monkeypatch, capsys):
    code, out_dir = run_pipeline(
        tmp_path,
        "python3 -c 'import time; time.sleep(5)'",
        monkeypatch,
    )
    captured = capsys.readouterr()
    summary = json.loads((out_dir / "demo" / "summary.json").read_text())

    assert code == 1
    assert "ERROR" in captured.out, "error should be visibly displayed in console"
    assert summary["errors"] == 1, "timeout should be tracked separately"
    assert summary["total"] == 0, "errored eval must not pollute pass-rate total"


def test_pass_and_error_mixed(tmp_path, fake_skill, monkeypatch):
    skill_dir = tmp_path / "skills" / "demo"
    evals_path = skill_dir / "evals" / "evals.json"
    evals_path.write_text(
        json.dumps(
            {
                "evals": [
                    {"prompt": "Pass one", "expectations": ["ok"]},
                    {"prompt": "Crash one", "expectations": ["ok"]},
                ]
            }
        )
    )

    real_run_agent = eval.run_agent

    def fake_run_agent(agent_cmd, prompt, timeout=eval.EVAL_TIMEOUT):
        if "Pass one" in prompt:
            return real_run_agent("python3 -c 'print(\"agent output\")'", prompt, timeout)
        return {"stdout": "", "stderr": "", "returncode": 3, "error": "agent exited with code 3"}

    def fake_judge(response_text, expectations, agent_cmd, timeout=eval.JUDGE_TIMEOUT):
        return [{"expectation": e, "passed": True, "reason": "done"} for e in expectations]

    monkeypatch.setattr(eval, "run_agent", fake_run_agent)
    monkeypatch.setattr(eval, "judge_response", fake_judge)
    monkeypatch.setattr(eval, "SKILLS_DIR", tmp_path / "skills")
    out_dir = tmp_path / "out"
    monkeypatch.setattr(eval, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(
        sys,
        "argv",
        ["eval.py", "--skill", "demo", "--agent", "python3 fake.py", "--timeout", "2", "--judge-timeout", "5"],
    )
    with pytest.raises(SystemExit) as exc:
        eval.main()
    summary = json.loads((out_dir / "demo" / "summary.json").read_text())

    assert exc.value.code == 1
    assert summary["errors"] == 1, "crash tracked as error, not eval failure"
    assert summary["passed"] == 1
    assert summary["total"] == 1, "pass rate only counts evals that actually ran"
    assert summary["pass_rate"] == 1.0
    errored = [r for r in summary["results"] if "error" in r]
    assert errored and errored[0]["error"] == "agent exited with code 3"


def test_agent_artifacts_stay_in_workspace_not_repo_root(tmp_path, monkeypatch):
    skill_dir = tmp_path / "skills" / "demo"
    (skill_dir / "evals").mkdir(parents=True)
    evals_path = skill_dir / "evals" / "evals.json"
    evals_path.write_text(
        json.dumps(
            {
                "evals": [
                    {
                        "prompt": "Create a file called artifact.txt in the working directory",
                        "expectations": ["ok"],
                    }
                ]
            }
        )
    )
    ws_root = tmp_path / "workspaces"
    ws_root.mkdir()
    import tempfile

    counter = [0]

    def fake_mkdtemp(**kwargs):
        counter[0] += 1
        d = ws_root / f"kiss-eval-{counter[0]}"
        d.mkdir()
        return str(d)

    monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)
    real_run_agent = eval.run_agent

    def fake_run_agent(agent_cmd, prompt, timeout=eval.EVAL_TIMEOUT):
        if "artifact.txt" in prompt:
            return real_run_agent(
                "python3 -c 'import os; print(os.environ.get(\"PWD\"))'",
                prompt,
                timeout,
            )
        return {"stdout": "", "stderr": "", "returncode": 3, "error": "agent exited with code 3"}

    def fake_judge(response_text, expectations, agent_cmd, timeout=eval.JUDGE_TIMEOUT):
        return [{"expectation": e, "passed": True, "reason": "done"} for e in expectations]

    monkeypatch.setattr(eval, "run_agent", fake_run_agent)
    monkeypatch.setattr(eval, "judge_response", fake_judge)
    monkeypatch.setattr(eval, "SKILLS_DIR", tmp_path / "skills")
    out_dir = tmp_path / "out"
    monkeypatch.setattr(eval, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(
        sys,
        "argv",
        ["eval.py", "--skill", "demo", "--agent", "python3 fake.py", "--timeout", "5", "--judge-timeout", "5"],
    )
    with pytest.raises(SystemExit):
        eval.main()

    response = json.loads((out_dir / "demo" / "response-0.json").read_text())
    agent_pwd = response["stdout"].strip()
    assert agent_pwd.startswith(str(ws_root)), (
        f"agent PWD must resolve to the isolated workspace (got {agent_pwd!r}, expected under {ws_root})"
    )
    assert not (tmp_path / "artifact.txt").exists(), "no artifacts may leak to the repo root"
