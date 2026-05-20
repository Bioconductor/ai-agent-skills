---
name: compute-sequence-composition-for-genomic-regions
description: Compute GC content and CpG observed/expected ratio for genomic regions using Bioconductor
---

# Compute Sequence Composition for Genomic Regions

Use Bioconductor to extract DNA sequences for genomic regions and compute
composition features such as GC percentage and CpG dinucleotide ratios.
This is commonly used to identify CpG island promoters.

## Required Packages

```r
BiocManager::install(c(
    "TxDb.Hsapiens.UCSC.hg38.knownGene",
    "BSgenome.Hsapiens.UCSC.hg38",
    "GenomicFeatures",
    "Biostrings"
))

library(GenomicFeatures)
library(TxDb.Hsapiens.UCSC.hg38.knownGene)
library(Biostrings)
library(BSgenome.Hsapiens.UCSC.hg38)
```

## Steps

### 1. Get promoter coordinates from a TxDb

```r
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene

# Define promoters as 2000 bp windows centered on TSS (1000 upstream, 1000 downstream)
prom <- promoters(txdb, upstream = 1000, downstream = 1000)
```

### 2. Trim promoters to chromosome boundaries and deduplicate

```r
# Trim regions that extend beyond chromosome ends
prom <- trim(prom)

# Remove duplicate promoters (from transcripts sharing the same TSS)
prom <- prom[!duplicated(prom)]
```

### 3. Extract sequences from the reference genome

```r
promseq <- getSeq(BSgenome.Hsapiens.UCSC.hg38, prom)
# promseq is a DNAStringSet
```

### 4. Compute mono- and dinucleotide frequencies

```r
mo <- oligonucleotideFrequency(promseq, width = 1, as.prob = TRUE)  # mononucleotides
di <- oligonucleotideFrequency(promseq, width = 2, as.prob = TRUE)  # dinucleotides
```

### 5. Calculate GC content and CpG observed/expected ratio

```r
percentGC <- 100 * (mo[, "C"] + mo[, "G"])

expectedCpG    <- mo[, "C"] * mo[, "G"]
obsExpRatioCpG <- di[, "CG"] / expectedCpG
```

### 6. Visualize distributions

```r
hist(percentGC, 60)           # GC% distribution across promoters
hist(obsExpRatioCpG, 60)      # obs/exp CpG ratio — bimodal for CpG islands
abline(v = 0.45, col = 2, lty = 2)  # typical CpG island threshold

plot(obsExpRatioCpG, percentGC, pch = "*", col = "#22222205")
abline(v = 0.45, col = 2, lty = 2)
```

## Key Functions

- `promoters(txdb, upstream, downstream)` — extract promoter `GRanges` from a `TxDb`
- `trim()` — clip ranges to chromosome boundaries
- `getSeq(genome, ranges)` — fetch sequences from a `BSgenome` for given `GRanges`
- `oligonucleotideFrequency(seqs, width, as.prob)` — compute k-mer frequencies from a `DNAStringSet`

## Notes

- `getSeq()` also accepts `DNAStringSet` objects and FASTA/2bit files;
  use `showMethods(getSeq)` to see all supported input types.
- The obs/exp CpG ratio reveals a bimodal structure useful for CpG island classification;
  ratios < 1.0 are expected because CpG dinucleotides are under-represented genome-wide.

## Further Reading

- `vignette(package = "Biostrings")` — working with biological sequences
