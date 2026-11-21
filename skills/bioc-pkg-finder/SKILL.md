---
name: bioc-pkg-finder
description: Find the R / Bioconductor packages best suited to a task or workflow
version: 1.2.1
category: r-packages
tags: [r-packages, bioconductor, package-discovery, biocViews]
author: bioconductor
---

# Finding R / Bioconductor packages

Bioconductor and CRAN publish curated, queryable indexes of their packages. Query them; do not
answer package names or canonical choices from memory, because names, defaults, and deprecations
drift every release.

## Usage

- "What package should I use for differential expression?"
- "What annotation or data is available for mouse ATAC-seq?"
- "Does an existing Bioconductor package overlap with the one I am submitting?"

## Prerequisites

- Network access to bioconductor.org and cran.r-project.org
- Optional: R with `BiocPkgTools`, `ctv`, `ExperimentHub`, and `AnnotationHub` for live queries.
  Without R, work from the web pages in step 2.

## Process

### 1. Get the context that changes the answer

Ask for whatever is missing from this list, and still give a best-effort answer in the same reply:

- **Data type and structure**: bulk, single-cell, or microarray; raw counts or normalized; the
  container (`SummarizedExperiment`, `GRanges`, a bare data.frame). The right package follows from
  the object.
- **Organism**: decides the annotation package (`org.Hs.eg.db` or `org.Mm.eg.db`, genome build).
- **Gene-ID namespace**: SYMBOL, ENTREZ, or ENSEMBL. Mismatched IDs are the most common reason
  enrichment and annotation silently return nothing; flag this before recommending any GSEA, ORA,
  or annotation tool.
- **Installed packages and Bioconductor release** (`BiocManager::version()`). A fresh install needs
  the `install.packages("BiocManager")` then `BiocManager::install()` path spelled out; an existing
  setup does not.

### 2. Query the live index

| Source | Covers | Live query | Web |
|---|---|---|---|
| **biocViews** | Bioconductor software | `BiocPkgTools::biocPkgList()` | https://bioconductor.org/packages/release/BiocViews.html |
| **CRAN Task Views** | CRAN (expert-curated topic lists) | `ctv::available.views()` | https://cran.r-project.org/web/views/ |
| **ExperimentHub** | curated **datasets** | `query(ExperimentHub::ExperimentHub(), "<topic>")` | https://bioconductor.org/packages/release/ExperimentHub |
| **AnnotationHub** | **annotation resources** (TxDb, genomes, org.*, manifests) | `query(AnnotationHub::AnnotationHub(), "<topic>")` | https://bioconductor.org/packages/release/AnnotationHub |

biocViews is a controlled vocabulary (e.g. `Software → GeneExpression → DifferentialExpression`).
Match the task to a biocViews term first (browse the web page if unsure of the term), then filter:

```r
library(BiocPkgTools)
pkgs <- biocPkgList()                                    # every pkg + metadata
hits <- pkgs[grepl("SingleCell", pkgs$biocViews), ]      # filter by biocViews term
dl   <- biocDownloadStats()                              # popularity proxy
```

For CRAN, read the relevant Task View and treat it as the canonical shortlist for its topic. When
the request is for data or annotation, not software, lead with a Hub `query()`, not a remembered
package name.

Present the shortlist as the output of a `biocPkgList()` filter or Hub `query()` that the user can
paste and rerun each release, even when the query cannot be executed here. Quote a package's
biocViews terms only if they were retrieved; otherwise say "approximate, confirm with
biocPkgList()".

### 3. Rank candidates and verify status

Weight, in this order:

1. **biocViews or Task View match**: is the package tagged for this task?
2. **Active maintenance**: a recent passing build, not deprecated. `biocPkgList()` still lists
   packages slated for deprecation, so presence there is not proof of active status; check the
   landing page or build report. When calling a package stale or active, show the check
   (`biocDownloadStats()` trend, build-report date, GitHub last commit).
3. **Download rank** (`biocDownloadStats()`): a proxy for standard use.
4. **Fit**: read the `DESCRIPTION` and the vignette titles, not only the name.
5. **Reverse dependencies**: many packages building on it signals a foundation.

### 4. Calibrate confidence

