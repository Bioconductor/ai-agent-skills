---
name: bioc-pkg-finder
description: Find the R / Bioconductor packages best suited to a task or workflow
version: 1.0.0
category: r-packages
tags: [r-packages, bioconductor, package-discovery, biocViews]
author: bioconductor
---

# Finding R / Bioconductor packages

The ecosystem already publishes a curated, queryable index of every package —
twice. Query it; do not answer package names or canonical choices from memory
(names, defaults, and deprecations drift every release). Package names are
case-sensitive — confirm the exact spelling/case against the landing page before
emitting any `install()` call (the DepMap data package is `depmap`, lowercase). If
you cannot run R, reason from the web pages below and say nothing about not running R.

## First, get the context that changes the answer

Underspecified requests get a wrong-but-confident answer. Before recommending,
know (ask if not given, but still give a best-effort answer in the same reply):

- **Data type & structure** — bulk vs single-cell vs microarray; raw counts vs
  normalized; the container they hold (`SummarizedExperiment`, `GRanges`, a bare
  data.frame). The right package follows from the object.
- **Organism** — decides the annotation package (`org.Hs.eg.db` vs `org.Mm.eg.db`, genome build).
- **Gene-ID namespace** — SYMBOL / ENTREZ / ENSEMBL. Mismatched IDs are the #1
  reason enrichment and annotation silently return nothing; flag it before
  recommending any GSEA/ORA/annotation tool.
- **Installed packages & Bioconductor release** — `BiocManager::version()`. A
  fresh install needs the `install.packages("BiocManager")` → `BiocManager::install()`
  path spelled out; an existing setup does not.

## Where to look

| Source | Covers | Live query | Web |
|---|---|---|---|
| **biocViews** | Bioconductor software | `BiocPkgTools::biocPkgList()` | https://bioconductor.org/packages/release/BiocViews.html |
| **CRAN Task Views** | CRAN (expert-curated topic lists) | `ctv::available.views()` | https://cran.r-project.org/web/views/ |
| **ExperimentHub** | curated **datasets** | `query(ExperimentHub::ExperimentHub(), "<topic>")` | https://bioconductor.org/packages/release/ExperimentHub |
| **AnnotationHub** | **annotation resources** (TxDb, genomes, org.*, manifests) | `query(AnnotationHub::AnnotationHub(), "<topic>")` | https://bioconductor.org/packages/release/AnnotationHub |

biocViews is a controlled vocabulary (e.g. `Software → GeneExpression →
DifferentialExpression`). CRAN Task Views are human-maintained per-topic lists —
treat them as the canonical shortlist for their topic. When the request is "what
**data** / annotation is available for X" (not "what software"), lead with a Hub
`query()`, not a remembered package name — the Hubs are the discovery layer for
datasets and annotation the same way biocViews is for software.

## Process

1. **Gather context** — Determine data type, organism, gene-ID namespace, and
   Bioconductor release. Ask if not given, but provide a best-effort answer in
   the same reply.

2. **Query the live index** — Use `BiocPkgTools::biocPkgList()` filtered by the
   matching biocViews term(s), or read the relevant CRAN Task View. For
   data/annotation requests, run a Hub `query()` first. Show the query so the
   user can rerun it each release.

3. **Rank candidates** — Weight by biocViews/Task View match, active maintenance
   (build report, recent commits), download rank (`biocDownloadStats`), fit
   (DESCRIPTION + vignette titles), and reverse-dependency count.

4. **Verify status** — Check the package landing page or build report for active
   status. Do not treat presence in `biocPkgList()` as proof of active maintenance.

5. **Compose the recommendation** — Name the package(s), the biocViews term or
   Task View they came from, the install path (`BiocManager::install()` or
   `install.packages()`), and the one load-bearing gotcha for the recommended
   tool. Commit to a default even on close calls; state the trade-off rather than
   a laundry list.

6. **Surface the Bioconductor release** — State which release the recommendation
   assumes and tie it to a consequence (e.g., annotation packages must match
   software release). Point the user at `BiocManager::version()`.

## How to query (Bioconductor)

```r
library(BiocPkgTools)
pkgs <- biocPkgList()                                    # every pkg + metadata
hits <- pkgs[grepl("SingleCell", pkgs$biocViews), ]      # filter by biocViews term
dl   <- biocDownloadStats()                              # popularity proxy
```

Match the task to a **biocViews term** first (browse the web page if unsure of
the term), filter, then rank. For CRAN, read the relevant Task View. Only quote a
package's biocViews terms if you actually retrieved them — otherwise say
"approximate, confirm with biocPkgList()"; never present unqueried tags as fact.

