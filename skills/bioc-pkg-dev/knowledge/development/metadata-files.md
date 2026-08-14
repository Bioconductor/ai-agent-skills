# Metadata Files

Covers: Chapters 6-12 - README, DESCRIPTION, NAMESPACE, NEWS, LICENSE, CITATION,
and system dependencies.

## README (Chapter 6)

- README is optional but useful, especially for packages developed on GitHub.
- If present, it must clearly give Bioconductor installation instructions using
  `BiocManager::install()`.
- Any installation code blocks must use `eval = FALSE` so they do not execute.
- Files with executable code (including `README.Rmd`) must NOT install packages,
  download system dependencies, or download applications; assume dependencies are
  already present.
- Declare external software in DESCRIPTION `SystemRequirements`, not in the README.
- `README.md` may be auto-generated from a vignette via `README.Rmd` (R Markdown
  child documents) and `rmarkdown::render()`.

## DESCRIPTION (Chapter 7)

Required fields:

- **Package** - must match the repository name (case-sensitive).
- **Title** - brief but descriptive summary.
- **Version** - `x.y.z` scheme. New submissions start at **0.99.0**. `y` is even
  for release versions, odd for devel; `z` increments with each commit.
- **Description** - relatively short but detailed overview; at least three complete
  sentences.
- **Authors@R** - required (use this, not `Authors:`). Must include the maintainer
  with the `cre` role and an actively maintained email. Use a single maintainer.
  Include ORCID in `comment` if available. Example:
  `person("First", "Last", email = "me@x.org", role = c("cre", "aut"), comment = c(ORCID = "..."))`.
- **License** - standard R license spec, version-specific (see LICENSE section).
- **biocViews** - REQUIRED (case-sensitive, lowercase 'b'). At least two leaf
  nodes, all from the same trunk/package type; single comma-separated line.

Dependency fields (Depends, Imports, Suggests, Enhances):

- All dependencies must come from Bioconductor or CRAN. The `Remotes:` field is
  NOT supported.
- List each package only once across these fields.
- **Imports** - functions/methods/classes used within the package namespace
  (the usual place for dependencies).
- **Depends** - only for functionality essential to users; rarely more than 3
  packages (avoid Depends bloat).
- **Suggests** - packages used only in vignettes, examples, or conditional code.
- **Enhances** - optional performance packages such as `Rmpi` or `parallel`.
- Version specifications are usually not needed.

Other fields:

- **LazyData** - omit `LazyData: TRUE` for large data packages (it slows loading).
- **SystemRequirements** - external software not auto-installed; add an INSTALL
  file for non-trivial installs.
- **BugReports** - encouraged; link to the GitHub issues page.
- **URL** - source repo and help resources.
- **VignetteBuilder** - name the builder (e.g., `knitr`) when using vignettes.
- **BiocType** - required for Docker/Workflow submissions; values `Software`,
  `ExperimentData`, `Annotation`.
- **Config/Bioconductor/UnsupportedPlatforms** - comma-separated list to exclude
  platforms (`windows`, `windows-x64`, `macosx`, `macosx-x86_64`, `macosx-arm64`).

## NAMESPACE (Chapter 8)

- Prefer `importFrom()` to import specific functions; use `import()` only when
  importing many functions from one package.
- For Bioconductor classes, `import()` the whole package so full class
  functionality is inherited automatically.
- Do NOT use broad export patterns: `exportPattern("^[[:alpha:]]+")` is strongly
  discouraged and almost always not allowed. Export functions/generics
  individually.
- Exported function names should use camelCase or underscores; avoid dots (dots
  imply S3 dispatch). Functions beginning with `.` stay internal and are not
  exported.
- Use `exportMethods()` / `exportClasses()` for S4 methods and classes, and
  `useDynLib()` for compiled code.

## NEWS (Chapter 9)

- Exactly one NEWS file per package, in one of: `./inst/NEWS.Rd`, `./inst/NEWS`,
  `./inst/NEWS.md`, `./NEWS.md`, or `./NEWS`.
- NEWS files MUST use list elements/structure; plain text files are not allowed.
- Document the forthcoming release version, in non-technical language.
- Version heading format:

  ```text
  CHANGES IN VERSION X.Y.Z
  -------------------------
  ```

- Use section headers such as "NEW FEATURES" and "SIGNIFICANT USER-VISIBLE
  CHANGES" with bullet points.
- Bioconductor compiles NEWS files into semi-annual release announcements.
- Validate formatting with `utils::news(package = "<package_name>")`.

## LICENSE (Chapter 10)

- Use R's standard license specifications (r-project.org/Licenses). Be version
  specific (e.g., `GPL-2`). Core packages typically use `Artistic-2.0`.
- Forbidden: licenses restricting use (e.g., to academic or non-profit
  researchers) and other restrictive licenses (CC BY-NC variants, ACM).
- For a non-standard license, add a full `LICENSE` file at the package root and
  reference it as `file LICENSE`; the file must match the `License:` field.
- All dependencies must have compatible open-source licenses, and the package must
  contain only code that can be redistributed under its license.

## CITATION (Chapter 11)

- Place the file at `inst/CITATION`. It is optional but recommended.
- Validate with `readCitationFile("inst/CITATION")` (must run without errors) so it
  displays correctly on the package landing page.
- Follow Writing R Extensions conventions; specify author/maintainer details for
  correct name formatting. If absent, Bioconductor auto-generates a citation.
- Also include citations in help pages and vignettes.

## System dependencies (Chapter 12)

- Declare external software in the DESCRIPTION `SystemRequirements` field, with an
  optional INSTALL file giving install instructions for Linux, Windows, and Mac.
- System requirements must never be exclusive to a specific version; work with
  current versions of the external software.
- Declaring a requirement does not guarantee Bioconductor will agree to install it.
- Discuss additional system requirements on <bioc-devel@r-project.org> before
  development. Do not install system dependencies from within package code.

Source: [README](https://contributions.bioconductor.org/readme.html),
[DESCRIPTION](https://contributions.bioconductor.org/description.html),
[NAMESPACE](https://contributions.bioconductor.org/namespace.html),
[NEWS](https://contributions.bioconductor.org/news.html),
[LICENSE](https://contributions.bioconductor.org/license.html),
[CITATION](https://contributions.bioconductor.org/citation.html),
[System dependencies](https://contributions.bioconductor.org/sysdep.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
