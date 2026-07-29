#!/usr/bin/env bash
set -euo pipefail

SKILLS_DIR="skills"
errors=0

for skill_dir in "$SKILLS_DIR"/*/; do
  skill=$(basename "$skill_dir")
  # Skip directories starting with underscore (internal/fixture dirs)
  if [[ "$skill" == _* ]]; then
    continue
  fi
  skill_md="$skill_dir/SKILL.md"
  evals_json="$skill_dir/evals/evals.json"

  echo "=== $skill ==="

  if [ ! -f "$skill_md" ]; then
    echo "  FAIL: SKILL.md not found"
    errors=$((errors + 1))
    continue
  fi

  name=$(head -5 "$skill_md" | grep -E '^name: ' | sed 's/^name: //' | tr -d '[:space:]')
  description=$(head -10 "$skill_md" | grep -E '^description: ' | sed 's/^description: //')

  if [ -z "$name" ]; then
    echo "  FAIL: name not found in frontmatter"
    errors=$((errors + 1))
  else
    echo "  name: $name"
  fi

  if [ -z "$description" ]; then
    echo "  FAIL: description not found in frontmatter"
    errors=$((errors + 1))
  else
    echo "  description: ${description:0:60}..."
  fi

  if [ ! -f "$evals_json" ]; then
    echo "  FAIL: evals/evals.json not found"
    errors=$((errors + 1))
  else
    count=$(python3 -c "import json; d=json.load(open('$evals_json')); print(len(d.get('evals', [])))" 2>/dev/null || echo "parse-error")
    if [ "$count" = "parse-error" ]; then
      echo "  FAIL: evals.json is not valid JSON"
      errors=$((errors + 1))
    elif [ "$count" -lt 3 ]; then
      echo "  FAIL: evals.json has $count evals (need at least 3)"
      errors=$((errors + 1))
    else
      echo "  evals: $count scenarios"
    fi
  fi

  echo ""
done

if [ "$errors" -gt 0 ]; then
  echo "FAILED: $errors validation errors"
  exit 1
else
  echo "All skills validated successfully."
fi
