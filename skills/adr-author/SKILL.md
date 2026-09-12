---
name: adr-author
description: Write a new Architecture Decision Record following the established Nygard format and conventions.
version: 1.1.0
category: meta
author: bioconductor
tags: [adr, architecture, documentation, decision]
---

# Authoring an ADR

Write a new Architecture Decision Record (ADR) following the established Nygard format and conventions. Use this skill when a non-trivial, behavior-affecting decision is made and should be recorded, or the user says "write an ADR", "record this decision", or "document the design rationale".

## Usage

Invoke this skill when you want to create a new Architecture Decision Record.
- "Write an ADR for..."
- "Record the decision to..."
- "Document the design rationale for..."

## Prerequisites

- The repository keeps ADRs in a standard location, typically `docs/adr/`.
- An index of ADRs (e.g., `docs/adr/README.md`) and a template (e.g., `docs/adr/template.md`) usually exist in this directory. If a `template.md` does not exist in the target repository, copy the `template.md` provided alongside this skill into the target repository's `docs/adr/` directory so it is available for future use.

## Conventions

- **Filename:** `NNNN-kebab-title.md`, zero-padded sequential number. The next number should be the highest existing number plus 1 (e.g., check `ls docs/adr/`).
- **Format:** Sections must include `Context` → `Decision` → `Alternatives considered` → `Consequences`, preceded by a metadata block. Nygard's original four sections are Title, Context, Decision, Status and Consequences; `Alternatives considered` is a later and near-universal addition, kept here because it is the part future readers actually reread.
  ```markdown
  # NNNN. <Title in sentence case>

  - **Status:** Accepted   (or: Proposed | Superseded by NNNN)
  - **Date:** YYYY-MM-DD
  - **Deciders:** <Names>
  ```
- **Supersession:** Never rewrite an accepted ADR's Context, Decision, or Consequences to say something it did not say. Write a NEW ADR and mark the old one `Superseded by NNNN`; the new ADR says `supersedes MMMM`.

  What *is* expected to change on the old record is its status and its forward reference — Nygard's own words are "if a decision is reversed, we will keep the old one around, but mark it as superseded", "with a reference to its replacement". So editing an accepted ADR to point at its replacement is the mechanism, not an exception to it. A short banner under the metadata block naming what changed, and leaving the original prose untouched below it, is preferred to a bare status line: a reader who lands on the old record mid-search needs to know what is still in force before reading on.

- **Partial correction:** `deprecated` and `superseded` both retire a whole record, and the format offers nothing for "still in force except for one claim". When a later ADR corrects part of an earlier one, do not mark the earlier one superseded — that would be false. Add a banner naming the correction and what survives it (`> **Corrected by [ADR-0010](...) (date).** The claim below that X is wrong ... The rename this ADR records is unaffected.`), and give the new ADR an `Amends:` line saying which part it touches.
- **Index:** Add a line to the index file, e.g., `docs/adr/README.md`.

## When an ADR is Warranted

Record decisions that change runtime behavior, are expensive to reverse, or are non-obvious from the code (e.g., retry/error policies, storage/publish layouts, framework choices, container strategies).
Do NOT write ADRs for routine bug fixes, version bumps, or anything self-evident from the diff.

## Scoping an ADR

The "warranted" test above decides *whether* to write a record. This decides *how many*.

**One decision per record.** The test is not length or topic breadth, it is **supersession granularity**: an ADR's value is that it can be pointed at, and reversed, on its own. Bundle two decisions and you have coupled their futures — reversing one means either superseding a record that also holds the other, or bolting on an amendment banner that every later reader has to parse before reaching the decision they came for.

Before bundling, ask of each decision in the draft:

1. **Could it be reversed on its own?** If yes, it needs its own record.
2. **Would someone search for it by name?** If the decision is not findable from the ADR's title, it is in the wrong ADR. A decision about what a status value means does not belong in a record titled for validation rules.
3. **Does it share a context with the others, or just a sitting?** Decisions made in the same afternoon are not thereby one decision. A shared triggering incident is cohesion; a shared calendar slot is not.

**Split by weight, not only by count.** A draft that bundles four decisions is usually not four ADRs — more often two of them never warranted a record at all. Re-apply the warranted test to each item separately:

- A field's optionality, a naming convention, an error-message format → belongs in the specification or the code it describes, not in the decision log.
- An implementation choice nothing outside the module can observe → belongs in a code comment and the commit message.
- A choice that changes what conforming input looks like, or that a future maintainer could plausibly reverse → its own ADR.

A decision log cluttered with small records is a real cost, but the usual cause is recording things that were never architectural, not splitting things that were.

## Content Guidance

- **Context** = The forces and the triggering experience, described concretely. Real incidents and specifics beat abstractions.
- **Decision** = What will be done, including actual config or code snippets if relevant.
- **Alternatives considered** = Each rejected option AND why it was rejected. This is the part future readers actually reread.
- **Consequences** = What gets better, and what new costs or trade-offs are accepted.

## Process

1. Read the 2-3 latest ADRs in the repository (e.g., in `docs/adr/`) to understand the established tone and context.
2. Determine the next sequential number `NNNN` for the new ADR.
3. Copy the `template.md` (from the repository or from this skill's directory) to `docs/adr/NNNN-<kebab-case-title>.md`. If the target repository did not have a template, also save a copy of the template to `docs/adr/template.md`.
4. Fill in the template following the content guidance above.
5. If the new ADR supersedes an older one, edit the old ADR's Status to `Superseded by NNNN`.
6. Add an entry for the new ADR to the index file (`docs/adr/README.md`).
7. Ask the user for explicit approval before committing any changes. If approved, commit the changes with the related code change (or alone if it's purely a decision).

## Examples

### Example: Authoring an ADR
**User:** "Write an ADR for switching our retry policy to exponential backoff."
**Agent:**
1. Checks `docs/adr/` for the latest ADR to get the tone and next sequence number.
2. Copies `docs/adr/template.md` to `docs/adr/0012-exponential-backoff-retry-policy.md`.
3. Fills out the Context, Decision, Alternatives Considered, and Consequences.
4. Adds the new ADR to `docs/adr/README.md`.
5. Prompts the user to review the ADR.

## Notes

- See `template.md` in this skill directory for a reference Nygard ADR template.
