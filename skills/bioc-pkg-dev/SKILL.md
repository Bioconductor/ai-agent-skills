---
name: bioc-pkg-dev
description: "Guide an R package or a set of analysis scripts through Bioconductor submission: the pre-submission gate, the Contributions tracker, and post-acceptance maintenance"
version: 1.0.0
category: r-packages
author: bioconductor
tags: [r-packages, bioconductor, submission, bioccheck, biocviews, peer-review]
---

# bioc-pkg-dev

Takes existing R work - a package, or just a pile of analysis scripts - and moves it toward an
accepted Bioconductor package. Covers the pre-submission gate, the Contributions tracker, and
what happens after acceptance.

The common case is conversion, not creation: there is already a working tool on GitHub, and the
question is what stands between it and acceptance. Start from what exists and find the gaps
against the gate. Do not scaffold from scratch unless there is no package yet.

Condensed from the official guide,
[Bioconductor Packages: Development, Maintenance, and Peer Review](https://contributions.bioconductor.org).
Detail lives in [knowledge/](knowledge/index.md), one file per topic; open the file for the task
at hand rather than reading all of it. Each file links back to its canonical chapter, which stays
authoritative when the two disagree.

## Usage

- "Is this package ready to submit to Bioconductor?"
- "Get this package ready for Bioconductor"
- "Turn these analysis scripts into a Bioconductor package"
- "Move my package from CRAN to Bioconductor"
- "What would a Bioconductor reviewer flag here?"
- "How do I push to git.bioconductor.org after acceptance?"

Applies whenever the work targets Bioconductor, even when the user does not name it: `biocViews`,
`BiocCheck`, the Contributions tracker, `git.bioconductor.org`, or S4 classes built on
Bioconductor core classes such as `SummarizedExperiment` all imply it.

## Prerequisites

- R-devel matching the current Bioconductor devel cycle. Build a new submission against devel,
  not release.
- The package sources in a git repository, on the default branch of a public GitHub repo by
  submission time.
- Validation and scaffolding packages installed:

```r
BiocManager::install(c(
    "BiocCheck", "biocthis",
    # biocthis::use_bioc_vignette() adds these to Suggests and refuses to run
    # unless they are already installed
    "BiocStyle", "knitr", "RefManageR", "sessioninfo", "testthat"
))
```

Use these tools rather than reimplementing them. `BiocCheck` is the authoritative validator and
`biocthis` writes Bioconductor-shaped files; reusing existing infrastructure is itself a review
criterion (see [Reusing methods and classes](https://contributions.bioconductor.org/important-bioconductor-package-development-features.html)).

## Process

### 1. Identify the lifecycle stage

Authoring, conversion and submission, maintenance, or review. The stage decides which detail file
to open; the map is in [knowledge/index.md](knowledge/index.md). For an end-to-end submission,
follow the runbook in [knowledge/workflow.md](knowledge/workflow.md), starting at its "Converting
an existing package" section when a package already exists.

If the starting point is loose scripts rather than a package, the first move is package structure:
naming rules in [knowledge/development/package-name.md](knowledge/development/package-name.md),
setup in [knowledge/development/general-dev.md](knowledge/development/general-dev.md).

### 2. Pin the current Bioconductor cycle

Never assert the release/devel pair from memory - it changes twice a year, and a stale value sends
someone to build against the wrong R. Read it from
[config.yaml](https://bioconductor.org/config.yaml), which is authoritative, and note the date.
The last verified value is recorded in
[knowledge/SOURCES.md](knowledge/SOURCES.md) with its fetch date.

### 3. Check the package against the gate, in two tiers

Upstream states these at two different strengths, so report them at two different strengths. A
tier-2 item is not a blocker; it is something a reviewer will very likely ask about.

Tier 1, stated as requirements:

- `R CMD check` and `BiocCheck` pass with no ERROR and no WARNING on current R-devel. The
  tracker's own wording is "a minimum requirement for package acceptance". It also says "Passing
  these checks does not result in automatic acceptance" - a human review follows.
- At least 80% of man pages documenting exported objects have a runnable example. Below that,
  BiocCheck raises an ERROR, not a warning. An example wrapped entirely in `\dontrun` or
  `\donttest` counts as no example at all, because BiocCheck comments both out before parsing.
- Individual files are 5 MB or smaller. Upstream states this one as "must", and states it for
  **software** packages. Experiment data and annotation packages are governed by
  [knowledge/development/non-software-pkgs.md](knowledge/development/non-software-pkgs.md)
  instead; do not report a data file in one of those as a size blocker.
- `biocViews` present; a vignette and man pages present; maintainer email valid and belonging to
  the person submitting; not on CRAN, since "a package can only be submitted to one or the
  other"; hosted on the GitHub default branch.

Tier 2, stated as should or recommended:

- `Version: 0.99.0` for a new package (upstream: "should set"). Expected in practice; set it.
- Source build under 10 MB (upstream: "should occupy less than").
- `R CMD check --no-build-vignettes` under 10 minutes (upstream: "should require less than").
- Vignettes, examples and tests under 8 GB memory (upstream: "it is recommended that").

Detail: [knowledge/development/build-check-bioccheck.md](knowledge/development/build-check-bioccheck.md)
and [knowledge/development/general-dev.md](knowledge/development/general-dev.md).

### 4. Close the metadata gaps

`DESCRIPTION`, `NAMESPACE`, `NEWS`, `LICENSE`, `CITATION`:
[knowledge/development/metadata-files.md](knowledge/development/metadata-files.md).

`biocViews` is where new packages most often fail. `biocViews: Software` on its own is a BiocCheck
ERROR - "Add biocViews other than Software". The four top-level terms (Software, AnnotationData,
ExperimentData, Workflow) do not count on their own. Pick specific terms from the
[biocViews vocabulary](https://bioconductor.org/packages/release/BiocViews.html), for example
`Software, GeneExpression, Transcriptomics`.

### 5. Write the documentation and the tests

A vignette that shows the actual analysis, not a stub, plus man pages with runnable examples:
[knowledge/development/documentation.md](knowledge/development/documentation.md). Count the
examples rather than eyeballing them - the 80% threshold in step 3 is an ERROR, and a package can
look well documented while failing it, since pages whose only example sits inside `\dontrun` score
as zero. Unit tests:
[knowledge/development/tests.md](knowledge/development/tests.md). Large data belongs in
ExperimentHub or AnnotationHub rather than in the package:
[knowledge/development/data.md](knowledge/development/data.md).

### 6. Run the gate

Both entry points, on current R-devel. They check different things - the first inspects the git
clone, the second the package:

```r
BiocCheck::BiocCheckGitClone()
BiocCheck::BiocCheck('new-package' = TRUE)
```

BiocCheck cannot measure the two timing items in tier 2 (`R CMD check --no-build-vignettes` under
10 minutes, under 8 GB memory). Those need a real build, so time and measure one.

### 7. Do the style pass last, and keep it a style pass

Bioconductor style differs from tidyverse style: `<-` for assignment, 4-space indentation,
80-column lines, vectorized code, and `seq_len`/`seq_along` in place of `1:n`. Details in
[knowledge/development/r-code.md](knowledge/development/r-code.md) and the
[R code guidelines](https://contributions.bioconductor.org/r-code.html).

Two of those substitutions are not cosmetic. `1:n` to `seq_len(n)` and `sapply` to `vapply` change
behavior at exactly the edge cases that motivate them - `n == 0`, and a `FUN.VALUE` mismatch that
`sapply` swallows and `vapply` raises. Apply them where the new behavior is the intended one,
leave them where that cannot be determined, and run the tests before and after so the diff is
provably cosmetic.

### 8. Submit

Host on the GitHub default branch, then open an issue whose title is the package name at the
[Contributions tracker](https://github.com/Bioconductor/Contributions/issues/new). Annotation
packages go by email to <packages@bioconductor.org> instead. The Single Package Builder must then
pass on all platforms. Eligibility and package types:
[knowledge/01-submissions.md](knowledge/01-submissions.md).

### 9. After acceptance, maintain

Register an SSH key at BiocCredentials, add `upstream` pointing at `git.bioconductor.org`, and
push to both remotes; only `devel` and `RELEASE_x_y` branches accept pushes.

Version scheme `x.y.z`: start at `0.99.0`; `y` is odd in devel and even in release, maximum 99;
bump `z` by 1 on every commit; `0.99.z` becomes `1.0.0` at the first Bioconductor release; `x` is
changed only by the Bioconductor team. Git workflow, build reports, and deprecation:
[knowledge/maintenance.md](knowledge/maintenance.md).

## Output Format

For a readiness question, report gaps in the two tiers above, never merged into one list:

- **Blockers** - tier-1 items that currently fail, each with the file and the fix.
- **Likely reviewer requests** - tier-2 items and anything in
  [knowledge/reviewer.md](knowledge/reviewer.md) that the package does not satisfy.
- **Verdict** - submittable now, or not, and what remains.

For a development or maintenance question, answer from the relevant detail file and cite the
canonical chapter it links to, so the answer stays checkable against upstream.

## Examples

**User**: "Is my package ready to submit to Bioconductor?"

**Skill produces**: a two-tier gap report, for example - blockers: `biocViews` contains only
`Software` (BiocCheck ERROR), `inst/extdata/ref.rds` is 12 MB (exceeds the 5 MB per-file limit),
no vignette. Likely reviewer requests: `Version` is `0.1.0` rather than `0.99.0`; three exported
functions have no runnable examples. Verdict: not submittable yet; the three blockers must clear
first.

**User**: "Turn these RNA-seq scripts into a Bioconductor package."

**Skill produces**: a plan starting from package structure and naming, then the metadata files,
then a vignette built from the existing analysis, then tests, and only then the gate - with a note
that a Software package declaring no Bioconductor dependencies draws a BiocCheck warning
suggesting CRAN instead, so the S4 or `SummarizedExperiment` integration should be settled early
rather than bolted on.

**User**: "Why does `R CMD build` fail right after I scaffolded the package?"

**Skill produces**: the `inst/CITATION` diagnosis in Notes below, plus the fix.

## Notes

Three `biocthis` behaviors that cost time if they are not known in advance. Verified against
biocthis 1.23.0 on 2026-08-14.

- `use_bioc_description()` writes a **fresh** `DESCRIPTION`; it does not merge into an existing
  one. It calls `usethis::use_description()`, which calls `write_over()`, which asks before
  replacing an existing file - and declines silently in a non-interactive session. On a package
  that already has a `DESCRIPTION`, the call therefore often does nothing at all, with no error.
  Add `biocViews` by hand instead, or approve the overwrite knowing it discards the `DESCRIPTION`
  already present. The rest of the `biocthis` chain appends and is safe on an existing package.
- `use_bioc_citation()` leaves `inst/CITATION` unfinished, and unfinished here means broken. The
  template substitutes `{{Title}}` and `{{github_owner}}`; the function passes neither a title
  nor - on a package with no GitHub remote configured yet - an owner. The file lands with an empty
  title and an empty author, `utils::citation()` errors on either ("a bibentry of bibtype 'Manual'
  has to specify the field: title"), and because the generated vignette calls `citation()`,
  `R CMD build` fails at "creating vignettes". Fill in the title, the author, and the placeholder
  `10.1101/TODO` DOI before building anything.
- A freshly scaffolded package also draws two BiocCheck complaints worth pre-empting: the
  placeholder Description is "too concise", since it wants at least three sentences, and a
  Software package with no Bioconductor dependencies gets a warning suggesting CRAN instead.

Passing the gate is necessary, not sufficient. Human peer review follows, and it looks at things
no checker measures - whether the package duplicates an existing one, whether it reuses
Bioconductor core classes instead of inventing parallel ones, and whether the vignette shows a
real analysis. Those expectations are in
[knowledge/reviewer.md](knowledge/reviewer.md).
