---
name: create-package-instructions
description: Create complete AI instruction documentation for an R/Bioconductor package in .github/instructions/
version: 1.0.0
category: r-packages
tags: [r-packages, documentation, bioconductor]
author: waldronlab
---

# create-package-instructions

Create complete AI instruction documentation for an R/Bioconductor package in `.github/instructions/`.

## Usage

Invoke this skill when you want to generate AI-friendly documentation for an R package:
- "Create instructions for this package"
- "Create .github/instructions for this R package"

## Prerequisites

- Working directory is an R package root (contains DESCRIPTION file).

## Process

1. **Run Package Analysis**: Invoke `analyze-r-package` to understand the package structure.
2. **Determine Required Instruction Files**: Based on the analysis, select the appropriate templates from `templates/package-instructions/`:
   - `00-overview.md.template` (Always)
   - `10-data-access.md.template` (If Type: Remote or Hybrid)
   - `20-development.md.template` (Always)
   - `30-testing-and-docs.md.template` (Always)
   - `40-vignettes.md.template` (If Vignettes > 0)
   - `INDEX.md.template` (Always)
3. **Create Directory**: Ensure `.github/instructions/` exists.
4. **Create Files from Templates**: Perform variable substitution for each `{{VARIABLE_NAME}}` using the analysis output (refer to `templates/package-instructions/README.md` for mappings). Write the results to `.github/instructions/`.
5. **Update Package Config**:
   - Ensure `.github/instructions/` is NOT ignored in `.gitignore`.
   - Add `^\.github/instructions$` to `.Rbuildignore`.
6. **Provide Summary**: Inform the user about the files created, documented functions, and next steps.

## Error Handling

- **Analysis fails**: Propagate error, provide guidance.
- **Instructions exist**: Ask user to overwrite or use `update-package-instructions`.
- **Template not found**: Verify templates directory exists.

## Integration

- **Uses**: `analyze-r-package`
- **Works with**: `update-package-instructions`

---

**Related**: See [analyze-r-package](../analyze-r-package/SKILL.md), [update-package-instructions](../update-package-instructions/SKILL.md).
