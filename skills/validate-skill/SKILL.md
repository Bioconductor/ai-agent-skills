---
name: validate-skill
description: Validate that a skill conforms to the ai-agent-skills repository standards
version: 1.2.0
category: meta
tags: [meta, infrastructure, validation, quality-control]
author: bioconductor
---

# validate-skill

Validate that a skill conforms to bioconductor standards. Uses generic validators (markdownlint, yamllint) for basic checks, then adds bioconductor-specific validation for platform-agnostic compliance and repository conventions.

## Usage

Invoke this skill to validate a skill file:
- "Validate this skill"
- "Check if skills/[skill-name]/SKILL.md meets standards"

## Prerequisites

- Target skill file exists at `skills/{skill-name}/SKILL.md`
- Optional: `markdownlint` and `yamllint` installed

> **Note — CI/CD integration**: The deterministic subset of these checks
> (frontmatter completeness, directory-name matching, name uniqueness,
> SKILLS.md sync, broken links, version bump) runs automatically via GitHub
> Actions on every PR that modifies a `SKILL.md` file. Use this skill for
> **interactive local validation** before opening a PR and for the full
> subjective review (agent neutrality, verbosity, SSOT compliance) that the
> static script cannot evaluate.

## Process

1. **Locate Target Skill**: Determine the skill to validate from the user's prompt or current directory.
2. **Run Generic Validation (Optional)**: If available, run `markdownlint` on the file, and validate the YAML frontmatter syntax (e.g., by extracting the frontmatter and running `yamllint -d relaxed` on it).
3. **Validate Repository Standards**: Check the file against the requirements in [AGENTS.md](../../AGENTS.md) and [SKILL_STANDARD.md](../../SKILL_STANDARD.md).
   - Ensure the YAML frontmatter contains required fields and no prohibited fields (`platforms`, `triggers`).
   - Check that the structure matches the standard format.
   - Verify agent neutrality (no tool references or platform commands in instructions).
   - Confirm it describes a workflow, not just code snippets.
   - Ensure it does not duplicate content from SSOT documents.
4. **Generate Validation Report**: Produce a summary of passed and failed checks, categorized by CRITICAL, WARNING, and INFO.
5. **Suggest Next Steps**: Offer to help fix any identified issues.

## Output Format

Generate a validation report in markdown format:

```markdown
# Skill Validation Report: [skill-name]

**Status**: ✅ PASS | ❌ FAIL ([N] issues)

## Generic Validation
**markdownlint**: ✅ PASS | ⚠️ [N] warnings
**YAML frontmatter**: ✅ PASS | ❌ FAIL

## Bioconductor-Specific Validation
### CRITICAL Issues (Must Fix)
❌ **[Issue title]** ([location])
   - Issue: [What violates standards]
   - Fix: [How to fix it]
   - Reference: [AGENTS.md or SKILL_STANDARD.md section]

### WARNING Issues (Should Fix)
⚠️ **[Issue title]** ([location])

### INFO Issues (Optional Improvements)
ℹ️ **[Issue title]** ([location])
```

## Examples

### Example: Validating a Skill
**User**: "Check if the analyze-r-package skill meets standards"
**Agent**:
1. Locates `skills/analyze-r-package/SKILL.md`
2. Runs generic and repository-specific validations
3. Reports results, identifying any CRITICAL or WARNING issues.

---

**See also**: [SKILL_STANDARD.md](../../SKILL_STANDARD.md), [AGENTS.md](../../AGENTS.md)
