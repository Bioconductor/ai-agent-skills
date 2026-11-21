---
name: create-skill
description: Help create a new AI agent skill through collaborative Q&A
version: 1.4.0
category: meta
tags: [meta, infrastructure, skill-creation]
author: bioconductor
---

# create-skill

Help a user turn an idea into a skill file through Q&A. The questions look for what an agent would get wrong without the skill, because that is what the skill should contain.

## Usage

- "Help me create a new skill for [domain/purpose]"

## Prerequisites

- Working directory is the ai-agent-skills repository

## Process

### 1. Find What the Skill Must Add

Ask the user:
- What task should the skill cover, and what does a typical input and output look like?
- What does a coding agent get wrong, or not know, when asked to do this without the skill? Ask for a case where they had to correct one.
- Which Bioconductor, R, or project conventions apply that an agent would not follow by default?
- Where must the agent stop and ask the user, or get confirmation before acting?

If the answers show that an agent already does the task well without instructions, say that a skill is not needed. If the task belongs in an existing skill (see [SKILLS.md](../../SKILLS.md)), propose extending that skill; if the user agrees, edit it as step 3 describes, bump its version, and continue from step 4.

### 2. Choose the Category and Name

Existing categories are `meta`, `r-packages`, and `bioconductor-how-tos`; suggest the closest. The name is the purpose in kebab-case, e.g. "analyze R package" → `analyze-r-package`, and the file is `skills/[skill-name]/SKILL.md`. Draft the one-line `description` with the user, since agents match requests against it.

### 3. Draft the Skill File

Follow [AGENTS.md](../../AGENTS.md) and [SKILL_STANDARD.md](../../SKILL_STANDARD.md); do not copy their rules into the skill. Keep the `## Usage`, `## Prerequisites`, `## Process`, and `## Examples` headings, which CI requires.

- Write only steps that carry the content found in step 1. Apply AGENTS.md § Only What an Agent Wouldn't Do Unprompted to each line as you write it, not as a later pass.
- The result is still a workflow, not a list of pitfalls: keep the steps needed to put the others in order, and leave out a step the agent would do anyway and that carries no instruction, even if that leaves the process short.
- Put source documents, version pins, and the history of a decision in `skills/[skill-name]/SOURCES.md`.
- Give one example that shows a concrete input and the output expected, taken from the user's case where possible.
- Mark what the user has not settled with `TODO`; do not fill a gap with an invented fact.

### 4. Review with the User

Show the draft and ask whether it captures their intent. Point out any step you think an agent would have done without the skill, and ask whether to remove it.

### 5. Validate

Run `validate-skill` on the new or changed file and fix any CRITICAL issues before continuing.

### 6. Update Repository Documentation

Run `document-skill` on the new or changed skill to update `SKILLS.md`, then suggest the user test the skill on a real case.

## Examples

**User**: "I want a skill for deprecating a function in a Bioconductor package."

Asked what an agent gets wrong, the user says it added a deprecation cycle for a function that had never been in a release. The agent finds the deprecation rules, including that exemption, already in `bioc-pkg-dev` (`knowledge/maintenance.md`), so a new skill would repeat them. It asks why the agent missed the rule, and proposes making `bioc-pkg-dev` point to it where maintenance tasks start. Result: an edit to `bioc-pkg-dev` with a version bump, and no new skill.
