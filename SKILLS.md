---
layout: default
title: Skills Index
nav_order: 2
---
# Available Skills
{: .no_toc}

<details markdown="1">
<summary><b>📖 Table of Contents (click to expand)</b></summary>

* TOC
{:toc}

</details>

---

This is the canonical index of all available AI agent skills in the bioconductor/ai-agent-skills repository. Use this to discover and understand what skills are available and when to use them.

> **Note**: For instructions on how to use these skills, see the [Skills Usage Guide](USAGE.md). All skills are located at `skills/{skill-name}/SKILL.md`.


## Meta Skills

Infrastructure and workflow skills for working with this repository itself.

### adr-author

**Purpose**: Write a new Architecture Decision Record following the established Nygard format and conventions.

**When to use**:
- Documenting a non-trivial, behavior-affecting decision
- When you need to create an ADR

**Invocation**:
- "Write an ADR for..."
- "Record the decision to..."
- "Document the design rationale for..."

**Output**: A new ADR file in the target repository's `docs/adr/` directory

---


### create-skill

**Purpose**: Help create a new AI agent skill through collaborative Q&A

**When to use**:
- Creating a new skill from scratch or from a manual workflow

**Invocation**:
- "Help me create a new skill"
- "Create a skill for [domain]"

**Output**: A complete skill with validated file and updated SKILLS.md, ready for testing and committing

**Related skills**: validate-skill, document-skill, check-bioconductor-skills

---

### check-bioconductor-skills

**Purpose**: List and verify installed bioconductor skills

**When to use**:
- Verifying skills are correctly installed or discovering available skills

**Invocation**:
- "What skills are available?"
- "List bioconductor skills"

**Output**: List of available skills and setup status

---

### validate-skill

**Purpose**: Validate that a skill conforms to the ai-agent-skills repository standards

**When to use**:
- Creating new skills, reviewing PRs, or ensuring standards compliance

**Invocation**:
- "Validate this skill"
- "Check if skills/[skill-name]/SKILL.md meets standards"

**Output**: Comprehensive validation report with pass/fail status, categorized issues, and specific fix suggestions

**Related skills**: create-skill, check-bioconductor-skills, document-skill

---

### document-skill

**Purpose**: Automate documentation updates to SKILLS.md after creating or modifying a skill

**When to use**:
- After creating a new skill or modifying an existing skill to update SKILLS.md

**Invocation**:
- "Document the new skill I just created"
- "Update SKILLS.md for the validate-r-docs skill"

**Output**: Updated SKILLS.md with the skill entry added to all relevant sections

**Related skills**: create-skill, validate-skill, check-bioconductor-skills

---

## R/Bioconductor Package Skills

Skills for analyzing, documenting, and developing R/Bioconductor packages following bioconductor conventions.

### analyze-r-package

**Purpose**: Analyze R/Bioconductor package structure and characteristics

**When to use**:
- Understanding a package's architecture, type, or identifying key functions

**Invocation**:
- "Analyze this R package"
- "What type of package is this?"

**Output**: Structured analysis of the package

---

### create-package-instructions

**Purpose**: Generate comprehensive .github/instructions files for R/Bioconductor packages

**When to use**:
- Creating AI agent instructions for a new R package or standardizing documentation

**Invocation**:
- "Create .github/instructions for this package"
- "Generate AI agent instructions"

**Output**: Modular instruction files in `.github/instructions/`

**Related skills**: analyze-r-package, update-package-instructions

---

### update-package-instructions

**Purpose**: Update existing .github/instructions files based on recent package changes

**When to use**:
- Refreshing package instructions after major architecture or pattern changes

**Invocation**:
- "Update the package instructions"
- "Refresh .github/instructions"

**Output**: Updated `.github/instructions/` files

**Related skills**: analyze-r-package, create-package-instructions

---

### improve-code-coverage

**Purpose**: Analyze R package code coverage using covr, audit existing tests for tautological assertions, classify testing gaps, and proactively write test cases to improve coverage and result correctness.

**When to use**:
- Evaluating testing rigor, auditing for vacuous or tautological tests, identifying gaps, and proactively writing test cases

**Invocation**:
- "Check my code coverage and help me write missing tests."
- "Audit my existing tests for tautological or vacuous test cases."
- "Improve code coverage, focusing on edge cases and correctness."

**Output**: A chat summary breaking down coverage by test category and audit findings, and code blocks containing framework-native test cases.

**Related skills**: analyze-r-package, security-audit-r-package

---

### security-audit-r-package

**Purpose**: Perform comprehensive security audit of R/Bioconductor packages

**When to use**:
- Auditing packages before CRAN/Bioconductor submission or reviewing for vulnerabilities

