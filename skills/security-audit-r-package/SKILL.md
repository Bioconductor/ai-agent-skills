---
name: security-audit-r-package
description: Perform comprehensive security audit of R/Bioconductor packages
version: 1.0.1
category: r-packages
tags: [security, bioconductor, quality-control, validation, audit]
author: bioconductor
---

# security-audit-r-package

Audit an R/Bioconductor package for security vulnerabilities, native code safety, code quality problems, and dependency risks, against a shared checklist fetched at run time.

## Usage

- "Run security audit on this R package"
- "Check this package for security vulnerabilities"
- "Security audit only the R/ directory"

## Prerequisites

- Working directory is an R package.
- Internet access to fetch audit instructions from the reference gist.

## Process

1. **Determine Audit Scope**: Default is the entire package (`DESCRIPTION`, `NAMESPACE`, `R/`, `src/`). The user may specify a subset.
2. **Fetch Audit Instructions**: Read the standardized security audit instructions from:
   **https://gist.github.com/lwaldron/0606c678e7d81b012a1b05901cf4b732**
   These instructions define the categories to check, standardized issue type labels, and required fields.
3. **Analyze for Issues**: Review every file in scope against every category in the fetched instructions.
4. **Report**: Display a report in the Output Format below.

## Output Format

```markdown
# Security Audit Report: [Package Name]

**Scope**: [audited files/directories]

## Summary
[Brief summary of findings]

## Findings
### [Issue Title]
**Issue Type**: [Label]
**Severity**: [Level]
**Location**: [file:line]
**Description**: [Details]
**Fix**: [Recommendation]
```

Issue Type is exactly one of the standardized labels from the fetched instructions. Severity is Critical, High, Medium, or Low. If there are no findings, say so explicitly.

## Examples

A single finding:

```markdown
### Unserializing a downloaded file
**Issue Type**: UNSAFE_DESERIALIZATION
**Severity**: High
**Location**: R/cache.R:42 (`loadRemote()`)
**Description**: `readRDS(url(u))` loads an R object from a caller-supplied URL without verifying its source.
**Fix**: Restrict `u` to the package's own host and verify a checksum before reading.
```
