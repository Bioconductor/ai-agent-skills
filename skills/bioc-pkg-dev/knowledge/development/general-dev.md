# General Development Requirements

Covers: Chapter 3 - General guidelines, and Chapter 4 - Important Bioconductor
package development features.

## Development environment

- Develop against the devel version of Bioconductor and use devel Bioconductor
  packages.
- Use a recent R-devel matching the current Bioconductor devel branch.

## Pre-submission gate (build and check)

- Must pass `R CMD build` and `R CMD check` with NO errors and NO warnings on
  recent R-devel.
- Must pass `BiocCheck::BiocCheckGitClone()` with no errors/warnings.
- Must pass `BiocCheck::BiocCheck('new-package' = TRUE)` with no errors/warnings.
- All ERRORs, WARNINGs, and NOTEs must be addressed or explicitly justified.

## Numeric thresholds (note the modality - only one of these is a "must")

- Individual files (software packages): **<= 5 MB** each. Upstream: "individual files must be
  <= 5MB".
- Source package produced by `R CMD build`: **< 10 MB**. Upstream: "should occupy less than
  10 MB on disk".
- `R CMD check --no-build-vignettes` runtime: **< 10 minutes**. Upstream: "should require less
  than 10 minutes to run R CMD check --no-build-vignettes".
- Memory across vignettes, examples, and tests: **< 8 GB**. Upstream: "it is recommended that
  the vignettes, man page examples, and unit tests do not require more than 8 GB of memory".
- Use lossy compression (e.g., pngquant) to shrink large images/screenshots.

Treat the three "should" items as strong expectations: the build system enforces them in practice
and a reviewer will ask. But do not tell a submitter they are blocked from submitting by them.

## File hygiene

- Do not include filenames that differ only in case (cross-platform safety).
- Exclude unnecessary files: `.DS_Store`, `.project`, `.git`, cache files, logs,
  `*.Rproj`, `*.so`.
- Use `.gitignore` to keep undesirable files out of the repository.
- Application-specific tooling (GitHub Actions, devtools config) "should be in a different
  branch" than the default one holding package code. A recommendation upstream, not a rule.
- R CMD check options are customized by Bioconductor via flags configurable
  through the `R_CHECK_ENVIRON` environment variable.

## biocViews (required feature)

- The DESCRIPTION file MUST contain a `biocViews:` field (case-sensitive,
  lowercase 'b').
- Choose terms from only ONE category: Software, Annotation Data, Experiment Data,
  or Workflow.
- Use leaf-level terms rather than broad parent categories.
- Terms must match the official hierarchy exactly (spelling and capitalization);
  consult the devel branch biocViews list.
- Submission validation checks that biocViews are present, valid, and from a
  single category.

## Vignettes (required feature)

- Every submitted package must have at least one Rmd (preferred) or Rnw vignette.
- Render with `BiocStyle::html_document`.
- Vignettes must contain evaluated (non-trivial, runnable) R code.
- Include a detailed introduction motivating inclusion in Bioconductor and, where
  relevant, compare against existing similar packages.

## Reuse existing infrastructure

- Reuse established Bioconductor classes and methods where appropriate (see the
  Common Bioconductor Methods and Classes guidance / methods-classes.md).

Source: [General package development](https://contributions.bioconductor.org/general.html) and
[Important Bioconductor package development features](https://contributions.bioconductor.org/important-bioconductor-package-development-features.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
