---
name: draft-r-package-pr
description: Check that a pull request against an R/Bioconductor package is focused and ready for review, then draft its title and description, following Bioconductor policy
version: 1.1.0
category: r-packages
tags: [r-packages, bioconductor, git, pull-request, code-review, documentation]
author: bioconductor
---

# draft-r-package-pr

Prepare a pull request (PR) against an R or Bioconductor package: check that the change is focused,
confirm the checks a reviewer will expect, and draft a title and description for the user to approve.

This skill covers what is particular to R and Bioconductor packages. General PR practice (a title
that says what the change does, a description of the problem and the approach, linked issues) is
assumed. [SOURCES.md](SOURCES.md) lists where the guidance comes from and which parts are this
skill's own conventions; read it only when updating the skill.

## Usage

- "Draft a PR description for this branch"
- "Help me open a PR against this Bioconductor package"
- "Is this branch ready for a PR?"

## Prerequisites

- Working directory is an R package root (contains `DESCRIPTION`) inside a git repository
- The change is committed on a feature branch; for Bioconductor packages the base is usually `devel`

## Process

### 1. Gather context

1. Read the repository's `CONTRIBUTING.md` and PR template, if any. Where they conflict with this
   skill, they win.
2. Work out whether the PR author is a package author or an outside contributor, without asking.
   Take their GitHub username from the open PR or the fork the branch is pushed to, and their name
   and email from the branch's commits, and compare them with `Authors@R` in `DESCRIPTION`. A
   person with role `"cre"` or `"aut"` is a package author. Ask only if they can't be matched.
   This decides the reminder in step 5.

### 2. Check that the PR is focused

Report what should be split or dropped and let the user decide. Do not rewrite their history, and
do not make these changes yourself while preparing the PR.

- **Unrelated changes.** A second fix or feature, refactoring mixed with a behaviour change, or
  restyling of code the PR doesn't otherwise touch each belong in a separate PR. Small cleanups
  next to the changed code are fine. Around 100 changed lines is usually reasonable and 1000 is
  usually too large.
- **Whitespace-only changes.** Compare the diff with and without whitespace
  (`git diff -w --ignore-blank-lines`) and recommend reverting lines that differ only in whitespace
  or blank lines; they hide the real change from the reviewer.
- **Package maintenance changes.** Recommend dropping these or moving them to a separate PR:
  - A `RoxygenNote` or `Config/roxygen2/version` bump in `DESCRIPTION`, and `.Rd` files that change
    only because a newer roxygen2 regenerated them.
  - `NAMESPACE` or `Collate` changes beyond what the PR's code needs. Compare the set of
    directives or files before and after; a reordering by roxygen2 is noise.
  - New `Imports`, `Depends`, `Suggests`, or `LinkingTo` entries the PR's code doesn't use. Name
    the ones it does need in the description (step 6).
  - Committed build or check output: a pkgdown `docs/` site, `*.Rcheck/` directories, built
    tarballs, or rendered vignette `.html` files.
- **Indentation in new code.** Follow the file's existing indentation. Where the package has no
  set style, use Bioconductor's: 4 spaces, no tabs, lines of at most 80 characters.

### 3. Confirm the checks a reviewer will expect

1. **Tests.** A change in behaviour needs a new or updated test. A pure refactor should already be
   covered; if it isn't, suggest adding tests first in a separate PR.
2. **Documentation.** The package uses roxygen2 only if `DESCRIPTION` has a `RoxygenNote` or
   `Config/roxygen2/version` field. If it does, edit the roxygen comments, regenerate `man/`, and
   confirm the generated files are committed. If a newer roxygen2 also changes `RoxygenNote` or
   unrelated `.Rd` files, revert those (step 2). If it has neither field, the `.Rd` files are written
   by hand: edit them directly and do not run roxygen2, which would overwrite them.
3. **Build and check.** Use existing results when they cover the branch's head commit: CI on the PR
   or pushed branch, or a check the user ran earlier in the session. Otherwise run `R CMD build`,
   `R CMD check`, and, for Bioconductor packages, BiocCheck once, following
   [build-check-bioccheck](../build-check-bioccheck/SKILL.md). To tell new problems from old ones,
   compare with the base branch's latest CI results; do not run a second full check on the base
   branch for the comparison.

### 4. Offer a NEWS entry for user-facing changes

A NEWS entry is welcome but not required (this skill's convention), since the maintainer can write
NEWS when preparing a release. Offer one when users will notice the change, and draft it with
[update-r-news](../update-r-news/SKILL.md), which sets the conventions. For a single bullet written
by hand:
- For a Bioconductor package, put it under the upcoming release version heading as
  `update-r-news` derives it (e.g. `1.20.0` when `devel` is at `1.19.4`), not a
  `(development version)` heading, as a list element in the file's existing style.
- Say what now happens, with the function name near the start.
- Credit the PR author's GitHub username, whether or not they are a package author, with the
  PR number if the PR is already open and otherwise the issue it fixes, in the order the file
  already uses or `(#42, @user)` if it has none.

### 5. Do not bump the version in the PR

Advise against changing `Version:` in `DESCRIPTION`, and if the branch already bumps it, recommend
reverting that before the PR is opened. Bioconductor requires a bump of `z` in `x.y.z` for each
push to `git.bioconductor.org`; this skill reads that as the maintainer's push after merging. Bumps inside PRs
collide when several PRs are open, or go stale while a PR waits for review.

If the PR author is a package author (step 1), remind them to bump when pushing upstream after the
merge; [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) covers that push.

### 6. Draft the title and description

Add a prefix such as `feat:` or `fix:` to the title
only if the repository's history already uses them. Beyond the problem, the approach, and
`Fixes #N`, include what applies:
- A before/after reprex for a behaviour change, or a before/after benchmark (e.g. `bench::mark()`)
  for a performance change, including input sizes where the speed-up is negligible.
- New dependencies and why each is needed.
- Which checks were run and on what (step 3), and anything still failing.
- **AI and third-party code.** Bioconductor requires disclosure in the PR description when a
  non-trivial part of the change was generated by AI or copied from another project. Name the
  source (e.g. `Assisted-by: <AI name>` or `Code copied from: <source>`), and confirm that the
  provenance is also cited in the code and that the code can be redistributed under the package's
  license.

### 7. Review the draft with the user

Show the pre-PR report, title, and description. Open or update the PR only after the user approves
the text, and open it as a draft if a check is failing.

## Output Format

```markdown
## Pre-PR report
- Focus: <ok | suggested splits>
- Whitespace-only changes: <none | files and lines to revert>
- Maintenance changes: <none | files to drop or move to a separate PR>
- Tests: <added/updated | missing for ...>
- Documentation: <roxygen2, regenerated | hand-written Rd, edited | no changes>
- R CMD check / BiocCheck: <no new issues | new: ...> (<run now | CI run for <commit>>)
- NEWS: <entry added | offered, not added | not user-facing>
- Version: <unchanged | bumped in branch, recommend reverting>

## Title
<title>

## Description
<description, in the repository's template if it has one>
```

The pre-PR report is for the user. Keep its bookkeeping, such as the version line, out of the PR
description.

## Examples

### Branch that does too much

**User**: "Is this branch ready for a PR?"

**Skill produces**: a report that the branch adds a `summarize_by()` method, renames three internal
helpers across 14 files, bumps `RoxygenNote` (rewriting 40 `.Rd` files), and bumps `Version:`. It
recommends one PR for the rename, one for the new method with its tests, and reverting the roxygen
and version bumps, then drafts the title and description for the first.
