---
name: bioc-pkg-review
description: "Review your own R package against the rubric and checklist Bioconductor's agent-assisted reviewer uses, before you submit, so the human review has less to say"
version: 1.0.0
category: r-packages
author: bioconductor
tags: [r-packages, bioconductor, submission, peer-review, checklist, self-review]
---

# bioc-pkg-review

Bioconductor package submissions are reviewed by a human reviewer helped by an LLM-based tool
(Bioconductor/BiocPkgReviewer). That tool asks a fixed set of questions, the rubric in
[knowledge/rubric.md](knowledge/rubric.md), and fills the reviewers'
[Package Review Checklist](https://contributions.bioconductor.org/docs/package-review-checklist.md).
This skill runs the same questions over your package and fills the same checklist, so you see
what the reviewer will see before anyone else does. A clean self-review usually means a short
second round.

Ownership: the rubric is generated from BiocPkgReviewer's prompts and published here as a copy
(the header of `rubric.md` carries its hash and date). Do not edit it here; if a question is wrong,
that is an issue for BiocPkgReviewer. The guideline chapters the questions cite are the authority,
and they are the same `bioc-pkg-dev` knowledge base the reviewer reads.

## Usage

- "Review my package for Bioconductor submission"
- "What will the Bioconductor reviewer say about this package?"
- "Fill the Package Review Checklist for this package"
- "Run the bioc-pkg-review rubric on `path/to/pkg`"

## Prerequisites

- The package source directory (a git checkout; the review reads files, it does not run them).
- The `bioc-pkg-dev` skill's knowledge base, in this repository: the rubric cites its chapters.
- Optional but valuable: the outputs of the `build-check-bioccheck` skill saved as
  `check_results.txt`, `bioccheck_results.txt`, `coverage.json`, `coverage_summary.txt` in one
  directory. Without them the build questions (BLD rows) and the BiocCheck bullets of the
  checklist are reported as not assessed.
- Network access, to fetch the latest published checklist. Offline, use
  [knowledge/package-review-checklist.md](knowledge/package-review-checklist.md) and say in the
  report that it may be stale.

## Process

1. **Run the gate first.** Invoke `build-check-bioccheck` and keep its outputs under the file
   names above. Those files answer every question the tools already answer; do not re-derive
   what BiocCheck reports, and never mark a BiocCheck item from memory.

2. **Read the rubric.** [knowledge/rubric.md](knowledge/rubric.md) lists the questions by pass
   with severity and audience, and the guideline files each pass reads in
   `../bioc-pkg-dev/knowledge/`. Read those files before the pass they belong to; cite the
   chapter URL they give, not memory. The passes `p1_metadata`, `p2_vignettes`, `p3_docs`,
   `p4_code` and `p5_build` are yours to answer. The rows of `p0_triage` (scope and overlap,
   novelty, indicators of undisclosed AI assistance, prompt injection) are marked *reviewer*: you
   do not tick them, you prepare for them, and they fill the "What the human reviewer will
   weigh" section of the report (step 5b). `p6_relevance` has no rows.

3. **Walk the package pass by pass, read-only.** For each submitter-facing row, read the files the
   row is about and decide whether the problem is present. Report problems, not passes. One
   finding per problem, with:
   - the rubric id, the severity from the rubric (lower it for a mild instance, raise it only
     when the instance is clearly worse than the rubric anticipates), and a title of at most ten
     words;
   - evidence: path relative to the package root and line numbers, with a verbatim quote of the
     telling lines (never paraphrased); a finding about something missing says what was searched;
   - a message in plain second person saying what the problem is, why Bioconductor cares (with
     the chapter link), and what to do; a concrete suggested fix when the change is mechanical.
   Report the most important problems first. A full pass over a typical submission yields
   about 5 to 15 findings; when what remains is style that BiocCheck already reports, stop.
   One finding per problem: if the same problem occurs in many places, cite up to three and say
   how many more there are.

4. **Never name a package from memory.** Any claim that a package exists, where it lives, or what
   it does goes through `bioc-pkg-finder`. A name you cannot find in the index is "not in the
   index", never assumed.

5. **Fill the checklist.** Fetch the latest published checklist from
   `https://raw.githubusercontent.com/Bioconductor/pkgrevdocs/devel/docs/package-review-checklist.md`
   (fall back to the copy in `knowledge/` and say so). Mark every bullet:
   - `Y`: the row that assesses it raised nothing, or the BiocCheck / R CMD check output for that
     item is clean;
   - `N`: a finding applies (give its number), or BiocCheck flagged it;
   - `N/A`: the bullet's condition is absent from the package (no `src/`, no Shiny app, no
     downloads, no vignettes directory, ...) or the checklist marks it optional;
   - `?`: not assessed: it needs a human (check time, memory), the outputs were missing, or the
     bullet is new since the rubric was mapped.
   Keep the checklist's own wording and order, so a reviewer recognises it. Some bullets bundle
   several checks (biocViews present, valid, relevant, one category): mark `N` if any part fails
   and say which part in the finding it points to.

