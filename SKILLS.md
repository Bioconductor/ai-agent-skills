# Available Skills

**[🏠 Home](README.md)** | **[🎯 Skills Index](SKILLS.md)** | **[⚙️ Installation](instructions/README.md)** | **[🤖 Agent Behavior](AGENTS.md)** | **[📋 Skill Standards](SKILL_STANDARD.md)**

---
This is the canonical index of all available AI agent skills in the bioconductor/ai-agent-skills repository. Use this to discover and understand what skills are available and when to use them.

> **Note**: All skills are located at `skills/{skill-name}/SKILL.md`.

## Quick Start

1. **Browse by category** below to find a skill that matches your need
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

## Table of Contents

- [Meta Skills](#meta-skills)
- [R/Bioconductor Package Skills](#rbioconductor-package-skills)
- [Bioconductor How-Tos](#bioconductor-how-tos)
- [Metagenomics Skills](#metagenomics-skills)
- [Statistical Methods Skills](#statistical-methods-skills)
- [Skill Categories & Tags](#skill-categories--tags)
- [Finding Skills by Use Case](#finding-skills-by-use-case)
- [How Skills Are Discovered and Invoked](#how-skills-are-discovered-and-invoked)
- [Contributing New Skills](#contributing-new-skills)
- [Platform-Specific Information](#platform-specific-information)
- [Questions?](#questions)

## Meta Skills

Infrastructure and workflow skills for working with this repository itself.

### create-skill

**Purpose**: Help create a new AI agent skill through collaborative Q&A

**When to use**:
- Creating a new skill from scratch or from a manual workflow

**Invocation**:
- "Help me create a new skill"
- "Create a skill for [domain]"

**Output**: A complete skill with validated file and updated SKILLS.md, ready for testing and committing

**Related skills**: validate-skill, document-skill, check-bioconductor-skills

---

### check-bioconductor-skills

**Purpose**: List and verify installed bioconductor skills

**When to use**:
- Verifying skills are correctly installed or discovering available skills

**Invocation**:
- "What skills are available?"
- "List bioconductor skills"

**Output**: List of available skills and setup status

---

### validate-skill

**Purpose**: Validate that a skill conforms to the ai-agent-skills repository standards

**When to use**:
- Creating new skills, reviewing PRs, or ensuring standards compliance

**Invocation**:
- "Validate this skill"
- "Check if skills/[skill-name]/SKILL.md meets standards"

**Output**: Comprehensive validation report with pass/fail status, categorized issues, and specific fix suggestions

**Related skills**: create-skill, check-bioconductor-skills, document-skill

---

### document-skill

**Purpose**: Automate documentation updates to SKILLS.md after creating or modifying a skill

**When to use**:
- After creating a new skill or modifying an existing skill to update SKILLS.md

**Invocation**:
- "Document the new skill I just created"
- "Update SKILLS.md for the validate-r-docs skill"

**Output**: Updated SKILLS.md with the skill entry added to all relevant sections

**Related skills**: create-skill, validate-skill, check-bioconductor-skills

---

## R/Bioconductor Package Skills

Skills for analyzing, documenting, and developing R/Bioconductor packages following bioconductor conventions.

### analyze-r-package

**Purpose**: Analyze R/Bioconductor package structure and characteristics

**When to use**:
- Understanding a package's architecture, type, or identifying key functions

**Invocation**:
- "Analyze this R package"
- "What type of package is this?"

**Output**: Structured analysis of the package

---

### create-package-instructions

**Purpose**: Generate comprehensive .github/instructions files for R/Bioconductor packages

**When to use**:
- Creating AI agent instructions for a new R package or standardizing documentation

**Invocation**:
- "Create .github/instructions for this package"
- "Generate AI agent instructions"

**Output**: Modular instruction files in `.github/instructions/`

**Related skills**: analyze-r-package, update-package-instructions

---

### update-package-instructions

**Purpose**: Update existing .github/instructions files based on recent package changes

**When to use**:
- Refreshing package instructions after major architecture or pattern changes

**Invocation**:
- "Update the package instructions"
- "Refresh .github/instructions"

**Output**: Updated `.github/instructions/` files

**Related skills**: analyze-r-package, create-package-instructions

---

### improve-code-coverage

**Purpose**: Analyze R package code coverage using covr, classify testing gaps, and proactively write test cases.

**When to use**:
- Evaluating testing rigor, identifying gaps, and proactively writing test cases

**Invocation**:
- "Check my code coverage and help me write missing tests."
- "Improve code coverage, focusing on edge cases and correctness."

**Output**: A chat summary breaking down coverage by test category, and code blocks containing `testthat` cases.

**Related skills**: analyze-r-package, security-audit-r-package

---

### security-audit-r-package

**Purpose**: Perform comprehensive security audit of R/Bioconductor packages

**When to use**:
- Auditing packages before CRAN/Bioconductor submission or reviewing for vulnerabilities

**Invocation**:
- "Run security audit on this R package"
- "Check this package for security vulnerabilities"

**Output**: Security audit report (markdown format) with findings categorized by severity.

**Related skills**: analyze-r-package, validate-skill, create-package-instructions

---

### bioc-pkg-finder

**Purpose**: Find the R / Bioconductor packages best suited to a task or workflow

**When to use**:
- When the user asks "what package should I use for X" or "is there a Bioconductor package that does Y"
- Assembling an analysis workflow and needing to pick tools

**Invocation**:
- "What package should I use for differential expression?"
- "Is there a Bioconductor package that does single-cell clustering?"
- "Which package is standard for variant annotation?"

**Output**: Recommended package(s) with biocViews term or CRAN Task View source, install path, and the key gotcha for the recommended tool

**Related skills**: analyze-r-package, create-package-instructions

---

### update-r-news

**Purpose**: Draft or update an R package NEWS file from git commit history, examining diffs when commit messages are vague

**Location**: `skills/update-r-news/SKILL.md`

**When to use**:
- Adding a NEWS entry before a Bioconductor release
- Drafting a changelog from recent commits
- Updating `NEWS.md`, `NEWS`, or `NEWS.Rd` after a development cycle
- Saving time when commit messages alone are insufficient to write clear NEWS entries

**What happens**:
- Detects the NEWS file format in use (`NEWS.md`, `NEWS`, or `NEWS.Rd`)
- Derives the upcoming even-numbered release version from the current devel version
- Finds the most recent Bioconductor devel-version bump commit ("bump x.y.z version to odd y...") and retrieves all commits since then
- Extracts PR titles from merge commits when available
- Identifies vague commit messages (≤ 3 words or known filler phrases) and inspects their diffs to infer what changed
- Categorises changes using headings already present in the NEWS file
- Shows a full preview and asks for confirmation before writing to disk

**Output**: A drafted NEWS block shown for review; upon confirmation, the updated NEWS file on disk with the new version block prepended.

**Related skills**: analyze-r-package, update-package-instructions

---

## Bioconductor How-Tos

Skills indexing focused, practical how-tos for common Bioconductor data analysis tasks.

### bioc-howto

**Purpose**: A consolidated index of Bioconductor how-to skills covering genomics, sequencing, and omics data analysis tasks

**When to use**:
- Looking for step-by-step instructions for common Bioconductor tasks (e.g., loading BAM files, manipulating GRanges, extracting sequences)
- Needing examples of standard Bioconductor workflows

**Invocation**:
- "How do I do [task] in Bioconductor?"
- "Can you show me a Bioconductor how-to for [task]?"
- "Check the bioc-howto index for [task]"

**Output**: Links to and instructions from the relevant how-to markdown file.

---

## Metagenomics Skills

*Planned for future release*

Skills for standard metagenomics data processing and analysis workflows.

---

## Statistical Methods Skills

*Planned for future release*

Skills for statistical analysis patterns in microbiome and multi-omics research.

---

## Skill Categories & Tags

### By Category

| Category | Skills | Purpose |
|----------|--------|---------|
| **meta** | create-skill, check-bioconductor-skills, document-skill, validate-skill | Repository and workflow infrastructure |
| **r-packages** | analyze-r-package, bioc-pkg-finder, create-package-instructions, improve-code-coverage, security-audit-r-package, update-package-instructions, update-r-news | R/Bioconductor package development |
| **bioconductor-how-tos** | bioc-howto | Bioconductor data analysis practical guides |
| **metagenomics** | (Planned) | Metagenomics data workflows |
| **statistical-methods** | (Planned) | Statistical analysis patterns |

### By Tag

| Tag | Skills | Use Case |
|-----|--------|----------|
| **infrastructure** | create-skill, check-bioconductor-skills, document-skill, validate-skill | Repository and workflow tasks |
| **testing** | improve-code-coverage | Software testing and coverage |
| **validation** | security-audit-r-package, validate-skill | Quality control and standards compliance |
| **quality-control** | security-audit-r-package, validate-skill | Ensuring skill quality |
| **documentation** | create-package-instructions, document-skill, update-package-instructions, update-r-news | Generating and maintaining docs |
| **automation** | document-skill, update-r-news | Automating repetitive documentation tasks |
| **analysis** | analyze-r-package, bioc-pkg-finder | Understanding code and architecture |
| **security** | security-audit-r-package | Security audits and vulnerability detection |
| **audit** | security-audit-r-package | Comprehensive code auditing |
| **bioconductor** | analyze-r-package, bioc-pkg-finder, create-package-instructions, improve-code-coverage, security-audit-r-package, update-package-instructions, update-r-news | Bioconductor-specific workflows |
| **code-coverage** | improve-code-coverage | Code coverage analysis |
| **covr** | improve-code-coverage | Tools wrapping the covr package |
| **data-access** | analyze-r-package (detects), create-package-instructions | Working with remote data |
| **git** | update-r-news | Git-based workflows |
| **changelog** | update-r-news | Changelog and release note generation |
| **news** | update-r-news | R package NEWS file management |
| **data-analysis** | bioc-howto | Practical guides for analyzing omics data |

---

## Finding Skills by Use Case

### "I want to work on an R package..."
Use `analyze-r-package` to understand it, `create-package-instructions` to generate AI docs, `improve-code-coverage` or `security-audit-r-package` for quality control, and `update-r-news` for release notes.

### "I want to create a new skill..."
Start with `create-skill` for guided help, then `validate-skill` and `document-skill`.

### "I want to verify my setup..."
Run `check-bioconductor-skills` or check the `instructions/` directory.

### "I want to perform a Bioconductor data analysis task..."
Check the `bioc-howto` index for step-by-step guides and code examples.

### "I want to analyze a workflow and automate it..."
Use `create-skill`.

### "I want to ensure my skill meets standards..."
Use `validate-skill` iteratively until it passes.

---

## How Skills Are Discovered and Invoked

### For Users

1. **Browse this file** to understand what's available
2. **Describe your need** to your AI agent in natural language
3. **Agent handles the rest**: Matches need, reads skill file, executes process, and outputs result

### For AI Agents

1. **Read SKILLS.md** as the primary discovery mechanism
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
4. **Document**: Use `document-skill` to update this file
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

---

**Last Updated**: 2026-07-02
**Version**: 2.0.1
**Maintained by**: bioconductor
