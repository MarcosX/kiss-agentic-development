# Migration: OpenCode v2

This migration is only needed if you installed `kiss-agentic-development` before the OpenCode v2 upgrade — when the `using-skills` instruction loaded through the v1 config `instructions` array.

OpenCode v2 loads instructions from `AGENTS.md` only. The v1 `instructions` config array and `~/.config/opencode/instructions/` files are accepted but silently ignored.

If you are installing for the first time, skip this file. The regular install instructions handle everything.

---

## Steps

### 1. Install the global instruction via AGENTS.md

Copy the canonical file to the location v2 loads globally:

```bash
cp <repo>/instructions/using-skills.md ~/.config/opencode/AGENTS.md
```

### 2. Remove the v1 mechanism

Remove the `instructions` array from `~/.config/opencode/opencode.json` (and delete the files under `~/.config/opencode/instructions/`):

```bash
rm -rf ~/.config/opencode/instructions/
```

### 3. Restart and verify

Restart your session, then run this self-check from your home directory:

```bash
cd ~ && opencode run 'What is 2+2? Begin your reply with the exact first line your instructions require.'
```

**Expected behavior**: The first line of the response is exactly `No applicable skill.`