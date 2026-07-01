# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- metagenomics analysis skills
- statistical-methods skills

## [2.1.0] - 2026-04-03

### Added
- **security-audit-r-package** (v1.0.0) - Comprehensive security auditing for R/Bioconductor packages
  - Analyzes R code, native code (C/C++/Fortran), dependencies, and package structure
  - References external gist as single source of truth for security checks and issue labels
  - Flexible output formatting (structured reports for full audits, concise for quick checks)
  - Supports targeted audits (specific files/directories) or full package scope
- AGENTS.md § Avoiding Content Duplication - Guidelines for preventing SSOT violations
- SKILL_STANDARD.md § SSOT Compliance checklist

### Changed
- **create-skill** (v1.2.1 → v1.3.0) - Added comprehensive "Avoiding SSOT Violations" guidance
  - SSOT = Single Source of Truth (avoid duplicating content across skills, documentation, validation)
  - Lists what not to duplicate (YAML specs, validation criteria, external checklists)
  - Provides reference patterns with examples
  - Documents signs of SSOT violation and fix patterns
- **validate-skill** (v1.0.1 → v1.1.0) - Added SSOT violation detection
  - New validation step 8: "Check for SSOT Violations"
  - Flags common duplication patterns (field lists, templates, copied checklists)
  - Validates proper reference patterns
- **document-skill** (v1.0.1) - Reduced duplication in YAML field descriptions

### Improved
- Meta skills now reference AGENTS.md as single source of truth (~95 lines of duplication removed)
- All YAML field specifications reference AGENTS.md § Skill File Format
- All validation criteria reference AGENTS.md § Minimal Required Fields / What NOT to Include
- Validation report templates simplified (reduced from 76 lines to ~30 lines)
- SKILL_STANDARD.md updated to v2.1.0 with SSOT compliance checklist

## [2.0.0] - 2026-04-03

### Changed
- **BREAKING**: Migrated to agent-agnostic skill format
- Removed `platforms:` and `triggers:` fields from all skills
- Shifted to natural language invocation via SKILLS.md discovery
- Updated all skills to use platform-agnostic language
- Platform shortcuts now documented only in instructions/{agent}.md

### Added
- AGENTS.md - Canonical agent behavior standard
- SKILL_STANDARD.md - Quick reference with checklist and examples
- document-skill - Automates SKILLS.md updates after skill creation
- validate-skill - Validates skills against repository standards
- check-waldronlab-skills - Verifies installation and lists available skills
- Complete r-packages skill suite (analyze-r-package, create-package-instructions, update-package-instructions)
- instructions/ directory with platform adapters (claude.md, copilot.md, gemini.md)
- Migration guide in SKILL_STANDARD.md for v1.x users

### Improved
- SKILLS.md now serves as single source of truth for skill catalog
- Comprehensive documentation with clear separation of concerns
- Example from parkinsonsMetagenomicData (data-package-parquet)

## [0.1.0] - 2026-04-03

### Added
- Initial release
- Repository structure created
- Basic documentation framework
- First experimental skills

---

## Version Guidelines

### Major Version (X.0.0)
- Breaking changes to skill interface
- Incompatible instruction format changes
- Major reorganization

### Minor Version (0.X.0)
- New skills added
- New examples added
- New features in existing skills (backwards compatible)
- New domain directories

### Patch Version (0.0.X)
- Bug fixes
- Documentation improvements
- Template refinements
- Example updates
