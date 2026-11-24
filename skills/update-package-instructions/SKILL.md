---
name: update-package-instructions
description: Update existing AI instruction documentation when an R/Bioconductor package changes
metadata:
  version: 1.0.2
  category: r-packages
  author: bioconductor
  tags: r-packages, documentation, bioconductor
---

# update-package-instructions

Update existing `.github/instructions/` files when an R/Bioconductor package changes, preserving manual customizations.

## Usage

- "Update the package instructions"
- "Sync instructions with current package state"

## Prerequisites

- Working directory is an R package root.
- Existing instructions exist at `.github/instructions/`.

## Process

1. **Analyze Current State**: Run the `analyze-r-package` skill to produce a current package analysis.
2. **Identify Changes**: Read existing `.github/instructions/` `.md` files. If there are none, direct the user to `create-package-instructions`. Compare the current package analysis to the documented state to identify changes in metadata (version, dependencies), structure (functions, vignettes, classes), and content (data sources).
3. **Determine Update Scope**: Check which template variables have changed by referencing `templates/package-instructions/README.md` at the root of the skills repository. If a variable differs, its corresponding file needs an update.
4. **Apply Update Strategy**:
   - **Preserve Custom Content**: Retain manually-added domain explanations, examples, and warnings. If a manual change conflicts directly with a template update, ask the user whether to keep, replace, or merge.
   - **Update Systematically**: Update version numbers globally. Add new functions (with `[Description needed]`), remove deleted ones, and preserve custom descriptions.
   - **Targeted Edits**: Modify only the changed variables, rather than completely replacing files.
5. **List Items for Manual Review**: Tell the user which entries were left as `[Description needed]` and which conflicts are unresolved.

## Examples

Since the instructions were written, the package version went from 1.4.0 to 1.5.2, `filterSamples()` was added, and `oldLoader()` was removed. The skill replaces `1.4.0` with `1.5.2` wherever it appears, adds a `filterSamples()` entry reading `[Description needed]`, and deletes the `oldLoader()` entry. Hand-written descriptions of the other functions and a maintainer's warning about API rate limits stay as they are, and files whose variables did not change are not touched.

---

**Related**: See [create-package-instructions](../create-package-instructions/SKILL.md), [analyze-r-package](../analyze-r-package/SKILL.md).
