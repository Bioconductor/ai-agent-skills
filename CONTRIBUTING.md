# Contributing

Thank you for your interest in contributing to bioconductor AI Agent Skills!

## What You Can Contribute

### New Skills

Have a workflow or pattern that would help others?

**Quick start**: Use the `create-skill` skill for guided help:
- "Help me create a new skill for [purpose]"

### Improve Existing Skills

Found a bug or enhancement?
1. Test your changes on multiple projects
2. Update [SKILLS.md](SKILLS.md) if description changes
3. Document breaking changes clearly
4. Submit PR

### Documentation

Fix typos, clarify instructions, update outdated info - all welcome via PR.

### Issues

Report bugs or suggest features via [GitHub Issues](https://github.com/bioconductor/ai-agent-skills/issues).

## How to Contribute

### Small Changes (typos, doc fixes)

1. Fork the repository
2. Make your changes
3. Submit pull request

### New Skills or Major Changes

1. **Open an issue first** to discuss your proposal
2. Get feedback from maintainers
3. Fork and create feature branch
4. Develop following [SKILL_STANDARD.md](SKILL_STANDARD.md)
5. **Validate**: Run `validate-skill` to ensure standards compliance
6. Fix any CRITICAL or WARNING issues from validation
7. Test thoroughly (at least 3 projects)
8. Update [SKILLS.md](SKILLS.md) using `document-skill` to include your skill
9. Submit pull request

## Skill Guidelines

Skills must conform strictly to [AGENTS.md § Skill File Format](AGENTS.md#skill-file-format) and [SKILL_STANDARD.md](SKILL_STANDARD.md). Do not duplicate required fields or metadata definitions in your skill files.

### Testing & Validation

Before submitting:
- **Run validation**: Use `validate-skill` to check standards compliance
- Fix all CRITICAL issues and strongly consider fixing WARNING issues
- Test on at least 3 different projects
- Verify output accuracy
- Check edge cases
- Get feedback from others if possible

## Pull Request Process

We use a combination of automated tools and human review to ensure high-quality skills. **Branch protection rules prevent even collaborators from committing directly to the `devel` branch**, so all changes must go through a pull request.

When you submit a PR, you will receive automated feedback from three sources:
1. **Validate Skills (CI)**: A deterministic script that enforces structural and metadata standards (e.g., frontmatter requirements, `SKILLS.md` synchronization).
2. **Qualitative Skill Review (CI)**: An automated LLM that reviews your skill for qualitative guidelines (like agent-neutrality).
3. **GitHub Copilot PR Review**: General AI feedback based on repository context.

### Steps to merge
1. Create clear PR description explaining what and why.
2. Reference any related issues.
3. **Resolve all CI errors**: Ensure that the "Validate Skills" and "Qualitative Skill Review" workflows both pass. 
4. Wait for human review and respond to feedback. Be patient - reviews typically take 2-7 days.
5. Once approved, maintainers will merge your PR.

## Questions?

- **Skill creation help**: Use the `create-skill` skill
- **Validation help**: Use the `validate-skill` skill to check if your skill meets standards
- **Setup questions**: See [instructions/](instructions/) for your platform
- **General questions**: [GitHub Discussions](https://github.com/bioconductor/ai-agent-skills/discussions)
- **Bugs/features**: [GitHub Issues](https://github.com/bioconductor/ai-agent-skills/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
