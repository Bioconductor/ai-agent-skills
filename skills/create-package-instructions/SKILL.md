---
name: create-package-instructions
description: Create complete AI instruction documentation for an R/Bioconductor package in .github/instructions/
version: 1.0.1
category: r-packages
tags: [r-packages, documentation, bioconductor]
author: bioconductor
---

# create-package-instructions

Create complete AI instruction documentation for an R/Bioconductor package in `.github/instructions/`.

## Usage

- "Create instructions for this package"
- "Create .github/instructions for this R package"

## Prerequisites

- Working directory is an R package root (contains DESCRIPTION file).

## Process

1. **Run Package Analysis**: Invoke `analyze-r-package` to understand the package structure.
2. **Determine Required Instruction Files**: Based on the analysis, select the appropriate templates from `templates/package-instructions/` at the root of the skills repository:
   - `00-overview.md.template` (Always)
   - `10-data-access.md.template` (If Type: Remote or Hybrid)
   - `20-development.md.template` (Always)
   - `30-testing-and-docs.md.template` (Always)
   - `40-vignettes.md.template` (If Vignettes > 0)
   - `INDEX.md.template` (Always)
3. **Create Files from Templates**: If `.github/instructions/` already holds instruction files, ask the user whether to overwrite them or to use `update-package-instructions` instead. Perform variable substitution for each `{{VARIABLE_NAME}}` using the analysis output (refer to `templates/package-instructions/README.md` for mappings). Write the results to `.github/instructions/`.
4. **Update Package Config**:
   - Ensure `.github/instructions/` is NOT ignored in `.gitignore`.
   - Add `^\.github/instructions$` to `.Rbuildignore`.

## Examples

The analysis reports data sources of Type: Remote and no vignettes. The skill writes five files, each named after its template without the `.template` suffix: `00-overview.md`, `10-data-access.md`, `20-development.md`, `30-testing-and-docs.md`, and `INDEX.md`.

---

**Related**: See [analyze-r-package](../analyze-r-package/SKILL.md), [update-package-instructions](../update-package-instructions/SKILL.md).
