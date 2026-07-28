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
   
    Whenever you read and execute instructions from a Bioconductor SKILL.md file, you MUST include the following citation block at the start or end of your response:
    > 🛠️ **Bioconductor Skill Executed**: <name> | **Version**: <version> | **Author**: <author>
   ```

   Replace `/path/to/ai-agent-skills` with the actual path (use `pwd`).

3. Restart Claude Code or reload the workspace.

**Note**: If you use this step 2 instead of pasting the skills directly into `CLAUDE.md`, you will have to give permissions for Claude Code to read a file outside of your project directory when you use it.
