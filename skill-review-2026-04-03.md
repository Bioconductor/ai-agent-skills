# Skill Review: check-waldronlab-skills, create-package-instructions, update-package-instructions

**Date**: 2026-04-03
**Reviewer**: Claude Code
**Focus**: SSOT violations, duplication, wordiness

## Executive Summary

**check-waldronlab-skills**: ✅ Good SSOT discipline, but verbose examples
**create-package-instructions**: ⚠️ Major SSOT violation - embeds full templates
**update-package-instructions**: ⚠️ Duplicates structure knowledge, very verbose

---

## 1. check-waldronlab-skills (234 lines)

### ✅ SSOT Compliance
- **Excellent**: Explicitly reads SKILLS.md dynamically rather than hard-coding skill lists
- Lines 222-223: Clearly states SSOT principle
- No violations found

### Duplication Issues
- **Minor**: Platform-specific notes (187-199) likely duplicate setup guide content
- **Minor**: Troubleshooting (202-218) duplicates adapter documentation

### Wordiness Issues
- **Process section** (lines 30-70): Could consolidate 4 steps into 2
- **Examples** (lines 112-185): Four verbose examples with repeated patterns - could reduce to 2 concise examples
- **Platform notes** (187-199): Adds little value beyond "works with slash commands"

### Recommendations
1. Reduce to 2 examples (health check + fit recommendation)
2. Remove or drastically shorten platform-specific section
3. Condense troubleshooting to bullet points with links to setup guides
4. **Target**: Reduce from 234 → ~120 lines

---

## 2. create-package-instructions (433 lines)

### ⚠️ MAJOR SSOT Violation

**Problem**: Lines 66-369 embed complete file templates that should be separate template files.

**Current approach**:
```markdown
#### 00-overview.md

Content structure:

```markdown
# [Package Name] Overview
## Classification
...
```

Populate from analysis:
- Package type classification
- Version number
...
```

**Should be**:
```markdown
#### 00-overview.md

Use template: `templates/package-instructions/00-overview.md.template`

Variable substitutions:
- `{{PACKAGE_NAME}}`: from DESCRIPTION
- `{{VERSION}}`: from DESCRIPTION
- `{{FUNCTIONS_BY_CATEGORY}}`: from analysis
```

**Impact**:
- Template content duplicated in skill file instead of actual template files
- Changes to template format require editing skill documentation
- Templates referenced in lines 162, 197, 282 exist, but file templates don't

### Duplication Issues
- File structure knowledge duplicated with update-package-instructions
- Each template section repeats "Populate from analysis" pattern
- Integration section (398-407) uses same pattern as other skills

### Wordiness Issues
- 433 lines, ~300 are embedded templates
- Lines 32-64: "Determine Required Instruction Files" could be table format
- Process steps could reference template files instead of showing full structure

### Recommendations
1. **Create actual template files** in `templates/package-instructions/`:
   - `00-overview.md.template`
   - `10-data-access.md.template`
   - `20-development.md.template`
   - `30-testing-and-docs.md.template`
   - `40-vignettes.md.template`
   - `50-git-workflow.md.template`
   - `INDEX.md.template`

2. **Skill references templates**:
   - "Read template from `templates/package-instructions/[filename]`"
   - "Perform variable substitution using analysis output"
   - "Write to `.github/instructions/[filename]`"

3. **Consolidate file determination** into table:
   ```markdown
   | File | Condition | Template |
   |------|-----------|----------|
   | 00-overview.md | Always | templates/.../00-overview.md.template |
   | 10-data-access.md | Type: Remote/Hybrid | templates/.../10-data-access.md.template |
   ```

4. **Target**: Reduce from 433 → ~200 lines

---

## 3. update-package-instructions (372 lines)

### ⚠️ SSOT Violations

**Problem**: Duplicates file structure knowledge from create-package-instructions

**Lines 77-123**: "Determine Update Scope" lists when to update each file
- This logic should be derived from template structure, not duplicated
- Violates DRY principle with create-package-instructions

**Lines 52-75**: "Identify Changes" lists what to detect
- Much of this is general diff logic, not skill-specific

### Duplication Issues
- **File structure** (77-123): Duplicates which files contain what from create-package-instructions
- **Smart strategies** (199-251): Duplicates general version control and diff principles
- **Preservation tactics** (237-251): Very detailed, overlaps with general editing guidance
- **Error handling** (275-326): Verbose example outputs could be condensed

