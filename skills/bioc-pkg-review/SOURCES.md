# Sources for bioc-pkg-review

Read this file when updating the skill, not when running it.

## The rubric

- `knowledge/rubric.md` and `knowledge/rubric.yaml` are generated from the prompt tables of
  Bioconductor/BiocPkgReviewer (a private repository of the review team) with
  `python3 rubric.py --export`. The copy here is the public artifact. The header of `rubric.md`
  carries its hash and export date, so anyone can see how current it is.
- The questions are owned in BiocPkgReviewer. A wrong question is reported on this repository,
  and the review team carries it over.
- The guideline chapters the questions cite are the `bioc-pkg-dev` knowledge base, the same one
  the reviewer's tool reads.

## The checklist

- Published at Bioconductor/pkgrevdocs, `devel`, `docs/package-review-checklist.md`.
  `knowledge/package-review-checklist.md` is the offline fallback copy.
- Proposed additions to the checklist are discussed at Bioconductor/pkgrevdocs. The skill
  follows the published checklist only.

## Relationship to other tools and skills

- BiocPkgReviewer posts the same review to the human reviewer, and its composed feedback to
  submitters points to this skill. Its tool never runs the package's code, which is why this
  review only reads.
- `bioc-pkg-dev` step 8 asks for this review before submitting.
- `build-check-bioccheck` produces the four output files that feed the BLD rows and the
  BiocCheck bullets.
- The data-package patterns in step 3 come from the reviewer's runs, not from the guide, and
  change as reviews accumulate.
