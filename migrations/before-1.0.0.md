# Migration: Before 1.0.0

This migration is only needed if you installed `kiss-agentic-development` before the 1.0.0 release — when `using-skills` was a skill in `skills/` that you loaded via the `skill` tool.

If you are installing for the first time, skip this file. The regular install instructions handle everything.

---

## Steps

### 1. Remove the old `using-skills` skill directory

```bash
rm -rf ~/.agents/skills/using-skills/
```

### 2. Re-install domain skills

```bash
git clone https://github.com/MarcosX/kiss-agentic-development.git /tmp/kiss-agentic-dev
cp -r /tmp/kiss-agentic-dev/skills/* ~/.agents/skills/
```

This installs only the 6 domain skills. The old `using-skills/` directory will not return.

### 3. Update global instructions

Replace the old "load the `using-skills` skill" pattern with the content of `instructions/using-skills.md` directly in your tool's global instructions.

**OpenCode** — `~/.config/opencode/opencode.json`:
- Remove `"~/.agents/skills/using-skills/SKILL.md"` from the `instructions` array
- Add `"~/.config/opencode/instructions/using-skills.md"`
- Copy the instructions file:

```bash
mkdir -p ~/.config/opencode/instructions/
curl -o ~/.config/opencode/instructions/using-skills.md \
  https://raw.githubusercontent.com/MarcosX/kiss-agentic-development/refs/tags/latest/instructions/using-skills.md
```

**Claude Code** — `~/.claude/CLAUDE.md`:
- Remove the `<CRITICAL>...using-skills skill...</CRITICAL>` block
- Append the content of `instructions/using-skills.md` directly

**GitHub Copilot** — `~/.copilot/copilot-instructions.md`:
- Remove the `<CRITICAL>...using-skills skill...</CRITICAL>` block
- Append the content of `instructions/using-skills.md` directly

**Cursor** — User Rules or `.cursor/rules/using-skills.mdc`:
- Remove the `<CRITICAL>...using-skills skill...</CRITICAL>` block from User Rules
- If using `.cursor/rules/using-skills.mdc`, delete the file
- Append the content of `instructions/using-skills.md` directly instead

### 4. Verify

Restart your agent session and run:

> What should you do before responding to me?

Expected: The agent explains it checks for and invokes skills before acting. It does NOT mention loading a skill called "using-skills" — the behavior is automatic in every session.
