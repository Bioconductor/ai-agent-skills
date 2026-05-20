---
name: read-single-end-reads-from-bam-file
description: Load single-end reads from a BAM file into a GAlignments object using Bioconductor
---

# Read Single-End Reads from a BAM File

Use **GenomicAlignments** to import single-end reads from a BAM file into a
`GAlignments` object. Reads can be filtered by genomic region, strand, or flag
before loading.

## Required Packages

```r
BiocManager::install(c("GenomicAlignments", "Rsamtools", "pasillaBamSubset"))

library(GenomicAlignments)
library(Rsamtools)
```

## Steps

### 1. Load all reads from a BAM file

```r
library(pasillaBamSubset)
bam_path <- untreated1_chr4()  # example single-end BAM
# Replace with your own: bam_path <- "/path/to/single_end.bam"

gal <- readGAlignments(bam_path)
class(gal)  # "GAlignments"
gal
```

### 2. Load a filtered subset with ScanBamParam

Use `ScanBamParam` to restrict reads by genomic position, strand, flags,
or to import additional BAM fields.

```r
# Example: reads on the negative strand overlapping chr4:1-5000,
#          keeping the "flag" and "cigar" metadata columns
what  <- c("flag", "cigar")
which <- GRanges("chr4", IRanges(1, 5000))
flag  <- scanBamFlag(isMinusStrand = TRUE)
param <- ScanBamParam(which = which, what = what, flag = flag)

neg <- readGAlignments(bam_path, param = param)
neg
```

### 3. Export a filtered BAM file

Use `filterBam()` to write reads that pass user-defined criteria to a new BAM:

```r
# Writes passing reads to a new file
filterBam(bam_path, destination = "filtered.bam", param = param)
```

## Key Functions

- `readGAlignments(file, param)` — load single-end reads into a `GAlignments`
- `ScanBamParam(which, what, flag)` — define filters (region, fields, flags)
- `scanBamFlag(...)` — build a flag filter (strand, paired, mapped, duplicate, etc.)
- `filterBam(file, destination, param)` — write filtered reads to a new BAM
- `scanBam(file, param)` — low-level reader returning a list-of-lists

## Notes

- `readGAlignments()` is the high-level function for most use cases.
  `scanBam()` is lower-level and returns a list; use it when you need raw
  BAM fields not wrapped into `GAlignments`.
- The `which` argument in `ScanBamParam` requires the BAM to be indexed (`.bai` file).
- For paired-end data use `readGAlignmentPairs()` or `readGAlignmentsList()`.

## Further Reading

- `?ScanBamParam` / `?scanBamFlag` — full parameter reference
- `?filterBam` — BAM filtering
- `vignette("GenomicAlignments")` — full package vignette
