---
name: security-audit-r-package
description: Perform comprehensive security audit of R/Bioconductor packages
version: 1.0.0
category: r-packages
tags: [security, bioconductor, quality-control, validation, audit]
author: bioconductor
---

# security-audit-r-package

Perform comprehensive security audits of R/Bioconductor packages, identifying vulnerabilities, native code security issues, code quality problems, and dependency risks.

## Usage

Invoke this skill to audit an R package:
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
3. **Read Files**: Read all files within the defined scope.
4. **Analyze for Issues**: Review the code against the checklist defined in the gist. Address vulnerabilities, native code safety, code quality, and dependency risks.
5. **Generate Report**: Produce a structured markdown report including findings with the required fields (Issue Type Label, Severity, Location, Description, Fix).
6. **Output Report**: Display the report and confirm completion.

## Output Format

Generate a security report tailored to the context (full package vs quick check). All reports must include:
- Standardized labels from the gist.
- Severity levels (Critical, High, Medium, Low).
- Clear indications if no issues are found.

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

## Examples

### Example: Full Package Audit
**User**: "Run security audit on this R package"
**Agent**:
1. Confirms scope: `DESCRIPTION`, `NAMESPACE`, `R/`, `src/`
2. Fetches gist instructions and reads files.
3. Analyzes for vulnerabilities and generates report.
**Output**: A detailed report listing any High/Medium/Low issues, or a Clean status if no issues are found.

---

**Reference**: Security audit criteria defined at https://gist.github.com/lwaldron/0606c678e7d81b012a1b05901cf4b732
