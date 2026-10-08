# Install Instructions

Install the [kiss-agentic-development](https://github.com/MarcosX/kiss-agentic-development) skills collection.

---

## 1. Detect your environment

Determine which tool is running this prompt:

- **OpenCode** — global config at `~/.config/opencode/opencode.json`
- **Claude Code** — global instructions in `~/.claude/CLAUDE.md`
- **GitHub Copilot** — global instructions at `~/.copilot/copilot-instructions.md`
- **Cursor** — User Rules in Settings > Rules, or `.cursor/rules/*.mdc` with `alwaysApply: true`
- **Other** — find where your tool reads global instructions, then follow the same pattern below

Then check whether Node.js is available:

```bash
command -v npx
```

Steering rule for steps 2, 4, and 5: if `npx` is available, use the `npx skills` path (2A, and later 5A). If Node.js is not installed or the user prefers not to use `npx skills`, use the manual path (2B, and later 5B). Both paths are complete — either one fully installs the skills.

---

## 2. Install domain skills

Both paths install the skills to your tool's global skills path:

| Agent          | Global skills path                          |
| -------------- | ------------------------------------------- |
| OpenCode       | `~/.config/opencode/skills/`                |
| Claude Code    | `~/.claude/skills/`                         |
| GitHub Copilot | `~/.copilot/skills/` or `~/.agents/skills/` |
| Cursor         | `~/.cursor/skills/` or `~/.agents/skills/`  |

### 2A. Install with `npx skills` (requires Node.js)

The [skills CLI](https://github.com/vercel-labs/skills) installs every skill in this repo to your agent's global skills directory:

```bash
npx skills add MarcosX/kiss-agentic-development -g -y -a <AGENT>
```

Replace `<AGENT>` with the CLI name for the tool detected in step 1: `opencode`, `claude-code`, `github-copilot`, or `cursor`. Omit `-a` to let the CLI install to every agent it detects. The CLI creates symlinks to a canonical copy by default — that is fine; pass `--copy` only if symlinks are not supported on your system.

Known difference from the manual path: the CLI copies each skill directory as-is, so each skill's `evals/` directory may be installed too. Evaluation fixtures are development-only and no skill references them at runtime.

### 2B. Install manually (git clone + copy)

Clone the repo and copy the skills to your agent's skills path:

```bash
git clone https://github.com/MarcosX/kiss-agentic-development.git /tmp/kiss-agentic-dev
```

Then pick the target path for your tool and copy the skills:

```bash
for skill in /tmp/kiss-agentic-dev/skills/*/; do
  name=$(basename "$skill")
  mkdir -p "<TARGET_PATH>/$name"
  for item in "$skill"*; do
    [ "$(basename "$item")" = "evals" ] && continue
    cp -r "$item" "<TARGET_PATH>/$name/"
  done
done
```

The loop skips each skill's `evals/` directory; evaluation fixtures are development-only and no skill references them at runtime.

---

## 3. Install the using-skills global instruction

The skills CLI manages skill files only — this step is manual in both paths. Copy the following content into your tool's global instructions file:

```
# Using Skills

<HARD-GATE>
Before responding to any user message, check the available skills. If any skill applies, you MUST load it and follow it. Responding without loading an applicable skill — or loading it and then not following it — is a violation. Stop and do it properly.
</HARD-GATE>

## Every response

Begin every response with exactly one line, then continue:

- "Using [skill] to [goal]." — when a skill applies (load and follow it)
- "No applicable skill." — only when none does

A response without this line is non-compliant; rewrite it before sending.

## When to load

Load a skill whenever there is any chance it applies, not only when you're sure. The signal scan is the floor, not the ceiling.

- bug, error, crash, fail, unexpected → `debugging`
- idea, approach, explore, design → `brainstorming`
- plan, implement, build, add, feature → `writing-plans`

Process skills first (`brainstorming`, `debugging`), implementation skills after.

## After loading

1. Restate the skill's key rules in your own words in that response. If you can't, re-read it.
2. Create TODOs for each step the skill prescribes.
3. Follow the skill's workflow. User instructions define WHAT; the skill defines HOW.
4. Before sending, check your work against the skill's gates and checklists. If a step is missing, do it — don't ship around it.

## Rationalizing

These thoughts are how agents skip skills. If you catch yourself thinking one, stop and load the skill:

- "This is just a simple question" / "I'll quickly check files"
- "Just a high-level answer is fine" / "Keep it short" / "Quick question"
- "Let me explore the codebase first" / "Let me gather information first"
- "I know what that means" / "This doesn't need a skill" / "The skill is overkill"
- "I'll just do this thing first" / "Let me investigate this" / "Let me understand the problem first"
- "I already know what skill I need"
```

### OpenCode

1. Save the above content to `~/.config/opencode/AGENTS.md` (OpenCode v2 loads global instructions only from `AGENTS.md`).

### Claude Code

Append the above content to `~/.claude/CLAUDE.md`.

### GitHub Copilot

Append the above content to `~/.copilot/copilot-instructions.md`.

### Cursor

Append the above content to:

- **Global**: Cursor Settings > Rules > User Rules
- **Project-level**: Create `.cursor/rules/using-skills.mdc` with `alwaysApply: true` and the content

---

## 4. Verify

Restart your agent session (new global instructions take effect on session start).

Then run this self-check prompt:

> What should you do before responding to me?

**Expected behavior**: The agent explains that it checks for and invokes skills before acting. It does NOT mention loading a skill called "using-skills" — the behavior is automatic, not something it loads on demand.

You can also confirm the domain skills are installed — use the check for the path you used in step 2:

```bash
# Path 2A (npx skills)
npx skills list -g

# Path 2B (manual)
ls <TARGET_PATH>/
# Expected: brainstorming  debugging  executing-plans  practicing-tdd  reviewing-code  writing-plans
```

For the manual check, replace `<TARGET_PATH>` with the path you copied skills to (see table in section 2).

---

## 5. Updating

### Domain skills

Use the same path you used in step 2.

#### 5A. With `npx skills`

```bash
npx skills update -g -y
```

Updates every skill installed from this repo. Pass a skill name (e.g. `npx skills update -g brainstorming`) to update only that one.

#### 5B. Manually (git clone + copy)

```bash
cd /tmp/kiss-agentic-dev && git pull
for skill in skills/*/; do
  name=$(basename "$skill")
  mkdir -p "<TARGET_PATH>/$name"
  for item in "$skill"*; do
    [ "$(basename "$item")" = "evals" ] && continue
    cp -r "$item" "<TARGET_PATH>/$name/"
  done
done
```

The loop skips each skill's `evals/` directory; evaluation fixtures are development-only and no skill references them at runtime.

The copy runs from the clone directory, which the `cd` above sets up.

Replace `<TARGET_PATH>` with your tool's skills path (see table in section 2).

### using-skills instruction

Update your global instructions to match the content in section 3 above (the canonical version is in `instructions/using-skills.md` in the repo).

Restart your session for changes to take effect.
