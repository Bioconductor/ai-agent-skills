---
name: check-bioconductor-skills
description: Verify that bioconductor/ai-agent-skills are available and help users find the right skill
version: 1.1.0
category: meta
tags: [meta, infrastructure, discovery]
author: bioconductor
---

# check-bioconductor-skills

Confirm bioconductor skills are installed and visible, then provide a concise catalog of available skills by querying SKILLS.md.

## Usage

Invoke this skill to check your setup or discover available skills:
- "Do I have the bioconductor skills?"
- "Is there a good bioconductor skill for [task]?"

## Prerequisites

- The `bioconductor/ai-agent-skills` repository is present locally.

## Process

1. **Read SKILLS.md** from the repository root — this is the primary discovery mechanism.
2. **Read USAGE.md** (if present) for the "Finding Skills by Use Case" section, which provides curated task-to-skill mappings for richer recommendations.
3. **Parse** skill names, descriptions, and categories from SKILLS.md.
4. **List/Recommend**: Present skills organized by category, or recommend the 1-2 best-fit skills for a specific task. Use the use-case mappings from USAGE.md when the user asks task-oriented questions (e.g. "Is there a skill for X?").
5. **Report Status**: Start with "✅ Skills detected" if found, or "❌ Skills not detected" if missing.

## Examples

### Example: Discovery and Recommendation

**User**: "Do I have the bioconductor skills? Is there one for testing?"

**Agent**: (Reads SKILLS.md and USAGE.md)
```
✅ Skills detected

Available bioconductor skills:
[Lists top-level categories and skills]

For testing, I recommend:
**Primary**: improve-code-coverage
[Rationale]
```

## Troubleshooting

- **Skills not detected**: Verify skill paths in editor settings, ensure the repository is cloned, and see platform-specific instructions.
- **Duplicate listings**: Multiple configuration locations pointing to the same skills (normal).

---

**Related**: See [SKILLS.md](../../SKILLS.md) for the complete index and [USAGE.md](../../USAGE.md) for use-case guidance.
