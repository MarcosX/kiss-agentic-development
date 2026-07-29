#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Run skill evaluations against an agent CLI and judge results.

Options:
  --skill <name>       Skill to evaluate (default: all skills)
  --agent <cmd>        Agent CLI command (default: "opencode run")
  --judge <cmd>        Judge agent CLI (default: same as --agent)
  --timeout <secs>     Agent timeout in seconds (default: 300)
  --judge-timeout <secs>  Judge timeout in seconds (default: 120)
  --baseline <path>    Compare against a previous report.json
  --keep-workspace     Preserve temp workspace after eval
  --dry-run            List evals without running them
  -h, --help           Show this help message

Examples:
  $(basename "$0") --skill brainstorming
  $(basename "$0") --skill brainstorming --agent "opencode run --format json"
  $(basename "$0") --dry-run
EOF
  exit 0
}

# Parse args
SKILL=""
AGENT="opencode run"
JUDGE=""
TIMEOUT=""
JUDGE_TIMEOUT=""
BASELINE=""
KEEP_WORKSPACE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill)
      SKILL="$2"
      shift 2
      ;;
    --agent)
      AGENT="$2"
      shift 2
      ;;
    --judge)
      JUDGE="$2"
      shift 2
      ;;
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --judge-timeout)
      JUDGE_TIMEOUT="$2"
      shift 2
      ;;
    --baseline)
      BASELINE="$2"
      shift 2
      ;;
    --keep-workspace)
      KEEP_WORKSPACE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

# Check Python
if ! command -v "$PYTHON" &>/dev/null; then
  echo "ERROR: python3 not found. Install Python 3.8+."
  exit 1
fi

# Build args for Python
PY_ARGS=()
if [ -n "$SKILL" ]; then
  PY_ARGS+=(--skill "$SKILL")
fi
if [ -n "$AGENT" ]; then
  PY_ARGS+=(--agent "$AGENT")
fi
if [ -n "$JUDGE" ]; then
  PY_ARGS+=(--judge "$JUDGE")
fi
if [ -n "$TIMEOUT" ]; then
  PY_ARGS+=(--timeout "$TIMEOUT")
fi
if [ -n "$JUDGE_TIMEOUT" ]; then
  PY_ARGS+=(--judge-timeout "$JUDGE_TIMEOUT")
fi
if [ -n "$BASELINE" ]; then
  PY_ARGS+=(--baseline "$BASELINE")
fi
if [ "$KEEP_WORKSPACE" = true ]; then
  PY_ARGS+=(--keep-workspace)
fi
if [ "$DRY_RUN" = true ]; then
  PY_ARGS+=(--dry-run)
fi

exec "$PYTHON" "$SCRIPT_DIR/eval.py" "${PY_ARGS[@]}"
