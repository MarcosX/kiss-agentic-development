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

Clone the repo and copy the skills to your agent's skills path:

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

Copy the following content into your tool's global instructions file:

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

1. Create the instructions directory:

```bash
mkdir -p ~/.config/opencode/instructions/
```

2. Save the above content to `~/.config/opencode/instructions/using-skills.md`.

3. Add to `~/.config/opencode/opencode.json`:

```json
{
  "instructions": ["~/.config/opencode/instructions/using-skills.md"]
}
```

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

You can also confirm the domain skills are installed:

```bash
ls <TARGET_PATH>/
# Expected: brainstorming  debugging  executing-plans  practicing-tdd  reviewing-code  writing-plans
```

Replace `<TARGET_PATH>` with the path you copied skills to in step 2.

---

## 5. Updating

### Domain skills

```bash
cd /tmp/kiss-agentic-dev && git pull
cp -r skills/* <TARGET_PATH>/
```

Replace `<TARGET_PATH>` with your tool's skills path (see table in section 2).

### using-skills instruction

Update your global instructions to match the content in section 3 above (the canonical version is in `instructions/using-skills.md` in the repo).

Restart your session for changes to take effect.
