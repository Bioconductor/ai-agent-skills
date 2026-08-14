Covers: Chapters 22 and 23 - Build, check, BiocCheck, and conclusion

# Build, Check, and BiocCheck

Run all three tools successfully before submission. Build and check against the
current Bioconductor devel version, using the matching R version (Bioconductor
releases are tied to specific R versions).

## Exact commands

Build the source tarball first, then check the tarball it produces:

```sh
R CMD build MyPackage
R CMD check MyPackage_0.99.0.tar.gz
```

Then run BiocCheck. For a git clone / working directory:

```r
BiocCheck::BiocCheckGitClone()
```

For a new-package submission (runs the stricter new-package rules):

```r
BiocCheck::BiocCheck('new-package' = TRUE)
```

BiocCheck can also be run on the built tarball. During development,
`devtools::check()` is a convenient wrapper around `R CMD build`/`check`.

## Pass/fail gate

- BiocCheck is the submission gate. The package MUST pass with no ERRORs and no
  WARNINGs. Address NOTEs where possible; unresolved notes may be questioned in
  review.
- `R CMD build` and `R CMD check` must complete without ERROR.
- New packages should carry version `0.99.x` in DESCRIPTION.

## What BiocCheck enforces (selection)

- Bioconductor coding style, dependency and NAMESPACE correctness.
- Presence of a vignette, runnable examples, and unit tests. The example check
  is quantitative and is an ERROR below 80% - see the Examples section of
  [documentation.md](documentation.md) for the exact rule and for why
  `\dontrun` makes it worse rather than better.
- Correct DESCRIPTION fields including valid `biocViews`.
- No forbidden files tracked in git (see gitignore chapter).
- Function length, line length, and other style thresholds.

## CI

- GitHub Actions workflows can mimic the submission environment; see the
  R-Universe Bioconductor integration docs.

## Submission (conclusion)

- All contributions undergo formal peer review.
- Submit through the official GitHub package submission repository/tracker.
- See "How to Build a Bioconductor Package with RStudio" for a walkthrough.
- Once build, check, and BiocCheck are clean, the package is ready to submit.

Source: [Build, check and BiocCheck](https://contributions.bioconductor.org/build-check-bioccheck.html) and [Conclusion](https://contributions.bioconductor.org/conclusion.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
