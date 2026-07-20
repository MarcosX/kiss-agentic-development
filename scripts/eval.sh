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
  --judge-model <id>   Model for judging (default: claude-sonnet-4-20250514)
  --dry-run            List evals without running them
  -h, --help           Show this help message

Environment:
  OPENCODE_API_KEY      Anthropic API key for judge (or ANTHROPIC_API_KEY)

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
JUDGE_MODEL="claude-sonnet-4-20250514"
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
    --judge-model)
      JUDGE_MODEL="$2"
      shift 2
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
if [ -n "$JUDGE_MODEL" ]; then
  PY_ARGS+=(--judge-model "$JUDGE_MODEL")
fi
if [ "$DRY_RUN" = true ]; then
  PY_ARGS+=(--dry-run)
fi

exec "$PYTHON" "$SCRIPT_DIR/eval.py" "${PY_ARGS[@]}"
