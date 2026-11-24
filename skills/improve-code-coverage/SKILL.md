---
name: improve-code-coverage
description: Analyze R package code coverage using covr, audit existing tests for tautological assertions, classify testing gaps, and proactively write test cases to improve coverage and result correctness.
metadata:
  version: 1.1.2
  category: r-packages
  author: bioconductor
  tags: r-packages, testing, code-coverage, covr, bioconductor
---

# improve-code-coverage

Measure an R package's test coverage with `covr`, audit the existing tests for assertions that add line coverage without verifying behaviour (pseudo-coverage), and draft tests for the gaps in the package's own testing framework.

## Usage

- "Check my code coverage and help me write missing tests."
- "Audit my existing tests for tautological or vacuous test cases."
- "Summarize current code coverage."

## Prerequisites

- An R package with `covr` and its testing framework installed. The framework determines where tests live:
  - `testthat`: `tests/testthat/` (runner `tests/testthat.R`)
  - `tinytest`: `inst/tinytest/` (runner `tests/tinytest.R`)
  - `RUnit`: `inst/unitTests/` (runner `tests/runTests.R`)

## Process

### 1. Run Coverage Analysis

- Run `covr::package_coverage()`. When the user names specific files, restrict the report and the later steps to those files (`covr::file_coverage()` is an alternative).
- Report coverage percentages for the files in `R/` and `src/`.
- Where the user can view it, generate the HTML report with `covr::report()`; otherwise give them the command.
- If coverage of `src/` is unexpectedly zero, tell the user that compiled-code coverage depends on the compiler flags.

### 2. Audit Existing Tests for Tautological and Vacuous Assertions

Before treating covered lines as tested, read the existing test files and flag these patterns:

- **Implementation-mirroring**: the test computes `expected` by re-implementing or copying the function's own formula or algorithm.
- **Vacuous assertions**: assertions that cannot meaningfully fail, or that only verify execution when the contract requires observable output (e.g. a lone `expect_no_error()` or `!is.null(x)` with no assertion on the result). A class-only check (`expect_s4_class()`) is valid for an external or remote contract, but vacuous when the contract is data accuracy or slot contents.
- **Over-mocked circularity**: a mock returns hardcoded data and the test only asserts that the function returned it, without verifying argument delegation or transformation logic.

Recommend refactoring each flagged test with an independent ground-truth check (Step 5).

### 3. Summarize and Identify Gaps

Summarize for the user:

- The coverage percentages from Step 1
- The pseudo-coverage found in Step 2
- Which of the four categories in Step 4 the existing tests address
- The functions, branches, or lines in `R/` and `src/` that have no coverage or rely on vacuous tests

### 4. Classify Testing Needs

For each uncovered or pseudo-covered region, classify the missing tests:

- **Normal Use**: standard inputs and typical workflows.
- **Edge Cases**: `NA` handling, empty inputs (e.g. a 0-row `DataFrame` or `GRanges`), boundary values, extreme but valid inputs.
- **Error Handling**: invalid inputs or unsupported types throw informative errors (`expect_error()` or the framework's equivalent).
- **Correctness of Results**: statistical or computational outputs are mathematically and scientifically correct.

### 5. Propose and Write Tests

- Draft tests in the package's framework for the gaps, and refactors for the tests flagged in Step 2.
- Label each test with its Step 4 category.
- Never compute `expected` by re-running the function's internal logic. Use independent ground truth: benchmarks, hand-calculated values, reference outputs, or mathematical invariants. Assert on contents and dimensions, not on object existence.
- For each Correctness of Results test, explain how the expected output was determined.
- Do not write tautological or vacuous assertions to reach a coverage target. Bioconductor mandates no minimum percentage, so put the correctness of the assertions ahead of the line count.

### 6. Review and Iterate

Present the drafted tests and refactors. Write them into the package's test directory only if the user asks, then suggest re-running Step 1 to confirm the improvement.

## Examples

### Example 1: High coverage that is pseudo-coverage

**User**: "Check my code coverage and help me write missing tests."

`covr::package_coverage()` reports high line coverage for `R/normalize.R`, but its tests compute expected values with the same formula as the function and assert only `expect_true(!is.null(result))`. The summary reports that file as pseudo-covered, and reports that no test exercises `NA` inputs or 0-length count vectors. The drafted tests replace the mirrored expectations with hand-calculated values (Correctness of Results) and add the `NA` and 0-length cases (Edge Cases).
