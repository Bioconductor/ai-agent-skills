Covers: Chapter 18 - Shiny apps in packages

# Shiny Apps

## Code location and organization

- UI and server code for a submitted Shiny app must live under the package
  `R/` directory (not in a top-level `app.R` / `inst/shiny`).
- Keep business logic out of `shinyApp()` calls. Build internal functions that
  generate UI and server components separately, so logic is testable without
  launching the app.
- Recommended file naming:
  - `interface_*.R` - functions returning UI elements
  - `outputs_*.R` - functions returning server outputs
  - `observers_*.R` - functions creating reactive observers
  - `utils_*.R` - misc processing helpers

## Launching restrictions

- `shiny::runApp()` must NOT appear anywhere in the package source.
- Exported functions should RETURN a Shiny app object; the user calls
  `runApp()` themselves.

## Testing

- Unit-test all non-reactive functions (e.g. with testthat).
- Wrap untestable reactive code with `# nocov start` / `# nocov end`.
- Use shinytest2 to test visual and computational aspects of the app.
- Put reusable test fixtures in `tests/testthat/setup-*.R`.

## Documentation

- Wrap example code that launches an app in `if (interactive()) { ... }`.
- Document internal functions with roxygen2 `@keywords internal`.
- Include screenshots in the vignette; optimize with pngquant or webshot2.

## Review expectations

- Reviewers run `R CMD build`, `R CMD check`, and BiocCheck, test the app with
  shinytest2, and check graceful error handling and responsive UI.

Source: [Shiny apps](https://contributions.bioconductor.org/shiny.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
