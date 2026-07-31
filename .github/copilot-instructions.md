# Copilot Instructions for bioconductor/ai-agent-skills

This repository contains AI agent skill files (`skills/*/SKILL.md`). These are
platform-agnostic Markdown documents that teach AI agents how to perform tasks
in the Bioconductor ecosystem. They are **prompts and workflow descriptions**,
not executable code.

When reviewing pull requests that modify `SKILL.md` files, apply the following
standards. Flag violations as inline code review comments on the relevant lines.

---

## Critical: Agent Neutrality

Skills must be platform-agnostic. Flag any of the following:

- References to a specific tool by vendor name in instructions:
  - ❌ "use the Read tool", "run the Bash tool", "call the Edit tool"
  - ❌ "use `/analyze`", "ask `@workspace`", "trigger `#skill-name`"
  - ✅ "read the file", "run the command", "check the output"
- Any YAML frontmatter field named `platforms:` or `triggers:`.
- Instructions that only work on one specific agent platform (e.g., "In VS Code,
  open the Copilot panel and...").

---

## Important: Workflow Structure

Skills must describe a **workflow** with numbered steps, not just provide raw
code or commands.

Flag these issues:

- A `## Process` section that consists only of a single code block with no
  surrounding explanation or numbered steps. Code snippets are acceptable only
  as guardrails *embedded within* numbered workflow steps.
- A `## Process` section with fewer than 2 numbered steps (likely too thin to
  be a meaningful skill).
- Absence of a `## Process` section entirely.

---

## Advisory: Content Quality

Flag as advisory comments (not blocking):

- Sections that restate content from `AGENTS.md` or `SKILL_STANDARD.md` verbatim.
  Skills should *reference* those documents, not duplicate them.
- Flowery or padded language where concise instructional prose would suffice
  (e.g., "This incredible skill will help you masterfully navigate...").
- A description field that is vague or generic (e.g., `description: Does stuff`).

---

## CI Results

This repository runs two automated checks on every pull request that modifies
`SKILL.md` files. Your review is requested only after both have completed
successfully. When reviewing:

- **Reference the CI outcomes.** If `Validate Skills` or `Qualitative Skill
  Review` posted comments on this PR, read them and incorporate their findings
  into your review. Do not repeat findings already surfaced by CI.
- **If CI caught a violation**, treat it as confirmed — do not second-guess a
  structural failure. You may add context or suggest a fix, but mark the issue
  as already identified.
- **If CI passed**, you can focus your review on issues CI does not cover:
  clarity of prose, correctness of examples, adherence to the workflow-over-
  code-snippets principle, and overall usefulness of the skill.

---

## Do Not Flag

- Normal Markdown formatting variation (e.g., use of bold vs. headers).
- Optional frontmatter fields (`tags`) being absent.
- Code snippets when they are clearly embedded *within* numbered workflow steps
  as domain-specific guardrails (this is explicitly allowed and encouraged for
  Bioconductor-specific APIs).
- R or Bioconductor package names used in examples.
