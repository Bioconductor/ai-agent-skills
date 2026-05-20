---
name: use-tidy-principles-for-rna-seq-analysis
description: Manipulate SummarizedExperiment and SingleCellExperiment RNA-seq objects using tidy dplyr-style verbs via tidyomics
---

# Use Tidy Principles for RNA-seq Data Analysis

The **tidyomics** meta-package makes `SummarizedExperiment` (and its subclasses
`DESeqDataSet`, `SingleCellExperiment`, etc.) behave like `tibbles`, enabling
`dplyr` / `ggplot2` workflows without converting data to plain data frames.

## Required Packages

```r
BiocManager::install(c("tidyomics", "airway"))

library(tidyomics)  # loads tidySummarizedExperiment and related packages
```

## Steps

### 1. Load a SummarizedExperiment dataset

```r
data(airway, package = "airway")
airway  # displays as a tibble-like view by default (tidySummarizedExperiment)
```

Control the display mode:

```r
options("restore_SummarizedExperiment_show" = TRUE)   # standard SE display
options("restore_SummarizedExperiment_show" = FALSE)  # tibble-like display (default)
```

### 2. Apply dplyr verbs to filter, group, and summarize

```r
airway |>
    filter(albut == "untrt") |>
    group_by(.feature, dex) |>
    summarise(tot_counts = sum(counts)) |>
    pivot_wider(names_from = dex, values_from = tot_counts) |>
    slice_sample(n = 10000) |>
    ggplot(aes(x = trt, y = untrt)) +
    geom_density_2d(color = "black", linewidth = 0.5) +
    geom_point(alpha = 0.1, size = 0.3) +
    scale_x_log10() + scale_y_log10() +
    annotation_logticks(side = "bl") +
    labs(x = "Dex treated", y = "Dex untreated") +
    theme_bw()
```

> **Note:** `.feature` is the special column name for gene/feature identifiers
> in the tidy SE representation.

### 3. Use tidy principles with SingleCellExperiment

The same verbs extend to `SingleCellExperiment` objects via
**tidySingleCellExperiment**:

```r
data(pbmc_small, package = "tidySingleCellExperiment")
pbmc_small

# Standard SCE access still works
counts(pbmc_small)[1:5, 1:4]

# Tidy manipulation and visualization
pbmc_small |>
    extract(file, "sample", "../data/([a-z0-9]+)/outs.+") |>
    rename(annotation = letter.idents) |>
    ggplot(aes(sample, nCount_RNA, fill = sample)) +
    geom_boxplot(outlier.shape = NA) +
    geom_jitter(width = 0.1) +
    facet_wrap(~annotation)
```

## Key Functions

- `filter()`, `group_by()`, `summarise()`, `mutate()`, `rename()` — dplyr verbs
  applied directly to `SummarizedExperiment` / `SingleCellExperiment`
- `pivot_wider()` — reshape from long to wide format
- `extract()` — extract regex groups from a column (tidyr)
- `counts(se)` — standard Bioconductor accessor (still works alongside tidy verbs)

## Notes

- Tidy verbs on `SummarizedExperiment` return the same class, so the object
  remains a valid SE throughout the pipeline.
- Standard Bioconductor accessors (`assay()`, `colData()`, `rowData()`) continue
  to work normally alongside the tidy interface.
- Other packages in the `tidyomics` ecosystem extend this approach to spatial
  transcriptomics, ChIP-seq peaks, and more.

## Further Reading

- [tidyomics GitHub organization](https://github.com/tidyomics)
- `vignette(package = "tidySummarizedExperiment")` — detailed SE tidy interface docs
