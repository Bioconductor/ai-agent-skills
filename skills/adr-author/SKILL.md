---
name: adr-author
description: Write a new Architecture Decision Record following the established Nygard format and conventions.
version: 1.0.0
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
- **Format (Nygard):** Sections must include `Context` → `Decision` → `Alternatives considered` → `Consequences`, preceded by a metadata block:
  ```markdown
  # NNNN. <Title in sentence case>

  - **Status:** Accepted   (or: Proposed | Superseded by NNNN)
  - **Date:** YYYY-MM-DD
  - **Deciders:** <Names>
  ```
- **Immutable:** Never rewrite an accepted ADR to reflect a new decision. Instead, write a NEW ADR and mark the old one `Superseded by NNNN`. The new ADR should say `supersedes MMMM` in its Status line.
- **Index:** Add a line to the index file, e.g., `docs/adr/README.md`.

## When an ADR is Warranted

Record decisions that change runtime behavior, are expensive to reverse, or are non-obvious from the code (e.g., retry/error policies, storage/publish layouts, framework choices, container strategies).
Do NOT write ADRs for routine bug fixes, version bumps, or anything self-evident from the diff.

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
