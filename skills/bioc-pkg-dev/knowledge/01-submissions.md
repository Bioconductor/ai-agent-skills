# Covers: Chapter 1 - Bioconductor package submission overview, eligibility, package types, and submission mechanics

## Eligibility

Upstream states this list as "To submit a package to Bioconductor the package **should**" - these
are review criteria, not a mechanical pass/fail gate. Some individual items carry harder modality
than the list stem, and that difference is preserved below.

- Should address areas of high-throughput genomic analysis (sequencing, expression and other
  microarrays, flow cytometry, mass spectrometry, image analysis); see biocViews.
- Should interoperate with other Bioconductor packages by re-using common data structures and
  existing infrastructure (e.g. `rtracklayer::import()` for common genomic file input) rather
  than reinventing them.
- Should adopt software best practices enabling reproducible research: full documentation and
  fully evaluated vignettes, plus commitment to long-term user support on the support site.
- **Cannot** exist on CRAN - "A package can only be submitted to one or the other."
- **Cannot** depend on any package, or version of a package, not yet available on CRAN or
  Bioconductor; it should work with the current publicly available version.
- Should comply with the Package Guidelines.

Note on scope: the genomic-analysis criterion is a "should", and Bioconductor does host accepted
Software packages that perform no genomic analysis themselves (BiocCheck, biocthis, BiocStyle are
developer infrastructure). A tool outside classic genomics is therefore a judgement call for the
reviewers, not an automatic rejection - but the burden is on the submitter to argue the fit, and
this is a good thing to raise in the submission issue rather than discover during review.

## Package types

- Software: algorithms, resource access, analysis, visualization. Most common
  submission type. Goes through the Contributions issue tracker.
- Experiment Data: curated datasets for examples/vignettes. Typically a single
  dataset; for larger files use ExperimentHub. Do NOT open a separate issue -
  add the experiment data package to the SAME issue as its software package.
- Annotation: databases mapping identifiers to information; updated every 6
  months. Prefer AnnotationHub when possible. Do NOT use the tracker - instead
  email <packages@bioconductor.org>.
- Workflow: demonstrate a multi-package bioinformatics workflow. No man/, R/, or
  data/ directories required. Follow the non-software development section.

## Submission mechanics (Software / Experiment Data)

- Host the package in a GitHub repository.
- The package must live on the repository's DEFAULT branch - you cannot specify an
  alternative branch. Upstream: "The default branch must contain only package code.
  Any files or directories for other applications (Github Actions, devtools, etc)
  should be in a different branch." Note the two different strengths in those two
  sentences: do not report a package as non-compliant solely for carrying a CI
  workflow on the default branch.
- Package name should not conflict (case-insensitive) with any current or past
  Bioconductor or CRAN package. The contributor grants Bioconductor rights to
  the package name (CRAN-style naming/ownership policy applies).
- Open a NEW issue on the tracker at github.com/Bioconductor/Contributions with
  the package name as the issue title; link the GitHub repo in the issue and
  follow the tracker README.md guidelines.
- The submitter MUST be listed as the package maintainer in DESCRIPTION
  (maintainer == submitter) - used to verify credentials.
- The Single Package Builder webhook auto-builds the package on submission (and
  on each subsequent push); the build must PASS on all platforms before review
  proceeds.
- Annotation packages: email <packages@bioconductor.org> instead of opening an
  issue on the tracker.

## Maintainer obligations (ongoing)

- Follow Bioconductor guidelines: version numbering, coding style, performance,
  and memory usage standards.
- Maintain the package with git version control.
- Monitor build reports (weekly to daily) and fix breakages promptly.
- Subscribe to the bioc-devel mailing list.
- Register on the support site and monitor the package's "Watched Tags".
- Respond promptly to bug reports and user questions.
- Keep the maintainer email in DESCRIPTION accurate and reachable.
- Bump the "z" (patch) version number on EVERY commit; without a version bump,
  changes will not propagate to the build system.

## Review timeline and response deadlines (hard numbers)

- Full review typically takes 2 to 6 weeks.
- Expect progress (submitter updates or reviewer comments) within 2-3 weeks.
- After roughly 3-4 weeks of inactivity, reviewers MAY close the issue; respond
  within the 2-3 week window to keep it open.
- Changes pushed to the devel branch appear in builds within about 24-48 hours.

## Release cycle and post-acceptance

- Two releases per year (approximately April and October).
- Accepted packages first enter the 'devel' branch.
- Bug fixes allowed in both devel and release branches; NEW features restricted
  to the devel branch only.
- Annotation packages are updated every 6 months.
- On successful build, a landing page is auto-created and the package becomes
  installable via BiocManager::install() (devel users first).

## Getting help

- General maintainer help: <maintainer@bioconductor.org> and the bioc-devel list.
- Topics: S4 class design, implementation guidance, code structure,
  documentation review.

Source: [Bioconductor package submissions](https://contributions.bioconductor.org/bioconductor-package-submissions.html) (and overview: [Submission overview](https://contributions.bioconductor.org/submission-overview.html))
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
