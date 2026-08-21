---
layout: default
title: Skills Usage Guide
nav_order: 3
---
# Skills Usage Guide

<details markdown="1">
<summary><b>📖 Table of Contents (click to expand)</b></summary>

* TOC
{:toc}

</details>

---

## Quick Start

1. **Browse by category** in [SKILLS.md](SKILLS.md) to find a skill that matches your need
2. **Read the skill description** to understand when to use it
3. **Invoke naturally**: Describe what you need to your AI agent
   - Example: "Help me create a new skill"

**Platform shortcuts**: Optional shortcuts (like `/skill-name` or `@workspace` patterns) are documented in [instructions/](instructions/) for each platform.

## Setup & Discovery

**First time?**
- See [instructions/claude.md](instructions/claude.md) (Claude Code)
- See [instructions/copilot.md](instructions/copilot.md) (GitHub Copilot)

**Understanding the design:**
- See [AGENTS.md](AGENTS.md) for how skill discovery and invocation work

## Finding Skills by Use Case

**"I want to work on an R package..."**
Use `analyze-r-package` to understand it, `create-package-instructions` to generate AI docs, `improve-code-coverage` or `security-audit-r-package` for quality control, and `update-r-news` for release notes.

**"I want to submit a package to Bioconductor..."**
Use `bioc-pkg-dev` for the pre-submission gate, the Contributions tracker, and post-acceptance maintenance; pair it with `improve-code-coverage` and `security-audit-r-package` for quality control before submitting.

**"I want to create a new skill..."**
Start with `create-skill` for guided help, then `validate-skill` and `document-skill`.

**"I want to verify my setup..."**
Run `check-bioconductor-skills` or check the `instructions/` directory.

**"I want to perform a Bioconductor data analysis task..."**
Check the `bioc-howto` index for step-by-step guides and code examples.

**"I want to analyze a workflow and automate it..."**
Use `create-skill`.

**"I want to ensure my skill meets standards..."**
Use `validate-skill` iteratively until it passes.

---

## How Skills Are Discovered and Invoked

### For Users

1. **Browse [SKILLS.md](SKILLS.md)** to understand what's available
2. **Describe your need** to your AI agent in natural language
3. **Agent handles the rest**: Matches need, reads skill file, executes process, and outputs result

### For AI Agents

1. **Read [SKILLS.md](SKILLS.md)** as the primary discovery mechanism
2. **Match user intent** to skill descriptions
3. **Locate and read** the skill file at `skills/{skill-name}/SKILL.md`
4. **Execute** using platform tools and deliver output

See [AGENTS.md](AGENTS.md) for the complete agent behavior standard.

---

## Contributing New Skills

Want to add a new skill?

1. **Brainstorm**: Use `create-skill`
2. **Create**: Follow guidance to create the skill file
3. **Validate**: Run `validate-skill`
4. **Document**: Use `document-skill` to update `SKILLS.md`
5. **Test**: Verify it works on your platform
6. **Submit**: Create a PR for review

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Platform-Specific Information

### Claude Code
See [instructions/claude.md](instructions/claude.md) for setup and `/skill-name` shortcuts.

### GitHub Copilot
See [instructions/copilot.md](instructions/copilot.md) for setup and `@workspace` shortcuts.

### Other Agents
See [instructions/](instructions/) for available adapters.

---

## Questions?

- **How does skill invocation work?** → See [AGENTS.md](AGENTS.md)
- **How do I create a new skill?** → Use `create-skill` or see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Where are the actual skill files?** → `skills/{skill-name}/SKILL.md`
- **Can I use skills on multiple platforms?** → Yes! Skills are platform-agnostic
- **How do I verify my setup?** → Ask your agent: _Do I have the Bioconductor skills?_ This should invoke `check-bioconductor-skills` if your setup is working. See [instructions/](instructions/) for agent-specific setup (e.g. `instructions/copilot.md`).
- **I found an issue with a skill or want to suggest a new skill** → File an issue at https://github.com/bioconductor/ai-agent-skills/issues
