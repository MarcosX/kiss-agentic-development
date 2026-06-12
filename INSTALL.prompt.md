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

---

## 2. Install domain skills

### Preferred: use `npx skills`

```bash
npx skills add MarcosX/kiss-agentic-development#latest --global --all
```

This installs the 6 domain skills to `~/.agents/skills/`.

### Fallback: clone the repo

```bash
git clone https://github.com/MarcosX/kiss-agentic-development.git /tmp/kiss-agentic-dev
```

Then pick the target path for your tool and copy the skills:

```bash
cp -r /tmp/kiss-agentic-dev/skills/* <TARGET_PATH>/
```

| Agent          | Global skills path                          |
| -------------- | ------------------------------------------- |
| OpenCode       | `~/.config/opencode/skills/`                |
| Claude Code    | `~/.claude/skills/`                         |
| GitHub Copilot | `~/.copilot/skills/` or `~/.agents/skills/` |
| Cursor         | `~/.cursor/skills/` or `~/.agents/skills/`  |

---

## 3. Install the using-skills global instruction

`using-skills` is NOT a skill. It is a global instruction that tells the agent to always check for and invoke skills before acting. It must be present in every session.

Read the content of `instructions/using-skills.md` (from the cloned repo or the [raw GitHub URL](https://raw.githubusercontent.com/MarcosX/kiss-agentic-development/refs/tags/latest/instructions/using-skills.md)) and add it to your tool's global instructions.

### OpenCode

1. Create the instructions directory and copy the file:

```bash
mkdir -p ~/.config/opencode/instructions/
cp /tmp/kiss-agentic-dev/instructions/using-skills.md ~/.config/opencode/instructions/using-skills.md
# OR if using npx skills (no repo clone):
curl -o ~/.config/opencode/instructions/using-skills.md \
  https://raw.githubusercontent.com/MarcosX/kiss-agentic-development/refs/tags/latest/instructions/using-skills.md
```

2. Add to `~/.config/opencode/opencode.json`:

```json
{
  "instructions": ["~/.config/opencode/instructions/using-skills.md"]
}
```

### Claude Code

Append the content of `instructions/using-skills.md` to `~/.claude/CLAUDE.md`.

### GitHub Copilot

Append the content of `instructions/using-skills.md` to `~/.copilot/copilot-instructions.md`.

### Cursor

Append the content of `instructions/using-skills.md` to:
- **Global**: Cursor Settings > Rules > User Rules
- **Project-level**: Create `.cursor/rules/using-skills.mdc` with `alwaysApply: true` and the content

---

## 4. Verify

Restart your agent session (new global instructions take effect on session start).

Then run this self-check prompt:

> What should you do before responding to me?

**Expected behavior**: The agent explains that it checks for and invokes skills before acting. It does NOT mention loading a skill called "using-skills" — the behavior is automatic, not something it loads on demand.

You can also confirm the domain skills are installed:

```bash
ls ~/.agents/skills/
# Expected: brainstorming  debugging  executing-plans  practicing-tdd  reviewing-code  writing-plans
```

---

## 5. Updating

### Domain skills

```bash
npx skills add MarcosX/kiss-agentic-development#latest --global --all -y
```

### using-skills instruction

Re-fetch the latest `instructions/using-skills.md` and overwrite your copy:

```bash
# OpenCode
curl -o ~/.config/opencode/instructions/using-skills.md \
  https://raw.githubusercontent.com/MarcosX/kiss-agentic-development/refs/tags/latest/instructions/using-skills.md
```

For other tools, re-read the raw file and replace the old content in your global instructions file.

Restart your session for changes to take effect.
