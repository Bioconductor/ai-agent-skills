---
name: document-skill
description: Automate documentation updates to SKILLS.md after creating or modifying a skill
version: 1.0.2
category: meta
tags: [meta, infrastructure, documentation, automation]
author: bioconductor
---

# document-skill

Automate updating SKILLS.md after creating or modifying a skill. Reads the skill file, generates entries, and updates all relevant sections with user confirmation.

## Usage

Invoke this skill after creating or modifying a skill file:
- "Document the new skill I just created"
- "Update SKILLS.md for the validate-r-docs skill"

## Prerequisites

- Skill file exists at `skills/{skill-name}/SKILL.md`
- SKILLS.md exists in the repository root

## Process

1. **Input and Validation**: Parse the `skills/{skill-name}/SKILL.md` file to extract YAML frontmatter and main sections.
2. **Generate SKILLS.md Entry**: Create a new entry following the format specified in [SKILLS.md](../../SKILLS.md). Auto-generate 2-3 natural language invocation examples. Present the generated entry to the user for confirmation and editing.
3. **Update SKILLS.md Sections**:
   - Check if the skill already exists in SKILLS.md. If so, prompt to replace.
   - Insert the entry alphabetically into the appropriate domain section.
   - Update the "By Category" and "By Tag" tables.
   - Ask the user if the skill should be added to the "Finding Skills by Use Case" section in [USAGE.md](../../USAGE.md).
4. **Confirm and Apply**: Show a summary of changes to SKILLS.md and apply them upon user confirmation.

## Output Format

This skill produces an updated **SKILLS.md** file. No new files are created.

## Examples

### Example: Documenting a New Skill
**User**: "Document the validate-r-docs skill I just created"
**Agent**:
1. Reads `skills/validate-r-docs/SKILL.md`.
2. Generates entry with invocation examples and shows a preview.
3. Adds to the "R/Bioconductor Domain" section and updates Category/Tag tables.
4. User confirms, SKILLS.md is updated.
5. Reports: "✅ Documentation updated successfully!"

## Integration with Other Skills

- **create-skill**: Automatically invoked at the end of the skill creation workflow.
- **validate-skill**: Should be run before document-skill to ensure standards compliance.

---

**Related**: See [SKILLS.md](../../SKILLS.md) for the skill catalog format.