**Invocation**:
- "Run security audit on this R package"
- "Check this package for security vulnerabilities"

**Output**: Security audit report (markdown format) with findings categorized by severity.

**Related skills**: analyze-r-package, validate-skill, create-package-instructions

---

### build-check-bioccheck

**Purpose**: Run and interpret R CMD build, R CMD check, and both BiocCheck entry points against a Bioconductor package, separating real defects from environment gaps and known false positives

**Location**: `skills/build-check-bioccheck/SKILL.md`

**When to use**:
- Checking whether a package passes the Bioconductor validation gate
- Interpreting a BiocCheck ERROR, WARNING or NOTE
- Distinguishing a real package defect from a missing build tool, an account-level setting, or a known false positive

**Invocation**:
- "Run BiocCheck on this package"
- "Does this package pass the Bioconductor checks?"
- "Why is BiocCheck reporting this error?"

**Output**: Per-step results with a pass/blocked verdict, findings classified as defect / environment / account action / false positive

**Related skills**: bioc-pkg-dev, analyze-r-package, improve-code-coverage

---

### bioc-pkg-dev

**Purpose**: Guide an R package or a set of analysis scripts through Bioconductor submission: the pre-submission gate, the Contributions tracker, and post-acceptance maintenance

**Location**: `skills/bioc-pkg-dev/SKILL.md`

**When to use**:
- Asking whether a package is ready to submit to Bioconductor, or what a reviewer would flag
- Preparing a package on GitHub for the Bioconductor Contributions tracker
- Turning analysis scripts into a submittable package, or moving a package from CRAN to Bioconductor
- Working on `biocViews`, `BiocCheck`, version numbering, vignettes, or large-data placement
- Maintaining an accepted package on `git.bioconductor.org`

**Invocation**:
- "Is this package ready to submit to Bioconductor?"
- "Get this package ready for Bioconductor"
- "Turn these analysis scripts into a Bioconductor package"
- "How do I push to git.bioconductor.org after acceptance?"

**Output**: A two-tier gap report separating hard blockers from likely reviewer requests, ending in a submittable-or-not verdict; or a targeted answer citing the canonical guide chapter

**Related skills**: analyze-r-package, security-audit-r-package, improve-code-coverage, update-r-news, bioc-pkg-review

---

### bioc-pkg-finder

**Purpose**: Find the R / Bioconductor packages best suited to a task or workflow

**When to use**:
- When the user asks "what package should I use for X" or "is there a Bioconductor package that does Y"
- Assembling an analysis workflow and needing to pick tools

**Invocation**:
- "What package should I use for differential expression?"
- "Is there a Bioconductor package that does single-cell clustering?"
- "Which package is standard for variant annotation?"

**Output**: Recommended package(s) with biocViews term or CRAN Task View source, install path, and the key gotcha for the recommended tool

**Related skills**: analyze-r-package, create-package-instructions

---

### bioc-pkg-review

**Purpose**: Review your own R package against the rubric and checklist Bioconductor's agent-assisted reviewer uses, before you submit, so the human review has less to say

**When to use**:
- Before opening a BiocContributions tracker issue, after the gate (`build-check-bioccheck`) passes
- When a reviewer's feedback arrives and you want to check the rest of the package the same way
- When you want the Package Review Checklist filled for a package

**Invocation**:
- "Review my package for Bioconductor submission"
- "What will the Bioconductor reviewer say about this package?"
- "Fill the Package Review Checklist for this package"

**Output**: Numbered findings with rubric id, severity, evidence and a suggested fix; what the human reviewer will weigh (overlap, provenance); the Package Review Checklist filled Y / N / N/A / ?; Blockers, likely reviewer requests, verdict

**Related skills**: bioc-pkg-dev, build-check-bioccheck, bioc-pkg-finder

---

### update-r-news

**Purpose**: Draft or update an R package NEWS file from git commit history, examining diffs when commit messages are vague

**Location**: `skills/update-r-news/SKILL.md`

**When to use**:
- Adding a NEWS entry before a Bioconductor release
- Drafting a changelog from recent commits
- Updating `NEWS.md`, `NEWS`, or `NEWS.Rd` after a development cycle
- Saving time when commit messages alone are insufficient to write clear NEWS entries

**What happens**:
- Detects the NEWS file format in use (`NEWS.md`, `NEWS`, or `NEWS.Rd`)
- Derives the upcoming even-numbered release version from the current devel version
- Finds the most recent Bioconductor devel-version bump commit ("bump x.y.z version to odd y...") and retrieves all commits since then
- Extracts PR titles from merge commits when available
- Identifies vague commit messages (≤ 3 words or known filler phrases) and inspects their diffs to infer what changed
- Categorises changes using headings already present in the NEWS file
- Shows a full preview and asks for confirmation before writing to disk

