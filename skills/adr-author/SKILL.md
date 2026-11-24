---
name: adr-author
description: Write a new Architecture Decision Record following the established Nygard format and conventions.
metadata:
  version: 1.1.2
  category: meta
  author: bioconductor
  tags: adr, architecture, documentation, decision
---

# Authoring an ADR

Write a new Architecture Decision Record (ADR) in the Nygard format, with the conventions below. Sources are in `SOURCES.md`, read only when updating this skill.

## Usage

- "Write an ADR for..."
- "Record the decision to..."
- "Document the design rationale for..."

## Prerequisites

- The repository keeps ADRs in a standard location, typically `docs/adr/`, usually with an index (e.g., `docs/adr/README.md`) and a template (e.g., `docs/adr/template.md`).

## Conventions

- **Filename:** `NNNN-kebab-title.md`, where `NNNN` is the highest existing number plus 1, zero-padded.
- **Format:** a metadata block, then `Context` → `Decision` → `Alternatives considered` → `Consequences`.
  ```markdown
  # NNNN. <Title in sentence case>

  - **Status:** Accepted   (or: Proposed | Superseded by NNNN)
  - **Date:** YYYY-MM-DD
  - **Deciders:** <Names>
  ```
- **Supersession:** Never rewrite an accepted ADR's Context, Decision, or Consequences to say something it did not say. Write a new ADR that says `supersedes MMMM`, and mark the old one `Superseded by NNNN`. Only the old record's status and forward reference change. Prefer to give them as a short banner under the old record's metadata block naming what changed, with the original prose untouched below it, over a bare status line: a reader who lands on the old record needs to know what is still in force.
- **Partial correction:** When a later ADR changes part of an earlier one that otherwise stands, do not mark the earlier one superseded or deprecated, since both retire a whole record. Name the amended part in its Status line and add a banner directly under the metadata block saying what changed and what still stands:

  ```markdown
  - **Status:** Accepted; decision §1 amended YYYY-MM-DD

  > **Amendment (YYYY-MM-DD):** decision §1 below places X in this repository. It has since moved to
  > Y, because <reason>. The rest stands unchanged: <what survives>.
  ```

## When an ADR is Warranted

Record decisions that change runtime behavior, are expensive to reverse, or are non-obvious from the code (e.g., retry/error policies, storage/publish layouts, framework choices, container strategies).
Do NOT write ADRs for routine bug fixes, version bumps, or anything self-evident from the diff.

## Scoping an ADR

**One decision per record.** The test is supersession granularity, not length or topic breadth: a record must be reversible on its own, and bundling two decisions means reversing one requires superseding or amending a record that also holds the other.

Before bundling, ask of each decision in the draft:

1. **Could it be reversed on its own?** If yes, and it passes the warranted test on its own, it needs its own record. A reversible choice that was never architectural does not become one by being separable.
2. **Would someone search for it by name?** A decision that is not findable from the ADR's title is in the wrong ADR.
3. **Does it share a context with the others, or just a sitting?** A shared triggering incident is cohesion; being decided in the same afternoon is not.

**Split by weight, not only by count.** A draft that bundles four decisions is usually not four ADRs; more often two of them never warranted a record. Re-apply the warranted test to each item separately:

- A field's optionality, a naming convention, an error-message format → belongs in the specification or the code it describes, not in the decision log.
- An implementation choice nothing outside the module can observe → belongs in a code comment and the commit message.
- A choice that changes what conforming input looks like, or that a future maintainer could plausibly reverse → its own ADR.

## Process

1. Read the 2-3 latest ADRs in the repository for the established tone and context.
2. Determine the next number `NNNN`.
3. Copy the repository's `template.md` to `docs/adr/NNNN-<kebab-case-title>.md`. If the repository has no template, use the `template.md` beside this skill and also save a copy as `docs/adr/template.md`.
4. Fill in the template:
   - **Context**: the forces and the triggering experience, with real incidents and specifics.
   - **Decision**: what will be done, with the actual config or code where relevant.
   - **Alternatives considered**: each rejected option and why it was rejected. This is the section future readers reread.
   - **Consequences**: what gets better, and what costs or trade-offs are accepted.
5. If the new ADR supersedes or amends an older one, update the old record as described in Conventions.
6. Add a line for the new ADR to the index file (e.g., `docs/adr/README.md`).
7. Ask the user for explicit approval before committing. Commit the ADR with the related code change, or alone if it is purely a decision.

## Examples

### Example: a draft that bundles decisions

**User:** "Write an ADR for the manifest validation changes: unknown fields are now rejected, `status: retired` now means the entry is excluded from builds, and error messages use the `file:line: message` format."

The draft holds three decisions. Rejecting unknown fields changes what conforming input looks like, so it gets `0012-reject-unknown-manifest-fields.md`. The meaning of `retired` could be reversed on its own and would not be found under a validation title, so it gets `0013-retired-entries-excluded-from-builds.md`. The error-message format belongs in the specification and gets no record.
