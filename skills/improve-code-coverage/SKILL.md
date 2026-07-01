---
name: improve-code-coverage
description: Analyze R package code coverage using covr, classify testing gaps, and proactively write test cases to improve coverage and result correctness.
version: 1.0.0
category: r-packages
tags: [r-packages, testing, code-coverage, covr, bioconductor]
author: waldronlab
---

# improve-code-coverage

Analyzes an R package's code coverage using the `covr` package, identifies uncovered lines (specifically in `R/` and `src/`), and actively suggests and writes new test cases. It emphasizes a Bioconductor-standard approach to testing by classifying coverage and new tests into: a) normal use, b) edge cases, c) error handling, and d) correctness of results.

## Usage

Invoke this skill when you want to increase your package's test coverage or evaluate testing rigor:
- "Check my code coverage and help me write missing tests."
- "Run covr on the package and improve testing for uncovered lines in `R/my_function.R`."
- "Improve code coverage, focusing on edge cases and correctness."
- "Summarize current code coverage."

## Prerequisites

- An R package structure with an `R/` directory and typically a `tests/` directory (e.g., using `testthat`).
- R packages `covr` and `testthat` installed.
- (Optional but recommended) `src/` directory if the package uses compiled code.

## Process

### 1. Run Coverage Analysis
- Execute `covr::package_coverage()` (or `covr::file_coverage()` if focused on specific files).
- Generate a local HTML report using `covr::report()` for the user to view visually, if applicable.
- Extract and calculate the current coverage percentages for files in the `R/` and `src/` directories.

### 2. Summarize and Identify Gaps
- Present a high-level summary of the coverage results in the chat. Crucially, when summarizing, evaluate not only the raw percentage but also the type of testing present (normal use, edge cases, error handling, correctness).
- Identify specific functions, branches, or lines in `R/` and `src/` that lack test coverage.

### 3. Classify Testing Needs
For the uncovered lines, analyze the function's logic and classify the missing test requirements into four categories:
- **Normal Use**: Standard expected inputs and typical workflows.
- **Edge Cases**: NA handling, empty inputs, and extreme but valid values.
- **Error Handling**: Verifying that invalid inputs or unsupported types gracefully throw informative errors (e.g., using `expect_error()`).
- **Correctness of Results**: Validating that the statistical or computational outputs are mathematically and scientifically correct (crucial for Bioconductor packages).

### 4. Propose and Write Tests
- Draft new `testthat` code blocks targeting the identified gaps.
- Explicitly label which of the four categories (Normal Use, Edge Cases, Error Handling, Correctness) each new test addresses.
- Focus on assertions that verify *correctness* (e.g., `expect_equal()`, `expect_identical()`) rather than just checking if the code runs without error (`expect_no_error()`), alongside proper `expect_error()` checks for invalid states.

### 5. Review and Iterate
- Present the suggested tests to the user.
- If requested, append or insert the new tests into the appropriate files in `tests/testthat/`.
- Suggest re-running the coverage analysis to verify the improvement.

## Output Format

- A chat summary that explicitly breaks down coverage by test category (Normal Use, Edge Cases, Error Handling, Correctness).
- Code blocks containing `testthat` test cases, categorized by their testing purpose.
- Instructions or scripts to generate the `covr` HTML report.

## Examples

### Example 1: Full Package Coverage Check

**User**: "Check my code coverage and help me write missing tests."

**Agent**:
1. Runs `covr::package_coverage()`.
2. Summarizes the results, noting for example that `R/normalize.R` is missing edge case tests for `NA` inputs.
3. Drafts new `test_that` blocks addressing those gaps, labeled clearly by their category.

### Example 2: Focusing on a Single File

**User**: "Run covr on the package and improve testing for uncovered lines in R/stats.R."

**Agent**:
1. Identifies gaps specifically within `R/stats.R`.
2. Drafts Correctness of Results tests comparing the output of the functions to known expected statistical outputs.
3. Suggests inserting these tests into `tests/testthat/test-stats.R`.

## Notes

- For Bioconductor packages, establishing ground truth for "correctness of results" is often the hardest part of testing. When writing correctness tests, explain the logic used to determine the expected output.
- Coverage of `src/` (C/C++) requires proper compiler flags; the skill should note this if compiled code coverage is unexpectedly zero.
