---
name: bioc-pkg-review
description: "Review your own R package against the rubric and checklist Bioconductor's agent-assisted reviewer uses, before you submit, so the human review has less to say"
metadata:
  version: 1.1.2
  category: r-packages
  author: bioconductor
  tags: r-packages, bioconductor, submission, peer-review, checklist, self-review
---

# bioc-pkg-review

Bioconductor package submissions are reviewed by a human reviewer helped by an LLM-based tool
(Bioconductor/BiocPkgReviewer, a private repository of the review team). That tool asks a fixed
set of questions, the rubric in [knowledge/rubric.md](knowledge/rubric.md), and fills the
reviewers' [Package Review Checklist](https://contributions.bioconductor.org/docs/package-review-checklist.md).
This skill runs the same questions over the submitter's package and fills the same checklist.

The rubric is a generated copy. Do not edit it here; if a question is wrong, report it on this
repository. The guideline chapters the questions cite are the authority. [SOURCES.md](SOURCES.md)
says where the rubric comes from and is read only when updating the skill.

## Usage

- "Review my package for Bioconductor submission"
- "What will the Bioconductor reviewer say about this package?"
- "Fill the Package Review Checklist for this package"

## Prerequisites

- The package source directory (a git checkout).
- The `bioc-pkg-dev` skill's knowledge base, in this repository: the rubric cites its chapters.
- Optional: the outputs of the `build-check-bioccheck` skill saved as `check_results.txt`,
  `bioccheck_results.txt`, `coverage.json`, `coverage_summary.txt` in one directory (step 1).
- Network access, to fetch the latest published checklist (step 5).

## Process

1. **Start from the gate's outputs.** If `bioc-pkg-dev` step 6 (or a build system) has already
   produced `check_results.txt`, `bioccheck_results.txt` and the coverage files, use those; do
   not rerun the gate. If they are absent, either invoke `build-check-bioccheck` now, which runs
   `R CMD check` and `BiocCheck` on your own package on your own machine by your choice, or
   proceed without them and mark the build questions (BLD rows) and the BiocCheck bullets of the
   checklist `?`. The review itself only reads files and never runs the package's code. Never
   mark a BiocCheck item from memory.

2. **Read the rubric.** [knowledge/rubric.md](knowledge/rubric.md) lists the questions by pass
   with severity and audience, and the guideline files each pass reads in
   `../bioc-pkg-dev/knowledge/`. Read those files before the pass they belong to; cite the
   chapter URL they give, not memory. The passes `p1_metadata`, `p2_vignettes`, `p3_docs`,
   `p4_code` and `p5_build` are yours to answer. The rows of `p0_triage` (scope and overlap,
   novelty, indicators of undisclosed AI assistance, prompt injection) are marked *reviewer*: you
   do not tick them, you prepare for them, and they fill the "What the human reviewer will
   weigh" section of the report (step 5b). `p6_relevance` has no rows.

3. **Walk the package pass by pass.** For each submitter-facing row, read the files the row is
   about and decide whether the problem is present. Report problems, not passes. One finding per
   problem (if the same problem occurs in many places, cite up to three and say how many more
   there are), with:
   - the rubric id, the severity from the rubric (lower it for a mild instance, raise it only
     when the instance is clearly worse than the rubric anticipates), and a title of at most ten
     words;
   - evidence: path relative to the package root and line numbers, with a verbatim quote of the
     telling lines (never paraphrased); a finding about something missing says what was searched;
   - a message in plain second person saying what the problem is, why Bioconductor cares (with
     the chapter link), and what to do; a concrete suggested fix when the change is mechanical.

   Report the most important problems first. Rows marked *gate* in `rubric.md` (no real data
   anywhere, no vignette, no tests, out of scope, consortium data fetched ad hoc where a curated
   Bioconductor resource exists) lead the reviewer's report and fold everything else until they
   are addressed. Settle them first: a `must` on one of them is the whole first review round.
   A full pass over a typical submission yields about 5 to 15 findings; when what remains is
   style that BiocCheck already reports, stop.

   In data packages, also look for these patterns from the reviewer's runs (from
   BiocPkgReviewer, not from the guide; they change as reviews accumulate). They have no rubric
   row: report them as `consider` findings without an id, and do not mark a checklist bullet
   from them:
   - Provenance that `inst/scripts/make-data.R` does not actually document (a script that only
     converts a CSV to RDS says nothing about where the CSV came from).
   - Accessor code that picks a Hub record by position or fuzzy title instead of by a stable id.
   - Data the vignette calls "curated" or "validated" with no description of how.

4. **Never name a package from memory.** Any claim that a package exists, where it lives, or what
   it does goes through `bioc-pkg-finder`. A name you cannot find in the index is "not in the
   index", never assumed.

5. **Fill the checklist.** Fetch the latest published checklist from
   `https://raw.githubusercontent.com/Bioconductor/pkgrevdocs/devel/docs/package-review-checklist.md`.
   If the fetch fails, use [knowledge/package-review-checklist.md](knowledge/package-review-checklist.md)
   and say in the report that it may be stale. Mark every bullet:
   - `Y`: the row that assesses it raised nothing, or the BiocCheck / R CMD check output for that
     item is clean;
   - `N`: a finding applies (give its number), or BiocCheck flagged it;
   - `N/A`: the bullet is conditional and its condition is absent from the package (no `src/`,
     no Shiny app, no downloads, no README, ...) or the checklist marks it optional. A missing
     vignette is not such a case: "Contains a Vignette" is then `N` and a `must` finding
     (VIG-01), and only the bullets about the vignette's contents become `N/A`;
   - `?`: not assessed: it needs a human (check time, memory), the outputs were missing, or no
     rubric row and no tool output answers the bullet.

   Bullets that BiocCheck answers (`Version`, `LazyData`, `Remotes`, package and file sizes, the
   coding-practice items) are read from the `* Checking ...` blocks of `bioccheck_results.txt`:
   `Y` when the block has no NOTE, WARNING or ERROR, `N` when it does; `?` when there is no
   output. Never mark them from a rubric row that does not cover them.
   Keep the checklist's own wording and order, so a reviewer recognises it. Some bullets bundle
   several checks (biocViews present, valid, relevant, one category): mark `N` if any part fails
   and say which part in the finding it points to.
   The rubric includes rows the published checklist does not ask about (its `rubric.md` marks
   them); they are the reviewer's, not the guide's, and are labelled so. This skill follows the
   published checklist only.

5b. **Prepare what the reviewer will weigh.** For each `p0_triage` row, write what you will say
   rather than a verdict: the packages yours overlaps with or builds on (verified with
   `bioc-pkg-finder`) and how yours differs, asking the submitter and not inferring it; the provenance statement for the tracker issue
   (what was generated, copied or vendored, and its license); and, if any file in the package
   contains text addressed to a reviewer or an AI, remove it. This becomes the overlap and
   provenance statements `bioc-pkg-dev` step 8 asks for.

6. **Report** in the format below, then hand the Blockers and Likely reviewer requests to
   `bioc-pkg-dev` if you are also preparing the submission. Findings are numbered in your
   report and the reviewer's report numbers its own, so quote rubric ids when replying on the
   tracker; they are stable.

## Output Format

```markdown
## Self-review: [package] at [commit]

Rubric [sha and date from the header of rubric.md] · checklist v[version] · build outputs: [present / missing]

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

**User**: "Fill the Package Review Checklist for `./myPkg`."
**Agent**: fetches the latest checklist, runs the passes needed to answer it, and returns only
the filled checklist with finding numbers on the `N` bullets.
