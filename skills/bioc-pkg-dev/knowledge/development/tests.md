Covers: Chapter 15 - Unit tests

# Unit Testing

## Framework choice

- Bioconductor slightly prefers testthat. RUnit and tinytest are also accepted.
- testthat: active development, rich assertions, integrates with devtools,
  informative failures.
- tinytest: lightweight, zero dependencies.
- RUnit: long Bioconductor history but unmaintained since ~2010.
- Declare the framework in DESCRIPTION `Suggests:` (e.g. `Suggests: testthat`,
  or `Suggests: RUnit, BiocGenerics`, or `Suggests: tinytest`).

## Directory structure and naming

- testthat: tests in `tests/testthat/`, files start with `test`.
  Set up with `usethis::use_testthat()`.
- RUnit: tests in `inst/unitTests/`, files match `test_*.R`
  (e.g. `test_divideBy.R`). Add `tests/runTests.R` containing:
  `BiocGenerics:::testPackage("MyPackage")`.
- tinytest: tests in `inst/tinytest/`. Add `tests/tinytest.R`:
  `if (requireNamespace("tinytest", quietly=TRUE)) tinytest::test_package("PACKAGE")`.

## What to test

- Test functions, methods, and classes with known inputs and expected outputs.
- Test edge cases and error conditions, not only the happy path.
- No hard minimum coverage percentage is mandated, but higher coverage is
  expected and reduces bug risk.

## Coverage measurement

- Use the covr package: `covr::package_coverage()`.

## Running tests

- Full check (runs all tests): `R CMD check MyPackage`.
- During development: `devtools::test()` (reloads code and reruns).
- Manual: source the package and test files, then call the test function.

## Long-running tests

- Tests in `tests/` must finish within 40 minutes as part of `R CMD check`.
- Tests too slow for that belong in a `longtests/` directory at the top level of
  the package, alongside `tests/`, with a `.BBSoptions` file at the top level
  containing `RunLongTests: TRUE`. They are given up to 6 hours.
- Long tests run weekly (Saturdays) on their own builders, on both devel and
  release. Their failures do **not** block propagation after a version bump;
  only the nightly `tests/` results do.
- `longtests/` is structured like `tests/` and typically runs unit tests, but no
  framework is mandated.
- Reach out to the bioc-devel mailing list before adding long tests, so their use
  is justified and they do not slow the builds.
- This is the alternative to deleting coverage or skipping it on the Bioconductor
  builders: skipping (`skip_on_bioc()`, and similar guards) means the nightly
  builds never exercise that code, so regressions in it go unnoticed.
- Long tests do not apply to vignettes. A vignette is evaluated during the build,
  so a chunk that is slow needs a smaller example, precomputed results shipped
  with the package, or caching -- not `longtests/` and not `eval=FALSE`.

Source: [Unit tests](https://contributions.bioconductor.org/tests.html) , [Long tests](https://www.bioconductor.org/developers/how-to/LongTests/) , [Advanced build options](https://contributions.bioconductor.org/advanced-build-options.html#long-tests)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
"Long-running tests" was verified 2026-09-26 against the Long tests page and tests.html 15.5,
which links to it; the mechanism is also summarised in Appendix B of `../appendices.md`.
