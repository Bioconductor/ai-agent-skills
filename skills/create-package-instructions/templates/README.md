# R Package Instruction Templates

This directory contains shared templates and standards used by the r-packages skills to generate package-specific instructions.

## Core Standards Documents

### [bioconductor-usage.md](bioconductor-usage.md)
**Purpose**: Understanding and using Bioconductor packages

For AI agents helping with **data analysis** and package usage:
- Working with S4 classes
- Common data structures (SummarizedExperiment, MultiAssayExperiment, etc.)
- Using accessor functions properly
- ExperimentHub/AnnotationHub data access
- BiocParallel for users
- Finding and understanding documentation

**Audience**: Data analysts, researchers, AI agents assisting with analysis workflows

### [bioconductor-development.md](bioconductor-development.md)
**Purpose**: Standards for developing Bioconductor/CRAN packages

For AI agents helping with **package development**:
- Code style and formatting requirements
- Function development best practices
- S4 class implementation and organization
- Documentation requirements (roxygen2)
- Testing standards (testthat)
- R CMD check and BiocCheck requirements
- Version numbering conventions
- Package structure requirements
- Dependency management
- Bioconductor submission requirements

**Audience**: Package developers, AI agents assisting with package development

**Usage**: Referenced by generated instruction files to avoid duplication of universal standards. Package-specific instructions focus on what's unique to that package.

### [waldronlab-standards.md](waldronlab-standards.md)
**Purpose**: Lab-specific conventions and patterns

Waldronlab conventions that complement Bioconductor standards:
- Git workflow (branch naming, commit messages)
- AI agent acknowledgments in commits
- Pull request guidelines
- Code organization patterns
- Documentation best practices
- Testing practices
- Domain-specific patterns (microbiome data, data access)
- Release process

**Usage**: Referenced by generated instruction files for lab-wide conventions.

## Architecture: Hybrid Approach

Generated package instructions follow a **hybrid approach**:

### Self-Contained Essentials
Package-specific `.github/instructions/` files include:
- Package classification and architecture
- Key functions and their purposes
- Package-specific patterns and conventions
- Custom validation patterns
- Special data handling for this package
- Vignette purposes and organization

### Referenced Standards
Package instructions **reference** (not duplicate) universal rules:
- Core Bioconductor standards → [bioconductor-development.md](bioconductor-development.md)
- Lab-wide conventions → [waldronlab-standards.md](waldronlab-standards.md)

### Example Structure

A generated `20-development.md` file looks like:

```markdown
# Development Patterns

For complete Bioconductor standards, see:
- [Core standards](https://github.com/waldronlab/ai-agent-skills/blob/main/skills/create-package-instructions/templates/bioconductor-development.md)
- [Waldronlab conventions](https://github.com/waldronlab/ai-agent-skills/blob/main/skills/create-package-instructions/templates/waldronlab-standards.md)

## Package-Specific Patterns

### S4 Classes

This package defines the following S4 classes:

#### MetagenomicData
**Slots**:
- `counts` (matrix): Raw count data
- `taxonomy` (data.frame): Taxonomic annotations
...

### Validation Patterns

Functions in this package use these validation helpers:
- `confirm_valid_uuid()` - Validates UUID format
- `check_parquet_structure()` - Verifies parquet column structure
...
```

## Benefits of This Approach

✅ **Single source of truth** - Update Bioconductor standards once, applies everywhere
✅ **Easier maintenance** - When standards change, update one file
✅ **Clearer separation** - Obvious what's universal vs package-specific
✅ **Reasonable self-containment** - Critical package context still inline
✅ **Flexibility** - Packages can customize without affecting others

## When to Update These Files

### Update bioconductor-standards.md when:
- Bioconductor package guidelines change
- CRAN policies update
- New best practices emerge for R package development
- testthat or roxygen2 introduce breaking changes

### Update waldronlab-standards.md when:
- Lab adopts new conventions
- Git workflow changes
- New domain-specific patterns emerge
- CI/CD practices evolve

### Do NOT include in these files:
- Package-specific patterns (belongs in package instructions)
- Project-specific requirements (belongs in project README)
- Ephemeral best practices (wait until stable)

## Future Template Additions

As the skills mature, we may add:

- `00-overview.template.md` - Template structure for package overviews
- `10-data-access.template.md` - Template for data package instructions
- `common-patterns/` - Reusable snippets for common scenarios
- `examples/` - Example instruction sets (currently in `../examples/`)

## Using These Templates

### For AI Agents Generating Instructions

When creating package instructions:

1. **Read package-specific information** (DESCRIPTION, README, code)
2. **Reference core standards** - Link to these template files
3. **Extract package patterns** - What's unique to this package
4. **Combine** - Self-contained context + references to standards

### For Humans Customizing Instructions

After generating instructions:

1. **Review accuracy** of package-specific patterns
2. **Add domain context** specific to your package
3. **Don't duplicate** standards already in these templates
4. **Do customize** where your package differs from conventions

## Version History

- **1.0.0** (2026-04-03) - Initial creation with bioconductor-standards.md and waldronlab-standards.md

---

**Maintainers**: waldronlab
**Purpose**: Shared standards and templates for R package instruction generation
