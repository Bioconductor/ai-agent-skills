# Documentation

Covers: Chapter 13 - Documentation (man pages and vignettes).

## Man pages (Rd files)

- Every exported function and class must have a man page.
- Class documentation must be very detailed about the structure and type of
  information stored in the object.
- Data man pages must include provenance information and data structure
  information.
- A package-level man page is encouraged, accessible via `?<package name>`.
- Documentation may be authored with roxygen2 (comments compiled to Rd) or written
  directly as Rd.

## Examples (runnable)

- All man pages should have runnable examples.
- The enforced threshold is 80%: BiocCheck counts man pages that document an
  exported object, and raises an **ERROR** - "At least 80% of man pages
  documenting exported objects must have runnable examples" - when fewer than
  80% of them have one. Verified in `checkExportsAreDocumented()`, BiocCheck
  devel, 2026-08-14.
- A page whose examples sit entirely inside `\dontrun` or `\donttest` counts as
  having **no** example: BiocCheck runs `tools::Rd2ex(commentDontrun = TRUE,
  commentDonttest = TRUE)` and then parses what is left. Wrapping an example to
  silence a check therefore moves the package toward the ERROR, not away from it.
- `\donttest` and `\dontrun` are generally not allowed except with proper
  justification.
- If wrapping is unavoidable, prefer `\donttest` over `\dontrun`.

## Vignettes

- At least one vignette is required, in Rmd (recommended), qmd (Quarto), or Rnw
  (Sweave) format.
- Code must be executable and demonstrate actual functionality: "Non-trivial
  executable code is a must!!! Static vignettes are not acceptable."
- Each vignette should include an Introduction, Installation instructions, a Table
  of Contents (when appropriate), and a `sessionInfo()` call.
- Installation instruction chunks must use `eval = FALSE`.
- R Markdown vignettes should use the BiocStyle package for rendering.
- Quarto vignettes require the Quarto command-line tool to be listed in
  DESCRIPTION.

## Overall documentation standards

- Vignettes demonstrating core functionality.
- Man pages for all exported functions, each with runnable examples.
- Well-documented data structures and datasets.
- References to the methods used and to related packages.

Source: [Documentation](https://contributions.bioconductor.org/docs.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
