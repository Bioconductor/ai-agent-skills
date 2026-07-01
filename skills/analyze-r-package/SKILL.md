---
name: analyze-r-package
description: Analyze R/Bioconductor package structure to extract key information about its purpose, exports, and characteristics
version: 1.0.0
category: r-packages
tags: [r-packages, analysis, bioconductor, documentation]
author: bioconductor
---

# analyze-r-package

Analyze an R/Bioconductor package to understand its structure, purpose, and key characteristics.

## Usage

Invoke this skill when you want to understand an R package's architecture:
- "Analyze this R package"
- "Tell me about this package structure"

## Prerequisites

- Working directory is an R package root (contains DESCRIPTION file)
- Package has standard R structure (R/, NAMESPACE, etc.)

## Process

1. **Read Package Metadata**: Analyze `DESCRIPTION` for name, purpose, version, dependencies, and classify its type (Data, Analysis, Infrastructure, Utility) based on `biocViews`.
2. **Identify Exports**: Parse `NAMESPACE` for exported functions and (if present) S4 classes/methods. Categorize exports broadly (Data access, Processing, Visualization, Utility).
3. **Examine Directory Structure**: Note the presence of `data/`, `inst/extdata/`, `vignettes/`, `tests/testthat/`, and `src/`.
4. **Detect Data Access Patterns**: Search `R/` source files for remote data access (ExperimentHub, AnnotationHub, DuckDB, AWS S3, HuggingFace, etc.) vs local data access.
5. **Identify Classes**: List R class definitions (S3, S4, R6, S7) and their properties/slots/fields.
6. **Read README**: Extract high-level purpose and key features.
7. **Analyze Testing**: Check `tests/testthat/` structure, file count, and remote vs local test data.
8. **List Vignettes**: Check `vignettes/` for `.Rmd` files, extracting titles and purposes.

## Output Format

Produce a structured markdown summary:

```markdown
## Package Analysis: [Package Name]

### Classification
- **Type**: [Data/Analysis/Infrastructure/Utility]
- **Purpose**: [1-2 sentence summary]
- **Version**: [version number]

### Key Exports ([count] total)
- **Data Access Functions**: [list]
- **Data Processing Functions**: [list]
- **Utility Functions**: [list]

### Data Access Pattern
- **Type**: [None / Local Only / Remote / Hybrid]
- **Technologies**: [e.g., ExperimentHub, DuckDB]

### Classes
- [ClassName] - [Type: S3/S4/R6/S7] - [description]

### Documentation & Testing
- **Vignettes**: [List with titles]
- **Testing**: [Framework, count, data types]

### Special Characteristics
[List notable patterns that should be documented]

### Dependencies of Note
[List key Bioconductor or specialized packages]
```

## Examples

### Example: Data Package Analysis

**User**: "Analyze this R package"

**Agent**: (Analyzes `parkinsonsMetagenomicData` repository)

```markdown
## Package Analysis: parkinsonsMetagenomicData

### Classification
- **Type**: Data Package
- **Purpose**: Provides uniformly processed gut microbiome data via remote parquet files accessed through DuckDB.
- **Version**: 0.99.0

### Key Exports (18 total)
**Data Access Functions** (5):
- `returnSamples()` - Main high-level data retrieval function
- `loadParquetData()` - Load filtered data from DuckDB connection

**Discovery Functions** (5):
- `parquet_colinfo()` - Inspect column structure
- `biobakery_files()` - List available data types

### Data Access Pattern
- **Type**: Hybrid (Remote primary, Local for testing)
- **Technologies**: DuckDB for remote parquet access, TreeSummarizedExperiment output

### Documentation & Testing
**Vignettes** (4):
1. codebook.Rmd - Data Codebook
2. full-workflow.Rmd - Comprehensive tutorial

**Testing**:
- Framework: testthat (3 files)
- Test data: inst/extdata/ (parquet, TSV, RDS)

### Special Characteristics
- Uses DuckDB for efficient remote parquet file querying without full download
```

## Integration

This analysis output is consumed by `create-package-instructions` and `update-package-instructions`.

---

**See also**: [create-package-instructions](../create-package-instructions/SKILL.md)
