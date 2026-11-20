---
name: draft-r-package-pr
description: Draft the title, description, and pre-submission checks for a pull request against an R/Bioconductor package, following tidyverse code review guidance and Bioconductor policy
version: 1.0.0
category: r-packages
tags: [r-packages, bioconductor, git, pull-request, code-review, documentation]
author: bioconductor
---

# draft-r-package-pr

Prepare a pull request (PR) against an R or Bioconductor package: check that the change is focused,
run the checks a reviewer will expect, add a NEWS entry when users will notice the change, and draft
a title and description that let a reviewer understand the PR before reading the code.

The Bioconductor contributions guide says little about PRs themselves. It requires disclosure of
AI-generated or copied code, and it sets rules for pushing to `git.bioconductor.org`. The guidance
on titles, descriptions, and scope comes from the tidyverse team's published code review principles
and contributing template. See [Sources](#sources) for the exact documents and the versions read.

## Usage

Invoke this skill when a change to an R package is ready, or nearly ready, for review:
- "Draft a PR description for this branch"
- "Write up a pull request for these changes"
- "Help me open a PR against this Bioconductor package"
- "Is this branch ready for a PR?"
- "Write a better title for this PR"

## Prerequisites

- Working directory is an R package root (contains `DESCRIPTION`) inside a git repository
- The change is committed on a feature branch, not on the default branch
- The base branch is known; for Bioconductor packages it is usually `devel`
- Optional: the GitHub CLI or API, to read linked issues and open the PR

## Process

### 1. Gather context

1. Identify the base branch and compute the diff and commit list of the feature branch against it.
2. Read the repository's own contribution rules: `CONTRIBUTING.md` or `.github/CONTRIBUTING.md`, and
   any PR template (`.github/PULL_REQUEST_TEMPLATE.md` or `.github/PULL_REQUEST_TEMPLATE/`). Where
   these conflict with this skill, the repository's rules win.
3. Collect the issues the change addresses, from commit messages, the branch name, or the user. Read
   each issue so the description can summarise any long discussion.
4. Work out who the PR author is and whether they are a package maintainer or an outside
   contributor, without asking the user. Take the author's GitHub username from the open PR, or
   from the fork the branch is pushed to, and their name and email from the branch's commits, then
   compare them with the `Authors@R` field in `DESCRIPTION`. A person listed with role `"cre"` or
   `"aut"` is a package author; anyone else is an outside contributor. Ask only if the two can't be
   matched. The answer decides whether to remind the user about the version bump (step 5); the NEWS
   entry credits the PR author either way (step 4).

### 2. Check that the PR is focused

A focused PR is one self-contained change. Review the diff for:
- **Unrelated changes.** A bug fix plus an unrelated feature, or a feature plus a bug found along
  the way, should be separate PRs. Propose a split and open an issue for the unrelated bug.
- **Refactoring mixed with behaviour changes.** Moving or renaming a function goes in a different PR
  from fixing it. Small cleanups next to the changed code are fine.
- **Restyling.** Style fixes belong only in the code the PR touches; package-wide restyling is its
  own PR.
- **Whitespace changes.** Whitespace-only changes distract the reviewer from the real change and
  should not be included in the PR. Look for lines the PR changes only in whitespace: trailing
  spaces stripped by an editor, re-indented blocks, tabs swapped for spaces, changed line endings, or
  added or removed blank lines. Comparing the diff with and without whitespace (e.g. `git diff -w`)
  shows them. Recommend reverting them; if the user wants the formatting, it goes in a separate PR.
- **Indentation in new code.** Follow the indentation the file already uses. Where the package has no
  set style, use Bioconductor's: 4 spaces, no tabs, and lines of at most 80 characters.
- **Size.** Around 100 changed lines is usually reasonable and 1000 is usually too large, though
  spread across files matters as much as line count. Deleting a whole file counts as one change.

Report anything that should be split and let the user decide. Do not rewrite their history.

### 3. Run the checks a reviewer will expect

1. **Tests.** A PR that adds or changes logic should add or update tests for that behaviour. A pure
   refactor should be covered by tests that already exist; if they don't, suggest adding them first
   in a separate PR.
2. **Documentation.** Check whether the package uses roxygen2: `DESCRIPTION` has a
   `Config/roxygen2/version` or `RoxygenNote` field. If it does, regenerate `man/` from the roxygen
   comments, confirm the generated files are committed, and make documentation fixes in the `.R`
   source, not the `.Rd` file. If it has neither field, the `.Rd` files are written by hand: edit
   them directly and do not run roxygen2, which would overwrite them.
3. **Build and check.** Use existing results when they cover the branch: CI runs on the PR or the
   pushed branch for the current head commit, or a check the user ran on that commit earlier in the
   session. Otherwise run `R CMD build`, `R CMD check`, and, for Bioconductor packages, BiocCheck,
   once on the branch; [build-check-bioccheck](../build-check-bioccheck/SKILL.md) covers running
   and interpreting them. Every PR draft gets at least one check run, existing or new. To tell new
   problems from old ones, compare with the base branch's latest CI results if it has them; do not
   run a second full check on the base branch just for the comparison.
4. **Vignettes.** Confirm they still build if the change touches code they use.

If a check fails and the user still wants to open the PR, open it as a draft (step 7).

### 4. Offer a NEWS entry for user-facing changes

A NEWS entry is welcome in a PR but not required. The maintainer can write or edit NEWS when
preparing a release, so a missing entry is not a reason to hold the PR. Offer to add one when users
will notice the change; skip it for purely internal changes. Draft entries with
[update-r-news](../update-r-news/SKILL.md), which sets the conventions; when writing one bullet by
hand, follow them:
- Put the entry under the upcoming release version heading (e.g. `1.20.0` when `devel` is at
  `1.19.4`), as `update-r-news` derives it, matching the file's existing heading and bullet style.
  Don't add a `(development version)` heading.
- Write it for users, not developers: put the function name near the start, use the present tense,
  and describe what now happens.
- Credit the PR author with their GitHub username and the issue or PR number, whether or not they
  are a package author. Either order is fine, `(#42, @user)` or `(@user, #42)`; follow the order the
  NEWS file already uses, and use `update-r-news`'s `(#42, @user)` when it has none, e.g.
  `` * `foo()` now accepts `GRanges` input (#42, @contributor). ``
- Bioconductor NEWS files must use list elements, not free text.

### 5. Do not bump the version in the PR

Advise against changing `Version:` in `DESCRIPTION` in a pull request. If the branch already bumps
it, recommend reverting that change before the PR is opened, and say so in the pre-PR report.

Bioconductor requires every commit pushed to `git.bioconductor.org` to bump the `z` in `x.y.z`.
That rule applies to the maintainer's push after merging, not to each PR: the maintainer merges the
PR on GitHub, bumps the version, and pushes `devel` upstream. Bumps inside PRs also collide when
several PRs are open at once, and a PR that sits in review can carry a version that is already
taken by the time it merges.

If the PR author is a maintainer (step 1), remind them to bump when pushing upstream after the
merge, not in the PR. Pushing upstream is package maintenance and is covered by
[bioc-pkg-dev](../bioc-pkg-dev/SKILL.md).

### 6. Draft the title and description

**Title**
- A short summary of *what the change does*, ideally under 72 characters.
- It must stand alone in the git history. Reject titles like "Fix bug", "Fixes #123", "Add patch",
  "Phase 1", or "Moving code from A to B".
- Describe the change, not the problem; don't restate the issue title.
- Use a prefix such as `feat:` or `fix:` only if the repository's history or CONTRIBUTING already
  uses one.

**Description body.** Give the reviewer the context to understand the code before they open it.
Include what applies:
- The problem being solved, in a sentence or two.
- How the change solves it, and any shortcomings or alternatives the reviewer should weigh.
- `Fixes #N` or `Closes #N` for issues the PR resolves (GitHub closes these on merge), and
  `Related to #N` or `Part of #N` for issues it only touches.
- A summary of the outcome of a long issue discussion, so the reviewer doesn't have to read it.
- A before/after reprex for behaviour changes, or a before/after benchmark (e.g. with `bench`) for
  performance changes.
- A suggested reading order for large PRs, such as "start with the tests".
- A checklist of what was run (step 3) and any remaining to-do items.
- **AI and third-party code.** Bioconductor requires disclosure in the PR description when a
  non-trivial part of the change was generated by AI or copied from another project. Name the source
  (e.g. `Assisted-by: <AI name>` or `Code copied from: <source>`), and confirm that the provenance is
  also cited in the code and that the code can be redistributed under the package's license.

If describing the PR is hard, it is probably doing too much. Go back to step 2.

### 7. Review the draft with the user

1. Show the full title and description, plus a summary of the step 3 results.
2. Re-read the description against the final diff; descriptions drift as PRs change.
3. Recommend a draft PR if checks fail, work remains, or the user wants to self-review later.
4. Open or update the PR only after the user approves the text. Once it's open, suggest that the
   author leave comments on their own PR for tricky lines that need context but don't belong in a
   code comment.

After the PR merges, see [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) for the version bump and the
push to Bioconductor.

## Output Format

A pre-PR report followed by the drafted PR text:

````markdown
## Pre-PR report
- Focus: <ok | suggested splits>
- Whitespace-only changes: <none | files and lines to revert>
- Tests: <added/updated | missing for ...>
- Documentation: <roxygen2, regenerated | hand-written Rd, edited | no changes>
- R CMD check / BiocCheck: <no new issues | new: ...> (<run now | CI run for <commit>>)
- NEWS: <entry added | offered, not added | not user-facing>
- Version: <unchanged | bumped in branch, recommend reverting>

## Title
<title, under 72 characters>

## Description
<problem and approach>

<shortcomings or decisions for the reviewer>

Fixes #<N>

### Before / after
```r
<reprex or benchmark>
```

### Checklist
- [x] Tests added or updated
- [x] `R CMD check` passes with no new warnings or notes
- [x] BiocCheck passes (Bioconductor packages)
- [ ] NEWS entry added (optional)

<AI or third-party code disclosure, if applicable>
````

Drop sections that don't apply rather than filling them with "N/A".

## Examples

### Example 1: Bug fix from an outside contributor

**User**: "Draft a PR for my branch that fixes the strand bug in `import_gff()`"

**Skill produces**:
- Pre-PR report: focused; new test added in `tests/testthat/test-import.R`; no new check notes
  (taken from the branch's CI run); NEWS bullet added under the upcoming release heading.
- Title: `Keep strand from GFF column 7 in import_gff()`
- Body: one paragraph on the cause (the strand column was parsed after filtering and set to `*`),
  `Fixes #58`, a before/after reprex showing `strand()` output, and the checklist.
- NEWS: `` * `import_gff()` now keeps the strand given in column 7 (#58, @contributor). ``
- `DESCRIPTION` version left unchanged.

### Example 2: Branch that does too much

**User**: "Is this branch ready for a PR?"

**Skill produces**: A report noting that the branch adds a `summarize_by()` method, renames three
internal helpers across 14 files, and restyles `R/utils.R`. It recommends three PRs (the rename,
then the new method with its tests, with the restyle dropped or sent separately) and drafts the
title and description for the first.

### Example 3: Performance change

**User**: "Write up a pull request for the faster overlap code"

**Skill produces**: A description that explains the change, links the profiling issue, and gives a
`bench::mark()` before/after table, including input sizes where the speed-up is negligible and why.

## Notes

- The repository's own `CONTRIBUTING.md` and PR template take precedence over this skill.
- Guidance the sources disagree on, or that this skill adds, is marked here:
  - **Version bumps.** Advised against in PRs (step 5). This reads Bioconductor's per-push rule as
    the maintainer's job at push time. It is this skill's convention, not upstream text, and it
    deliberately departs from projects that require a bump in every PR.
  - **Whitespace.** Whitespace-only changes are excluded from PRs, and new code matches the file's
    existing indentation (step 2). These are this skill's conventions. Bioconductor's indentation
    rules are the fallback, and the usethis template's "don't restyle code that has nothing to do
    with your PR" is the closest upstream text.
  - **NEWS entries.** Welcome but optional (step 4). The usethis template asks for one for every
    user-facing change; this skill does not hold a PR for a missing entry.
  - **Conventional-commit prefixes.** Used only when the repository already uses them; none of the
    sources requires them.
- Skill-specific prerequisites and conventions are maintained here; format rules are in
  [AGENTS.md](../../AGENTS.md).

## Sources

Read on 2026-11-20. Re-check these pins when updating the skill.

- **Bioconductor contributions guide**, [Bioconductor/pkgrevdocs](https://github.com/Bioconductor/pkgrevdocs)
  `devel` at `b453cb4` (2026-11-18):
  - [AI policy and third-party code](https://contributions.bioconductor.org/ai-policy-third-party.html):
    disclosure in the PR description (step 6).
  - [Git version control](https://contributions.bioconductor.org/git-version-control.html):
    "Checks and version bumps" and "Pull requests on GitHub" (step 5).
  - [Version numbering](https://contributions.bioconductor.org/versionnum.html): the `x.y.z` scheme
    (step 5).
  - [The NEWS file](https://contributions.bioconductor.org/news.html): locations and the
    list-element requirement (step 4).
  - [R code](https://contributions.bioconductor.org/r-code.html): "Indentation" (4 spaces, no
    tabs, 80-character lines), used as the fallback style for new code (step 2).
- **Tidyteam code review principles** (Posit), [tidyverse/code-review](https://github.com/tidyverse/code-review)
  at `7ce6c9e` (2023-06-05):
  - [Submitting a PR](https://code-review.tidyverse.org/author/submitting.html): titles,
    descriptions, `Fixes #N`, reading order, drafts, self-review (steps 6 and 7).
  - [Focused PRs](https://code-review.tidyverse.org/author/focused.html): scope, size,
    refactoring, tests (steps 2 and 3).
- **usethis tidyverse contributing template** (Posit), [r-lib/usethis](https://github.com/r-lib/usethis)
  `inst/templates/tidy-contributing.md` at `772fad9` (2026-10-27): issue before a large change,
  `R CMD check`, NEWS for user-facing changes, editing roxygen sources, and restyling only touched code
  (steps 2-4). The [Pull request helpers](https://usethis.r-lib.org/articles/pr-functions.html) article
  covers the `pr_*()` workflow.
- **Tidyverse style guide, News** (Posit), [tidyverse/style](https://github.com/tidyverse/style)
  `news.qmd` at `2aed77e` (2025-10-17), rendered at <https://style.tidyverse.org/news.html>: bullet
  placement, wording, and crediting contributors (step 4).