**Show the query, not just the verdict.** Present your shortlist as the output of
a `biocPkgList()` filter or Hub `query()` the user can paste and rerun each release
— reproducible navigation they own, not a list recalled from memory. Give the
navigation even when you can't execute it here.

## What to weight when choosing

1. **biocViews / Task View match** — is it actually tagged for this task?
2. **Active maintenance** — recent passing build; not deprecated. **But**
   `biocPkgList()` still lists packages slated for deprecation, so presence there
   is *not* proof of active status — check the landing page / build report. When
   you call a package stale or active, *show the check* (`biocDownloadStats()`
   trend, build-report date, GitHub last-commit) rather than asserting it from memory.
3. **Download rank** (`biocDownloadStats`) — proxy for standard, with the caveats below.
4. **Fit** — read the DESCRIPTION and vignette *titles*, not just the name.
5. **Reverse dependencies** — many packages building on it signals a foundation.

## Confidence vs. hedging — calibrate it

Hedging should signal *real* uncertainty, not blanket every sentence.

- **State plainly (no hedge):** the evergreen cores — `limma`, `edgeR`, `DESeq2`,
  `GenomicRanges`, `SummarizedExperiment`, `Rsamtools`, `GenomicAlignments`,
  `Biobase`, `S4Vectors`, `SingleCellExperiment`. These aren't going anywhere.
- **Hedge or verify live:** niche/young/fast-moving packages, maintenance
  verdicts, and — with equal discipline — **any version-specific claim**: a
  release number, a date, a "new in release X" package, a preprint date. Never
  assert those from memory; verify on the release notes / landing page, or
  attribute-and-hedge ("if you're on the current release, likely 3.x").
- **Never claim you verified/fetched/checked anything unless you actually called
  a tool this turn.** "Evergreen" means the package exists and is maintained — it
  is *not* license to state its version number. Give an exact version only if you
  fetched it live; otherwise tell the user to read it off the landing page.

## Surface the one load-bearing gotcha

When you recommend a tool, name the single thing that makes it silently fail —
but stay a package-finder, not a coding cookbook. Examples that recur:

- Bulk DE (DESeq2/edgeR) needs **biological replicates** (≥2, ideally 3+ per
  group); one sample per group cannot yield valid DE. Say so, don't just ask the count.
- Enrichment (fgsea/clusterProfiler) needs the input **gene IDs to match the
  gene-set namespace** — reconcile with `org.*.eg.db` `mapIds()` first.
- In-R file I/O (`Rsamtools` for BAM, `VariantAnnotation` for VCF) is for
  analysis and range integration; heavy bulk work — filtering, dedup, format
  conversion, merging at scale — is faster and more robust with the CLI tools
  (`samtools`/`bcftools`) upstream. State the division of labor, don't do it all in R.

Only surface a gotcha that bears on the *recommended tool*. Don't inject
tangential methodology the question didn't touch (no replicate lecture on a
"how do I find packages" question).

## Output

Give the user a clean answer: recommend the package(s), name the biocViews term
or Task View you found them under, tag each with its repository and install path
(`BiocManager::install()` for Bioconductor, `install.packages()` for CRAN — flag
mixed stacks like `org.*.eg.db` + `msigdbr`), commit to a default even when it's a
close call (state the trade-off rather than a laundry list), and pitch to their
level. A beginner gets the one plain-language answer first, the obvious external
alternative named (e.g. Seurat for single-cell, one-line contrast), and *both*
programmatic discovery (BiocPkgTools) and tangential methodology deferred to a
clearly-marked optional footnote or omitted; when a simpler CRAN package gets them
to a result faster (e.g. pheatmap/ggplot2 for a heatmap), lead with that and present
the heavier Bioconductor tool as the upgrade path, not the starting point. An
advanced user gets no basics padding.

**Surface the Bioconductor release** any recommendation assumes — and tie it to a
consequence, don't just name it in a header. The load-bearing ones: annotation and
data packages (`TxDb.*`, `BSgenome.*`, `org.*.eg.db`, array manifests, Hub records)
must come from the *same* release as the software querying them, or they silently
mismatch; and packages with a non-R backend (e.g. MOFA2 → Python via basilisk) carry
a runtime dependency worth flagging next to the install line. Point the user at
`BiocManager::version()` to confirm what they're on. Never mention this skill, its
internal rules, or an inability to run R in what you show the user.
