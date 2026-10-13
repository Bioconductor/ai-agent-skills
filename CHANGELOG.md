# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **adr-author** (v1.0.0 → v1.1.0) - Adds scoping guidance, corrects the supersession rule, and
  corrects one point of Nygard attribution.
  - **New "Scoping an ADR" section.** The skill said when an ADR is warranted but nothing about how
    many. The test given is supersession granularity: an ADR's value is that it can be pointed at
    and reversed on its own, so bundling couples the futures of the decisions bundled. Includes the
    observation that an over-broad draft is usually not N ADRs but two decisions that never
    warranted a record, plus where those belong instead.
  - **Supersession corrected.** The skill said never to rewrite an accepted ADR. Nygard says the
    opposite about the status and the forward reference: "if a decision is reversed, we will keep
    the old one around, but mark it as superseded", "with a reference to its replacement". Editing
    the old record to point at its replacement is the mechanism. What must not be rewritten is the
    Context, Decision, or Consequences.
  - **Partial correction.** `deprecated` and `superseded` both retire a whole record, and the
    format offers nothing for "still in force except for one claim" — a case that arises as soon as
    ADRs start correcting each other in detail. Documents the convention this repository already
    uses in `docs/adr/0002-federated-protocol-repositories.md`: name the amended part in the Status
    line, and explain it in a banner under the metadata block.
  - **Attribution.** `Alternatives considered` was labelled part of the Nygard format. Nygard's
    elements are Title, Context, Decision, Status, Consequences. The section is kept, now named as
    the later addition it is.

### Removed
- **bioc-protocol-runner** - Moved to
  [`waldronlab/agent-protocol-standard`](https://github.com/waldronlab/agent-protocol-standard) and
  renamed `protocol-runner`. Its behaviour — trust ranking, protocol status handling, the
  `PROTOCOLS.yaml` fields it reads, and the Method Provenance block — is defined by
  `PROTOCOL_STANDARD.md` rather than by Bioconductor, so it now versions with that standard. Anyone
  who installed it should repoint at `agent-protocol-standard/skills/protocol-runner`. Amends
  ADR 0002 §1.

### Added
- **profile-r-package** (v1.0.0) - Measures where an R/Bioconductor package spends its
  `R CMD check` time and peak memory, then reduces both against the 10-minute and 8 GB submission
  expectations without changing results. `BiocCheck` cannot measure either figure, which
  `bioc-pkg-dev` notes at step 6 before moving on; this skill performs the build they require.
  - The measurement workflow is base R throughout - `R CMD check`, `tools::pkgVignettes`,
    `Rprof`/`summaryRprof`, `tracemem`, `Rprofmem`, `gc` - with GNU `time` as the only external
    tool, used for the one figure base R cannot reach: the peak memory of a child process.
    Bioconductor infrastructure is named only as remediation, for packages that already depend
    on it.
  - A single annotated run yields the total, the peak memory and the per-step breakdown.
    `_R_CHECK_TIMINGS_=0` is what produces the per-step `[user/elapsed]` annotations; unset, the
    threshold is infinite and nothing is annotated at any duration.
  - Records measurement traps verified on R 4.6.1 against jsonlite 2.0.0, digest 0.6.39 and
    R6 2.6.1: `--no-build-vignettes` runs vignette code
    and skips only the re-building of outputs; `checking running R code from vignettes` tangles and
    sources rather than weaving, so timing a full `buildVignette()` overstates the cost against this
    budget; `<pkg>-Ex.timings` rows carry a trailing tab that makes the default reader return
    `elapsed` as `NA`; the check log uses typographic quotes, so a straight-quote pattern matches
    nothing; GNU `time` reports the largest single process rather than a process tree; and a
    single-runner test framework reports one line for an entire suite.
  - Distinguishes peak resident memory from R's heap as reported by `gc()`, which excludes memory
    held by compiled code and therefore under-reports.
  - References upstream policy on wrapped examples, long-running tests and slow vignette chunks
    rather than restating it, per ADR 0003, and surfaces rather than resolves the upstream tension
    between the 40-minute `tests/` limit and the 10-minute whole-check expectation.
- **bioc-pkg-dev** (v1.0.0) - Guides an R package or a set of analysis scripts through
  Bioconductor submission: the pre-submission gate, the Contributions tracker, and post-acceptance
  maintenance.
  - Reports gate items in two tiers, separating what upstream states as requirements from what it
    states as recommendations, so a recommendation is not reported as a blocker.
  - Ships 21 task-oriented `knowledge/` summaries of the official guide, each linking back to its
    canonical chapter, loaded per topic rather than on every invocation.
  - Drives `BiocCheck` and `biocthis` rather than reimplementing validation or templates.
- SKILLS.md and USAGE.md entries for `bioc-pkg-dev` and `profile-r-package`.

## [3.0.0] - 2026-07-07

### Added
- **CI/CD Skills Validation**
  - Added GitHub Actions workflow `.github/workflows/validate-skills.yml` to run structural validation automatically on PRs.
  - Added deterministic check script `scripts/validate_skills.py` to enforce required frontmatter fields, name matching, uniqueness, link integrity, and version bumps.
  - Added `.github/copilot-instructions.md` to guide GitHub Copilot Code Review for inline subjective feedback on PRs.
- **Bioc-HowTo Integration**
  - Merged `waldronlab/ai-agent-skills` into the official `bioconductor/ai-agent-skills` repository.
  - Added `bioc-howto` skill and 11 R-oriented how-to guides (e.g. coverage computation, sequence composition, GRanges manipulation, BAM reading).
- **GitHub Pages Navigation**
  - Improved documentation structure and FAQ accessibility on GitHub Pages.

### Changed
- **validate-skill** (v1.1.0 → v1.2.0) - Updated with CI/CD integration note clarifying the local vs CI/CD division of labor.
- **antigravity** adapter (formerly gemini) - Updated setup instructions and renamed adapter to `instructions/antigravity.md`.

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
- check-bioconductor-skills - Verifies installation and lists available skills
- Complete r-packages skill suite (analyze-r-package, create-package-instructions, update-package-instructions)
- instructions/ directory with platform adapters (claude.md, copilot.md, antigravity.md)
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
