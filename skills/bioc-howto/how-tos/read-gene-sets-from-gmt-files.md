---
name: read-gene-sets-from-gmt-files
description: Read gene sets from GMT files (e.g. MSigDB) into Bioconductor GeneSetCollection objects
---

# Read Gene Sets from GMT Files

GMT (Gene Matrix Transposed) files store gene sets line-by-line with tab-separated
fields (identifier, description, gene IDs). They are the standard format of the
Molecular Signatures Database (MSigDB). Use **GSEABase** or **GSVA** to read them
into Bioconductor `GeneSetCollection` objects.

## Required Packages

```r
BiocManager::install(c("GSEABase", "GSVA"))

library(GSEABase)
library(GSVA)
```

## Steps

### 1. Read a GMT file with GSEABase::getGmt()

```r
# From a local file or URL
url <- "https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2023.2.Hs/c7.immunesigdb.v2023.2.Hs.symbols.gmt"

genesets <- getGmt(url, geneIdType = SymbolIdentifier())
genesets
length(genesets)  # number of gene sets
```

The `geneIdType` argument adds metadata so downstream tools know the identifier type.
Supported types include `SymbolIdentifier()`, `EntrezIdentifier()`, `EnsemblIdentifier()`.

### 2. Convert a GeneSetCollection to a plain list

```r
genesets_list <- geneIds(genesets)
head(lapply(genesets_list, head, 3), 3)
```

### 3. Handle GMT files with duplicated gene set IDs (GSVA::readGMT)

`getGmt()` raises an error on duplicated identifiers. Use `readGMT()` instead,
which auto-deduplicates:

```r
url_dup <- "https://data.broadinstitute.org/gsea-msigdb/msigdb/release/7.5/c2.all.v7.5.symbols.gmt"

# readGMT detects and resolves duplicate identifiers
genesets2 <- readGMT(url_dup)
genesets2

# Change deduplication policy if needed; see ?readGMT for options
```

## Key Functions

- `getGmt(con, geneIdType)` — read GMT into a `GeneSetCollection`; fails on duplicate IDs
- `readGMT(con)` — read GMT with automatic deduplication (from GSVA)
- `geneIds(gsc)` — extract gene identifiers as a named `list`
- `SymbolIdentifier()` / `EntrezIdentifier()` — gene ID type metadata objects

## Notes

- GMT is not a rectangular table, so base R `read.table()` / `read.csv()` cannot
  be used directly.
- The resulting `GeneSetCollection` is accepted by many Bioconductor gene-set
  analysis functions (e.g. `GSVA::gsva()`, `fgsea`).
- The Bioconductor package **msigdb** provides a programmatic API to download
  MSigDB collections directly as `GeneSetCollection` objects without GMT files.

## Further Reading

- `vignette("GSEABase")` — introduction to GSEABase
- `?getGmt` / `?readGMT` — full parameter reference
- [MSigDB](https://www.gsea-msigdb.org/gsea/msigdb) — gene set database
