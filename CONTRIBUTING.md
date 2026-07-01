# Contributing

Thank you for your interest in contributing to waldronlab AI Agent Skills!

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

Report bugs or suggest features via [GitHub Issues](https://github.com/waldronlab/ai-agent-skills/issues).

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

1. Create clear PR description explaining what and why
2. Reference any related issues
3. Ensure all tests pass (if applicable)
4. Respond to review feedback
5. Be patient - reviews typically take 2-7 days

## Questions?

- **Skill creation help**: Use the `create-skill` skill
- **Validation help**: Use the `validate-skill` skill to check if your skill meets standards
- **Setup questions**: See [instructions/](instructions/) for your platform
- **General questions**: [GitHub Discussions](https://github.com/waldronlab/ai-agent-skills/discussions)
- **Bugs/features**: [GitHub Issues](https://github.com/waldronlab/ai-agent-skills/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
