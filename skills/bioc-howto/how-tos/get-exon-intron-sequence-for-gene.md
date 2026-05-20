---
name: get-exon-intron-sequence-for-gene
description: Retrieve exon and intron DNA sequences for a specific gene using Bioconductor
---

# Get Exon and Intron Sequences for a Gene

Use Bioconductor to extract the genomic coordinates and DNA sequences of all
exons and introns across all known transcripts of a given gene.

## Required Packages

```r
BiocManager::install(c(
    "TxDb.Hsapiens.UCSC.hg38.knownGene",
    "BSgenome.Hsapiens.UCSC.hg38",
    "GenomicFeatures",
    "Biostrings"
))

library(TxDb.Hsapiens.UCSC.hg38.knownGene)
library(GenomicFeatures)
library(BSgenome.Hsapiens.UCSC.hg38)
```

## Steps

### 1. Identify transcripts for the gene of interest

```r
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene

# Use Entrez gene ID (e.g. TRAK2 = "66008")
trak2 <- "66008"

# Get all transcripts for this gene as a GRanges object
trak2_txs      <- transcriptsBy(txdb, by = "gene")[[trak2]]
trak2_tx_names <- mcols(trak2_txs)$tx_name
```

### 2. Extract exon coordinates per transcript

```r
# Returns a GRangesList (one element per transcript)
trak2_exbytx <- exonsBy(txdb, "tx", use.names = TRUE)[trak2_tx_names]
elementNROWS(trak2_exbytx)  # number of exons per transcript
```

### 3. Extract intron coordinates per transcript

```r
trak2_inbytx <- intronsByTranscript(txdb, use.names = TRUE)[trak2_tx_names]
elementNROWS(trak2_inbytx)  # number of introns per transcript
```

### 4. Retrieve DNA sequences for exons

```r
trak2_ex_seqs <- getSeq(Hsapiens, trak2_exbytx)
# Returns a DNAStringSetList; each element is a DNAStringSet of exon sequences
trak2_ex_seqs[[1]]  # exon sequences for first transcript
```

### 5. Retrieve DNA sequences for introns

```r
trak2_in_seqs <- getSeq(Hsapiens, trak2_inbytx)
trak2_in_seqs[[1]]  # intron sequences for first transcript
```

## Key Functions

- `transcriptsBy(txdb, by = "gene")` — get transcripts grouped by gene (returns `GRangesList`)
- `exonsBy(txdb, by = "tx", use.names = TRUE)` — get exons grouped by transcript
- `intronsByTranscript(txdb, use.names = TRUE)` — get introns grouped by transcript
- `getSeq(BSgenome, GRangesList)` — retrieve sequences for a list of ranges
- `elementNROWS()` — count elements per list entry

## Notes

- Entrez gene IDs are used with `TxDb.Hsapiens.UCSC.hg38.knownGene`.
  Use `AnnotationDbi::mapIds()` to convert gene symbols to Entrez IDs if needed.
- `getSeq()` returns a `DNAStringSetList` when given a `GRangesList`;
  each element corresponds to one transcript.
- Replace the TxDb and BSgenome packages with species-appropriate packages for
  non-human organisms.

## Further Reading

- `vignette("GenomicFeatures")` — working with gene models