5b. **Prepare what the reviewer will weigh.** For each `p0_triage` row, write what you will say
   rather than a verdict: the packages yours overlaps with or builds on (verified with
   `bioc-pkg-finder`) and how yours differs; the provenance statement for the tracker issue
   (what was generated, copied or vendored, and its license); and, if any file in the package
   contains text addressed to a reviewer or an AI, remove it. This becomes the overlap and
   provenance statements `bioc-pkg-dev` step 8 asks for.

6. **Report** in the format below, then hand the Blockers and Likely reviewer requests to
   `bioc-pkg-dev` if you are also preparing the submission.

## Output Format

```markdown
## Self-review: [package] at [commit]

Rubric [sha, date] · checklist v[version] · build outputs: [present / missing]

### Findings ([n])
1. **[title]** ([severity], [rubric id]). [message]. See `[path:lines]`.
   Suggested fix: [snippet or direction, if mechanical]
...

### What the human reviewer will weigh
- Scope and overlap: [packages you name, verified with bioc-pkg-finder, and how yours differs]
- Provenance: [what was generated, copied, or written by hand; what the tracker issue will state]

### Package Review Checklist (draft)
[the checklist, every bullet marked Y / N (finding n) / N/A / ?]

### Blockers / Likely reviewer requests / Verdict
[as in bioc-pkg-dev: must rows that fail; should and consider rows; submittable or not]
```

## Examples

**User**: "Review my package before I submit it to Bioconductor."
**Agent**: runs `build-check-bioccheck`, saves the four output files, walks the five passes over
the source, reports nine findings (three `must`: a vendored Python dependency undeclared in
`SystemRequirements`, examples all gated behind `interactive()`, no test for the core function),
lists two packages found in the index that overlap and asks how this one differs, fills the
checklist with 44 Y, 9 N, 21 N/A and 2 ?, and ends with a verdict of "not yet: three blockers".

**User**: "Fill the Package Review Checklist for `./myPkg`."
**Agent**: fetches the latest checklist, runs the passes needed to answer it, and returns only
the filled checklist with finding numbers on the `N` bullets.

## Integration

- **Uses**: `build-check-bioccheck` (outputs feed the BLD rows and BiocCheck bullets),
  `bioc-pkg-finder` (every package name), `bioc-pkg-dev/knowledge` (the guideline text cited).
- **Used by**: `bioc-pkg-dev` step 8, which asks for this review before submitting.
- **Mirror of**: Bioconductor/BiocPkgReviewer, which posts the same review to the reviewer; its
  composed feedback to submitters points here.

## Notes

- The reviewer's tool never runs the package's code, and neither should this review: it reads.
  Build and check output comes from `build-check-bioccheck`, which the submitter runs on their
  own package deliberately.
- The rubric includes rows the published checklist does not ask about (its `rubric.md` marks
  them); they are the reviewer's, not the guide's, and are labelled so. Proposed additions to
  the checklist itself are discussed at Bioconductor/pkgrevdocs; this skill follows the published
  checklist only.
- Findings are numbered in your report; the reviewer's report numbers its own. Quote rubric ids
  when replying on the tracker, they are stable.
