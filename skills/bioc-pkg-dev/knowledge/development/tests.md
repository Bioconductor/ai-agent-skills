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

- Consult the bioc-devel mailing list before adding tests that run very long,
  so they do not slow the nightly builds.

Source: [Unit tests](https://contributions.bioconductor.org/tests.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
