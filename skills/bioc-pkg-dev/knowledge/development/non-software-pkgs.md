Covers: Chapter 20 - Non-software packages

# Non-Software Packages

Non-software packages fall into two families: annotation packages and
experiment data packages. Hub-based distribution is preferred over
self-contained data packages.

## Annotation packages

- Link identifiers (gene names, probe IDs) to related information
  (chromosomal location, Gene Ontology categories, mappings).
- Must include proper documentation for the data provided.

## Experiment data packages

- Contain curated datasets from an experiment, course, or publication,
  typically a single dataset.
- Require documentation of the data (source, creation, use).
- Traditional self-contained experiment data packages are discouraged; prefer
  the Hub approach.

## Hub packages (AnnotationHub / ExperimentHub)

- Lightweight: data is stored externally (AWS S3, Azure Data Lakes, Ensembl,
  other public sites) and fetched on demand.
- Must minimally contain: resource metadata, man pages describing the
  resources, and a vignette. May include supporting R functions.
- Follow the `CreateAHubPackage` vignette in the HubPub package.

## biocViews

- Annotation packages must include `AnnotationData` (and appropriate child
  terms) in the DESCRIPTION `biocViews:` field.
- Experiment data packages must include `ExperimentData` (and child terms).
- Correct biocViews determine which of the three Bioconductor repositories the
  package is assigned to.

## Submission

- Submit through the GitHub package submission tracker.
- Indicate the package type (annotation, experiment data, workflow) at
  submission.

Source: [Non-software packages](https://contributions.bioconductor.org/non-software.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
