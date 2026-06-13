---
name: check-waldronlab-skills
description: Verify that waldronlab/ai-agent-skills are available and help users find the right skill
version: 1.0.0
category: meta
tags: [meta, infrastructure, discovery]
author: waldronlab
---

# check-waldronlab-skills

Confirm waldronlab skills are installed and visible, then provide a concise catalog of available skills by querying SKILLS.md.

## Usage

Invoke this skill to check your setup or discover available skills:
- "Do I have the waldronlab skills?"
- "Is there a good waldronlab skill for [task]?"

## Prerequisites

- The `waldronlab/ai-agent-skills` repository is present locally.

## Process

1. **Read SKILLS.md** from the repository root.
2. **Parse** skill names, descriptions, and categories.
3. **List/Recommend**: Present skills organized by category, or recommend the 1-2 best-fit skills for a specific task.
4. **Report Status**: Start with "🏃 Levi says let's go!" if found, or "❌ Not detected" if missing.

## Examples

### Example: Discovery and Recommendation

**User**: "Do I have the waldronlab skills? Is there one for testing?"

**Agent**: (Reads SKILLS.md)
```
🏃 Levi says let's go!

Available waldronlab skills:
[Lists top-level categories and skills]

For testing, I recommend:
**Primary**: improve-code-coverage
[Rationale]
```

## Troubleshooting

- **Skills not detected**: Verify skill paths in editor settings, ensure the repository is cloned, and see platform-specific instructions.
- **Duplicate listings**: Multiple configuration locations pointing to the same skills (normal).

---

**Related**: See [SKILLS.md](../../SKILLS.md) for the complete index.
