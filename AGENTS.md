---
layout: default
title: Agent Behavior
nav_order: 4
---
# Agent Behavior Standard

<details markdown="1">
<summary><b>📖 Table of Contents (click to expand)</b></summary>

* TOC
{:toc}

</details>

---

## Purpose

This document defines the canonical behavior rules that ALL AI agents must follow to work with bioconductor's skill repository. It establishes a platform-agnostic contract: agents adapt to this standard, not the other way around.

## Core Principles

### 1. Agent Neutrality

Skills are platform-agnostic by design. They contain no embedded vendor-specific metadata or logic. Agents are responsible for:
- Discovering skills via the canonical SKILLS.md index
- Matching user natural language to skill descriptions
- Adapting their platform-specific mechanics (slash commands, @workspace triggers, etc.) to invoke skills

Skills do not reference `platforms:`, `triggers:`, or other agent-specific configuration.

### 2. Single Source of Truth

- **One repository**: bioconductor/ai-agent-skills is the authoritative source
- **One skill file per skill**: Located at `skills/{skill-name}/SKILL.md`
- **One description per skill**: Agents use this description to understand when to invoke the skill
- **No duplication**: Do not maintain separate versions for Claude, Copilot, or other agents

### 3. Natural Language Invocation

Skills are discovered and invoked through natural language matching, not rigid command syntax. See § Skill Discovery & Invocation for details.

### 4. Skill Execution Model

**Agents read and follow skills as instructions:**

1. Read the skill file (SKILL.md)
2. Understand the skill's purpose from the description
3. Follow the documented process step-by-step
4. Adapt tool usage to agent's available capabilities
5. Produce output as documented in the skill

Skills are **prompts**, not code. Agents interpret and execute them using their own tools.

### 5. Portability Over Convenience

- Prioritize long-term interoperability over short-term optimization
- Make skills work on minimal assumptions (just markdown + YAML frontmatter)

### 6. Workflow over Code Snippets

Skills must define workflows (the *intent*, *multi-step process*, and *domain knowledge*), not just provide raw code. While highly specific code snippets can be provided to overcome LLM anti-patterns, handle unique APIs, or adhere to strict lab standards (e.g., `BiocParallel` vs `lapply`), they must serve strictly as **guardrails** embedded within a numbered workflow step, never as the entire skill itself.

## Skill File Format

### Minimal Required Fields

Every skill MUST include these YAML frontmatter fields:

```yaml
---
name: skill-name              # Unique identifier (kebab-case, REQUIRED)
description: Brief purpose    # One-line description driving discovery (REQUIRED)
version: 1.0.0               # Semantic version (REQUIRED)
category: meta               # Primary domain: meta, r-packages, etc. (REQUIRED)
author: bioconductor           # Creator/maintainer (REQUIRED)
tags: [tag1, tag2]          # Searchable tags (OPTIONAL)
---
```

### What NOT to Include

Skills **MUST NOT** contain:
- ❌ `platforms:` field (skills are agent-agnostic by design)
- ❌ `triggers:` field (agents use natural language + SKILLS.md for discovery)
- ❌ Agent-specific tool references (e.g., "use the Read tool")
- ❌ Platform-specific invocation syntax (e.g., "/command" or "@workspace" patterns)

### Content Structure (Recommended)

```markdown
# [Skill Name]

Brief overview (1-2 paragraphs).

## Usage

How users naturally invoke this skill.
Agents will adapt this to their platform.

## Prerequisites

Required files, setup, or dependencies.

## Process

Numbered steps describing what to do.
Platform-agnostic language: "read the file", not "use Read tool".

## Output Format

Expected output structure or examples.

## Platform-Specific Notes (Optional)

Only if meaningful platform differences exist.
Document HOW platforms differ, not what they should do.

## Examples

Concrete usage scenarios.

## Notes

Additional context or caveats.
```

**Principle**: Describe WHAT to do, not HOW (specific tools). Let agents figure out HOW with their available capabilities.

## Avoiding Content Duplication

Skills must maintain this document (AGENTS.md) as the single source of truth for format specifications and standards.

