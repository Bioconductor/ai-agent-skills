Covers: Chapter 17 - Code other than R (compiled and third-party)

# Compiled Code and Third-Party Code

## General rules

- Compiled code must follow the "System and foreign language interfaces"
  section of the Writing R Extensions (R-exts) manual.
- Use `Makevars`/`Makefile` sparingly; they are often unnecessary. See the
  "Configure and cleanup" section of R-exts.
- Code must be portable and build across all supported platforms
  (Linux, macOS, Windows). Test on all before submission.
- Place compiled sources in `src/`.

## Language-specific guidance

- C++: use Rcpp for cross-platform C++ integration (see the Rcpp Gallery).
- Fortran: consider dotCall64 for modern Fortran integration.
- Python: use basilisk to configure Python environments automatically so users
  need no manual install. reticulate is at developer discretion.
- CMake-based builds: use the biocmake package.

## Third-party code responsibilities

- Do not bundle external libraries that duplicate functionality already
  provided by supported R/Bioconductor packages.
- Maintainers take full responsibility for any bundled third-party code:
  keep it updated with upstream bug fixes and releases.
- Complex external libraries may require you to provide pre-built binaries for
  some platforms.
- Ensure the license of any bundled third-party code is compatible with, and
  redistributable under, the package license.

Source: [Code other than R](https://contributions.bioconductor.org/other-than-Rcode.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
