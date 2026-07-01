# Package Instruction Templates

This directory contains templates for generating AI instruction documentation for R/Bioconductor packages.

## File Structure

| File | Required | Condition | Purpose |
|------|----------|-----------|---------|
| `00-overview.md.template` | Always | - | Package overview, key functions, data sources |
| `10-data-access.md.template` | Conditional | Type: Remote or Hybrid | Data access patterns and sources |
| `20-development.md.template` | Always | - | Development patterns and coding conventions |
| `30-testing-and-docs.md.template` | Always | - | Testing and documentation guidelines |
| `40-vignettes.md.template` | Conditional | Has vignettes | Vignette guide and reading order |
| `INDEX.md.template` | Always | - | Navigation and quick reference |

## Template Variables

### Common Variables (All Templates)

| Variable | Source | Example | Description |
|----------|--------|---------|-------------|
| `{{PACKAGE_NAME}}` | DESCRIPTION | `curatedMetagenomicData` | Package name |
| `{{VERSION}}` | DESCRIPTION | `3.10.0` | Current version number |
| `{{PACKAGE_TYPE}}` | Analysis | `Data Package` | Package classification |

### 00-overview.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{PURPOSE}}` | DESCRIPTION + README | 2-3 paragraphs explaining package purpose |
| `{{FUNCTIONS_BY_CATEGORY}}` | Analysis (exported functions) | Categorized function lists with descriptions |
| `{{QUICK_START_EXAMPLE}}` | README or vignettes | Simple usage example |
| `{{KEY_CONCEPTS}}` | Domain knowledge | Important domain concepts |
| `{{DATA_SOURCES}}` | Analysis (if applicable) | List of data sources |

### 10-data-access.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{DATA_ACCESS_OVERVIEW}}` | Analysis | How data is accessed in this package |
| `{{HIGH_LEVEL_FUNCTIONS}}` | Analysis | User-facing data retrieval functions |
| `{{LOW_LEVEL_FUNCTIONS}}` | Analysis | Advanced/direct access functions |
| `{{DATA_SOURCES_DETAILED}}` | Analysis | Detailed source information with URLs |
| `{{BASIC_RETRIEVAL_EXAMPLE}}` | README/vignettes | Simple data access example |
| `{{FILTERED_RETRIEVAL_EXAMPLE}}` | README/vignettes | Filtered data access example |
| `{{ADVANCED_QUERIES}}` | Code analysis | Advanced query patterns (if applicable) |
| `{{LARGE_FILE_HANDLING}}` | Analysis | Large file handling strategies |
| `{{PRODUCTION_DATA_ACCESS}}` | Code/docs | How to access full datasets |
| `{{TEST_DATA_LOCATION}}` | File structure | Location of test data (inst/extdata/) |
| `{{TEST_DATA_HANDLING}}` | Code analysis | How tests handle remote vs local data |

### 20-development.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{FUNCTION_ORGANIZATION}}` | R/ directory structure | How R/ files are organized |
| `{{NAMING_CONVENTIONS}}` | Code patterns | Package-specific naming patterns |
| `{{S4_CLASSES}}` | Analysis (setClass calls) | S4 class definitions |
| `{{KEY_DEPENDENCIES}}` | DESCRIPTION Imports | Important dependencies and their usage |
| `{{CODE_STYLE_NOTES}}` | Code analysis | Package-specific style patterns |

### 30-testing-and-docs.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{TEST_ORGANIZATION}}` | tests/testthat/ structure | How tests are organized |
| `{{TEST_DATA_LOCATION}}` | File structure | Test data location |
| `{{TEST_DATA_TYPES}}` | File analysis | Types of test data files |
| `{{TEST_DATA_PURPOSE}}` | Context | What test data represents |
| `{{REMOTE_DATA_TESTING}}` | Code analysis | How remote resources are tested |
| `{{RUNNING_TESTS}}` | Standard commands | Commands and examples for running tests |
| `{{FUNCTION_DOCUMENTATION}}` | Code patterns | How functions are grouped and documented |
| `{{COMMON_PARAMETERS}}` | Code analysis | Shared parameters across functions |
| `{{TESTING_PATTERNS}}` | Code patterns | Package-specific testing patterns |

### 40-vignettes.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{VIGNETTE_LIST}}` | vignettes/ + YAML | List of vignettes with titles and purposes |
| `{{READING_ORDER}}` | Content analysis | Recommended order and rationale |


| Variable | Source | Description |
|----------|--------|-------------|
| `{{PACKAGE_CONSIDERATIONS}}` | Analysis | Special requirements for this package |
| `{{CI_CD_INFO}}` | .github/workflows/ | CI/CD configuration details |

