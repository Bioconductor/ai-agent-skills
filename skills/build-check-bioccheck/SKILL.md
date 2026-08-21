---
name: build-check-bioccheck
description: Run and interpret R CMD build, R CMD check, and both BiocCheck entry points against a Bioconductor package, separating real defects from environment gaps and known false positives
version: 1.0.0
category: r-packages
tags: [r-packages, bioconductor, validation, quality-control, bioccheck, submission]
author: bioconductor
---

# build-check-bioccheck

Run the Bioconductor validation toolchain against a package and interpret what comes back.

This is the operational counterpart to the policy chapters: it covers *how to run* the tools,
*in what order*, and *how to read* the output, including the failure modes that look like
package defects but are not.

## Usage

Invoke this skill when you need to know whether a package passes:

- "Run BiocCheck on this package"
- "Does this package pass the Bioconductor checks?"
- "Why is BiocCheck reporting this error?"
- "Check this package before I submit it"

## Prerequisites

- Working directory is (or contains) an R package root with a `DESCRIPTION`
- R matching the target Bioconductor cycle. Never guess the pairing — it changes twice a
  year and <https://bioconductor.org/config.yaml> is authoritative
- `BiocCheck` installed: `BiocManager::install("BiocCheck")`
- For vignette building: `pandoc` for `.Rmd`, a LaTeX distribution for `.Rnw`

## Process

Run in this order. Each step consumes the previous step's artifact.

1. **Build the tarball.**

   ```
   R CMD build <package_dir>
   ```

   Then check the tarball rather than the source directory. Checking the built artifact is
   what the Bioconductor build system does, and it exercises the build step itself —
   `.Rbuildignore` handling and vignette rebuilding — which a directory check does not.

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

   This catches files that must not be tracked in git, and is the only step that reads the
   working tree rather than the tarball.

4. **BiocCheck on the tarball.** Both entry points accept either a directory or a tarball, so
   this is guidance rather than a signature constraint: point it at the *built tarball*, which
   is what the build system checks. Use `new-package = TRUE` only for a first submission:

   ```r
   BiocCheck::BiocCheck("<package>_<version>.tar.gz", `new-package` = TRUE)
   ```

5. **Classify every finding** before reporting (see below). Do not hand back raw tool output.

## Interpreting the results

The gate is **no ERRORs and no WARNINGs** on all of the above; NOTEs should be addressed where
practical, and unresolved ones may be questioned in review. That rule is Bioconductor policy —
see `bioc-pkg-dev` (`knowledge/development/build-check-bioccheck.md`) for its wording and
chapter source. It is repeated here only so this skill is usable on its own.

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

Report the per-step counts from the tools themselves. A wrapper script's exit code is not a
result: `BiocCheck` exits non-zero whenever it reports ERRORs, so a non-zero exit from a
pipeline says nothing beyond "something was reported".

## Examples

**User**: "Run BiocCheck on this package"

**Agent**: (runs the four steps, then reports)

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

Policy background — what each rule means and which guide chapter it comes from — lives in
`bioc-pkg-dev`, which mirrors the official guide. This skill is the execution layer: it states
the pass/fail rule only so far as it needs to act on it, and adds the operational detail that
the guide does not cover.

---

**See also**: [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md), [analyze-r-package](../analyze-r-package/SKILL.md)
