---
name: bioc-howto
description: A consolidated index of Bioconductor how-to skills covering genomics, sequencing, and omics data analysis tasks
version: 1.1.0
category: bioconductor-how-tos
author: bioconductor
---

# Bioconductor How-To Skills

This skill indexes a collection of focused, practical how-tos for common Bioconductor tasks.
Each entry links to a dedicated file with full step-by-step instructions, required packages,
example code, and further reading.

The individual how-to files are located in `skills/bioc-howto/how-tos/`.

## Usage

- "How do I compute read coverage from a BAM file in Bioconductor?"
- "Show me the Bioconductor how-to for reading gene sets from a GMT file"

## Prerequisites

- R with `BiocManager`; each how-to lists the packages it needs under "Required Packages"

## Process

1. Match the task to a row in the Index of How-Tos below. If no row fits, say so instead of
   stretching the nearest how-to, and suggest `bioc-pkg-finder` to find suitable packages.
2. Read the linked file and follow its steps. Its code runs on example data from Bioconductor
   data packages (e.g. `pasillaBamSubset`); swap in the user's files and keep the same functions.
3. Install missing packages with `BiocManager::install()`, not `install.packages()`, so their
   versions match the user's Bioconductor release.

## Index of How-Tos

| Skill | Description |
|---|---|
| [compute-read-coverage](how-tos/compute-read-coverage.md) | Compute per-base read coverage from a BAM file using Bioconductor's GenomicAlignments package |
| [compute-sequence-composition-for-genomic-regions](how-tos/compute-sequence-composition-for-genomic-regions.md) | Compute GC content and CpG observed/expected ratio for genomic regions using Bioconductor |
| [extract-promoter-sequences](how-tos/extract-promoter-sequences.md) | Extract promoter DNA sequences for any organism's genes using Bioconductor |
| [get-exon-intron-sequence-for-gene](how-tos/get-exon-intron-sequence-for-gene.md) | Retrieve exon and intron DNA sequences for a specific gene using Bioconductor |
| [load-gene-from-gff-gtf](how-tos/load-gene-from-gff-gtf.md) | Import a gene model from a GFF or GTF file as a TxDb object using Bioconductor |
| [read-big-bam-file-in-chunks](how-tos/read-big-bam-file-in-chunks.md) | Iterate through a large BAM file in memory-efficient chunks using Bioconductor |
| [read-gene-sets-from-gmt-files](how-tos/read-gene-sets-from-gmt-files.md) | Read gene sets from GMT files (e.g. MSigDB) into Bioconductor GeneSetCollection objects |
| [read-mass-spectrometry-data](how-tos/read-mass-spectrometry-data.md) | Load raw mass spectrometry data from mzML files into a Bioconductor Spectra object |
| [read-paired-end-reads-from-bam-file](how-tos/read-paired-end-reads-from-bam-file.md) | Load paired-end reads from a BAM file as GAlignmentPairs or GAlignmentsList using Bioconductor |
| [read-single-end-reads-from-bam-file](how-tos/read-single-end-reads-from-bam-file.md) | Load single-end reads from a BAM file into a GAlignments object using Bioconductor |
| [retrieve-gene-model-from-annotationhub](how-tos/retrieve-gene-model-from-annotationhub.md) | Download a gene model from AnnotationHub as a GRanges or GRangesList object using Bioconductor |
| [use-tidy-principles-for-granges-manipulation](how-tos/use-tidy-principles-for-granges-manipulation.md) | Manipulate GRanges objects using dplyr-style tidy verbs via the tidyomics/plyranges Bioconductor ecosystem |
| [use-tidy-principles-for-rna-seq-analysis](how-tos/use-tidy-principles-for-rna-seq-analysis.md) | Manipulate SummarizedExperiment and SingleCellExperiment RNA-seq objects using tidy dplyr-style verbs via tidyomics |

## Examples

"How do I get promoter sequences for my genes?" matches
[extract-promoter-sequences](how-tos/extract-promoter-sequences.md): follow its steps with the
user's organism and gene IDs in place of the example ones.
