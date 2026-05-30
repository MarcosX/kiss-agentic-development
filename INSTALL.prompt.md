# Install Instructions

Install the [kiss-agentic-development](https://github.com/MarcosX/kiss-agentic-development) skills collection.

---

## 1. Detect your environment

- **OpenCode** — config at `.opencode/opencode.json` or `~/.config/opencode/opencode.json`. Plugin system available.
- **Claude Code** — reads `~/.claude/CLAUDE.md`, skills in `.claude/skills/` or `~/.claude/skills/`.
- **GitHub Copilot** — reads global instructions at `~/.copilot/copilot-instructions.md`, skills in `.github/skills/`, `~/.agents/skills/`, or `~/.copilot/skills/`.
- **Cursor** — User Rules in Settings > Rules, project rules in `.cursor/rules/`, skills in `.cursor/skills/` or `~/.agents/skills/`.

If you are running inside one of these, follow that agent's section below.

If you are running inside a different agent, look at your tool's documentation to find:

- Where to store `SKILL.md` files (project-level or global skills directory)
- How to configure always-on instructions (equivalent of `instructions`, `CLAUDE.md`, or `copilot-instructions.md`)
- Then apply the same pattern using `~/.agents/skills/<name>/SKILL.md` as the target path after install.

---

## 2. Install the skill files

### Preferred: use `npx skills`

First check if the `skills` CLI is available:

```bash
npx skills --help
```

If it works, install all skills globally:

```bash
npx skills add MarcosX/kiss-agentic-development --global --all
```

Or install to a specific agent:

```bash
npx skills add MarcosX/kiss-agentic-development --global --agent opencode
npx skills add MarcosX/kiss-agentic-development --global --agent claude-code
```

### Fallback: clone the repo

If `npx skills` is not available, clone the repo and copy the skills into the correct directory for the agent you're running.

```bash
# Clone
git clone https://github.com/MarcosX/kiss-agentic-development.git /tmp/kiss-agentic-dev

# Pick the right target path based on the agent (see table below)
# Then copy the skills:
cp -r /tmp/kiss-agentic-dev/skills/* <TARGET_PATH>/
```

After the initial install, keep a reference to the clone location or the remote URL so you can re-pull later for updates.

| Agent          | Global (all projects)                       | Project (repo-scoped) |
| -------------- | ------------------------------------------- | --------------------- |
| OpenCode       | `~/.config/opencode/skills/`                | `.opencode/skills/`   |
| Claude Code    | `~/.claude/skills/`                         | `.claude/skills/`     |
| GitHub Copilot | `~/.copilot/skills/` or `~/.agents/skills/` | `.github/skills/`     |
| Cursor         | `~/.cursor/skills/` or `~/.agents/skills/`  | `.cursor/skills/`     |

---

## 3. Configure auto-loading for `using-skills`

After installation, configure your agent to load `using-skills` at the start of every session so it always checks for skills before acting.

### OpenCode

The `instructions` field injects the SKILL.md content directly into every session — the agent will already have the skill loaded and does **not** need to invoke the `skill` tool.

Add to `~/.config/opencode/opencode.json`:

```json
{
  "instructions": ["~/.agents/skills/using-skills/SKILL.md"]
}
```

If `npx skills` was not used and skills were installed manually, adjust the path to match where you placed them (e.g. `~/.config/opencode/skills/using-skills/SKILL.md`).

### Claude Code

Add to `~/.claude/CLAUDE.md`:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

### GitHub Copilot

Create or edit `~/.copilot/copilot-instructions.md`:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

### Cursor

1. Open Cursor Settings > Rules > User Rules
2. Add:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

For project-level only, create `.cursor/rules/using-skills.mdc`:

```yaml
---
description: Always check and invoke skills before acting
alwaysApply: true
---
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

---

## 4. Verify

Open a new session with your agent and ask:

> What skills are available?

The agent should list all 7 skills:

- `using-skills` — Skill discovery and invocation before any action
- `brainstorming` — Design before implementation
- `writing-plans` — Executable plans with acceptance criteria
- `executing-plans` — Isolated subagent tasks with review gates
- `practicing-tdd` — Test-first discipline
- `reviewing-code` — Five-axis structured review
- `debugging` — Root cause investigation before fixes

If the agent immediately checks for skills before responding to your question, `using-skills` is loading correctly.

You can also verify the installed version directly:

```bash
head -4 ~/.agents/skills/brainstorming/SKILL.md
```

The description field should match the table above (e.g. "Use when the prompt asks to brainstorm...").

---

## 5. Updating

To update the skills to the latest version:

### If installed via `npx skills`

`npx skills update` may fail for this repo. Instead, re-add to force a fresh clone:

```bash
npx skills add MarcosX/kiss-agentic-development --global --all -y
```

### If installed via fallback clone

```bash
cd /tmp/kiss-agentic-dev && git pull origin main
cp -r /tmp/kiss-agentic-dev/skills/* <TARGET_PATH>/
```

After updating, verify the version with the `head` command above.