### How to Reference Properly

Instead of duplicating, use references:
```markdown
✅ "See AGENTS.md § Skill File Format for complete specification"
✅ "Check that frontmatter conforms to AGENTS.md § Minimal Required Fields"
❌ Do not list required fields or copy YAML templates
❌ Do not duplicate external classification systems or checklists
```

### When to Include Content

Skills SHOULD include:
- ✅ Skill-specific logic and workflow steps
- ✅ Domain-specific knowledge and context
- ✅ Concrete examples relevant to the skill's purpose
- ✅ Decision trees or branching logic unique to the skill

**Principle**: Reference authoritative sources; only include content unique to the skill's purpose.

## Skill Discovery & Invocation

### Primary Discovery Mechanism: SKILLS.md

The file `SKILLS.md` is the canonical skill index. It is:
- **Human-readable**: Browse and search by category, tag, use case
- **Agent-parseable**: Agents extract skill locations and descriptions
- **Maintained in parallel with skills**: Updated when skills are added/changed
- **Source of truth for discovery**: Authoritative list of available skills

Format:
```markdown
### [Category]

#### [Skill Name]
**Purpose**: From skill description
**Location**: `skills/[name]/SKILL.md`
**Invocation**: "Natural language the user might say"
**When to use**: Context for when this skill applies
```

### Invocation Pattern

1. **User provides intent** (natural language): "Create a new skill for validating R packages"
2. **Agent reads SKILLS.md**: Finds matching skill based on description
3. **Agent invokes skill**: Using platform-specific mechanism
   - Claude Code: `/create-skill` (optional shortcut)
   - Copilot: `@workspace create a new skill` (optional shortcut)
   - Other agents: Custom mechanism, but same underlying skill
4. **Agent executes skill**: Follows documented process, adapts tools as needed
5. **User receives output**: Consistent regardless of platform

### Optional Platform-Specific Shortcuts

Agents MAY provide platform-specific shortcuts for convenience:
- Claude Code: `/skill-name` slash commands
- GitHub Copilot: `@workspace` pattern triggers
- Others: Platform-appropriate equivalents

**Important**: These shortcuts are **optional conveniences**, not the primary invocation mechanism. Users who don't know or use these shortcuts can still invoke skills through natural language.

## Agent Responsibilities

### MUST (Mandatory)

Compliant agents:
- [ ] MUST support SKILLS.md as the primary discovery mechanism
- [ ] MUST support natural language skill invocation matching descriptions
- [ ] MUST read and follow SKILL.md process documentation
- [ ] MUST adapt tool usage to agent's available capabilities
- [ ] MUST produce output as documented in the skill
- [ ] MUST explicitly cite any Bioconductor skill executed in the response (header or footer), including skill name, version, and author — values taken directly from the skill's YAML frontmatter.
- [ ] MUST NOT embed platform-specific requirements in skills
- [ ] MUST ask the user if the work should be done on a new branch before editing files
- [ ] MUST NOT commit changes without explicit approval from the user
- [ ] MUST show a draft commit message for the user's approval in a standard text response prior to committing
- [ ] MUST acknowledge the AI agent being used so that it will appear as a co-author (e.g., appending the GitHub co-author trailer `Co-authored-by: AI Agent <agent@example.com>` at the end of the commit message, separated by a blank line).

### SHOULD (Strong Recommendation)

- [ ] SHOULD document platform shortcuts in instructions/{agent}.md (setup and usage only, not skill descriptions)
- [ ] SHOULD test all skills before promoting to production
- [ ] SHOULD handle errors gracefully and guide users to skill documentation
- [ ] SHOULD direct users to [SKILLS.md](SKILLS.md) as the authoritative skill catalog

### MAY (Optional)

- [ ] MAY provide optional platform-specific shortcuts for convenience (e.g., `/skill-name`, `@workspace` patterns)
- [ ] MAY provide additional UX conveniences (auto-completion, suggestion UI, etc.)
- [ ] MAY extend skills with platform-specific enhancements
- [ ] MAY implement caching or optimization for performance

## Platform Adapter Requirements

