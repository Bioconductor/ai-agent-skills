# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **AGENTS.md** (v2.0.0 → v2.1.0) - Adds core principle 7, "Only What an Agent Wouldn't Do
  Unprompted": each line of a skill must change what a competent coding agent does. General
  practice, rules stated twice, examples that replay the process, and provenance are removed or
  moved to a `SOURCES.md`. SKILL_STANDARD.md's checklist references it.
- **validate-skill** (v1.2.0 → v1.3.0) - Checks skills against the new principle: flags lines a
  competent coding agent would not need, and rules stated more than once.
- **draft-r-package-pr** (v1.0.0 → v1.1.0) and **update-r-news** (v1.2.0 → v1.3.0) - Trimmed
  under the new principle, as a pilot for the other skills. Each is about half its previous length.
  - **draft-r-package-pr**: general title and description advice is removed, leaving what is
    particular to R and Bioconductor packages. Sources and the list of the skill's own conventions
    move to `SOURCES.md`. The PR description lists new dependencies, the agent is told not to
    introduce the focus problems it checks for (including roxygen2 churn when regenerating
    `man/`), and the whitespace check also covers blank lines. The separate vignette
    check is dropped, since `R CMD build` builds them. The description no longer cites tidyverse
    guidance.
  - **update-r-news**: the Error Handling and Notes sections, which restated the steps, are
    removed, and five examples become two that show input commits and the drafted output. Vague
    commits are identified by judgment instead of a word count and phrase list. The commit range
    is found with one `git log --grep` command. NEWS files in `inst/` are now detected, a file
    with entries but no category headings stays that way, entries follow the file's existing
    order for the issue number and username, and a block added to `NEWS.Rd` goes after its header.
    Diff inspection also covers `vignettes/`.
  - **Credit in NEWS entries**: both skills now credit the person who wrote the change. For a
    change that came through a PR, `update-r-news` cites the PR and its author, even when the PR
    fixes an issue someone else reported; before, it credited whoever opened the referenced issue
    or PR, which disagreed with `draft-r-package-pr`.
- **update-r-news** (v1.1.0 → v1.2.0) - Specifies the version heading for unpublished packages
  and handles non-Bioconductor packages.
  - A Bioconductor package below version `1.0.0` (e.g. `0.99.3` or `0.0.14`) puts new entries
    under a `1.0.0` heading, the version Bioconductor gives a first release, instead of a heading
    derived from the pre-release version. Existing pre-release headings, such as `0.99.2` or
    `(development version)`, are offered for merging into that block.
  - A package counts as Bioconductor only when `DESCRIPTION` has a `biocViews` or `BiocType`
    field. Otherwise it is treated as a CRAN or GitHub package: the user picks the heading
    version, and the commit range starts at the latest release tag or a user-supplied commit.
- **update-r-news** (v1.0.0 → v1.1.0) - Adjusts the NEWS style it drafts, based on use with
  Bioc.gff.
  - **No commit SHAs in entries.** The version heading tells users which release a change is in;
    entries keep issue and PR references such as `(#45)` only. The `NEWS.md` example also used
    `(#abc1234)`, which is GitHub's issue syntax, not a commit reference.
  - **Default categories.** When the NEWS file has no headings yet, the default set is `NEW
    FEATURES`, `SIGNIFICANT USER-VISIBLE CHANGES`, `BUG FIXES AND MINOR IMPROVEMENTS`, and
    `DEPRECATED AND DEFUNCT`. Internal changes (dependencies, documentation, CI, tests) go under
    `BUG FIXES AND MINOR IMPROVEMENTS` instead of a separate `INTERNAL CHANGES` heading, unless the
    file already uses one.
  - **Match the existing file.** The new block follows the existing version heading style (e.g.
    `# pkgname 1.18.0`) and bullet marker.
  - **Omit version bumps** and allow related commits, such as a fix and its tests, to share one
    entry.
  - **Layout-only `NAMESPACE` changes.** Compare directives, not diff lines, since a new roxygen2
    version can regroup imports without changing them.
  - **Credit issue and PR authors.** Entries that reference an issue or pull request add the GitHub
    username of the person who opened it, e.g. `(#1, @username)`, looked up with `gh api`. If the
    lookup is not possible, the entry keeps the number and is flagged for review.
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
- **draft-r-package-pr** (v1.0.0) - Drafts the title, description, and pre-submission checks for a
  pull request against an R/Bioconductor package.
  - Title, description, and scope guidance follows the tidyteam code review principles and the
    usethis tidyverse contributing template, cited with pinned commits.
  - Requires the AI and third-party code disclosure from Bioconductor's contributions guide.
  - Flags whitespace-only changes for removal, since they distract reviewers; new code matches the
    file's indentation, falling back to Bioconductor's 4-space style.
  - Advises against version bumps in PRs: Bioconductor's per-push bump is left to the maintainer
    when pushing to `git.bioconductor.org`.
  - NEWS entries, drafted with `update-r-news`, are welcome but not required, and follow its
    heading and credit conventions.
  - Reads maintainer vs. outside contributor from `Authors@R`, handles hand-written Rd when
    `DESCRIPTION` has no roxygen2 field, and reuses existing CI results instead of re-running checks.
- **bioc-pkg-dev** (v1.0.0) - Guides an R package or a set of analysis scripts through
  Bioconductor submission: the pre-submission gate, the Contributions tracker, and post-acceptance
  maintenance.
  - Reports gate items in two tiers, separating what upstream states as requirements from what it
    states as recommendations, so a recommendation is not reported as a blocker.
  - Ships 21 task-oriented `knowledge/` summaries of the official guide, each linking back to its
    canonical chapter, loaded per topic rather than on every invocation.
  - Drives `BiocCheck` and `biocthis` rather than reimplementing validation or templates.
- SKILLS.md and USAGE.md entries for the new skills.

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
