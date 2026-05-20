---
name: extract-promoter-sequences
description: Extract promoter DNA sequences for any organism's genes using Bioconductor
---

# Extract Promoter Sequences

Promoters are DNA sequences upstream of a gene's transcription start site (TSS)
that contain transcription factor binding sites. Use Bioconductor to extract
promoter sequences for any gene set from any organism, given a genome FASTA and
gene annotation (GFF/GTF or a `TxDb` object).

## Required Packages

```r
BiocManager::install(c(
    "Biostrings", "rtracklayer", "GenomicRanges",
    "txdbmaker", "GenomicFeatures", "BSgenome"
))

library(Biostrings)
library(GenomicRanges)
library(rtracklayer)
library(txdbmaker)
library(GenomicFeatures)
library(BSgenome)
```

## Steps

### 1. Load genome sequence and gene annotation

```r
# From local or remote FASTA / GFF3 files (example: Arabidopsis thaliana from Ensembl Plants)
genome <- Biostrings::readDNAStringSet(
    "https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-61/fasta/arabidopsis_thaliana/dna/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa.gz"
)
names(genome) <- gsub(" .*", "", names(genome))  # keep only chr name

annotation <- rtracklayer::import(
    "https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-61/gff3/arabidopsis_thaliana/Arabidopsis_thaliana.TAIR10.61.gff3.gz"
)
```

> **Tip for model organisms:** human, mouse, and other well-supported species
> have curated genomes and annotations available via `AnnotationHub`.

### 2. Subset annotation to gene-level ranges

```r
genes <- annotation[annotation$type == "gene"]
```

### 3. Extract promoter genomic coordinates

```r
# Default: 2000 bp upstream of TSS, 200 bp downstream (per gene's most-upstream TSS)
prom_genes <- GenomicRanges::promoters(genes)

# Adjust window size as needed:
# prom_genes <- GenomicRanges::promoters(genes, upstream = 1000, downstream = 0)
```

To get per-transcript promoters instead of per-gene:

```r
tx_ranges  <- annotation[annotation$type == "mRNA"]  # or "transcript"
prom_tx    <- GenomicRanges::promoters(tx_ranges)
```

### 4. (Alternative) Extract promoters from a TxDb object

```r
txdb    <- txdbmaker::makeTxDbFromGRanges(annotation)
prom_tx2 <- GenomicFeatures::promoters(txdb)
```

> `GenomicRanges::promoters()` accepts `GRanges` as input;
> `GenomicFeatures::promoters()` accepts `TxDb` objects.

### 5. Retrieve promoter sequences

```r
prom_seqs <- BSgenome::getSeq(genome, prom_genes)
# prom_seqs is a DNAStringSet with one entry per promoter
```

## Key Functions

- `GenomicRanges::promoters(gr, upstream, downstream)` — compute promoter `GRanges` from gene ranges
- `GenomicFeatures::promoters(txdb, upstream, downstream)` — compute promoter `GRanges` from a `TxDb`
- `BSgenome::getSeq(genome, ranges)` — extract sequences from a genome for given ranges
- `rtracklayer::import()` — read GFF/GTF/BED annotation files into `GRanges`
- `txdbmaker::makeTxDbFromGRanges()` — create a `TxDb` from a `GRanges`

## Notes

- If a gene has multiple TSSs, `GenomicRanges::promoters()` uses the most upstream one.
- For model organisms with `BSgenome` and `TxDb` data packages, those can replace
  the remote FASTA/GFF loading steps.

## Further Reading

- `vignette("GenomicRanges")` — genomic range operations
- `vignette(package = "Biostrings")` — working with biological sequences