### What Adapters Are

Platform adapters are **thin wrapper documents** located in `instructions/{agent-name}.md` that explain how to install skills for a specific agent, provide optional shortcuts, and list troubleshooting tips.

### What Adapters Should/Must Not Include

- ✅ Setup/installation instructions specific to the platform
- ✅ References to AGENTS.md and SKILLS.md as authoritative sources
- ✅ Optional platform-specific shortcuts (if any) with explanations
- ❌ Do not duplicate skill logic, descriptions, or purpose statements
- ❌ Do not define new invocation patterns or require platform-specific fields

Example minimal structure:

```markdown
# Claude Code Setup

## Installation

[Setup steps for configuring skills on Claude Code]

## Using Skills

1. Browse available skills in [SKILLS.md](../SKILLS.md)
2. Invoke naturally: "Analyze this R package"
3. Optional: Use slash commands if configured (e.g., `/analyze-r-package`)

## Troubleshooting

[Platform-specific troubleshooting tips]

See [AGENTS.md](../AGENTS.md) for canonical behavior and [SKILLS.md](../SKILLS.md) for skill catalog.
```

## Responsibility Mapping

| Concept | Who owns it | What it contains | What it MUST NOT contain |
|---------|-------------|------------------|--------------------------|
| **Skill Invocation Examples** | `SKILLS.md` | Natural language examples ("I want to make a skill that...") | N/A (Do not duplicate in `instructions/{agent}.md`) |
| **Platform-Specific Shortcuts** | `instructions/{agent}.md` | Optional shortcuts (e.g., `/create-skill`) | N/A (Do not put shortcuts in skill files) |
| **Skill Process & Logic** | `SKILL.md` files | Step-by-step process, prerequisites, output format, platform-agnostic logic | Platform-specific setup, shortcuts, or configuration (do not put these in skill files) |
| **Setup & Configuration** | `instructions/{agent}.md` | How to install skills, platform-specific troubleshooting | N/A |
| **Canonical Behavior Rules** | `AGENTS.md` | Discovery/invocation rules, compliance criteria, prohibited metadata | N/A |
| **Technical Format** | `SKILL_STANDARD.md` | YAML frontmatter fields, markdown structure, validation checklist | N/A |

## Scope & Limitations

### This Standard Does Not Cover

- Technical implementation details (see SKILL_STANDARD.md)
- Individual skill logic (see SKILLS.md for navigation)
- How agents manage state, context, or persistence
- Agent-specific optimizations or UX enhancements

## Relationship to Other Documents

- **SKILL_STANDARD.md**: Technical format specification for skill files (WHAT structure to use)
- **AGENTS.md** (this file): Canonical behavior rules for agents (WHAT agents must do)
- **SKILLS.md**: Human-readable index of available skills (WHERE to find skills, WHEN to use them)
- **instructions/{agent}.md**: Platform-specific setup and optional shortcuts (HOW to use on this platform)

## Questions & Clarifications

### Q: What if a skill needs different logic for different agents?

**A**: Document the platform differences in a "Platform-Specific Notes" section within the skill. Let each agent adapt the approach to their capabilities.

### Q: Can agents cache SKILLS.md or skill files?

**A**: Yes. But they must re-validate against the repository version periodically to stay current.

### Q: What about MCP (Model Context Protocol) servers?

**A**: MCP is optional infrastructure. Skills are designed to work as plain markdown + YAML, with or without MCP support. If an agent uses MCP, it's an implementation detail, not a requirement here.

## Version History

- **2.0.0** (2026-04-03) - Agent behavior standard

## Maintenance

**Maintained by**: bioconductor

**When to update**:
- New compliance criteria identified
- Major structural changes to skill repository
- New agent types added with novel requirements

**Change process**:
1. Open issue describing needed change
2. Discuss rationale with maintainers
3. Submit PR with updated AGENTS.md
4. Increment version
5. Tag release and notify affected agents

---

**The key principle**: Agents adapt to this standard and repository, not the other way around. Skills are portable, platform-agnostic prompts. Agents are the layer that brings them to life on specific platforms.
