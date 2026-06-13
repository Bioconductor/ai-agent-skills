---
name: create-skill
description: Help create a new AI agent skill through collaborative Q&A
version: 1.3.0
category: meta
tags: [meta, infrastructure, skill-creation]
author: waldronlab
---

# create-skill

Help create new AI agent skills through collaborative Q&A. Guides from rough ideas to structured skill files, focusing on intent over perfect formatting.

## Usage

Invoke this skill when you want to create a new skill:
- "Help me create a new skill for [domain/purpose]"

## Prerequisites

- You have a general idea of what you want the skill to do
- Working directory is the ai-agent-skills repository

## Process

1. Understand the user's intent through Q&A
2. Determine domain and location
3. Outline the process steps
4. Generate the skill file
5. Review and refine with user feedback
6. **Validate** the skill against repository standards
7. Update repository documentation

### 1. Understand the Intent

Start with open-ended questions:
- "What problem are you trying to solve?"
- "Who would use this skill?"
- "Can you give me an example of when you'd use this?"
- "What would be the typical input/output?"

### 2. Determine Domain and Location

**Existing domains**: `meta`, `r-packages`, `metagenomics`, `statistical-methods`
If uncertain, suggest the closest match. Convert purpose to kebab-case for the filename: "analyze R package" → `analyze-r-package`.

### 3. Outline the Process

Ask the user to walk through the steps. Capture major steps, key decisions, required inputs, expected outputs, and strategic code snippets (as guardrails). Help clarify and break down complex steps.

### 4. Generate the Skill File

Create a well-structured skill file following [AGENTS.md](../../AGENTS.md) and [SKILL_STANDARD.md](../../SKILL_STANDARD.md).
Do not duplicate SSOT guidelines; use references instead.
Fill in what's clear, use `TODO` markers for uncertainties, and prioritize clarity.

### 5. Review and Refine

Present a summary to the user, invite feedback ("Did I capture your intent correctly?"), and offer to iterate.

### 6. Validate the Skill

Before updating repository documentation, invoke `validate-skill` on the new file. Fix any CRITICAL issues. Only proceed to step 7 if validation passes.

### 7. Update Repository Documentation

Invoke `document-skill` by saying "Document the [skill-name] skill". It will automatically update `SKILLS.md`. Confirm completion with the user and suggest they test the skill.

## Output Format

Generate a markdown file saved to `skills/[skill-name]/SKILL.md`. See [SKILL_STANDARD.md](../../SKILL_STANDARD.md) for the required template and format.

## Key Principles

- **Skills are agent-agnostic**: No platform-specific metadata in the file
- **Describe what, not how**: Use "read the file" not "use Read tool"
- **Avoid duplication**: Reference authoritative sources instead of copying content

## Examples

### Example 1: Creating from Scratch
**User**: "I want to make a skill that helps validate R package documentation"
**Agent**: Engages in Q&A to understand documentation aspects, timing, and actions.
Result: `skills/validate-r-documentation/SKILL.md`

## Notes

- First draft doesn't need to be perfect—iteration expected
- Run `validate-skill` before `document-skill`
- Goal: lower the barrier to creating skills and sharing workflows

---

**Related**: See [SKILL_STANDARD.md](../../SKILL_STANDARD.md) for technical format details. See [AGENTS.md](../../AGENTS.md) for how agent discovery works.
