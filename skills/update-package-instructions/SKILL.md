---
name: update-package-instructions
description: Update existing AI instruction documentation when an R/Bioconductor package changes
version: 1.0.0
category: r-packages
tags: [r-packages, documentation, bioconductor]
author: waldronlab
---

# update-package-instructions

Update existing `.github/instructions/` files when an R/Bioconductor package changes, preserving manual customizations.

## Usage

Invoke this skill when your package has changed and you want to refresh the AI instructions:
- "Update the package instructions"
- "Sync instructions with current package state"

## Prerequisites

- Working directory is an R package root.
- Existing instructions exist at `.github/instructions/`.

## Process

1. **Analyze Current State**: Run the `analyze-r-package` skill to produce a current package analysis.
2. **Identify Changes**: Read existing `.github/instructions/` `.md` files. Compare the current package analysis to the documented state to identify changes in metadata (version, dependencies), structure (functions, vignettes, classes), and content (data sources).
3. **Determine Update Scope**: Check which template variables have changed by referencing `templates/package-instructions/README.md`. If a variable differs, its corresponding file needs an update.
4. **Apply Updates Strategy**:
   - **Preserve Custom Content**: Retain manually-added domain explanations, examples, and warnings.
   - **Update Systematically**: Update version numbers globally. Add new functions (with `[Description needed]`), remove deleted ones, and preserve custom descriptions.
   - **Targeted Edits**: Modify only the changed variables, rather than completely replacing files.
5. **Provide Update Summary**: Report the detected changes, updated files, and any items requiring manual review.

## Error Handling

- **No instructions found**: Direct the user to `create-package-instructions`.
- **Conflicts**: Prompt for a keep/replace/merge decision if manual changes conflict directly with template updates.

## Integration

- **Uses**: `analyze-r-package`
- **Works with**: `create-package-instructions`

---

**Related**: See [create-package-instructions](../create-package-instructions/SKILL.md), [analyze-r-package](../analyze-r-package/SKILL.md).
