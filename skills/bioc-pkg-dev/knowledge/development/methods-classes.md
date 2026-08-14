# Reusing Common Methods and Classes

Covers: Chapter 5 - Common Bioconductor methods and classes.

## Core principles

- Interoperability is required: packages are generally NOT accepted unless they
  demonstrate interoperability, typically by reusing existing Bioconductor classes
  and methods where appropriate.
- Bioconductor uses the S4 object system for genomic data because it provides
  formal class definitions, multiple inheritance, and validity checking.
- New classes require strong justification and must clearly describe how they
  interoperate with existing Bioconductor infrastructure.
- Before creating new classes, discuss the proposal on the bioc-devel mailing list
  or Bioconductor Slack for community feedback.

## Classes to reuse (by data type)

| Data type | Recommended class / package |
| ----------- | ----------------------------- |
| Count matrices, microarray data | `SummarizedExperiment::SummarizedExperiment()` |
| Genomic coordinates | `GenomicRanges::GRanges()` |
| Multi-sample genomic coordinates | `GenomicRanges::GRangesList()` |
| Variable-length / ragged coordinates | `RaggedExperiment::RaggedExperiment()` |
| DNA/RNA/protein sequences | `Biostrings::*StringSet()` |
| Gene sets / collections | `BiocSet::BiocSet()` or `GSEABase` equivalents |
| Multi-omics integration | `MultiAssayExperiment::MultiAssayExperiment()` |
| Single-cell data | `SingleCellExperiment::SingleCellExperiment()` |
| Mass spectrometry | `Spectra::Spectra()` |

## Import / parsing methods to reuse

Use existing importers instead of writing custom parsers:

- Genomic file formats (BED, GFF, etc.): `rtracklayer`
- VCF: `VariantAnnotation`
- BAM / sequencing alignments: `Rsamtools`, `GenomicAlignments`
- FASTA sequences: `Biostrings`
- Mass spectrometry data: `Spectra`

## When importing Bioconductor classes

- Import the full class package (via `import()`) so that full class functionality
  is inherited automatically (see namespace guidance in metadata-files.md).

Source: [Reusing Bioconductor methods and classes](https://contributions.bioconductor.org/reusebioc.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
