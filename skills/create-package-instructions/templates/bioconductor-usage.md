# Understanding and Using Bioconductor Packages

A guide for working with Bioconductor packages in data analysis workflows. This document helps AI agents assist users who are **using** existing packages, not developing new ones.

**For package development**, see [bioconductor-development.md](bioconductor-development.md).

## Overview

This document covers:
- **S4 classes** - How to work with Bioconductor's object-oriented structures
- **Common data structures** - SummarizedExperiment, MultiAssayExperiment, etc.
- **Accessors** - Proper ways to extract and manipulate data
- **Package documentation** - How to find and interpret help
- **ExperimentHub/AnnotationHub** - Accessing curated datasets
- **Parallel computing** - Using BiocParallel in analyses
- **Common patterns** - Design conventions across Bioconductor

**Reference**: [Bioconductor User Documentation](https://bioconductor.org/help/)

## Working with S4 Classes

### What are S4 Classes?

Bioconductor uses **S4 classes** - formal object-oriented structures that:
- Have defined slots (fields) with specific types
- Provide accessor functions for data access
- Validate object integrity
- Support inheritance

### Accessing Data: Use Accessors, Not `@`

**❌ Don't do this**:
```r
# Direct slot access - fragile and discouraged
data <- object@assays
samples <- object@colData
```

**✅ Do this**:
```r
# Use accessor functions
data <- assays(object)
samples <- colData(object)
```

**Why**: Accessor functions:
- Work across package versions
- Handle data transformations automatically
- Provide error checking
- Support future changes without breaking code

### Common Accessor Patterns

Most Bioconductor objects follow consistent naming:

**For SummarizedExperiment-like objects**:
```r
# Extract assay data
assays(se)         # All assays as a list
assay(se)          # First/default assay
counts(se)         # Count matrix (if available)

# Extract metadata
colData(se)        # Sample/column metadata
rowData(se)        # Feature/row metadata
metadata(se)       # Experiment-level metadata

# Extract dimensions
dim(se)
nrow(se), ncol(se)
rownames(se), colnames(se)
```

**For ExpressionSet-like objects**:
```r
exprs(eset)        # Expression matrix
pData(eset)        # Phenotype data
fData(eset)        # Feature data
```

### Finding Accessors

To discover available accessors for an object:

```r
# See object structure
str(object)

# View object
object  # Triggers show() method

# List methods for the class
methods(class = class(object))

# Get help
?ClassName
```

## Common Bioconductor Data Structures

### SummarizedExperiment

The foundational structure for rectangular feature × sample data.

**Structure**:
- **Assays**: Matrices (counts, normalized values, etc.)
- **rowData**: Feature annotations
- **colData**: Sample metadata
- **metadata**: Experiment-level information

**Usage**:
```r
library(SummarizedExperiment)

# Access components
raw_counts <- assay(se, "counts")
normalized <- assay(se, "logcounts")
sample_info <- colData(se)
feature_info <- rowData(se)

# Subset
se_subset <- se[1:100, se$condition == "treatment"]

# Modify
colData(se)$new_variable <- some_values
```

### TreeSummarizedExperiment

Extension of SummarizedExperiment for hierarchical data (e.g., taxonomic trees).

**Additional features**:
- Tree structure linking features
- Tree-aware subsetting

**Usage**:
```r
library(TreeSummarizedExperiment)

# Access tree
tree <- rowTree(tse)

# Access node information
rowLinks(tse)
```

### MultiAssayExperiment

For multi-omics data with samples across multiple assays.

**Structure**:
- Multiple assays (each a SummarizedExperiment or similar)
- Unified sample map linking samples across assays
- Unified colData for subject/sample metadata

**Usage**:
```r
library(MultiAssayExperiment)

# Extract specific assay
rna_data <- mae[["RNAseq"]]
protein_data <- mae[["Proteomics"]]

# Subset by samples
mae_subset <- mae[, mae$disease == "cancer"]

# Complete cases (samples in all assays)
mae_complete <- intersectColumns(mae)
```

### ExpressionSet

Legacy but still widely used for microarray data.

**Usage**:
```r
# Access components
expression_matrix <- exprs(eset)
sample_data <- pData(eset)
feature_data <- fData(eset)
```

## Accessing Curated Data

### ExperimentHub

**Purpose**: Access large-scale experimental datasets.

**Usage**:
```r
library(ExperimentHub)

# Create hub connection
eh <- ExperimentHub()

# Browse available data
query(eh, c("RNA-seq", "Human"))

# Access specific dataset
mydata <- eh[["EH1234"]]

# Cache location
cache(eh)
```

**Benefits**:
- Versioned datasets
- Automatic caching
- Persistent identifiers
- Reproducible access

### AnnotationHub

**Purpose**: Access annotation resources (genomes, gene sets, etc.).

**Usage**:
```r
library(AnnotationHub)

# Create hub connection
ah <- AnnotationHub()

# Search for annotations
query(ah, c("Ensembl", "GRCh38"))

# Access specific resource
genes <- ah[["AH1234"]]
```

## Parallel Computing with BiocParallel

### As a User

Many Bioconductor functions accept a `BPPARAM` argument for parallel processing.

**Basic usage**:
```r
library(BiocParallel)

# Serial processing (default, 1 core)
result <- someFunction(data, BPPARAM = SerialParam())

# Parallel on multiple cores
result <- someFunction(data, BPPARAM = MulticoreParam(workers = 4))

# Snow cluster (Windows-compatible)
result <- someFunction(data, BPPARAM = SnowParam(workers = 4))
```

### Registering a Default Backend

Set a default parallel backend for your session:

```r
# Use 4 cores for all BiocParallel operations
register(MulticoreParam(workers = 4))

# Now functions use parallel by default
result <- someFunction(data)  # Automatically uses 4 cores
```

### Progress Tracking

```r
# Enable progress bar
result <- someFunction(data,
                       BPPARAM = MulticoreParam(workers = 4,
                                                progressbar = TRUE))
```

## Understanding Package Documentation

### Function Documentation

```r
# View function help
?functionName

# See examples
example(functionName)

# Search help
help.search("keyword")
```

### Vignettes

Vignettes provide long-form tutorials and workflows.

**Accessing vignettes**:
```r
# List all vignettes for a package
browseVignettes("PackageName")

# Open specific vignette
vignette("introduction", package = "PackageName")

# See all available vignettes
vignette(package = "PackageName")
```

### Package Overview

```r
# Load package and see startup message
library(PackageName)

# View package help
?`PackageName-package`

# See citation
citation("PackageName")
```

## Common Bioconductor Patterns

### Subsetting

Bioconductor objects support R-like subsetting:

```r
# Subset rows (features)
object[1:10, ]
object[rownames(object) %in% genes_of_interest, ]

# Subset columns (samples)
object[, 1:5]
object[, object$condition == "treatment"]

# Subset both
object[features, samples]
```

### Combining Objects

```r
# Row-wise (add features)
combined <- rbind(object1, object2)

# Column-wise (add samples)
combined <- cbind(object1, object2)
```

### Conversion Between Formats

```r
# SummarizedExperiment to data.frame
df <- as.data.frame(assay(se))

# With metadata
df_full <- cbind(as.data.frame(rowData(se)),
                 as.data.frame(assay(se)))

# ExpressionSet to SummarizedExperiment
library(SummarizedExperiment)
se <- makeSummarizedExperimentFromExpressionSet(eset)
```

## Installation and Management

### Installing Packages

```r
# Install BiocManager (once)
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

# Install Bioconductor packages
BiocManager::install("SummarizedExperiment")
BiocManager::install(c("DESeq2", "edgeR"))

# Check for updates
BiocManager::valid()
```

### Version Information

```r
# Bioconductor version
BiocManager::version()

# Package version
packageVersion("PackageName")

# Session info (all loaded packages)
sessionInfo()
```

## Debugging and Troubleshooting

### Understanding Error Messages

**Common patterns**:

**"object of type 'S4' is not subsettable"**:
- Use accessor functions, not `$` or `[[`
- Example: Use `colData(se)$variable` not `se$variable`

**"the following object is masked from..."**:
- Multiple packages define the same function
- Use explicit namespace: `package::function()`

**"subscript out of bounds"**:
- Index exceeds object dimensions
- Check `dim()`, `nrow()`, `ncol()`

### Getting Object Information

```r
# Object class
class(object)

# Check if specific class
is(object, "SummarizedExperiment")

# See structure
str(object)

# View in console
object  # Calls show() method

# Detailed slot information
slotNames(object)
```

## Best Practices for Analysis

### Workflow Organization

1. **Load packages at the top**:
   ```r
   library(SummarizedExperiment)
   library(DESeq2)
   ```

2. **Set parallel backend once**:
   ```r
   library(BiocParallel)
   register(MulticoreParam(workers = 4))
   ```

3. **Use consistent object names**:
   ```r
   se <- loadData()
   se_filtered <- filterLowCounts(se)
   se_normalized <- normalize(se_filtered)
   ```

### Reproducibility

```r
# Always include session info in reports
sessionInfo()

# Record package versions
packageVersion("PackageName")

# Use set.seed() for random operations (but never in package code)
set.seed(123)
```

### Memory Management

```r
# Large objects - be mindful of memory
object.size(se)

# Remove unneeded objects
rm(large_object)
gc()  # Garbage collection
```

## Finding Help

**Package vignettes**:
```r
browseVignettes("PackageName")
```

**Support site**:
- https://support.bioconductor.org/

**Package landing pages**:
- https://bioconductor.org/packages/PackageName

**Workflows**:
- https://bioconductor.org/packages/release/BiocViews.html#___Workflow

## Verification

### Run BiocCheck

If you are modifying or validating a package, you can run BiocCheck:

```r
# Run BiocCheck on the package
BiocCheck::BiocCheck(".")
```

## External Resources

- [Bioconductor User Documentation](https://bioconductor.org/help/)
- [Common Workflows](https://bioconductor.org/packages/release/BiocViews.html#___Workflow)
- [Support Forum](https://support.bioconductor.org/)
- [Course Materials](https://bioconductor.org/help/course-materials/)

---

**Version**: 1.0.0
**Last Updated**: 2026-04-03
**Purpose**: Guide for using Bioconductor packages in data analysis
**Audience**: Data analysts, researchers, AI agents assisting with data analysis
