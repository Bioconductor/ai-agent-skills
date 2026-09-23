Covers: the Hub-based route for experiment data and annotation packages (chapters 14 "Package
data" and the "Non-software packages" chapter), and the HubPub `CreateAHubPackage` vignette.

# Hub-based data packages (ExperimentHub / AnnotationHub)

Large data belongs in a Hub, not in the package tarball. A Hub package ships code and metadata;
the files live on Bioconductor's storage and are fetched on demand.

## What the package must contain

- `inst/extdata/metadata.csv`: one row per resource with the fields the Hub requires (Title,
  Description, BiocVersion, Genome, SourceType, SourceUrl, SourceVersion, Species, TaxonomyId,
  Coordinate_1_based, DataProvider, Maintainer, RDataClass, DispatchClass, Location_Prefix,
  RDataPath, Tags). `AnnotationHubData::makeAnnotationHubMetadata()` (or the ExperimentHub
  equivalent) validates it; run it before submitting.
- `inst/scripts/make-data.R`: how every resource was produced from its source, so the data can be
  regenerated; and `inst/scripts/make-metadata.R`: how `metadata.csv` was written.
- Accessor functions (or the generic Hub `query()` shown in the vignette) documented in `man/`,
  with the provenance, source and license of each resource stated where a user will read it.
- A vignette that retrieves at least one resource and shows what it is for. If a chunk cannot
  run at build time, say why in the text; do not leave the core retrieval as `eval=FALSE`
  without a reason.

## Before review

- Contact <hubs@bioconductor.org> and upload the data; the resources must be resolvable through
  the Hub before the package is reviewed, otherwise the vignette and examples cannot run and the
  reviewer cannot check the metadata against the data.
- Licenses and terms of use of the underlying data are stated per resource when they differ from
  the package license.
- Experiment data packages are submitted through the same GitHub tracker as software packages;
  annotation packages are sent by email to <packages@bioconductor.org> instead (see
  [../01-submissions.md](../01-submissions.md)). `BiocType` is `ExperimentData` or `Annotation`,
  and `biocViews` come from the matching single category (`ExperimentData` or `AnnotationData`).

## What reviewers ask about most

- Provenance that `make-data.R` does not actually document (a script that only converts a CSV to
  RDS says nothing about where the CSV came from).
- Accessor code that picks a Hub record by position or fuzzy title instead of by a stable id.
- Data the vignette claims are "curated" or "validated" with no description of how.

Source: [Package data](https://contributions.bioconductor.org/data.html),
[Non-software packages](https://contributions.bioconductor.org/non-software-packages.html) (the
"Hub packages" section), and the HubPub vignette `CreateAHubPackage`. Fetched 2026-09-23 from
contributions.bioconductor.org (Bioconductor devel guide).
