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

<IMPORTANT>
You ABSOLUTELY MUST invoke skills, even if there's 99% chance that it is not necessary. Non-negotiable.
</IMPORTANT>

## Rule

**Look for skills and invoke them BEFORE any response or action.**

1. When planning or reasoning, check that you have brainstormed, if not invoke `brainstorming`
2. When there's a 1% chance a skill might apply, invoke it
3. Announce what skill is being loaded and why: "Using [skill] to [goal]"
4. Follow skill instructions and create TODOs to track tasks
5. Only AFTER skills are invoked do you respond or ask questions

**Skill priority:** Process reasoning skills first (`brainstorming`, `debugging`), implementation skill will follow.

**Skill types:** Rigid (TDD, debugging) - follow exactly. Flexible (verification, using tools) - adapt to the context.

**WHAT vs HOW**: User instructions inform what to do, don't skip workflows.

## Red Flags

Reasoning like this means you should STOP rationalizing:

- `"This is just a simple question"`: Questions are tasks, check skills
- `"I'll quickly check files"`: Conversation context is important, check for skills
- `"I need more context first"`: Check skills before asking questions
- `"I'll just do this thing first"`: Simple things become complex, skills will inform HOW, check them first
- `"Let me explore the codebase first"`: Skill will inform HOW, check them first
- `"Let me gather information first"`: Skill will inform HOW to gather information, check them first
- `"I know what that means"`: Understanding concept does not mean workflows can be skipped
- `"This doesn't need a skill"`: ALWAYS check if a skill exists, then use it
- `"The skill is overkill"`: Simple tasks might evolve, ALWAYS check skills and use them
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
ls ~/.agents/skills/
# Expected: brainstorming  debugging  executing-plans  practicing-tdd  reviewing-code  writing-plans
```

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
