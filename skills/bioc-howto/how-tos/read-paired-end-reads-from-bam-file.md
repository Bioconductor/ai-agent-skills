---
name: read-paired-end-reads-from-bam-file
description: Load paired-end reads from a BAM file as GAlignmentPairs or GAlignmentsList using Bioconductor
---

# Read Paired-End Reads from a BAM File

Use the **GenomicAlignments** package to load paired-end reads from a BAM file
into one of two representations: `GAlignmentPairs` (strict pairs only) or
`GAlignmentsList` (pairs plus non-mated reads).

## Required Packages

```r
BiocManager::install(c("GenomicAlignments", "pasillaBamSubset"))

library(GenomicAlignments)
```

## Steps

### 1. Get the path to a paired-end BAM file

```r
library(pasillaBamSubset)
bam_path <- untreated3_chr4()  # example paired-end BAM
# Replace with your own: bam_path <- "/path/to/paired.bam"
```

### 2a. Load as GAlignmentPairs (strict mate pairing)

`readGAlignmentPairs()` returns only properly paired reads; reads with no mate
or ambiguous pairing are discarded.

```r
gapairs <- readGAlignmentPairs(bam_path)
class(gapairs)  # "GAlignmentPairs"
gapairs

# Access first / last segments in a pair (i.e. read 1 and read 2)
first(gapairs)
last(gapairs)
```

### 2b. Load as GAlignmentsList (pairs + non-mates)

Set `asMates = TRUE` on the `BamFile` object. Non-mated reads (singletons,
unmapped mates, etc.) are included as variable-size groups.

```r
galist <- readGAlignmentsList(BamFile(bam_path, asMates = TRUE))
galist

# Check mate status for each group
mcols(galist)$mate_status  # "mated", "ambiguous", or "unmated"

# Access non-mated reads
non_mates <- galist[unlist(mcols(galist)$mate_status) == "unmated"]
table(elementNROWS(non_mates))  # group size distribution
```

## Key Functions

- `readGAlignmentPairs(file, param)` — load paired-end reads; strict pairing only
- `readGAlignmentsList(BamFile(file, asMates = TRUE))` — load all reads with pairing metadata
- `first(gapairs)` / `last(gapairs)` — access read 1 / read 2 from `GAlignmentPairs`
- `mcols(galist)$mate_status` — pairing status per group in `GAlignmentsList`
- `BamFile(path, asMates)` — create a `BamFile` handle with pairing options

## Notes

- Both functions accept a `ScanBamParam` to filter reads by genomic position,
  flags, or specific fields before loading.
- `GAlignmentPairs` is the more common output for downstream coverage or
  counting workflows.

## Further Reading

- `?GAlignmentPairs` (GenomicAlignments) — class documentation
- `vignette("GenomicAlignments")` — full package vignette
