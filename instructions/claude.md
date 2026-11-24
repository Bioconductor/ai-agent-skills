---
layout: default
title: Claude Code
parent: Installation
---
# Claude Code Setup

Add bioconductor skills to your global Claude instructions.

## Setup

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

## claude.ai / Skills API Upload

Each skill folder can be uploaded as-is: its frontmatter follows the layout Claude's skill upload
requires (see [AGENTS.md § Minimal Required Fields](../AGENTS.md#minimal-required-fields)).

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
