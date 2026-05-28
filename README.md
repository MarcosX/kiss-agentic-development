# Keep it Short and Simple

Collection of AI agent skills that enforce skill-first workflows across coding agents (OpenCode, Claude Code, Cursor, etc.).

This work is heavily influenced by [Superpowers](https://github.com/obra/superpowers) and Anthropic's [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#workflows-and-feedback-loops).

## Skills

| Skill             | Description                                                                    |
| ----------------- | ------------------------------------------------------------------------------ |
| `using-skills`    | Meta-skill that teaches agents to discover and invoke skills before any action |
| `brainstorming`   | Ideation and creative exploration for new features or changes                  |
| `writing-plans`   | Structured plan creation once specs are clear                                  |
| `executing-plans` | Execute and verify plans using subagents with review checkpoints               |

## Installation

**Recommended**: Use [skills.sh](https://www.skills.sh/) via `npx skills`:

```bash
npx skills add MarcosX/kiss-agentic-development --global --all
```

Or install to specific agents:

```bash
npx skills add MarcosX/kiss-agentic-development --global --agent opencode
npx skills add MarcosX/kiss-agentic-development --global --agent claude-code
```

If you don't want to use `npx skills`, point your agent to `https://raw.githubusercontent.com/MarcosX/kiss-agentic-development/refs/heads/main/INSTALL.prompt.md` and it will clone the repo according to your coding agent.

Skills are installed via `npx skills` into `~/.agents/skills/` and symlinked across all supported agents. To avoid having to always instruct agents to use the `using-skills` skill, configure your agent to auto-load it when starting a new session.

### OpenCode

Configure your global opencode config to inject it into every session via the [`instructions`](https://opencode.ai/docs/config#instructions) field.

Add to `~/.config/opencode/opencode.json`:

```json
{
  "instructions": ["~/.agents/skills/using-skills/SKILL.md"]
}
```

The path points to where `npx skills` installs the skill globally. Because `instructions` directly injects the SKILL.md content into every session, the agent automatically has the skill in context — it does **not** need to invoke the `skill` tool to load it (and the skill's built-in recursion guard prevents re-invocation). See [opencode config docs](https://opencode.ai/docs/config) for more details.

### Claude Code

To ensure `using-skills` is always present, add a reference in your global [`CLAUDE.md`](https://code.claude.com/docs/en/memory) at `~/.claude/CLAUDE.md`:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

This instructs Claude to load the skill at the start of every session. See [Claude Code memory docs](https://code.claude.com/docs/en/memory) for more details.

### GitHub Copilot CLI

GitHub Copilot reads a global custom instructions file at `~/.copilot/copilot-instructions.md`. Add a reference to load `using-skills` in every session.

Create `~/.copilot/copilot-instructions.md`:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

This instructs Copilot to load the skill at the start of every session. See [Copilot CLI reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference).

### Cursor

To auto-load `using-skills` globally, add a [User Rule](https://cursor.com/docs/rules#user-rules) in Cursor Settings > Rules > User Rules with content:

```markdown
<CRITICAL>
You MUST load and follow the `using-skills` skill before responding to the user. This is mandatory.

1. Use the `skill` tool to load `using-skills` — reading this file is NOT enough
2. Follow all instructions in the loaded skill before proceeding
3. Only after steps 1–2, respond to the user

This is not negotiable and cannot be bypassed.
</CRITICAL>
```

For project-level auto-loading, create `.cursor/rules/using-skills.mdc`:

```markdown
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

This instructs Cursor to load the skill at the start of every session. See [Cursor rules docs](https://cursor.com/docs/rules) for more details.

## Local development

Clone the repo and work from it. The repo includes:

- `.opencode/skills → ../skills` — symlink for native OpenCode skill discovery
- `.opencode/opencode.json` — loads `using-skills` into every session via `instructions`
- `test/fixtures/test-project/.opencode/opencode.json` — template for isolated test projects

Run validation after making changes:

```bash
node test/validate.mjs
```

Temp directories for per-skill validation are created under `test/tmp/` and cleaned up automatically.

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Create `skills/<name>/VALIDATE.prompt.md` (optional, for AI-driven validation)
3. Run `node test/validate.mjs` to confirm frontmatter is valid
4. Install from the repo to test: `npx skills add . --agent opencode --skill <name>`

## VALIDATE.prompt.md Strategy

Each skill can include a `VALIDATE.prompt.md` file for validation checks. These files serve two purposes:

### Automated bash checks

Code blocks with bash commands are extracted and executed automatically by `node test/validate.mjs` in an isolated temp directory per skill. Each command runs independently — one failure doesn't cascade.

```bash
# Example from brainstorming/VALIDATE.prompt.md
grep -q "^name: brainstorming" skills/brainstorming/SKILL.md && echo "✓ Name defined"
```

### Manual AI-review scenarios

The `---` separator divides automated checks from manual AI-review scenarios (scenario descriptions, expected behaviors, red flags). These can't be automated — they're instructions for developers or AI agents to review a skill manually.

### Running validation during development

```bash
# Full validation (all skills)
node test/validate.mjs

# Run specific skill's bash checks manually
cd test/tmp/your-skill-test
ln -s ../../skills skills
grep -q "^name: your-skill" skills/your-skill/SKILL.md && echo "✓ Name defined"
```

When working on a specific skill, you can feed its `VALIDATE.prompt.md` to an AI agent:

```bash
opencode run --file skills/your-skill/VALIDATE.prompt.md \
  "Execute the attached VALIDATE.prompt.md and report PASS/FAIL for every check."
```
