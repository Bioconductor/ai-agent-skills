# Waldronlab R Package Standards

Lab-specific conventions and patterns for R packages developed in waldronlab at CUNY SPH. These complement the core [Bioconductor standards](bioconductor-development.md).

**For package-specific patterns, see the package's `.github/instructions/` directory.**

## Git Workflow

### Branch Naming

Use descriptive, kebab-case branch names that indicate the type of work:

**Feature branches**:
- `feature/description` - New functionality
- `enhance/description` - Improvements to existing features

**Fix branches**:
- `fix/description` or `bugfix/description` - Bug fixes

**Documentation branches**:
- `docs/description` - Documentation updates only

**Examples**:
- `feature/add-diversity-metrics`
- `fix/uuid-validation`
- `enhance/vignettes`
- `docs/update-readme`

### Commit Messages

Use **conventional commit** style for clear, semantic commit history:

```
type: brief description

Optional detailed explanation of the changes.
Can span multiple lines.

Co-Authored-By: [AI Agent Name and Version] <noreply@[provider].com>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding or updating tests
- `refactor`: Code refactoring without functional changes
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `style`: Code style/formatting changes

**Examples**:
```
feat: add Shannon diversity calculation

- Implement shannon_diversity() function
- Add tests for edge cases
- Document in diversity vignette

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

```
fix: correct UUID validation for v4 format

UUID validation was rejecting valid v4 UUIDs due to regex pattern.
Updated pattern to match RFC 4122 specification.

Fixes #42

Co-Authored-By: GitHub Copilot <noreply@github.com>
```

### AI Agent Acknowledgements

**Always include a `Co-Authored-By` line** when AI agents contribute to code changes. This provides transparency and helps track AI involvement.

**Format for common agents**:
- **Claude Code**: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
- **GitHub Copilot**: `Co-Authored-By: GitHub Copilot <noreply@github.com>`
- **Cursor**: `Co-Authored-By: Cursor AI <noreply@cursor.sh>`
- **Other agents**: Use agent name, version if known, and appropriate noreply email

**When to include**:
- AI wrote or suggested substantial code changes
- AI helped debug or refactor code
- AI generated documentation or tests

**When to omit**:
- Minor autocomplete suggestions
- Simple formatting changes
- You significantly rewrote AI suggestions

## Pull Request Guidelines

### PR Title and Description

**Title**: Use the same conventional commit format
```
feat: add diversity metrics module
```

**Description template**:
```markdown
## Changes
- Brief description of what changed
- Key implementation details

## Testing
- How this was tested
- Any manual testing performed

## Related Issues
Fixes #123
Related to #456

## Checklist
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] R CMD check passes
- [ ] BiocCheck passes (if Bioconductor package)
```

### Before Opening PR

✅ All pre-commit checks pass (see [Bioconductor standards](bioconductor-development.md))
✅ Tests added for new functionality
✅ Documentation updated
✅ Vignettes still build (if applicable)
✅ Code follows package style

### Review Process

- PRs require at least one approval from package maintainer
- Address review comments before merging
- Use "Squash and merge" for cleaner history (when appropriate)

## Code Organization Patterns

### File Naming in R/

Organize R source files logically:

**By feature/module**:
- `data-access.R` - Data retrieval functions
- `data-processing.R` - Data transformation functions
- `validation.R` - Input validation helpers
- `plotting.R` - Visualization functions

**By class** (for packages with S4 classes):
- `ClassName-class.R` - Class definition
- `ClassName-methods.R` - Methods for the class
- `ClassName-accessors.R` - Getter/setter functions

**Special files**:
- `zzz.R` - Package startup/load hooks (`.onLoad`, `.onAttach`)
- `package.R` - Package-level documentation

### Function Organization Within Files

```r
# Public/exported functions first
#' @export
public_function <- function() {
  # ...
}

# Internal helpers after (with @noRd)
#' @noRd
.internal_helper <- function() {
  # ...
}
```

## Documentation Practices

### Package-Level Documentation

Create `R/package.R`:
```r
#' @keywords internal
#' @import methods
"_PACKAGE"
```

### Function Documentation Best Practices

**Good parameter documentation**:
```r
#' @param data A SummarizedExperiment object containing microbiome data.
#'   Assay must include count data, and colData should include sample metadata.
```

**Good return documentation**:
```r
#' @return A numeric vector of Shannon diversity values, one per sample.
#'   Names correspond to column names in the input object.
```

**Good examples**:
```r
#' @examples
#' # Basic usage with example data
#' data(example_se)
#' diversity <- calculate_shannon(example_se)
#'
#' # With custom parameters
#' diversity <- calculate_shannon(example_se, base = 2)
#'
#' \donttest{
#' # Example using remote data (requires network)
#' remote_data <- fetch_study_data("PRJEB1234")
#' diversity <- calculate_shannon(remote_data)
#' }
```

### Vignette Best Practices

**Naming**: Use descriptive, ordered names when there's a learning progression:
- `01-quick-start.Rmd`
- `02-data-access.Rmd`
- `03-advanced-analysis.Rmd`

