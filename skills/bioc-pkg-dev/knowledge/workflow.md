# End-to-end submission runbook

The sequential path from local package to first Bioconductor release. The per-chapter files
under this directory are reference; this file is the process. Follow it top to bottom.

## Converting existing work (start here whenever code already exists)

Most submitters are not starting from an empty directory. Two different starting points, and the
first thing to do is work out which one you are at - the advice diverges immediately.

**A package already** (there is a `DESCRIPTION`): skip to the numbered list below. Do not scaffold
from scratch; you would overwrite metadata you already have.

**Scripts, not a package** (no `DESCRIPTION` - analysis code, a bag of `.R` files, a repo of
notebooks): scaffolding is exactly right here, and it comes first. Do this, then join the list at
step 1.

- **Settle the type before writing anything.** A pile of analysis code is often not a Software
  package. If the point is to demonstrate an analysis using existing packages, it is a Workflow
  package and the rules differ - no `man/`, `R/` or `data/` required. See
  [development/non-software-pkgs.md](development/non-software-pkgs.md) and [01-submissions.md](01-submissions.md). Getting this wrong costs the most
  and is the cheapest thing to check.
- **Create the package**, then run the biocthis chain in the Prerequisites section of
  [../SKILL.md](../SKILL.md). This is the case that chain was written for.
- **Turn top-level script code into functions.** Anything that runs at load time is a defect here:
  no `setwd()`, no `rm(list = ls())`, no `install.packages()` or `library()` side effects, no
  hardcoded paths. Paths become arguments. See [development/r-code.md](development/r-code.md).
- **Decide what is exported.** Scripts have no public interface; a package is mostly interface.
  Export the few functions a user calls, keep the rest internal, and document every export with
  roxygen - man pages for exported objects are a gate item.
- **Find the data.** Scripts usually read local files that will not exist on the build machine.
  Small examples go in `inst/extdata`; anything large goes to ExperimentHub/AnnotationHub. See
  [development/data.md](development/data.md).
- **Then the numbered list below**, starting at step 1.

The numbered list is ordered by how expensive the problem is to discover late, not by how hard it
is to fix.

1. **Eligibility and type** - Phase 0 below. Cheapest to answer and the only one that can end the
   effort entirely.
2. **CRAN status** - "Not exist on CRAN. A package can only be submitted to one or the other."
   Moving from CRAN means leaving CRAN, not dual-listing. Note also that the naming policy says a
   name should not conflict with "any current or past CRAN package"; a maintainer migrating their
   own package should raise that in the submission issue rather than assume it is fine.
3. **Name** - see [development/package-name.md](development/package-name.md). Renaming after review has started is painful, and
   the check is a search, not a build.
4. **Version** - reset to `0.99.0` no matter what the package is at today. A package at `2.4.1` on
   GitHub still submits as `0.99.0`. See [maintenance.md](maintenance.md).
5. **Metadata gaps** - `biocViews` (usually missing entirely on a non-Bioc package), `Authors@R`
   with a valid `cre` email, `NEWS.md`, `inst/CITATION`. The `biocthis::use_bioc_*()` chain
   writes these; see the Prerequisites and Notes sections of [../SKILL.md](../SKILL.md). One trap
   for a conversion:
   `use_bioc_description()` replaces DESCRIPTION rather than merging into it, and declines
   silently when it cannot ask - so on an existing package add `biocViews` by hand.
6. **Reuse audit** - does the package define its own container where `SummarizedExperiment`,
   `GRanges`, or another core class would do? This is the single most common substantive review
   request and the most expensive to retrofit. See [development/methods-classes.md](development/methods-classes.md) (ch 5).
7. **Data placement** - anything large moves out of the package to ExperimentHub/AnnotationHub
   before you measure sizes. See [development/data.md](development/data.md).
8. **Documentation** - a real evaluated vignette, not a stub; man pages with runnable examples.
   Existing packages usually have a README doing the vignette's job. See
   [development/documentation.md](development/documentation.md).
9. **Code style** - `<-`, 4-space indent, 80 columns, no `1:n`. Mechanical, so do it last; doing it
   first only creates conflicts with the changes above. Keep it a style pass: it changes how the
   code reads, never what it computes. The two rewrites worth watching are behavior changes at
   exactly the edge cases that motivate them - `1:n` -> `seq_len(n)` differs when `n == 0`, and
   `sapply` -> `vapply` turns a type mismatch `sapply` swallows into an error. Apply them where
   the new behavior is the intended one, leave them where you cannot tell, and run the tests
   before and after so the diff is provably cosmetic.
10. **Run the gate** - Phase 1 below, then Phase 2 onward unchanged.

Steps 1-5 are usually a day. Step 6 is where a conversion either goes smoothly or becomes a
rewrite, so check it early even though it is fixed late.

## Phase 0 - Decide it belongs in Bioconductor

- Package addresses high-throughput genomic / biological data analysis.
- Reuses standard Bioconductor data structures (e.g. SummarizedExperiment, S4) where possible.
  See [development/methods-classes.md](development/methods-classes.md).
- Not already on CRAN; CRAN/Bioc-only dependencies.
- Pick a type: Software, Experiment Data, Annotation, or Workflow. See [01-submissions.md](01-submissions.md).

