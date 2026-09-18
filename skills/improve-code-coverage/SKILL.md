---
name: improve-code-coverage
description: Analyze R package code coverage using covr, audit existing tests for tautological assertions, classify testing gaps, and proactively write test cases to improve coverage and result correctness.
version: 1.1.0
category: r-packages
tags: [r-packages, testing, code-coverage, covr, bioconductor]
author: bioconductor
---

# improve-code-coverage

Analyzes an R package's code coverage using the `covr` package, audits existing tests for tautological or vacuous assertions (pseudo-coverage), identifies uncovered lines (specifically in `R/` and `src/`), and actively suggests and writes new test cases in the package's native testing framework. It emphasizes a Bioconductor-standard approach to testing by classifying coverage and new tests into: a) normal use, b) edge cases, c) error handling, and d) correctness of results.

## Usage

Invoke this skill when you want to increase your package's test coverage or evaluate testing rigor:
- "Check my code coverage and help me write missing tests."
- "Audit my existing tests for tautological or vacuous test cases."
- "Run covr on the package and improve testing for uncovered lines in `R/my_function.R`."
- "Improve code coverage, focusing on edge cases and correctness."
- "Summarize current code coverage."

## Prerequisites

- An R package structure with an `R/` directory and an established testing framework setup:
  - `testthat`: tests located in `tests/testthat/`
  - `tinytest`: tests located in `inst/tinytest/`
  - `RUnit`: tests located in `inst/unitTests/`
- R packages `covr` and the package's declared testing framework installed.
- (Optional but recommended) `src/` directory if the package uses compiled code.

## Process

### 1. Run Coverage Analysis
- Execute `covr::package_coverage()` (or `covr::file_coverage()` if focused on specific files).
- Generate a local HTML report using `covr::report()` for the user to view visually, if applicable.
- Extract and calculate the current coverage percentages for files in the `R/` and `src/` directories.

### 2. Audit Existing Tests for Tautological and Vacuous Assertions
Detect the package's testing framework (`testthat`, `tinytest`, or `RUnit`). Before assuming that covered lines are reliably tested, audit existing test files in their corresponding directories (`tests/testthat/`, `inst/tinytest/`, or `inst/unitTests/`) for anti-patterns that produce "pseudo-coverage" (high line coverage without verifying actual functionality):
- **Implementation-mirroring**: Computing `expected` values by re-implementing or copy-pasting the function's own mathematical formulas or algorithm logic inside the test body.
- **Vacuous assertions**: Assertions that cannot meaningfully fail or only verify that code ran without checking output correctness (e.g., sole assertions like `expect_no_error()` or `expect_true(!is.null(x))`). Note that class-only checks (e.g., `expect_s4_class()` or `tinytest::expect_inherits()`) are context-dependent; they can be valid contract tests for remote data or external API interfaces, but are vacuous when testing local transformations and computations whose primary contract is data accuracy, dimensions, or slot contents.
- **Over-mocked circularity**: Tests where mocks or stubs return hardcoded data and the test simply asserts that the function returned the mocked output.
- Flag any identified pseudo-coverage tests and recommend refactoring them with independent ground-truth checks using the package's existing testing framework.

### 3. Summarize and Identify Gaps
- Present a high-level summary of the coverage results in the chat. Crucially, when summarizing, evaluate not only the raw percentage but also:
  - Test hygiene and pseudo-coverage identified in the audit of existing tests.
  - The type of testing present across the four core dimensions (normal use, edge cases, error handling, correctness).
- Identify specific functions, branches, or lines in `R/` and `src/` that lack test coverage or rely on vacuous tests.

### 4. Classify Testing Needs
For the uncovered or pseudo-covered lines, analyze the function's logic and classify the missing test requirements into four categories:
- **Normal Use**: Standard expected inputs and typical workflows.
- **Edge Cases**: NA handling, empty inputs (e.g., 0-row `DataFrame`/`GRanges`), boundary values, and extreme but valid inputs.
- **Error Handling**: Verifying that invalid inputs or unsupported types gracefully throw informative errors (e.g., using `expect_error()` or framework equivalent).
- **Correctness of Results**: Validating that the statistical or computational outputs are mathematically and scientifically correct (crucial for Bioconductor packages).

### 5. Propose and Write Tests
- Draft new test code blocks matching the package's native testing framework (`testthat`, `tinytest`, or `RUnit`) targeting the identified gaps and refactoring any tautological tests.
- Explicitly label which of the four categories (Normal Use, Edge Cases, Error Handling, Correctness) each test addresses.
- **Enforce anti-tautology rules in new tests**:
  - Never generate `expected` outputs by re-executing the function's internal logic inside the test.
  - Establish independent ground truth: hand-calculated values, established benchmark datasets, verified outputs from standard base R / Bioconductor reference functions, or known mathematical invariants.
  - Test the actual contents, dimensions, and S4 object validities rather than just object existence or non-error status (unless testing an external contract).

### 6. Review and Iterate
- Present the suggested tests and test refactors to the user.
- If requested, append or insert the new tests into the appropriate test files in `tests/testthat/`, `inst/tinytest/`, or `inst/unitTests/`.
- Suggest re-running the coverage analysis to verify the improvement.

## Output Format

- A chat summary that explicitly breaks down coverage by test category (Normal Use, Edge Cases, Error Handling, Correctness) and notes any pseudo-coverage found in existing tests.
- Code blocks containing framework-native test cases, categorized by their testing purpose.
- Instructions or scripts to generate the `covr` HTML report.

## Examples

### Example 1: Full Package Coverage Check with Test Quality Audit

**User**: "Check my code coverage and help me write missing tests."

**Agent**:
1. Runs `covr::package_coverage()`.
2. Audits existing tests (e.g., in `tests/testthat/` or `inst/tinytest/`) and notes that while `R/normalize.R` has high line coverage, its tests use implementation-mirroring to generate expected values and only assert `expect_true(!is.null(result))`.
3. Identifies genuine missing edge case tests for `NA` inputs and 0-length count vectors.
4. Drafts new and refactored test blocks in the package's framework addressing those gaps with independent ground-truth assertions, labeled clearly by their category.

### Example 2: Focusing on a Single File

**User**: "Run covr on the package and improve testing for uncovered lines in R/stats.R."

**Agent**:
1. Identifies gaps specifically within `R/stats.R`.
2. Drafts Correctness of Results tests comparing the output of the functions to known expected statistical outputs (without replicating the internal algorithm in the test).
3. Suggests inserting these tests into the package test suite (e.g., `tests/testthat/test-stats.R`).

## Notes

- For Bioconductor packages, establishing ground truth for "correctness of results" is often the hardest part of testing. When writing correctness tests, explain the logic used to determine the expected output.
- Beware of "coverage chasing": writing tautological or vacuous assertions solely to hit arbitrary coverage targets creates technical debt and false confidence. While higher coverage is expected and reduces bug risk, no hard minimum percentage is mandated by Bioconductor; always prioritize semantic correctness over raw line counts.
- Coverage of `src/` (C/C++) requires proper compiler flags; the skill should note this if compiled code coverage is unexpectedly zero.
