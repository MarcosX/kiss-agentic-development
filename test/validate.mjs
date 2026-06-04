import fs from "fs";
import path from "path";
import { spawnSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const TEST_PROMPTS = path.join(ROOT, "test/prompts");

const PASS = "\x1b[32m\u2713\x1b[0m";
const FAIL = "\x1b[31m\u2717\x1b[0m";

let exitCode = 0;

function fail(msg) {
  console.error(`${FAIL} ${msg}`);
  exitCode = 1;
}

function pass(msg) {
  console.log(`${PASS} ${msg}`);
}

function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) return null;
  const fields = {};
  for (const line of match[1].split("\n")) {
    const sep = line.indexOf(":");
    if (sep === -1) continue;
    fields[line.slice(0, sep).trim()] = line.slice(sep + 1).trim();
  }
  return fields;
}

function discoverSkillDirs() {
  if (!fs.existsSync(SKILLS_DIR)) return [];
  return fs.readdirSync(SKILLS_DIR).filter((d) => {
    const stat = fs.statSync(path.join(SKILLS_DIR, d));
    return stat.isDirectory() && !d.startsWith(".");
  });
}

function extractBashBlocks(content) {
  const blocks = [];
  const lines = content.split("\n");
  let inBlock = false;
  let current = [];
  for (const line of lines) {
    if (line.trim().startsWith("```bash")) {
      inBlock = true;
      current = [];
      continue;
    }
    if (inBlock && line.trim().startsWith("```")) {
      inBlock = false;
      if (current.length > 0) blocks.push(current.join("\n"));
      continue;
    }
    if (inBlock) current.push(line);
  }
  return blocks;
}

function isCommandActionable(line) {
  const t = line.trim();
  if (!t) return false;
  if (t.startsWith("#")) return false;
  if (t.startsWith('echo "Test:')) return false;
  if (t.startsWith("cd ")) return false;
  if (t.startsWith("mkdir ")) return false;
  if (t.includes("rm -rf")) return false;
  return true;
}

function validateLocalConfig() {
  const configPath = path.join(ROOT, ".opencode", "opencode.json");
  if (!fs.existsSync(configPath)) {
    fail("Local dev config not found: .opencode/opencode.json");
    return;
  }
  try {
    const cfg = JSON.parse(fs.readFileSync(configPath, "utf8"));
    if (
      !cfg.instructions ||
      !cfg.instructions.some((i) => i.includes("using-skills"))
    ) {
      fail(".opencode/opencode.json missing instructions for using-skills");
      return;
    }
    pass(".opencode/opencode.json loads using-skills via instructions");
  } catch (e) {
    fail(`Invalid .opencode/opencode.json: ${e.message}`);
  }
}

function validateSkills() {
  const dirs = discoverSkillDirs();
  if (!dirs.length) {
    fail("No skill directories found in skills/");
    return;
  }
  pass(
    `Discovered ${dirs.length} skill director${dirs.length === 1 ? "y" : "ies"}: ${dirs.join(", ")}`,
  );
  for (const dir of dirs) {
    const skillPath = path.join(SKILLS_DIR, dir, "SKILL.md");
    if (!fs.existsSync(skillPath)) {
      fail(`skills/${dir}/SKILL.md not found`);
      continue;
    }
    const content = fs.readFileSync(skillPath, "utf8");
    const frontmatter = parseFrontmatter(content);
    if (!frontmatter) {
      fail(`skills/${dir}/SKILL.md: missing or invalid YAML frontmatter`);
      continue;
    }
    if (!frontmatter.name) {
      fail(`skills/${dir}/SKILL.md: missing "name" in frontmatter`);
    } else {
      pass(`skills/${dir}/SKILL.md: name="${frontmatter.name}"`);
    }
    if (!frontmatter.description) {
      fail(`skills/${dir}/SKILL.md: missing "description" in frontmatter`);
    } else {
      pass(`skills/${dir}/SKILL.md: description present`);
      if (!frontmatter.description.startsWith("Use ")) {
        fail(
          `skills/${dir}/SKILL.md: description should start with "Use when..." (got: "${frontmatter.description.slice(0, 40)}...")`,
        );
      }
      const wordCount = frontmatter.description.split(/\s+/).length;
      if (wordCount > 100) {
        fail(
          `skills/${dir}/SKILL.md: description word count ${wordCount} exceeds 100`,
        );
      }
    }
  }
}

function runValidatePrompts() {
  const dirs = discoverSkillDirs().filter((d) => {
    return fs.existsSync(path.join(TEST_PROMPTS, d, "VALIDATE.prompt.md"));
  });

  if (!dirs.length) {
    pass("No VALIDATE.prompt.md files found, skipping");
    return;
  }

  const tmpBase = path.join(ROOT, "test", "tmp");
  fs.mkdirSync(tmpBase, { recursive: true });

  for (const dir of dirs) {
    const validatePath = path.join(TEST_PROMPTS, dir, "VALIDATE.prompt.md");
    const content = fs.readFileSync(validatePath, "utf8");
    const bashBlocks = extractBashBlocks(content);

    if (!bashBlocks.length) {
      pass(
        `${TEST_PROMPTS}/${dir}/VALIDATE.prompt.md: no bash commands to run`,
      );
      continue;
    }

    const tmpDir = fs.mkdtempSync(path.join(tmpBase, `${dir}-`));

    try {
      const skillsLink = path.join(tmpDir, "skills");
      try {
        fs.unlinkSync(skillsLink);
      } catch {}
      fs.symlinkSync(path.join(ROOT, "skills"), skillsLink);

      let passedCount = 0;
      let failedCount = 0;

      for (const block of bashBlocks) {
        const lines = block.split("\n").filter(isCommandActionable);

        for (const line of lines) {
          const result = spawnSync("/bin/sh", ["-c", line.trim()], {
            cwd: tmpDir,
            stdio: "pipe",
            timeout: 30000,
          });
          const output = result.stdout?.toString().trim() || "";
          if (result.status === 0 && output && output.includes("✓")) {
            pass(
              `${TEST_PROMPTS}/${dir}: ${output.replace(/^✓\s*/, "").trim()}`,
            );
            passedCount++;
          } else if (result.status !== 0) {
            // grep failed → pattern not found
            fail(`${TEST_PROMPTS}/${dir}: ${line}`);
            failedCount++;
          }
          // status 0 but no ✓ → informational command, skip
        }
      }

      if (failedCount > 0) {
        fail(
          `${TEST_PROMPTS}/${dir}/VALIDATE.prompt.md: ${passedCount} passed, ${failedCount} failed`,
        );
      } else if (passedCount > 0) {
        pass(
          `${TEST_PROMPTS}/${dir}/VALIDATE.prompt.md: all ${passedCount} checks passed`,
        );
      } else {
        pass(`${TEST_PROMPTS}/${dir}/VALIDATE.prompt.md: no actionable checks`);
      }
    } catch (e) {
      fail(`${TEST_PROMPTS}/${dir}/VALIDATE.prompt.md: ${e.message}`);
    } finally {
      fs.rmSync(tmpDir, { recursive: true, force: true });
    }
  }
}

function main() {
  console.log("\n=== Local Config Validation ===");
  validateLocalConfig();

  console.log("\n=== Skill File Validation ===");
  validateSkills();

  console.log("\n=== VALIDATE.prompt.md Checks ===");
  runValidatePrompts();

  console.log("");
  process.exit(exitCode);
}

main();