## Phase 1 - Build to the gate (before you submit)

Author against the development chapters, then clear every item below. Detail:
[development/build-check-bioccheck.md](development/build-check-bioccheck.md), [development/general-dev.md](development/general-dev.md), [development/metadata-files.md](development/metadata-files.md).

Tier 1 - stated as requirements:

- `R CMD check` clean on current R-devel (no errors, no warnings).
- `BiocCheck::BiocCheckGitClone()` clean.
- `BiocCheck::BiocCheck('new-package' = TRUE)` clean (no errors, no warnings). The tracker calls
  passing check and BiocCheck "a minimum requirement for package acceptance", and notes that
  passing "does not result in automatic acceptance" - review still follows.
- Every individual file <= 5 MB (upstream: "must be"), for **software** packages. Experiment data
  and annotation packages follow [development/non-software-pkgs.md](development/non-software-pkgs.md)
  instead.
- `biocViews` field present and valid; a vignette; man pages for exported objects.
- At least 80% of the man pages documenting exported objects have a runnable example - below that
  BiocCheck errors, and a `\dontrun`-only example counts as none. See
  [development/documentation.md](development/documentation.md).
- Valid maintainer email; maintainer == the person who will submit.

Tier 2 - stated as should or recommended. Expected in practice and a reviewer will ask, but a
miss here is not a blocker:

- `Version: 0.99.0` in DESCRIPTION. See [maintenance.md](maintenance.md) (version rule) and metadata-files.
- Source build under 10 MB (`R CMD build`); `R CMD check --no-build-vignettes` under 10 min.
- Running vignettes/examples/tests uses under 8 GB memory.
- Bioc code style in R code: `<-`, 4-space indent, 80-col. See [development/r-code.md](development/r-code.md).

Use the current devel Bioconductor with the matching R version - see [appendices.md](appendices.md) (Appendix A)
and [development/general-dev.md](development/general-dev.md). BiocCheck is the authoritative validator for everything above
except the two timing items, which need a real build; see [../SKILL.md](../SKILL.md).

## Phase 2 - Host on GitHub

- Push the package to the DEFAULT branch of a public GitHub repository (not a subdirectory,
  not a non-default branch).
- Confirm `.gitignore` excludes build artifacts. See [development/gitignore.md](development/gitignore.md).

## Phase 3 - Submit to the tracker

- Open a new issue at <https://github.com/Bioconductor/Contributions/issues/new>
- Issue TITLE = the package name. Body = link to your GitHub repo; confirm you have read the
  guidelines and understand the review process.
- Annotation packages are the exception: email <packages@bioconductor.org> instead.
- Experiment Data that accompanies a software package: add to the same issue; submit the data
  package first if the software depends on it.

## Phase 4 - Single Package Builder (SPB) and review

- A webhook triggers the Single Package Builder; your package must build and check cleanly on
  all platforms. Fix issues, push to GitHub, the build re-runs.
- A reviewer is assigned. Expect 2-6 weeks total. Respond within 2-3 weeks or the issue may be
  closed for inactivity.
- On each change, bump the `z` in the version (0.99.0 -> 0.99.1 -> ...) and push. See
  [maintenance.md](maintenance.md) (version rule) and [reviewer.md](reviewer.md) for what reviewers check.

## Phase 5 - Acceptance and the Bioconductor git server

Once accepted (detail: [maintenance.md](maintenance.md), ch 24):

- Register your SSH public key at the BiocCredentials app
  (<https://git.bioconductor.org/BiocCredentials/>). Bioconductor also reads keys from
  `https://github.com/<your-id>.keys`
- Add the Bioconductor remote and keep GitHub as origin:
  - `git remote add upstream git@git.bioconductor.org:packages/<PKG>.git`
  - `git remote -v` should show origin (GitHub) and upstream (git.bioconductor.org)
- Sync then push to BOTH remotes:
  - `git fetch --all`
  - `git merge upstream/devel` (resolve conflicts if any)
  - `git push upstream devel` (triggers the daily build, ~24h) and `git push origin devel`
- Only `devel` and the current `RELEASE_x_y` branches accept pushes. You cannot create new
  branches on the Bioconductor server. Backport fixes with `git cherry-pick` onto the release
  branch, then push that branch.

## Phase 6 - Release and ongoing maintenance

- Bioconductor releases twice a year (around April and October). At the first release your
  `0.99.z` becomes `1.0.0`. Devel and release version parity: `y` odd in devel, even in release.
- Monitor the daily/weekly build reports and fix breakages promptly. See [maintenance.md](maintenance.md)
  (troubleshooting build report, debugging C/C++).
- Subscribe to the bioc-devel mailing list; create a support.bioconductor.org account and watch
  your package tag; keep the maintainer email in DESCRIPTION current.
- Deprecate/retire APIs per the lifecycle rules (`.Deprecated` -> `.Defunct` -> removed). See
  [maintenance.md](maintenance.md) (deprecation, end-of-life).

Source: [Bioconductor package submissions](https://contributions.bioconductor.org/bioconductor-package-submissions.html),
[Git version control](https://contributions.bioconductor.org/git-version-control.html),
[Version numbering](https://contributions.bioconductor.org/versionnum.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