**Output**: A drafted NEWS block shown for review; upon confirmation, the updated NEWS file on disk with the new version block prepended.

**Related skills**: analyze-r-package, update-package-instructions

---

## Bioconductor How-Tos

Skills indexing focused, practical how-tos for common Bioconductor data analysis tasks.

### bioc-howto

**Purpose**: A consolidated index of Bioconductor how-to skills covering genomics, sequencing, and omics data analysis tasks

**When to use**:
- Looking for step-by-step instructions for common Bioconductor tasks (e.g., loading BAM files, manipulating GRanges, extracting sequences)
- Needing examples of standard Bioconductor workflows

**Invocation**:
- "How do I do [task] in Bioconductor?"
- "Can you show me a Bioconductor how-to for [task]?"
- "Check the bioc-howto index for [task]"

**Output**: Links to and instructions from the relevant how-to markdown file.

---

## Protocols

Protocol execution lives in
[`waldronlab/agent-protocol-standard`](https://github.com/waldronlab/agent-protocol-standard), not
here. Its [`protocol-runner`](https://github.com/waldronlab/agent-protocol-standard/tree/main/skills/protocol-runner)
skill discovers protocols across the federation, ranks them by trust and status, and emits a Method
Provenance block before executing anything — semantics that belong to the protocol standard rather
than to Bioconductor, so the skill versions with it. See the amendment to
[ADR 0002](docs/adr/0002-federated-protocol-repositories.md).

---

## Skill Categories & Tags

### By Category

| Category | Skills | Purpose |
|----------|--------|---------|
| **meta** | adr-author, check-bioconductor-skills, create-skill, document-skill, validate-skill | Repository and workflow infrastructure |
| **r-packages** | analyze-r-package, bioc-pkg-dev, bioc-pkg-finder, bioc-pkg-review, create-package-instructions, improve-code-coverage, security-audit-r-package, update-package-instructions, update-r-news | R/Bioconductor package development |
| **bioconductor-how-tos** | bioc-howto | Bioconductor data analysis practical guides |

### By Tag

| Tag | Skills | Use Case |
|-----|--------|----------|
| **infrastructure** | create-skill, check-bioconductor-skills, document-skill, validate-skill | Repository and workflow tasks |
| **testing** | improve-code-coverage | Software testing and coverage |
| **validation** | security-audit-r-package, validate-skill | Quality control and standards compliance |
| **quality-control** | security-audit-r-package, validate-skill | Ensuring skill quality |
| **documentation** | adr-author, create-package-instructions, document-skill, update-package-instructions, update-r-news | Generating and maintaining docs |
| **adr** | adr-author | Architecture Decision Records |
| **architecture** | adr-author | Architectural decisions |
| **decision** | adr-author | Documenting decisions |
| **automation** | document-skill, update-r-news | Automating repetitive documentation tasks |
| **analysis** | analyze-r-package, bioc-pkg-finder | Understanding code and architecture |
| **security** | security-audit-r-package | Security audits and vulnerability detection |
| **audit** | security-audit-r-package | Comprehensive code auditing |
| **bioconductor** | analyze-r-package, bioc-pkg-dev, bioc-pkg-finder, bioc-pkg-review, create-package-instructions, improve-code-coverage, security-audit-r-package, update-package-instructions, update-r-news | Bioconductor-specific workflows |
| **submission** | bioc-pkg-dev, bioc-pkg-review | Preparing and submitting a package to Bioconductor |
| **bioccheck** | bioc-pkg-dev | The BiocCheck pre-submission gate |
| **biocviews** | bioc-pkg-dev | biocViews terms and package classification |
| **peer-review** | bioc-pkg-dev, bioc-pkg-review | Bioconductor peer review expectations |
| **checklist** | bioc-pkg-review | The Package Review Checklist, filled from a self-review |
| **self-review** | bioc-pkg-review | Reviewing your own package with the reviewer's rubric |
| **code-coverage** | improve-code-coverage | Code coverage analysis |
| **covr** | improve-code-coverage | Tools wrapping the covr package |
| **data-access** | analyze-r-package (detects), create-package-instructions | Working with remote data |
| **git** | update-r-news | Git-based workflows |
| **changelog** | update-r-news | Changelog and release note generation |
| **news** | update-r-news | R package NEWS file management |
| **data-analysis** | bioc-howto | Practical guides for analyzing omics data |

---

**Last Updated**: 2026-09-11
**Version**: 2.1.0
**Maintained by**: bioconductor
