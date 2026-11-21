---
name: build-check-bioccheck
description: Run and interpret R CMD build, R CMD check, and both BiocCheck entry points against a Bioconductor package, separating real defects from environment gaps and known false positives
version: 1.1.1
category: r-packages
tags: [r-packages, bioconductor, validation, quality-control, bioccheck, submission]
author: bioconductor
---

# build-check-bioccheck

Run the Bioconductor validation toolchain against a package and interpret what comes back,
including the failures that look like package defects but are not.

## Usage

- "Run BiocCheck on this package"
- "Does this package pass the Bioconductor checks?"
- "Why is BiocCheck reporting this error?"

## Prerequisites

- Working directory is (or contains) an R package root with a `DESCRIPTION`
- R matching the target Bioconductor cycle. Never guess the pairing — it changes twice a
  year and <https://bioconductor.org/config.yaml> is authoritative
- `BiocCheck` installed: `BiocManager::install("BiocCheck")`
- For vignette building: `pandoc` for `.Rmd`, a LaTeX distribution for `.Rnw`

## Process

Run in this order.

1. **Build the tarball.**

   ```
   R CMD build <package_dir>
   ```

   Then check the tarball, not the source directory: that is what the Bioconductor build system
   does, and it exercises `.Rbuildignore` handling and vignette rebuilding.

2. **Check the tarball.**

   ```
   R CMD check <package>_<version>.tar.gz
   ```

   Add `--no-manual` only if `texi2dvi` is unavailable, and say so in the report rather than
   presenting the run as complete.

3. **BiocCheck on the git clone.** Point it at the *source directory*:

   ```r
   BiocCheck::BiocCheckGitClone("<package_dir>")
   ```

   This catches files that must not be tracked in git; it is the only step that reads the
   working tree and not the tarball.

4. **BiocCheck on the tarball.** Both entry points accept either a directory or a tarball;
   point this one at the *built tarball*, which is what the build system checks. Use `new-package = TRUE` only for a first submission:

   ```r
   BiocCheck::BiocCheck("<package>_<version>.tar.gz", `new-package` = TRUE)
   ```

5. **Save the raw outputs** in one directory under the names other tools read:
   `check_results.txt` (the `R CMD check` log), `bioccheck_results.txt` (the `BiocCheck` console
   output, including its `* Checking ...` lines and the final totals), and, if you measure
   coverage, `coverage.json` and `coverage_summary.txt` written like this:

   ```r
   cov <- covr::package_coverage("<package_dir>", type = "all")
   jsonlite::write_json(covr::coverage_to_list(cov), "coverage.json", auto_unbox = TRUE, pretty = TRUE)
   writeLines(c(paste0("Total Coverage: ", round(covr::percent_coverage(cov), 2), "%"), "",
                capture.output(print(cov))), "coverage_summary.txt")
   ```

   The `bioc-pkg-review` skill reads these files, and Bioconductor's reviewer tool accepts them
   with `--artifacts`.

6. **Classify every finding** before reporting (see below). Do not hand back raw tool output.

## Interpreting the results

The gate is **no ERRORs and no WARNINGs** on all of the above; NOTEs should be addressed where
practical, and unresolved ones may be questioned in review. That rule is Bioconductor policy;
see `bioc-pkg-dev` (`knowledge/development/build-check-bioccheck.md`) for its wording and
chapter source.

Classify each finding into one of four buckets:

**a. Real defect in the package.** Fix it.

**b. Account or environment action, not code.** These are ERRORs the package author cannot fix
by editing files:

- *"The '<pkg>' tag must be added to your 'Watched Tags'"* — a Support Site profile setting at
  <https://support.bioconductor.org/accounts/edit/profile>. Verify with
  `https://support.bioconductor.org/api/watched/tags/<url-encoded-email>`, which returns the
  `watched_tags` list BiocCheck compares against (lowercased).
- *"Cannot determine whether maintainer is subscribed to the Bioc-Devel mailing list"* —
  requires admin credentials; informational.

**c. Missing tooling, reported as a package failure.** A vignette that fails to build because
`pandoc` or a LaTeX package is absent is an environment gap. Report it as such and install the
dependency; do not "fix" the vignette.

**d. Known false positives.** Verify before acting:

- `checkSingleColon` flags every `X:` token whose `X` matches a name in
  `BiocManager::available()`, hunting for `pkg:fun` typo'd from `pkg::fun`. A range expression
  over a local variable whose name collides with a CRAN package — `ROOT:(n + m)`, `c3:c4` —
  is flagged identically. Confirm with `"<name>" %in% BiocManager::available()` before
  changing code.

Two findings are worth calling out explicitly rather than burying in a count:

- *"No Bioconductor dependencies detected"* is the interoperability criterion in mechanical
  form. It is not fixed by packaging work, and a reviewer is likely to raise it.
- A WARNING that conflicts with documented behaviour — for example `set.seed` removal when the
  man page documents a `seed` argument as a reproducibility guarantee — should be disclosed and
  argued in the submission issue, not silently "fixed" by breaking a documented contract.

## Output Format

```markdown
## Validation: [Package] [version]

| Step | Result |
|---|---|
| R CMD build | [tarball produced / FAILED] |
| R CMD check | [Status: OK / n errors, n warnings, n notes] |
| BiocCheckGitClone | [n errors, n warnings] |
| BiocCheck(new-package) | [n errors, n warnings, n notes] |

**Verdict**: [passes the gate / blocked]

### Blocking (ERROR / WARNING)
- [finding] — [bucket a/b/c/d] — [what to do]

### Non-blocking (NOTE)
- [finding] — [what to do, or why it is being left]

### Not a package defect
- [environment gaps, account actions, verified false positives]
```

Report the per-step counts from the tools themselves, not a wrapper script's exit code:
`BiocCheck` exits non-zero whenever it reports ERRORs.

## Examples

A report for a first submission:

```markdown
## Validation: examplePkg 0.99.0

| Step | Result |
|---|---|
| R CMD build | tarball produced |
| R CMD check | Status: OK |
| BiocCheckGitClone | 0 errors, 0 warnings |
| BiocCheck(new-package) | 1 error, 2 warnings, 12 notes |

**Verdict**: blocked

### Blocking
- ERROR: 'examplepkg' tag missing from Watched Tags — bucket b — set it on the Support
  Site profile; no code change required.
- WARNING: Use RMarkdown instead of Sweave 'Rnw' vignettes — bucket a — convert
  `vignettes/intro.Rnw`.

### Not a package defect
- Vignette build failed on missing `tcolorbox.sty`; installed via
  `tinytex::tlmgr_install("tcolorbox")` and re-ran.
```

## Integration

- **Used by**: `bioc-pkg-dev` (as the gate step of the submission workflow)
- **Works with**: `analyze-r-package`, `improve-code-coverage`

---

**See also**: [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md), [analyze-r-package](../analyze-r-package/SKILL.md)
