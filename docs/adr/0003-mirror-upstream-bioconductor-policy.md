# 0003. Mirror upstream Bioconductor policy rather than fork it

- **Status:** Accepted
- **Date:** 2026-09-03
- **Deciders:** @lwaldron, @ybaeus, with review input from @LiNk-NY on [#24](https://github.com/Bioconductor/ai-agent-skills/pull/24)

## Context and Problem Statement

The `bioc-pkg-dev` skill ([#24](https://github.com/Bioconductor/ai-agent-skills/pull/24)) summarizes
[contributions.bioconductor.org](https://contributions.bioconductor.org) - 33 chapters maintained
upstream in [Bioconductor/pkgrevdocs](https://github.com/Bioconductor/pkgrevdocs) - into 21 files
under `skills/bioc-pkg-dev/knowledge/`. Upstream moves twice a year with the release cycle and is
edited in between. A summary that has silently drifted is worse than none, because the skill's output
is a submit-or-not verdict.

Review of #24 exposed the harder half. Upstream is not always self-consistent: `r-code` forbade `.`
in function names and one bullet later required it for internal helpers; reviewer eligibility
differed between the volunteer and expectations chapters. Fixing those in the skill would have been
the obvious move and the wrong one. The same review also produced a plausible but *incorrect*
correction - an automated reviewer flagged `Bioconductor/BiocContributions` as a typo, and @LiNk-NY
confirmed the original was right.

## Decision

**Treat `skills/bioc-pkg-dev/knowledge/` as a mirror of upstream policy, not a second source of it.**

1. **Mirror faithfully.** Each file is a derived summary citing its chapters in a `Source:` footer.
   Where skill and upstream disagree, upstream wins.

2. **Fix errors upstream, then sync down.** A contradiction found while writing or using the skill
   becomes a `pkgrevdocs` pull request; the skill changes only once that lands. Precedent, both from
   the #24 review and both merged: [pkgrevdocs#181](https://github.com/Bioconductor/pkgrevdocs/pull/181)
   (`.` in function names) and [pkgrevdocs#182](https://github.com/Bioconductor/pkgrevdocs/pull/182)
   (reviewer eligibility).

3. **Keep a machine-checkable sync baseline** in
   [`knowledge/SOURCES.md`](../../skills/bioc-pkg-dev/knowledge/SOURCES.md): dated pins for every
   tracked upstream (`pkgrevdocs` commit SHA, `BiocContributions` issue-template blob, `BiocCheck` and
   `biocthis` versions, the Bioconductor release/devel/R triple), a map from each upstream `.Rmd` to
   its rendered slug and knowledge file, and the endpoints that make drift detectable. Refreshes are
   then scoped: compare live upstream to the pins, re-derive only the mapped files. The slug column is
   required because the names differ (`package-maintainence.Rmd` renders to
   `package-maintenance.html`) - drift arrives as `.Rmd` names, citations are by slug.

4. **Mark, source and date anything not from upstream prose.** Two kinds: facts read from tool source
   (BiocCheck's 80% runnable-example threshold in `checkExportsAreDocumented()`, observed `biocthis`
   behavior), which expire on their own schedule; and deliberate local additions. Exactly one exists -
   `knowledge/development/ai-policy.md` recommends the `Co-authored-by:` trailer, added at @lwaldron's
   request in #24, where upstream gives only `Assisted-by:` and `Code copied from:`. It elaborates
   rather than contradicts, but per decision 2 it belongs upstream; until then it is the one tracked
   deviation and must survive re-syncs deliberately.

5. **Non-summary behavior lives in its own skill; existing skills are invoked, not restated.**
   `build-check-bioccheck` was split out and is called for the gate step, following the composition
   pattern `analyze-r-package` set with `create-package-instructions`; `metadata-files.md` likewise
   points NEWS authoring at `update-r-news`. The gate becomes reusable, and `knowledge/` stays
   summary-only.

6. **Where upstream names a vendor, keep the vendor name.** Upstream cites GitHub Actions and
   `biocthis` ships `use_bioc_github_action()`. Automated review called this an Agent Neutrality
   violation; @lwaldron granted an explicit exception in #24. Neutrality governs agent platforms, not
   the CI vendors upstream itself names - neutralizing the wording would make the summary say
   something upstream does not.

## Alternatives Considered

- **Correct upstream errors in the summaries.** Rejected: silent divergence, no record of what changed
  or why, a conflict at every sync, and no way for a reader to separate policy from opinion. The
  incorrect `BiocContributions` "fix" in #24 shows how convincing such an edit can look.
- **Track deviations with inline markup**, or **hold them in a re-applied patch file.** Both raised in
  #24, both rejected as machinery bought before it is needed; a patch file also rots faster than the
  text it patches, breaking on rewordings that changed no policy.
- **Link upstream instead of summarizing.** Rejected: agents need the rules in context at decision
  time, and the gate must be stated as thresholds, not fetched per invocation.
- **Trim `knowledge/` to a core subset**, as offered in [#23](https://github.com/Bioconductor/ai-agent-skills/issues/23).
  Rejected once mirroring was chosen: the file count follows the chapter map, and collapsing files
  breaks the mapping scoped refreshes depend on.
- **Keep build/check inside `bioc-pkg-dev`.** Rejected: it is useful beyond submission prep, and would
  plant permanent non-mirrored content inside a mirrored tree.

## Consequences

- Fixing a policy error is slower and gated on upstream review. Accepted: both #24 upstream pull
  requests merged.
- `SOURCES.md` must not go stale. Unadvanced pins make drift detection report "no change" and be
  silently wrong; updating them is part of a refresh, not follow-up.
- First drift already caught: as of 2026-09-03 the `pkgrevdocs` pin is two commits behind `devel` -
  the #181 and #182 merges - so `knowledge/development/r-code.md` and `knowledge/reviewer.md` still
  carry the pre-fix wording this repository asked upstream to change. Bumping the pin and re-deriving
  those two files is the immediate follow-up.
- Sync pull requests stay reviewable: a pin bump plus only the mapped files. Anything else in the diff
  is a deviation and needs justifying.
- A deliberate deviation now needs an ADR amending this one, not a quiet edit.
- `build-check-bioccheck` must stay independently invocable.
- The boundary is enforced by convention and review only - no CI check compares a knowledge file to the
  chapter it cites, so a stale pin stays invisible until someone looks.