### Wordiness Issues
- 372 lines - second longest skill
- **Update scope** (77-123): 47 lines of detailed conditions - could be decision tree or table
- **Update strategy** (125-174): 50 lines of preservation logic - could be bulleted principles
- **Smart strategies** (199-251): 53 lines of version/function handling - much is obvious
- **Configuration** (253-271): 19 lines for simple options

### Recommendations

1. **Reference template structure** instead of duplicating:
   ```markdown
   ### Determine Update Scope

   For each instruction file:
   - Read template variable list from corresponding template file
   - Compare template variables to current analysis output
   - If variables differ, file needs update
   ```

2. **Consolidate change detection** to core principles:
   - "Detect structural changes (new/removed functions, vignettes, dependencies)"
   - "Detect metadata changes (version, description, biocViews)"
   - "Preserve custom content (domain explanations, examples, warnings)"

3. **Simplify strategies** to essential rules:
   - Version changes: find-replace all occurrences
   - Function changes: add/remove from lists, preserve descriptions
   - Custom content: preserve paragraphs that aren't lists/metadata

4. **Condense error handling** to error types + recovery, not full example dialogs

5. **Target**: Reduce from 372 → ~200 lines

---

## Cross-Cutting Issues

### Shared Duplication
Both create and update skills should reference a shared understanding of:
- Instruction file structure (what files exist, what they contain)
- Template variable mappings
- Analysis-to-documentation field mappings

**Solution**: Create `templates/package-instructions/README.md` documenting:
- File structure and purpose
- Variable substitution rules
- When each file is required
- How analysis output maps to template variables

Both skills reference this instead of embedding the knowledge.

### Pattern: Verbose Error Handling
All three skills include detailed error messages with full example outputs.

**Current** (update-package-instructions lines 275-326):
```markdown
### No Existing Instructions Found

If `.github/instructions/` doesn't exist or is empty:

```
Error: No existing instructions found in .github/instructions/

These instructions can only update existing files...
```
```

**Should be**:
```markdown
### Error Handling

- **No instructions found**: Direct user to create-package-instructions
- **No changes detected**: Report up-to-date status
- **Conflicts**: Prompt for keep/replace/merge decision
- **Format mismatch**: Offer skip/attempt/regenerate options
```

### Pattern: Examples Could Be Terser
check-waldronlab-skills has 4 detailed examples (lines 112-185) that follow identical patterns.

**Recommendation**:
- Keep 1-2 most distinct examples
- Use compact format for remaining scenarios
- Trust that users understand the pattern after first example

---

## Actionable Changes

### Priority 1: Fix SSOT Violation in create-package-instructions

1. Create `templates/package-instructions/` directory
2. Move embedded templates to actual `.md.template` files
3. Add template README documenting structure
4. Update skill to reference templates instead of embedding
5. Update update-package-instructions to use same templates

**Estimated reduction**: 433 → ~200 lines, 372 → ~200 lines

### Priority 2: Consolidate Shared Knowledge

Create `templates/package-instructions/README.md`:
```markdown
# Package Instruction Templates

## File Structure
[Table of files, conditions, purposes]

## Template Variables
[Variable name, source (analysis field), example]

## Update Rules
[What analysis changes trigger updates to which files]
```

Reference from both create and update skills.

### Priority 3: Reduce Wordiness

- **check-waldronlab-skills**: Trim to 2 examples, condense troubleshooting → ~120 lines
- **create-package-instructions**: Remove embedded templates → ~200 lines
- **update-package-instructions**: Condense strategies and error handling → ~200 lines

**Total line reduction**: 1039 → ~520 lines (50% reduction)

---

## Summary Table

| Skill | Current | Target | Main Issues |
|-------|---------|--------|-------------|
| check-waldronlab-skills | 234 | 120 | Verbose examples, redundant platform notes |
| create-package-instructions | 433 | 200 | **SSOT violation** - embedded templates |
| update-package-instructions | 372 | 200 | Duplicates structure from create, very verbose |
| **Total** | **1039** | **520** | **50% reduction possible** |

---

## Conclusion

**check-waldronlab-skills** is SSOT-compliant but could be more concise.

**create-package-instructions** and **update-package-instructions** have significant SSOT violations due to embedded/duplicated template structure knowledge. Extracting templates to actual files and creating shared documentation would eliminate duplication and improve maintainability.

All three skills would benefit from:
1. More concise examples and error handling
2. Tables/bullets instead of prose where appropriate
3. Trusting users to understand patterns after one clear example
