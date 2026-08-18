---
layout: default
title: GitHub Copilot
parent: Installation
---
# GitHub Copilot

## Simple IDE-independent approach

The simplest portable approach is to give Copilot a short bootstrap prompt such as:

```text
Use the bioconductor AI agent skills from this repository: /path/to/ai-agent-skills.
Start with SKILLS.md to find the best matching skill.
Then read the corresponding skills/<skill-name>/SKILL.md file and follow it.
If more than one skill matches, list the options briefly and choose the best fit.

You must also read and adhere to the agent behavior and safe execution standards defined in AGENTS.md.

Whenever you read and execute instructions from a Bioconductor SKILL.md file, you MUST include the following citation block at the start or end of your response:
> 🛠️ **Bioconductor Skill Executed**: <name> | **Version**: <version> | **Author**: <author>
```

This is not the same as installed persistent skills, but it is the simplest natural-language pattern that can work across Copilot surfaces and IDEs.

## Persistent setup for Copilot Agent in VS Code

Open VS Code, then add the bioconductor skills you want to use to Copilot's skill locations.

1. Clone the repository if needed:
   ```bash
   git clone https://github.com/bioconductor/ai-agent-skills.git
   ```

2. Open VS Code user `settings.json` and add the skill directories you want from [SKILLS.md](../SKILLS.md):
   ```json
   {
     "chat.skillsLocations": [
       "/path/to/ai-agent-skills/skills/create-skill",
       "/path/to/ai-agent-skills/skills/check-bioconductor-skills",
       "/path/to/ai-agent-skills/skills/analyze-r-package"
     ]
   }
   ```

3. Reload VS Code.

## Usage

To confirm the setup worked, ask:

```text
What bioconductor skills do I have?
```

To use the skills, ask naturally. For example:

```text
Help me create a new skill
Analyze this R package
Create .github/instructions for this package
```

## PR Code Review

This repository disables Copilot's automatic PR review and instead gates the
review request on `Validate Skills` completion via
`.github/workflows/copilot-review.yml`. This avoids Copilot posting before
the `Validate Skills` (~12 s) structural gatekeeper check has finished,
ensuring Copilot always sees fresh CI results.

### How it works

1. A PR is opened or updated.
2. The `Validate Skills` workflow executes fast deterministic checks (~12 s).
3. Once `Validate Skills` passes, `copilot-review.yml` fires and requests a review from
   `copilot-pull-request-reviewer`.
4. Copilot reviews the PR with full access to CI comments already posted.

### Disabling automatic Copilot review

In your repository settings, disable **"Automatically request Copilot review"**
under **Settings → Code and automation → Code review → Copilot**. The gating
workflow handles the review request instead.

### CI-awareness in the review

`.github/copilot-instructions.md` includes a **CI Results** section that
instructs Copilot to read and incorporate CI findings rather than repeat them.
Violations already flagged by CI are treated as confirmed; Copilot focuses on
qualitative issues that automated checks cannot cover.
