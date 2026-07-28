---
layout: default
title: Skill Standards
nav_order: 5
---
# Skill Format Standard (Quick Reference)
Quick reference for creating skills with validation checklist, version management, and working examples.

**Authoritative specification**: [AGENTS.md § Skill File Format](AGENTS.md#skill-file-format)

## Documentation Map

- **[AGENTS.md](AGENTS.md)** - Canonical format requirements and agent behavior
- **SKILL_STANDARD.md** (this file) - Quick reference, checklist, examples
- **[SKILLS.md](SKILLS.md)** - Skill catalog organized by domain
- **[instructions/](instructions/)** - Platform-specific setup

## Quick Format Summary

See [AGENTS.md § Skill File Format](AGENTS.md#skill-file-format) for the complete format specification, including required fields, prohibited fields, and structural recommendations.

---

## Version Management

Skills use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to skill behavior or interface
- **MINOR**: New features, non-breaking enhancements
- **PATCH**: Bug fixes, clarifications, documentation updates

### When Updating Skills

1. Increment version in YAML frontmatter
2. If description changes, run `document-skill` to update SKILLS.md
3. Document changes in commit message
4. Consider updating CHANGELOG.md for significant changes

**Examples**:
- `1.0.0 → 1.0.1` - Fixed typo in Process section
- `1.0.1 → 1.1.0` - Added new optional section for error handling
- `1.1.0 → 2.0.0` - Changed required input format (breaking change)

---

## Validation Checklist

Use this checklist when creating or updating skills (or run `validate-skill` to automate):

### Required Elements
- [ ] Frontmatter conforms to [AGENTS.md § Minimal Required Fields](AGENTS.md#minimal-required-fields)
- [ ] `author` field is present and non-empty in frontmatter (see AGENTS.md § Minimal Required Fields)
- [ ] No prohibited fields present (see [AGENTS.md § What NOT to Include](AGENTS.md#what-not-to-include))
- [ ] `name` is unique and kebab-case
- [ ] Core logic is platform-agnostic (describes WHAT, not HOW)
- [ ] Usage section shows natural language invocation examples

### Content Quality
- [ ] Process section has numbered steps with clear actions
- [ ] Examples show realistic usage scenarios
- [ ] Output format is documented (if applicable)
- [ ] Prerequisites are clear and complete
- [ ] Cross-references use correct relative paths
- [ ] Strategic code snippets are embedded only as guardrails within workflows, not as the primary logic

### Portability
- [ ] Tool references are generalized or in platform-specific notes
- [ ] Examples work across platforms
- [ ] No platform-specific assumptions in core logic

### SSOT Compliance
- [ ] No duplication of YAML field specifications from AGENTS.md
- [ ] No duplication of validation rules or prohibited fields
- [ ] External sources referenced, not copied (e.g., gists, standards)
- [ ] Domain-specific content is skill's own, not duplicated from elsewhere

---

## Complete Skill Example

Here's a well-formed skill demonstrating the structural elements:

```markdown
---
name: example-skill
description: Brief one-line description of the skill's purpose
version: 1.0.0
category: meta
tags: [example, demo]
---

# example-skill

Brief overview of what the skill does (1-2 paragraphs).

## Usage

- "Invoke this example skill"
- "Show me how the skill format works"

## Prerequisites

- Required dependencies or context.

## Process

### 1. First Step

Describe what the agent should do, not how.

### 2. Second Step

Continue the workflow.

## Output Format

Describe the expected result structure.

## Examples

**User**: "Invoke this example skill"

**Skill produces**:
`[Example output here]`

## Notes

- Platform-specific tips or additional caveats.
```

---

## Questions?

- **How does skill discovery work?** → See [AGENTS.md § Skill Discovery & Invocation](AGENTS.md#skill-discovery--invocation)
- **How do I create a new skill?** → Use the `create-skill` skill or see [CONTRIBUTING.md](CONTRIBUTING.md)
- **Where are skills stored?** → `skills/{skill-name}/SKILL.md` (flat structure)
- **How do platform shortcuts work?** → See `instructions/` for your specific platform
- **How do I validate my skill?** → Run `validate-skill` or use the checklist above
- **I found an issue** → File at https://github.com/bioconductor/ai-agent-skills/issues

---

**Version**: 3.0.0
**Last Updated**: 2026-07-07
**Authors**: bioconductor
