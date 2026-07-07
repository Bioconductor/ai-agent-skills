---
name: create-package-instructions
description: Analyze R/Bioconductor package structure to extract key information about its purpose, exports, and characteristics
tags: [abc]
---

# analyze-r-package

Analyze an R/Bioconductor package to understand its structure, purpose, and key characteristics.

## Prerequisites

- Working directory is an R package root (contains DESCRIPTION file)
- Package has standard R structure (R/, NAMESPACE, etc.)

## Process

1. **Read Package Metadata**: Analyze `DESCRIPTION` for name, purpose, version, dependencies, and classify its type (Data, Analysis, Infrastructure, Utility) based on `biocViews`.

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

## Examples

TODO

---

**See also**: [create-package-instructions](../../create-package-instructions/SKILL.md)
