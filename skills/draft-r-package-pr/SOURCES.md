# Sources for draft-r-package-pr

Read this file when updating the skill, not when running it. Sources were read on 2026-11-20;
re-check the pins before changing the guidance they support.

## Upstream documents

- **Bioconductor contributions guide**, [Bioconductor/pkgrevdocs](https://github.com/Bioconductor/pkgrevdocs)
  `devel` at `b453cb4` (2026-11-18):
  - [AI policy and third-party code](https://contributions.bioconductor.org/ai-policy-third-party.html):
    disclosure in the PR description (step 6).
  - [Git version control](https://contributions.bioconductor.org/git-version-control.html):
    "Checks and version bumps" and "Pull requests on GitHub" (step 5).
  - [Version numbering](https://contributions.bioconductor.org/versionnum.html): the `x.y.z` scheme
    (step 5).
  - [The NEWS file](https://contributions.bioconductor.org/news.html): locations and the
    list-element requirement (step 4).
  - [R code](https://contributions.bioconductor.org/r-code.html): "Indentation" (4 spaces, no
    tabs, 80-character lines), used as the fallback style for new code (step 2).
- **Tidyteam code review principles** (Posit), [tidyverse/code-review](https://github.com/tidyverse/code-review)
  at `7ce6c9e` (2023-06-05):
  - [Submitting a PR](https://code-review.tidyverse.org/author/submitting.html): titles,
    descriptions, `Fixes #N`, reading order, drafts, self-review. Most of this was general
    practice and is no longer in the skill; what remains is in steps 6 and 7.
  - [Focused PRs](https://code-review.tidyverse.org/author/focused.html): scope, size,
    refactoring, tests (steps 2 and 3).
- **usethis tidyverse contributing template** (Posit), [r-lib/usethis](https://github.com/r-lib/usethis)
  `inst/templates/tidy-contributing.md` at `772fad9` (2026-10-27): issue before a large change,
  `R CMD check`, NEWS for user-facing changes, editing roxygen sources, and restyling only touched code
  (steps 2 to 4). The [Pull request helpers](https://usethis.r-lib.org/articles/pr-functions.html) article
  covers the `pr_*()` workflow.
- **Tidyverse style guide, News** (Posit), [tidyverse/style](https://github.com/tidyverse/style)
  `news.qmd` at `2aed77e` (2025-10-17), rendered at <https://style.tidyverse.org/news.html>: bullet
  placement, wording, and crediting contributors (step 4).

## Conventions this skill sets

These are not upstream text. The Bioconductor contributions guide says little about PRs: it
requires disclosure of AI-generated or copied code and sets rules for pushing to
`git.bioconductor.org`.

- **Version bumps.** Advised against in PRs (step 5). This reads Bioconductor's per-push rule as
  the maintainer's job at push time, and deliberately departs from projects that require a bump in
  every PR.
- **Whitespace.** Whitespace-only changes are excluded from PRs, and new code matches the file's
  existing indentation (step 2). Bioconductor's indentation rules are the fallback, and the usethis
  template's "don't restyle code that has nothing to do with your PR" is the closest upstream text.
- **NEWS entries.** Welcome but optional (step 4). The usethis template asks for one for every
  user-facing change; this skill does not hold a PR for a missing entry.
- **Conventional-commit prefixes.** Used only when the repository already uses them; none of the
  sources requires them.
- **General PR practice is left out.** Title, description, and issue-linking guidance from the
  tidyteam principles was removed in v1.1.0 under AGENTS.md § Only What an Agent Wouldn't Do
  Unprompted; what remains in the skill is specific to R and Bioconductor packages.
