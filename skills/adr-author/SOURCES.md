# Sources for adr-author

Read this file when updating the skill, not when running it.

## Upstream document

- **Michael Nygard, "Documenting Architecture Decisions"** (2011),
  <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>.
  - Nygard's original elements are Title, Context, Decision, Status and Consequences.
  - On supersession: "if a decision is reversed, we will keep the old one around, but mark it as
    superseded", "with a reference to its replacement". Editing an accepted ADR's status to point at
    its replacement is therefore the mechanism, not an exception to the rule against rewriting it.
  - `deprecated` and `superseded` are Nygard's statuses for retiring a record; both retire a whole
    record.

## Conventions this skill sets

These are not in Nygard's text.

- **`Alternatives considered` section.** A later and near-universal addition to the format, kept
  because it is the part future readers reread.
- **Supersession banner.** A banner under the old record's metadata block is preferred to a bare
  status line.
- **Partial correction.** The `Accepted; decision §N amended YYYY-MM-DD` status and the amendment
  banner, for a later ADR that changes part of an earlier one that otherwise stands.
- **Scoping.** One decision per record, tested by supersession granularity: an ADR's value is that
  it can be pointed at, and reversed, on its own. A decision log cluttered with small records is a
  cost, but the usual cause is recording things that were never architectural, not splitting things
  that were.

## History

- v1.1.0 added the scoping guidance, corrected the supersession rule, and corrected the Nygard
  attribution of `Alternatives considered` (see `CHANGELOG.md`).
- v1.1.1 trimmed the skill under AGENTS.md § Only What an Agent Wouldn't Do Unprompted.
