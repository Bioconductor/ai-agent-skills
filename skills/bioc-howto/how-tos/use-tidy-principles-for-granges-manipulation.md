---
name: use-tidy-principles-for-granges-manipulation
description: Manipulate GRanges objects using dplyr-style tidy verbs via the tidyomics/plyranges Bioconductor ecosystem
---

# Use Tidy Principles for Genomic Ranges Manipulation

The **tidyomics** meta-package extends tidy data principles (from the `tidyverse`)
to Bioconductor objects. Using **plyranges**, you can apply `dplyr` verbs
(`filter`, `mutate`, `select`, `arrange`, `group_by`, `summarize`) directly
to `GRanges` objects, and join ranges by overlap.

## Required Packages

```r
BiocManager::install("tidyomics")

library(tidyomics)  # loads plyranges, tidySummarizedExperiment, etc.
library(BiocFileCache)
library(readxl)
```

## Steps

### 1. Load or create a GRanges object

```r
# Example: read a supplementary XLSX with genomic coordinates
library(BiocFileCache)
bfc <- BiocFileCache()
xlsx_url  <- "https://genome.cshlp.org/content/suppl/2020/11/16/gr.265934.120.DC1/Supplemental_Table_S2.xlsx"
xlsx_file <- bfcrpath(bfc, xlsx_url)

library(readxl)
tbl <- read_xlsx(xlsx_file, sheet = "ATAC_metrics", skip = 2)

# Convert tibble to GRanges using tidy evaluation
gr <- tbl |>
    as_granges(seqnames = chrom_ce11, start = start_ce11, end = end_ce11)
```

### 2. Select metadata columns

```r
gr <- gr |>
    select(annot_dev_age_tissues, Annotation, ends_with("_RPM"))
```

### 3. Apply tidy verbs to a GRanges

Most `dplyr` verbs work directly on `GRanges`:

```r
gr |>
    mutate(start = start - 1000, end = end + 1000) |>
    filter(start > 1e6) |>
    arrange(Intest._RPM) |>
    group_by(annot_dev_age_tissues, Annotation) |>
    summarize(n = plyranges::n())
# Note: summarize() returns a DataFrame, not a GRanges
```

### 4. Convert to tibble for ggplot2 visualization

```r
gr |>
    filter(Annotation %in% c("Intest.", "Hypod.", "Soma", "Ubiq.")) |>
    as_tibble() |>
    ggplot(aes(x = `Intest._RPM`, y = `Hypod._RPM`, color = Annotation)) +
    geom_point() +
    facet_grid(Annotation ~ annot_dev_age_tissues) +
    theme_bw()
```

### 5. Join GRanges by overlap (genomic overlap join)

```r
# Define reference regions (e.g. chromosome arms)
arms <- GRanges(
    seqnames = rep(c("chrI", "chrII", "chrIII", "chrIV", "chrV", "chrX"), each = 3),
    ranges   = IRanges(start = c(...), end = c(...)),
    strand   = "*",
    part     = rep(c("arm", "center", "arm"), 6)
)

# Left join: add arm metadata to each range that overlaps an arm
gr |>
    join_overlap_left(arms) |>
    group_by(Annotation, part) |>
    filter(Annotation %in% c("Germline", "Neurons")) |>
    summarize(n = plyranges::n())
```

## Key Functions

- `as_granges(tbl, seqnames, start, end)` — convert a data frame to `GRanges`
- `as_tibble(gr)` — convert `GRanges` to a `tibble` for ggplot2
- `select()`, `filter()`, `mutate()`, `arrange()` — standard dplyr verbs applied to `GRanges`
- `group_by()` + `summarize()` — group-wise aggregation (returns `DataFrame`)
- `join_overlap_left(gr, ref)` — left join by genomic overlap
- `join_overlap_inner()`, `join_nearest()` — other range join types

## Notes

- `summarize()` on a `GRanges` returns a `DataFrame`, not a `GRanges`, because
  there is no single genomic coordinate for the summarized group.
- `plyranges::n()` must be used instead of `dplyr::n()` inside range operations.

## Further Reading

- [tidyomics GitHub organization](https://github.com/tidyomics)
- [Tidy Ranges Tutorial](https://tidyomics.github.io/tidy-ranges-tutorial/)
