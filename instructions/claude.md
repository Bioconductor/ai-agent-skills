# Claude Code Setup

Add waldronlab skills to your global Claude instructions.

## Setup

1. Clone the repository (if needed):
   ```bash
   git clone https://github.com/waldronlab/ai-agent-skills.git
   ```

2. Add to `~/.claude/CLAUDE.md`:
   ```markdown
   # waldronlab AI Agent Skills

   See: `/path/to/ai-agent-skills/SKILLS.md`
   Behavior Standard: `/path/to/ai-agent-skills/AGENTS.md`

   Describe what you need, and I'll match it to the appropriate skill. Always follow the canonical behavior and Git workflow rules defined in AGENTS.md.
   ```

   Replace `/path/to/ai-agent-skills` with the actual path (use `pwd`).

3. Restart Claude Code or reload the workspace.

**Note**: If you use this step 2 instead of pasting the skills directly into `CLAUDE.md`, you will have to give permissions for Claude Code to read a file outside of your project directory when you use it.
