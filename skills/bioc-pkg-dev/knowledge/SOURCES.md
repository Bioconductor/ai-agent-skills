# Sources and refresh baseline

This file records where each summary came from and the exact upstream state it was generated
against. Use it to detect drift and to refresh only what changed: compare the live upstream
against the pins below, and re-derive only the knowledge files the changed chapters map to.

## Tracked upstreams (update every pin on every refresh)

Four upstreams, not one. A change to any of them can silently invalidate the guidance here.

| Upstream | Pin | Verified | Invalidates |
| --- | --- | --- | --- |
| [Bioconductor/pkgrevdocs](https://github.com/Bioconductor/pkgrevdocs) (`devel`) | `9b078ea2a0ec05274be83cb12ea75473c6d0c808` (committed 2026-07-20) | 2026-08-14 | all of `knowledge/` |
| [Bioconductor/Contributions](https://github.com/Bioconductor/Contributions) `issue_template.md` | `d2631e3da63092937a96d476c6f7fb915a168069` (committed 2021-07-12) | 2026-08-14 | the pre-submission gate wording in [../SKILL.md](../SKILL.md) |
| [Bioconductor/BiocCheck](https://github.com/Bioconductor/BiocCheck) | release 1.48.1, devel 1.49.30 | 2026-08-14 | what "BiocCheck clean" means |
| [lcolladotor/biocthis](https://github.com/lcolladotor/biocthis) | release 1.22.0, devel 1.23.0 | 2026-08-14 | the scaffolding guidance in [../SKILL.md](../SKILL.md) |

Bioconductor cycle at the last refresh: Bioconductor release 3.23, devel 3.24, both on R 4.6.0
(source: <https://bioconductor.org/config.yaml>). Check that triple against config.yaml before
relying on it - it changes twice a year, and an agent that is not given it will invent one.

Other baseline facts:

- Rendered guide: <https://contributions.bioconductor.org>
- Summaries fetched: 2026-08-14. Every summary now carries that stamp. The earlier 2026-07-23
  pass is still the origin of most of the prose, but the pkgrevdocs pin was re-verified on
  2026-08-14 and no mapped chapter had changed between the two dates, so the later date is the
  one each file can actually back.

Machine-readable endpoints used for drift detection:

- pkgrevdocs commit: `https://api.github.com/repos/Bioconductor/pkgrevdocs/commits/devel`, field `sha`
- changed files since the pin: `https://github.com/Bioconductor/pkgrevdocs/compare/<pinned>...devel`
- chapter order: `https://raw.githubusercontent.com/Bioconductor/pkgrevdocs/devel/_bookdown.yml`
- BiocCheck / biocthis versions: `https://bioconductor.org/packages/release/bioc/VIEWS` and
  `.../devel/bioc/VIEWS` (parse `Package:` / `Version:` pairs - the HTML landing pages are not
  reliably parseable)
- Bioconductor release/devel pair and their R version: `https://bioconductor.org/config.yaml`

## Chapter map: .Rmd source -> rendered slug -> knowledge file

Two columns are needed, not one. The GitHub compare API reports changed **`.Rmd` filenames**,
while every `Source:` footer in `knowledge/` cites a **rendered slug** - and they routinely differ
(`package-maintainence.Rmd` renders to `package-maintenance.html`, note the upstream misspelling;
`bioc-classes-methods.Rmd` renders to `reusebioc.html`). A drift report can only be scoped to the
right files by joining through this table.

Rendered pages live at `https://contributions.bioconductor.org/<slug>.html`. Chapter order and
`.Rmd` names come from `_bookdown.yml`; slugs come from each chapter's `{#id}` anchor.

| .Rmd | Slug | Ch | Knowledge file |
| --- | --- | --- | --- |
| `index.Rmd` | `index` | - | not summarized (welcome page, no rules) |
| `package-submission.Rmd` | `submission-overview` | - | [01-submissions.md](01-submissions.md) |
| `package-submission.Rmd` | `bioconductor-package-submissions` | 1 | [01-submissions.md](01-submissions.md) |
| `devguide-introduction.Rmd` | `develop-overview` | - | not summarized (part overview, no rules) |
| `package-name.Rmd` | `package-name` | 2 | [development/package-name.md](development/package-name.md) |
| `general-package-development.Rmd` | `general` | 3 | [development/general-dev.md](development/general-dev.md) |
| `important-bioc-features.Rmd` | `important-bioconductor-package-development-features` | 4 | [development/general-dev.md](development/general-dev.md) |
| `bioc-classes-methods.Rmd` | `reusebioc` | 5 | [development/methods-classes.md](development/methods-classes.md) |
| `readme-file.Rmd` | `readme` | 6 | [development/metadata-files.md](development/metadata-files.md) |
| `description-file.Rmd` | `description` | 7 | [development/metadata-files.md](development/metadata-files.md) |
| `namespace-file.Rmd` | `namespace` | 8 | [development/metadata-files.md](development/metadata-files.md) |
| `news-file.Rmd` | `news` | 9 | [development/metadata-files.md](development/metadata-files.md) |
| `license-file.Rmd` | `license` | 10 | [development/metadata-files.md](development/metadata-files.md) |
| `citation-file.Rmd` | `citation` | 11 | [development/metadata-files.md](development/metadata-files.md) |
| `install-file.Rmd` | `sysdep` | 12 | [development/metadata-files.md](development/metadata-files.md) |
| `documentation.Rmd` | `docs` | 13 | [development/documentation.md](development/documentation.md) |
| `package-data.Rmd` | `data` | 14 | [development/data.md](development/data.md) |
| `unit-tests.Rmd` | `tests` | 15 | [development/tests.md](development/tests.md) |
| `r-code.Rmd` | `r-code` | 16 | [development/r-code.md](development/r-code.md) |
| `fortran-C-python.Rmd` | `other-than-Rcode` | 17 | [development/compiled-thirdparty.md](development/compiled-thirdparty.md) |
| `shiny-apps.Rmd` | `shiny` | 18 | [development/shiny.md](development/shiny.md) |
| `ai-policy-third-party.Rmd` | `ai-policy-third-party` | 19 | [development/ai-policy.md](development/ai-policy.md) |
| `non-software-packages.Rmd` | `non-software` | 20 | [development/non-software-pkgs.md](development/non-software-pkgs.md) |
| `gitignore-file.Rmd` | `gitignore` | 21 | [development/gitignore.md](development/gitignore.md) |
| `build-check-bioccheck.Rmd` | `build-check-bioccheck` | 22 | [development/build-check-bioccheck.md](development/build-check-bioccheck.md) |
| `devguide-conclusion.Rmd` | `conclusion` | 23 | [development/build-check-bioccheck.md](development/build-check-bioccheck.md) |
| `package-maintainence.Rmd` | `package-maintenance` | - | not summarized (part overview, no rules) |
| `git-version-control.Rmd` | `git-version-control` | 24 | [maintenance.md](maintenance.md) |
| `version-numbering.Rmd` | `versionnum` | 25 | [maintenance.md](maintenance.md) |
| `troubleshoot-build-report.Rmd` | `troubleshooting-build-report` | 26 | [maintenance.md](maintenance.md) |
| `debugging-c-code.Rmd` | `debugging-cc-code` | 27 | [maintenance.md](maintenance.md) |
| `deprecation.Rmd` | `deprecation` | 28 | [maintenance.md](maintenance.md) |
| `package-end-of-life.Rmd` | `package-end-of-life-policy` | 29 | [maintenance.md](maintenance.md) |
| `branch-rename-faq.Rmd` | `branch-rename-faqs` | 30 | [maintenance.md](maintenance.md) |
| `review-overview.Rmd` | `reviewer-resources-overview` | - | [reviewer.md](reviewer.md) |
| `review-expectations.Rmd` | `review-expectation` | 31 | [reviewer.md](reviewer.md) |
| `review-resources-and-tools.Rmd` | `reviewtools` | 32 | [reviewer.md](reviewer.md) |
| `volunteer-to-review.Rmd` | `review-volunteer-chapter` | 33 | [reviewer.md](reviewer.md) |
| `appendix.Rmd` | - | - | no page (part marker only) |
| `devel-branch.Rmd` | `use-devel` | A | [appendices.md](appendices.md) |
| `advanced-build-options.Rmd` | `advanced-build-options` | B | [appendices.md](appendices.md) |
| `web-query.Rmd` | `querying-web-resources` | C | [appendices.md](appendices.md) |
| `c-and-fortran.Rmd` | `c-fortran` | D | [appendices.md](appendices.md) |
| `mavericks.Rmd` | `cmavericks-best-practices` | E | [appendices.md](appendices.md) |
| `debug-rd-links.Rmd` | `man-links` | F | [appendices.md](appendices.md) |
| `news-for-bookdown.Rmd` | `booknews` | G | [appendices.md](appendices.md) |
| `references.Rmd` | `references-1` | H | [appendices.md](appendices.md) |

Three slugs are deliberately marked "not summarized": `index`, `develop-overview` and
`package-maintenance` are welcome or part-overview pages whose entire body is a sentence or two of
orientation. They carry no rules to summarize. They are listed anyway so that a chapter-coverage
check can tell "we decided not to summarize this" apart from "we missed a chapter".

## Not chapter-derived (maintain by hand)

[index.md](index.md) (router), [workflow.md](workflow.md) (runbook), and this file.
