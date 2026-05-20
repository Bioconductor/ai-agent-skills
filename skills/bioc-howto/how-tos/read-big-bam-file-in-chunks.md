---
name: read-big-bam-file-in-chunks
description: Iterate through a large BAM file in memory-efficient chunks using Bioconductor
---

# Read a Large BAM File in Chunks

When a BAM file is too large to load into memory at once, use a `BamFile`
object with a `yieldSize` parameter to iterate through it in fixed-size chunks.
This allows processing (e.g. computing coverage) without exhausting RAM.

## Required Packages

```r
BiocManager::install(c("Rsamtools", "GenomicAlignments", "pasillaBamSubset"))

library(Rsamtools)
library(GenomicAlignments)
```

## Steps

### 1. Create a BamFile with a chunk size

```r
bam_path <- "/path/to/your.bam"  # replace with your BAM file

# yieldSize controls how many records are returned per read call
bf <- BamFile(bam_path, yieldSize = 100000)
```

### 2. Open the file, iterate in chunks, then close

The file must be explicitly opened and closed; each call to `readGAlignments()`
advances through the file returning the next chunk.

```r
open(bf)
cvg <- NULL

repeat {
    chunk <- readGAlignments(bf)
    if (length(chunk) == 0L) break      # end of file

    chunk_cvg <- coverage(chunk)
    if (is.null(cvg)) {
        cvg <- chunk_cvg
    } else {
        cvg <- cvg + chunk_cvg          # accumulate coverage
    }
}

close(bf)
cvg  # RleList of per-base coverage
```

## Key Functions

- `BamFile(path, yieldSize)` — create a `BamFile` handle with chunk-read support
- `open(bf)` / `close(bf)` — open/close the BAM file for streaming
- `readGAlignments(bf)` — read the next chunk; returns empty `GAlignments` at EOF
- `coverage(galignments)` — compute per-base coverage for a chunk

## Notes

- Without calling `open()` first, repeated calls to `readGAlignments()` would
  return the same first chunk each time.
- The same chunking pattern applies to any per-chunk operation: replace the
  `coverage()` accumulation with any reduction or aggregation you need.
- For paired-end data use `readGAlignmentPairs(bf)` inside the loop.

## Further Reading

- `?BamFile` (Rsamtools) — BamFile class and yieldSize documentation
- `vignette("GenomicAlignments")` — working with aligned reads
