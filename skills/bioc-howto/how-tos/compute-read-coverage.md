---
name: compute-read-coverage
description: Compute per-base read coverage from a BAM file using Bioconductor's GenomicAlignments package
---

# Compute Read Coverage

"Read coverage" is the number of sequencing reads that cover each genomic position.
Use the `coverage()` function from the **GenomicAlignments** Bioconductor package to
compute per-base coverage across the genome from aligned reads stored in a BAM file.

## Required Packages

```r
# Install if needed
BiocManager::install(c("pasillaBamSubset", "GenomicAlignments"))

library(pasillaBamSubset)
library(GenomicAlignments)
```

## Steps

### 1. Load reads from a BAM file

```r
# Get path to a BAM file (single-end reads)
un1 <- untreated1_chr4()   # example from pasillaBamSubset

# Read alignments into a GAlignments object
reads <- readGAlignments(un1)
```

### 2. Compute genome-wide coverage

```r
cvg <- coverage(reads)
# cvg is an RleList, one Rle per chromosome
cvg
```

### 3. Extract coverage for a specific chromosome

```r
cvg$chr4
```

### 4. Summarize coverage statistics

```r
mean(cvg$chr4)
max(cvg$chr4)
```

### 5. Find high-coverage regions (slice)

Use `slice()` to identify contiguous regions where coverage meets a threshold:

```r
chr4_highcov <- slice(cvg$chr4, lower = 500)
chr4_highcov

# "Weight" of each region = total aligned nucleotides (area under coverage curve)
sum(chr4_highcov)
```

## Key Functions

- `readGAlignments()` — import single-end reads from a BAM file into a `GAlignments` object
- `coverage()` — compute per-position read depth; returns an `RleList`
- `slice()` — extract regions where coverage exceeds a threshold
- `mean()` / `max()` — summarize an `Rle` object

## Notes

- `coverage()` and `slice()` are generic functions with methods for multiple object types.
  See `?coverage` and `?slice` for details.
- For paired-end data, use `readGAlignmentPairs()` before calling `coverage()`.

## Further Reading

- `vignette("GenomicAlignments")` — GenomicAlignments package vignette
