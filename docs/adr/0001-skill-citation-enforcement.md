# 0001. Centralized Agent Skill Citation Enforcement

- **Status:** Accepted
- **Date:** 2026-07-28
- **Deciders:** Levi (User), AI Agent

## Context and Problem Statement

When AI agents use a Bioconductor skill from this repository, their responses often do not make it obvious that a specific skill was executed, which skill it was, or what version was used. This lack of transparency makes it difficult for users to track which skills were responsible for a given output and complicates debugging when skills are updated. We needed a way to guarantee that agents always cite the Bioconductor skill being used (name, version, and author).

## Decision

We will enforce a standard citation block in all agent responses using a centralized, single-source-of-truth approach. 

Specifically, we decided to:
1. **Update AGENTS.md**: Add a mandatory requirement for agents to include a standard citation block (`> 🛠️ **Bioconductor Skill Executed**: <name> | **Version**: <version> | **Author**: <author>`).
2. **Make `author` Required**: Change the `author` YAML frontmatter field from optional to REQUIRED in `AGENTS.md` and the `validate_skills.py` CI script to guarantee there is always an author to cite.
3. **Update Platform Instructions**: Add explicit rules to `instructions/claude.md`, `instructions/copilot.md`, and `instructions/antigravity.md` to bootstrap agents with the citation requirement.
4. **Avoid Duplicating Content in Skills**: Instead of hardcoding the citation format prose into the `Output Format` section of every individual `SKILL.md` file, the rule is defined globally and agents are instructed to extract the canonical values directly from each skill's YAML frontmatter.

## Alternatives Considered

- **Embedding citation instructions in every `SKILL.md` file**: We considered adding a required `Output Format` section to every skill file containing the exact markdown for the citation. This was rejected because it violates the repository's principle of avoiding content duplication. The `name`, `version`, and `author` already live canonically in the YAML frontmatter.
- **Using CI to enforce the exact citation markdown string inside skills**: We considered adding a python script check to look for the exact citation block inside `SKILL.md` files. This was rejected because checking for exact strings (with emojis) in free-form prose is brittle and mixes presentation concerns with structural validation.

## Consequences

- **Easier Maintenance**: If the standard citation format needs to change in the future, it only needs to be updated in the platform instruction files and `AGENTS.md`, not across all 13+ skill files.
- **Improved Transparency**: Users will now clearly see when a Bioconductor skill was utilized, including exactly which version was run.
- **Immediate Compliance**: `author` is now a mandatory frontmatter field for all new and existing skills.
