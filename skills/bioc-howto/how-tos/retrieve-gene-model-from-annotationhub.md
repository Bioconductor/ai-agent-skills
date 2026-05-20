---
name: retrieve-gene-model-from-annotationhub
description: Download a gene model from AnnotationHub as a GRanges or GRangesList object using Bioconductor
---

# Retrieve a Gene Model from AnnotationHub

When a gene model is not bundled as a Bioconductor data package, it may be
available through **AnnotationHub**. Use the hub to search, filter, and download
annotation resources (e.g. UCSC RefSeq gene tracks) as `GRanges` objects.

## Required Packages

```r
BiocManager::install("AnnotationHub")

library(AnnotationHub)
```

## Steps

### 1. Create an AnnotationHub instance and filter by species

```r
hub <- AnnotationHub()

# Filter to species of interest
hub <- subset(hub, hub$species == "Drosophila melanogaster")
length(hub)          # number of matching resources
head(names(hub))     # resource identifiers
head(hub$title, 10)  # titles to identify the record you want
```

### 2. Inspect a specific resource

```r
# Examine a particular record (e.g. index 5)
hub[5]
```

### 3. Download the resource as a GRanges object

```r
gr <- hub[[names(hub)[5]]]
summary(gr)
metadata(gr)  # source, genome version, and other provenance
```

### 4. Split GRanges by gene name to get a GRangesList

```r
# Group transcript ranges by gene name
txbygn <- split(gr, gr$name)
# txbygn is now a GRangesList suitable for summarizeOverlaps()
```

## Key Functions

- `AnnotationHub()` — create a hub instance (internet connection required)
- `subset(hub, condition)` — filter hub records by metadata fields
- `hub[[id]]` — download a resource by identifier
- `split(gr, gr$name)` — group a `GRanges` by a metadata column into `GRangesList`
- `metadata(gr)` — retrieve provenance metadata

## Notes

- An internet connection is required to query and download from AnnotationHub.
  Downloaded resources are cached locally.
- Before passing `txbygn` to `summarizeOverlaps()`, verify that seqlevels
  (chromosome names) match those in your BAM file.
  Use `renameSeqlevels()`, `keepSeqlevels()`, or `seqlevels()` to align them.
- Use `hub$dataprovider`, `hub$genome`, and `hub$rdataclass` as additional
  filters to narrow down the available resources.

## Further Reading

- `vignette("AnnotationHub")` — full package vignette
- `?renameSeqlevels` / `?keepSeqlevels` — chromosome name reconciliation
- `?summarizeOverlaps` — counting reads over genomic features
