---
name: load-gene-from-gff-gtf
description: Import a gene model from a GFF or GTF file as a TxDb object using Bioconductor
---

# Load a Gene Model from a GFF or GTF File

A **gene model** describes the genomic locations of genes, transcripts, exons, and CDS.
Use `makeTxDbFromGFF()` from the **txdbmaker** package to import a GFF3 or GTF file
as a `TxDb` object, which is the standard Bioconductor representation for gene models.

## Required Packages

```r
BiocManager::install("txdbmaker")

library(txdbmaker)
```

## Steps

### 1. Import a GFF/GTF file as a TxDb

```r
# Replace with a path to your own GFF3 or GTF file
gff_file <- "/path/to/annotation.gff3"   # or .gtf

txdb <- makeTxDbFromGFF(gff_file, format = "gff3")
# Use format = "gtf" for GTF files; "auto" also works for auto-detection
txdb
```

Using the example file bundled with txdbmaker:

```r
gff_file <- system.file("extdata", "GFF3_files", "a.gff3", package = "txdbmaker")
txdb <- makeTxDbFromGFF(gff_file, format = "gff3")
```

### 2. Extract gene model features

```r
# Exons grouped by gene
exonsBy(txdb, by = "gene")

# Transcripts grouped by gene
transcriptsBy(txdb, by = "gene")

# CDS grouped by transcript
cdsBy(txdb, by = "tx")
```

## Key Functions

- `makeTxDbFromGFF(file, format)` — create a `TxDb` from a GFF3 or GTF file
- `exonsBy(txdb, by)` — extract exon coordinates grouped by gene or transcript
- `transcriptsBy(txdb, by)` — extract transcript coordinates grouped by gene
- `cdsBy(txdb, by)` — extract CDS coordinates grouped by transcript or gene

## Notes

- The resulting `TxDb` object can be used with `GenomicFeatures` functions
  (`promoters()`, `exonsBy()`, etc.) and with `summarizeOverlaps()` for RNA-seq
  count table generation.
- For remote URLs, `makeTxDbFromGFF()` accepts HTTP/FTP paths directly.
- For UCSC or Ensembl gene models, consider `makeTxDbFromUCSC()` or
  `makeTxDbFromEnsembl()` as alternatives to file-based import.

## Further Reading

- `?makeTxDbFromGFF` — full parameter reference
- `vignette("GenomicFeatures")` — working with TxDb objects