### INDEX.md.template

| Variable | Source | Description |
|----------|--------|-------------|
| `{{CONDITIONAL_DATA_ACCESS}}` | Package type | Empty string or blank for non-data packages |
| `{{CONDITIONAL_VIGNETTES}}` | Vignette count | Empty string or blank if no vignettes |
| `{{REPOSITORY_URL}}` | README or DESCRIPTION | GitHub URL |
| `{{FUNCTIONS_QUICK_REF}}` | Analysis | Quick reference by category |
| `{{EXTERNAL_RESOURCES}}` | README/docs | Links to Bioconductor page, etc. |
| `{{KEY_FUNCTION}}` | Analysis | Primary user-facing function |

## Update Rules

When package analysis detects changes, determine which files need updates:

### Trigger: Version Change
- **Files**: All files
- **Action**: Find and replace version number

### Trigger: New Exported Functions
- **Files**: `00-overview.md`, `INDEX.md`
- **Action**: Add to function lists with placeholder descriptions

### Trigger: Removed Functions
- **Files**: `00-overview.md`, `INDEX.md`, potentially others
- **Action**: Remove from lists, check for references

### Trigger: New Vignettes
- **Files**: `40-vignettes.md` (create if needed), `INDEX.md`
- **Action**: Add vignette entries, update reading order

### Trigger: Data Source Changes
- **Files**: `00-overview.md`, `10-data-access.md`
- **Action**: Update data source listings and examples

### Trigger: New S4 Classes
- **Files**: `20-development.md`
- **Action**: Add class documentation

### Trigger: New Test Files
- **Files**: `30-testing-and-docs.md`
- **Action**: Update test organization section

### Trigger: Dependency Changes
- **Files**: `20-development.md`
- **Action**: Update key dependencies section

### Trigger: Package Type Change
- **Files**: `00-overview.md`, `10-data-access.md` (add/remove), `INDEX.md`
- **Action**: Adjust classification, add/remove data access file

## Variable Substitution Process

1. **Read template file** from `templates/package-instructions/[filename].template`
2. **Extract variables** (all text matching `{{VARIABLE_NAME}}`)
3. **Map to analysis output** using the table above
4. **Perform substitution** replacing `{{VAR}}` with actual values
5. **Handle conditionals**:
   - For `{{CONDITIONAL_X}}`, use empty string if condition false
   - For missing optional variables, use placeholder text: `[To be documented]`
6. **Write to target** `.github/instructions/[filename].md`

## Preservation Strategy (Updates)

When updating existing instructions:

### Preserve
- Domain-specific explanations
- Custom examples using actual package data
- Warning boxes and important notes
- Links to publications or external resources
- Author annotations

### Update
- Version numbers
- Function lists (add/remove)
- File counts and statistics
- Structural metadata
- Cross-references

### Detection Heuristics
- **Custom content**: Multi-sentence paragraphs not in original template
- **Auto-generated**: Lists, version numbers, function names, file counts
- **Preserved sections**: Content between custom HTML comments
- **Conflicts**: When custom content contradicts current analysis

## Usage in Skills

### create-package-instructions
```markdown
1. Run analyze-r-package
2. Determine which templates are needed (check conditionals)
3. For each required template:
   - Read template file
   - Perform variable substitution
   - Write to .github/instructions/
4. Update .Rbuildignore
```

### update-package-instructions
```markdown
1. Run analyze-r-package
2. Read existing instruction files
3. Compare with template structure:
   - Extract variables from existing files
   - Compare with current analysis values
   - Identify differences
4. For each changed variable:
   - Find in existing file
   - Replace with new value
   - Preserve surrounding custom content
5. Verify cross-references
```

## Example Substitution

**Template** (`00-overview.md.template`):
```markdown
# {{PACKAGE_NAME}} Overview

## Classification
- **Type**: {{PACKAGE_TYPE}} Package
- **Version**: {{VERSION}}
```

**Analysis Output**:
```json
{
  "package_name": "curatedMetagenomicData",
  "version": "3.10.0",
  "package_type": "Data"
}
```

**Result** (`00-overview.md`):
```markdown
# curatedMetagenomicData Overview

## Classification
- **Type**: Data Package
- **Version**: 3.10.0
```

## Maintenance

- Templates should be minimal and focus on structure
- Variable names use SCREAMING_SNAKE_CASE
- Preserve references to shared standards (bioconductor-development.md, waldronlab-standards.md)
- When adding new variables, update this README
- Test template changes against multiple package types
