---
name: document-skill
description: Automate documentation updates to SKILLS.md after creating or modifying a skill
metadata:
  version: 1.1.0
  category: meta
  author: bioconductor
  tags: meta, infrastructure, documentation, automation
---

# document-skill

Update SKILLS.md after a skill is created or modified.

## Usage

- "Document the new skill I just created"
- "Update SKILLS.md for the validate-r-docs skill"

## Prerequisites

- Skill file exists at `skills/{skill-name}/SKILL.md`
- SKILLS.md exists in the repository root
- `validate-skill` should be run on the skill first

## Process

1. **Input and Validation**: Parse the `skills/{skill-name}/SKILL.md` file to extract YAML frontmatter and main sections.
2. **Generate SKILLS.md Entry**: Create a new entry following the format specified in [SKILLS.md](../../SKILLS.md). Auto-generate 2-3 natural language invocation examples. Present the generated entry to the user for confirmation and editing.
3. **Update SKILLS.md Sections**:
   - Check if the skill already exists in SKILLS.md. If so, prompt to replace.
   - Insert the entry alphabetically into the appropriate domain section.
   - Update the "By Category" and "By Tag" tables.
   - For a new skill, add `./skills/{skill-name}` to the `skills` list of exactly one plugin in `.claude-plugin/marketplace.json` (`bioc-r-packages` for package and analysis skills, `bioc-skill-authoring` for skills about this repository).
   - Ask the user if the skill should be added to the "Finding Skills by Use Case" section in [USAGE.md](../../USAGE.md).
4. **Confirm and Apply**: Show a summary of changes to SKILLS.md and apply them upon user confirmation.

## Examples

"Document the validate-r-docs skill I just created": a skill with `metadata.category: r-packages` and `metadata.tags: r-packages, validation` gets an entry under "R/Bioconductor Package Skills", is added to the `r-packages` row of "By Category", and is added to the `validation` row of "By Tag".
