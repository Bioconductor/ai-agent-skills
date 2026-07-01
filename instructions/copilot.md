# GitHub Copilot

## Simple IDE-independent approach

The simplest portable approach is to give Copilot a short bootstrap prompt such as:

```text
Use the waldronlab AI agent skills from this repository: /path/to/ai-agent-skills.
Start with SKILLS.md to find the best matching skill.
Then read the corresponding skills/<skill-name>/SKILL.md file and follow it.
If more than one skill matches, list the options briefly and choose the best fit.

You must also read and adhere to the agent behavior and safe execution standards defined in AGENTS.md.
```

This is not the same as installed persistent skills, but it is the simplest natural-language pattern that can work across Copilot surfaces and IDEs.

## Persistent setup for Copilot Agent in VS Code

Open VS Code, then add the waldronlab skills you want to use to Copilot's skill locations.

1. Clone the repository if needed:
   ```bash
   git clone https://github.com/waldronlab/ai-agent-skills.git
   ```

2. Open VS Code user `settings.json` and add the skill directories you want from [SKILLS.md](../SKILLS.md):
   ```json
   {
     "chat.skillsLocations": [
       "/path/to/ai-agent-skills/skills/create-skill",
       "/path/to/ai-agent-skills/skills/check-waldronlab-skills",
       "/path/to/ai-agent-skills/skills/analyze-r-package"
     ]
   }
   ```

3. Reload VS Code.

## Usage

To confirm the setup worked, ask:

```text
What waldronlab skills do I have?
```

To use the skills, ask naturally. For example:

```text
Help me create a new skill
Analyze this R package
Create .github/instructions for this package
```
