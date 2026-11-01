---
layout: default
title: Claude Code
parent: Installation
---
# Claude Setup

The skills install as two Claude plugins from this repository's plugin marketplace
([`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)). Each skill keeps its own
description, so Claude still picks the individual skill that matches the request.

| Plugin | Skills | For |
|--------|--------|-----|
| `bioc-r-packages` | Package analysis, BiocCheck, review, submission, coverage, security, NEWS, data migration, how-tos | R/Bioconductor package developers and analysts |
| `bioc-skill-authoring` | create-skill, validate-skill, document-skill, check-bioconductor-skills, adr-author | Contributors to this repository |

See [SKILLS.md](../SKILLS.md) for what each skill does.

> **Branch**: until the `metadata:` frontmatter change reaches the default branch, install from the
> `claude-upload-metadata` branch by appending `#claude-upload-metadata` to the repository, as shown
> below. Drop the suffix once it is merged.

## Plugin Install (Recommended)

### Claude Code

```
/plugin marketplace add Bioconductor/ai-agent-skills#claude-upload-metadata
/plugin install bioc-r-packages@bioconductor-skills
/plugin install bioc-skill-authoring@bioconductor-skills
```

From a shell, use `claude plugin marketplace add ...` and `claude plugin install ...` with the same
arguments. Run `/plugin marketplace update bioconductor-skills` to pick up new skills.

### Claude desktop app / claude.ai

**Upload the plugin archives** (works everywhere):

1. From a checkout of the branch, build one archive per plugin:
   ```bash
   git switch claude-upload-metadata
   python scripts/build_claude_plugins.py   # writes dist/bioc-r-packages.zip, dist/bioc-skill-authoring.zip
   ```
2. Open **Customize → Plugins → Add → Upload plugin** and drop in both zips (or only
   `bioc-r-packages.zip` if you don't contribute skills).
3. To update, pull, rebuild and upload again.

**Or add the marketplace** (if your app offers **Add marketplace**), which follows the branch
without rebuilding: enter `https://github.com/Bioconductor/ai-agent-skills.git#claude-upload-metadata`
and install the plugins from it.

Team and Enterprise owners can instead add the repository under **Organization settings → Plugins &
skills → Sync from GitHub** and make the plugins available to, or installed for, everyone.

### Citing skills

Plugins do not carry instructions outside the skills themselves, so add the citation rule required
by [AGENTS.md](../AGENTS.md#must-mandatory) to `~/.claude/CLAUDE.md` (Claude Code) or your
claude.ai profile preferences:

```markdown
Whenever you read and execute instructions from a Bioconductor SKILL.md file, you MUST include the following citation block at the start or end of your response, filled from the skill's frontmatter (`name`, `metadata.version`, `metadata.author`):
> 🛠️ **Bioconductor Skill Executed**: <name> | **Version**: <version> | **Author**: <author>
```

## Manual Setup (Claude Code, from a clone)

Use this instead of the plugins to point Claude Code at a local checkout.

1. Clone the repository (if needed):
   ```bash
   git clone https://github.com/bioconductor/ai-agent-skills.git
   ```

2. Add to `~/.claude/CLAUDE.md`:
   ```markdown
   # bioconductor AI Agent Skills

   See: `/path/to/ai-agent-skills/SKILLS.md`
   Behavior Standard: `/path/to/ai-agent-skills/AGENTS.md`

   Describe what you need, and I'll match it to the appropriate skill. Always follow the canonical behavior and Git workflow rules defined in AGENTS.md.
   
    Whenever you read and execute instructions from a Bioconductor SKILL.md file, you MUST include the following citation block at the start or end of your response, filled from the skill's frontmatter (`name`, `metadata.version`, `metadata.author`):
    > 🛠️ **Bioconductor Skill Executed**: <name> | **Version**: <version> | **Author**: <author>
   ```

   Replace `/path/to/ai-agent-skills` with the actual path (use `pwd`).

3. Restart Claude Code or reload the workspace.

**Note**: If you use this step 2 instead of pasting the skills directly into `CLAUDE.md`, you will have to give permissions for Claude Code to read a file outside of your project directory when you use it.

## Single-Skill Upload (claude.ai)

To install only some skills without the plugins, upload skill folders one at a time. Each folder
can be uploaded as-is: its frontmatter follows the layout Claude's skill upload requires (see
[AGENTS.md § Minimal Required Fields](../AGENTS.md#minimal-required-fields)). Upload a skill
folder, not `SKILLS.md`: the index is not a skill and is rejected for missing a `name`.

1. Zip one skill folder so that `SKILL.md` sits inside a top-level folder named after the skill:
   ```bash
   cd skills && zip -r ../bioc-pkg-dev.zip bioc-pkg-dev
   ```
2. In claude.ai, open **Settings → Capabilities → Skills** and upload the zip (organization
   owners can provision it for the whole organization instead).
3. Repeat for each skill you want. Re-upload after pulling updates; `metadata.version` shows
   which version is installed.

Skills that link outside their own folder (e.g. to `../../SKILLS.md`) lose those links once
uploaded; the skill's own instructions still work.
