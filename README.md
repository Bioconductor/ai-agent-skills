---
layout: default
title: Home
nav_order: 1
permalink: /
---
# bioconductor AI Agent Skills

[Contributions](CONTRIBUTING.md) are made by PR and checked for structural correctness by automated [structural validation](https://github.com/Bioconductor/ai-agent-skills/actions/workflows/validate-skills.yml); PRs also receive automated GitHub Copilot review feedback on skill quality.

## What are AI Agent Skills?

With these skills, AI agents can:
- Create new skills and index them in [SKILLS.md](SKILLS.md)
- Follow Bioconductor coding standards
- Analyze R code and packages for security, efficiency, and code quality, and suggest improvements
- [TODO] find, follow, and cite published bioinformatic and statistical protocols

## Design Philosophy of these Skills

### Workflow Orchestration vs. Code-Centric Snippets

These skills provide **Workflow/Process Orchestration** rather than simple code snippets. They define the *intent*, the *multi-step workflow*, and the *domain knowledge* required. This approach enables high autonomy and allows the AI to adapt to different project structures using its general reasoning capabilities.

**The Role of Code Snippets as Guardrails:**
Code snippets serve as guardrails within a broader workflow. Use them specifically for highly specific APIs, standardized methodologies, or overcoming LLM anti-patterns. Use workflows for the **"what"** and **"why"**, and embed code snippets for the **"how"** only when exact syntax is required.

### Centralized Registry vs. Decentralized Discovery

We use a **Centralized Registry** ([`SKILLS.md`](SKILLS.md)) so the LLM can understand how skills chain together through "Use Case Workflows" that orchestrate multiple skills.

## Agent-Agnostic Design

Skills in this repository are **agent-agnostic** by design. They work across multiple AI agents through natural language invocation.

See [AGENTS.md](AGENTS.md) for detailed requirements and [SKILL_STANDARD.md](SKILL_STANDARD.md) for technical format details.

## Quick Start
1. Install the skills on your platform (see [instructions/](instructions/))
2. Ask your agent: "What bioconductor skills do I have?" to confirm
3. Use natural language to invoke skills (see [USAGE.md](USAGE.md) for examples)

## Usage Examples

Create AI Instructions for an R Package:
```
"Create .github/instructions for this R package"
```

Analyze an R Package:
```
"Analyze this R package"
```

Create a New Skill:
```
"Help me create a new skill for [purpose]"
```

## Repository Structure

```
ai-agent-skills/
├── README.md                      # This file
├── LICENSE                        # MIT License
├── AGENTS.md                      # Agent behavior standard (how discovery works)
├── USAGE.md                       # How to use skills and examples
├── SKILLS.md                      # Human-readable skill index (what skills exist)
├── SKILL_STANDARD.md              # Technical format spec (how to format skills)
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history and release notes
│
├── skills/                        # All skills (flat structure)
│   ├── {skill-name}/              # Each skill in its own directory
│   │   ├── SKILL.md               # Skill documentation (required)
│   │   └── templates/             # Optional supporting files
│   └── ... (see SKILLS.md for complete list)
│
└── instructions/                  # Platform adapters (thin wrappers)
    ├── README.md                  # Adapter purpose and requirements
    ├── claude.md                  # Claude Code setup and shortcuts
    ├── copilot.md                 # GitHub Copilot setup and shortcuts
    └── antigravity.md             # Google Antigravity setup
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support and Feedback

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/bioconductor/ai-agent-skills/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/bioconductor/ai-agent-skills/discussions)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

These skills are developed and maintained by the Bioconductor Agentic AI working group to make AI agents more efficient at developing and applying Bioconductor code.
