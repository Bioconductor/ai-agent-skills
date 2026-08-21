# Appendices

Covers: the key actionable point of each appendix (A-H) in the Bioconductor package development guide.

## Appendix A - Using Devel Bioconductor

Develop against Bioconductor devel so your package is ready when devel becomes the next release. The R version you pair with devel depends on the time of year (R releases once a year in mid-April; Bioconductor releases twice a year, mid-April and mid-October):

- Mid-April to mid-October: use R-release (the current released R) with Bioconductor devel.
- Mid-October to mid-April: use R-devel (daily build) with Bioconductor devel, because a new R is coming in April.

Rule of thumb: target the R version that users will have when the current devel branch becomes the release branch.

Install/switch to devel:

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install(version = "devel")
BiocManager::valid()   # check all packages are the correct devel versions
```

`BiocManager::install(version = "devel")` flips the active version to devel; `BiocManager::valid()` reports any out-of-date or "too new" packages. For the mid-October to mid-April window, first install R-devel (source from stat.ethz.ch/R/daily, macOS from mac.r-project.org, Windows rdevel from CRAN) and run the same commands in that R.

## Appendix B - Advanced Build Options

- Skip unsupported platforms via `Config/Bioconductor/UnsupportedPlatforms` in DESCRIPTION (or legacy `UnsupportedPlatforms:` in `.BBSoptions`); platforms are win, mac, etc.
- Long tests (>40 min): put them in a `longtests/` dir and set `RunLongTests: TRUE` in `.BBSoptions`; they run weekly (Saturdays, up to 6 hours) and their failures do not block propagation. Keep normal `tests/` under 40 minutes.
- GPU packages: declare `GPU_reliance: required` or `optional` in `.BBSoptions`.

## Appendix C - Querying Web Resources

- Keep downloads reasonably sized so `R CMD check` finishes well under 10 minutes.
- Never use unbounded `while()` retries; set an explicit max number of attempts (e.g. an `N.TRIES` loop wrapped in `tryCatch()`) and fail with a clear message that includes the URL and error.
- Respect `getOption("timeout")` and check HTTP status from `httr::GET()` / `download.file()`.

## Appendix D - C and Fortran

- Follow the "System and foreign language interfaces" section of Writing R Extensions.
- Use R's internal facilities (`R_alloc`, R's RNG) instead of system equivalents; register native routines.
- Add `R_CheckUserInterrupt()` in long C-level loops.
- Use `Makevars`/`Makefile` sparingly. During development enable all warnings and disable optimization, e.g. gcc `-Wall -Wextra -pedantic -O0 -ggdb`, clang `-Weverything -O0 -g` (put user Makevars in `~/.R/`).

## Appendix E - C++/Mavericks Best Practices

- Prefer Rcpp for C++ integration; use BH for Boost instead of bundling it.
- Define `R_NO_REMAP` and use fully-qualified names (`Rf_length()`, `std::map`); never `using namespace std;` (especially in headers).
- Keep R headers out of `extern "C"` blocks.
- Avoid dereferencing/incrementing past-the-end iterators (segfaults). Regenerate old SWIG code with a C++11-capable SWIG.

## Appendix F - Man Page Links

- `\linkS4class{}` cross-references (e.g. to `SummarizedExperiment`) can trigger check warnings. To resolve: put the target package in `Depends:` (not just `Imports:`), add `#' @import <pkg>` in roxygen, and run `devtools::document()` so NAMESPACE gets the `import()` entry.

## Appendix G - Book News

- Changelog for the guidelines. 1.0.0 (2021-06-02) initial release; 1.0.1 (2021-08-19) added the package-naming section. Tracks when new guidance was added.

## Appendix H - References

- Bibliography. Key citation: Soneson et al. (2025), "Eleven Quick Tips for Writing a Bioconductor Package," PLoS Computational Biology 21(3):e1012856.

Source: [Using devel Bioconductor](https://contributions.bioconductor.org/use-devel.html) , [Advanced build options](https://contributions.bioconductor.org/advanced-build-options.html) , [Querying web resources](https://contributions.bioconductor.org/querying-web-resources.html) , [C and Fortran code](https://contributions.bioconductor.org/c-fortran.html) , [C++ Mavericks best practices](https://contributions.bioconductor.org/cmavericks-best-practices.html) , [Links in man pages](https://contributions.bioconductor.org/man-links.html) , [Book news](https://contributions.bioconductor.org/booknews.html) , [References](https://contributions.bioconductor.org/references-1.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