**Content structure**:
1. **Introduction** - What this vignette covers
2. **Prerequisites** - Required packages, data
3. **Step-by-step examples** - With explanation
4. **Summary** - Key takeaways
5. **Session info** - For reproducibility

**Style**:
- Use `BiocStyle::html_document` for Bioconductor packages
- Include a table of contents
- Use informative section headers
- Provide context for code chunks

## Testing Practices

### Test File Organization

Match test files to source files:
```
R/data-access.R → tests/testthat/test-data-access.R
R/validation.R → tests/testthat/test-validation.R
```

### Test Structure

```r
test_that("function_name handles valid input correctly", {
  # Arrange
  input <- create_test_data()

  # Act
  result <- function_name(input)

  # Assert
  expect_true(is.numeric(result))
  expect_length(result, 10)
})

test_that("function_name handles invalid input gracefully", {
  expect_error(function_name(NULL), "input cannot be NULL")
  expect_error(function_name("invalid"), class = "invalid_input_class")
})
```

### Test Data Strategy

**Small local files**: Place in `inst/extdata/` or `tests/testthat/fixtures/`
- Use for regular unit tests
- Keep files small (<100 KB when possible)
- Include minimal representative data

**Remote data**: Use only when necessary
- Add skip conditions for offline testing
- Provide local alternatives

```r
test_that("remote data access works", {
  skip_if_offline()
  skip_on_cran()

  data <- fetch_remote_data()
  expect_s4_class(data, "SummarizedExperiment")
})
```

## Domain-Specific Patterns

### Microbiome Data Packages

**Preferred return types**:
- `TreeSummarizedExperiment` for taxonomic data with hierarchy
- `SummarizedExperiment` for flat feature tables
- `MultiAssayExperiment` for multi-omics data

**Data organization**:
- **Assays**: Count matrices, normalized values
- **rowData**: Feature annotations (taxonomy, functional annotations)
- **colData**: Sample metadata
- **metadata**: Study-level information

### Data Access Patterns

**Consistent function naming**:
- `get_*()` - Retrieve specific datasets
- `load_*()` - Load and cache data
- `fetch_*()` - Fetch remote data with caching
- `query_*()` - Filtered/queried access

**Filtering parameters**:
Use consistent parameter names across functions:
- `study_id` - Study identifier
- `sample_type` - Sample type filter
- `body_site` - Body site filter
- `data_type` - Data type (taxonomic, functional, QC)

## Version Control Best Practices

### What to Commit
✅ Source code (R/, src/)
✅ Documentation (man/, vignettes/)
✅ Tests (tests/)
✅ Package metadata (DESCRIPTION, NAMESPACE)
✅ Instructions (.github/instructions/)
✅ Configuration (.Rbuildignore, .gitignore)

### What NOT to Commit
❌ Generated files (man/*.Rd if auto-generated, *.tar.gz)
❌ User-specific files (.Rproj.user/, .Rhistory)
❌ Large data files (use external hosting)
❌ Sensitive credentials or API keys
❌ Build artifacts (*.o, *.so, *.dll)

### .gitignore Template

```
# R user files
.Rproj.user/
.Rhistory
.RData
.Ruserdata

# Build artifacts
*.tar.gz
*.o
*.so
*.dll

# IDE
.vscode/
.idea/
*.Rproj

# OS
.DS_Store
Thumbs.db
```

### .Rbuildignore Template

```
^\.github$
^\.git$
^\.Rproj\.user$
^.*\.Rproj$
^LICENSE\.md$
^README\.Rmd$
^CODE_OF_CONDUCT\.md$
^CONTRIBUTING\.md$
^\.pre-commit-config\.yaml$
```

## Release Process

### Pre-Release Checklist

1. **Version bump** in DESCRIPTION
2. **Update NEWS.md** with changes since last release
3. **Run full checks**:
   ```r
   devtools::check()
   BiocCheck::BiocCheck()
   ```
4. **Build and test vignettes**
5. **Update documentation**
6. **Tag release** in git:
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

### Bioconductor Release Cycle

- Bioconductor releases twice yearly (April and October)
- Feature freeze 2 weeks before release
- During freeze: bug fixes only, no new features
- Coordinate with Bioconductor core team for submission timing

## Communication and Collaboration

### Code Review Focus Areas

When reviewing PRs, pay attention to:
- Correctness and test coverage
- Documentation completeness
- Performance for large datasets
- API consistency with existing functions
- Error message clarity

### Issue Management

**Good issue titles**:
- ✅ `Bug: Incorrect diversity calculation for empty samples`
- ✅ `Feature request: Add Simpson index calculation`
- ❌ `It doesn't work`
- ❌ `Question`

**Issue labels**:
- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Docs updates
- `good-first-issue` - Good for newcomers
- `help-wanted` - Extra attention needed

## External Resources

- [Waldronlab GitHub](https://github.com/waldronlab)
- [Bioconductor standards](bioconductor-development.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Version**: 1.0.0
**Last Updated**: 2026-04-03
**Maintainers**: waldronlab
**Purpose**: Lab-specific conventions complementing core Bioconductor standards