- **State without hedging** the evergreen cores: `limma`, `edgeR`, `DESeq2`, `GenomicRanges`,
  `SummarizedExperiment`, `Rsamtools`, `GenomicAlignments`, `Biobase`, `S4Vectors`,
  `SingleCellExperiment`. "Evergreen" means the package exists and is maintained; it does not
  cover its version number.
- **Hedge or verify live**: niche, young, or fast-moving packages; maintenance verdicts; and any
  version-specific claim (a release number, a date, a "new in release X" package, a preprint
  date). Verify these on the release notes or landing page, or attribute and hedge ("if you're on
  the current release, likely 3.x"). Give an exact version only if it was fetched live; otherwise
  tell the user to read it off the landing page.
- Never claim to have verified, fetched, or checked anything that was not actually queried or
  fetched in this turn.

### 5. Compose the recommendation

- **Package(s) and source**: name the biocViews term or Task View each was found under.
- **Install path**: tag each package with its repository (`BiocManager::install()` for
  Bioconductor, `install.packages()` for CRAN) and flag mixed stacks such as `org.*.eg.db` with
  `msigdbr`. Package names are case-sensitive: confirm the exact spelling and case against the
  landing page before writing any `install()` call (the DepMap data package is `depmap`,
  lowercase).
- **A default**: commit to one even on a close call, and state the trade-off in place of a list of
  alternatives.
- **The one gotcha** that makes the recommended tool silently fail. Recurring ones:
  - Bulk DE (`DESeq2`, `edgeR`) needs biological replicates (at least 2, ideally 3 or more per
    group); one sample per group cannot yield valid DE. Say so; do not only ask for the count.
  - Enrichment (`fgsea`, `clusterProfiler`) needs the input gene IDs to match the gene-set
    namespace; reconcile with `mapIds()` on the `org.*.eg.db` package first.
  - In-R file I/O (`Rsamtools` for BAM, `VariantAnnotation` for VCF) is for analysis and range
    integration; filtering, deduplication, format conversion, and merging at scale are faster and
    more robust with `samtools` or `bcftools` upstream. State the division of labor.

  Surface only a gotcha that bears on the recommended tool, with no methodology the question did
  not touch (no replicate lecture on a "how do I find packages" question) and no coding cookbook.
- **The Bioconductor release** the recommendation assumes, tied to a consequence: annotation and
  data packages (`TxDb.*`, `BSgenome.*`, `org.*.eg.db`, array manifests, Hub records) must come
  from the same release as the software querying them, or they silently mismatch. Point the user
  to `BiocManager::version()`. Flag a non-R backend (e.g. `MOFA2` runs Python through `basilisk`)
  as a runtime dependency next to the install line.

Pitch to the user's level. A beginner gets the one plain-language answer first, then the obvious
external alternative with a one-line contrast (e.g. Seurat for single-cell); programmatic
discovery (`BiocPkgTools`) and tangential methodology go in a clearly marked optional footnote or
are omitted. When a simpler CRAN package gets a beginner to a result faster (e.g. `pheatmap` or
`ggplot2` for a heatmap), lead with it and present the heavier Bioconductor tool as the upgrade
path. An advanced user gets no basics.

Never mention this skill, its internal rules, or an inability to run R in what you show the user.

## Checking a submission for overlap

The same index answers a different question when the user is submitting a package: is there an
existing package that does this? Given a package root (or only its `DESCRIPTION`), take the
`biocViews`, the nouns of the `Title` and `Description`, and, when the source is available, the
exported class and function names from `NAMESPACE` and `R/`, and filter `biocPkgList()` (and the
CRAN Task View that fits) by those terms. Report every hit with its maintainer and one line on what it
does, and say plainly "not in the index" for any name that does not resolve. The output is the
overlap statement `bioc-pkg-dev` step 8 asks for: the packages named, and a sentence per package
on how the submission differs or builds on it. Do not soften a near-duplicate; the reviewer's
tool runs the same check against the same index and will name the package anyway.

## Examples

- **User**: "What's a good package for single-cell RNA-seq differential expression?"
  **Agent Action**: Filters `biocPkgList()` on the `SingleCell` and `DifferentialExpression`
  biocViews, checks download stats and build status for the top hits (such as `scran`), and returns
  a default with its install command and the filter the user can rerun.
- **User**: "I need human gene annotations."
  **Agent Action**: Leads with an `AnnotationHub` query, recommends `org.Hs.eg.db`, and asks which
  Bioconductor release the user is on, since the annotation must match it.
