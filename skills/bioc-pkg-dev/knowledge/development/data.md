Covers: Chapter 14 - Including data in a package

# Package Data

## Size limits and where large data goes

- Keep the whole package small. Source tarballs should stay under roughly
  5 MB for software packages; do not bloat a software package with data.
- Large data sets must NOT be committed to the package. There is no Git-LFS
  support. Distribute large data through ExperimentHub or AnnotationHub.
- Traditional (self-contained) experiment data packages need pre-approval on
  the bioc-devel mailing list. Prefer Hub-based distribution instead.

## Directory conventions

| Location        | Purpose                          | Access             |
|-----------------|----------------------------------|--------------------|
| `data/`         | Exported R datasets              | `data("mydata")`   |
| `inst/extdata/` | Raw files parsed by workflows    | `system.file()`    |
| `R/sysdata.rda` | Internal, non-exported data      | package-internal   |

- Small data used by examples, vignettes, and tests may ship directly in the
  package (`data/` or `inst/extdata/`).
- Store scripts that generated the data in `inst/scripts/` (or `data-raw/`).

## Formats and compression

- Preferred format for `data/`: `.RData` created with `save()`. Other formats
  allowed (see `?data`).
- Compress all data files.
- Avoid `LazyData: true`. Despite general R advice, Bioconductor recommends
  against it because it slows package loading when data is large.

## Documentation requirements

- Every dataset must be documented: creation method, source, and intended use.
- Raw files in `inst/extdata/` need metadata describing derivation and format.

## Caching and file-writing restrictions

- Forbidden: downloading or writing files to the user home directory, working
  directory, or the installed package directory.
- For persistent caching use BiocFileCache (preferred) or
  `tools::R_user_dir(package, which = "cache")`.
- For non-persistent scratch files use `tempdir()` / `tempfile()`.

## ExperimentHub / AnnotationHub

- ExperimentHub: curated experiment data stored externally, retrieved on demand.
- AnnotationHub: annotation resources (genomic identifiers, mappings) served
  externally.
- Both give a lightweight package: metadata + man pages + vignette, with the
  heavy data hosted remotely. See the HubPub `CreateAHubPackage` vignette.

Source: [Package data](https://contributions.bioconductor.org/data.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
