---
name: update-r-news
description: Draft or update an R package NEWS file from git commit history, examining diffs when commit messages are vague
version: 1.0.0
category: r-packages
tags: [r-packages, documentation, git, changelog, news, bioconductor]
author: waldronlab
---

# update-r-news

Draft or update an R package NEWS file (`NEWS.md`, `NEWS`, or `NEWS.Rd`) from the git commit history since the last Bioconductor release. When commit messages are too vague to classify, the skill inspects the associated diff to infer what changed. All drafts are shown for review and confirmation before writing to disk.

This skill is designed for Bioconductor packages on the `devel` branch, where the current development version is odd-numbered (e.g. `1.19.x`) and the upcoming release will be even-numbered (e.g. `1.20.0`).

## Usage

Invoke this skill when you want to draft or update a package NEWS file:
- "Update the NEWS file from recent commits"
- "Draft NEWS entries from git history"
- "Generate a changelog based on git commits"
- "Add a NEWS entry for the upcoming release"
- "Update NEWS based on what changed since the last release"

## Prerequisites

- Working directory is an R package root (contains `DESCRIPTION` file)
- Directory is a git repository with commit history (`git` available on PATH)
- A NEWS file (`NEWS.md`, `NEWS`, or `NEWS.Rd`) may already exist, but is not required

## Process

### 1. Detect NEWS File and Format

Check the package root for these files in priority order:
1. `NEWS.md` (markdown)
2. `NEWS.Rd` (R documentation format)
3. `NEWS` (plain text, Bioconductor-style)

If exactly one is found, use it. If multiple exist, ask the user which one to update. If none exist, ask which format to create (default: `NEWS.md`).

Record the detected file path and format for use throughout the remaining steps.

### 2. Read Package Version

Parse `DESCRIPTION` to extract the `Version:` field. In Bioconductor's versioning convention, the `devel` branch carries an **odd** minor version (the `Y` in `X.Y.Z`), while each released version has an **even** `Y`.

Examples:
- Current devel `1.19.4` → upcoming release is `1.20.0`
- Current devel `2.5.7` → upcoming release is `2.6.0`
- Current devel `0.99.3` → this is a new package submission (version below `1.0.0`)

This derived release version will be the heading for the new NEWS block.

### 3. Determine Commit Range

Bioconductor packages do **not** use git tags for releases. Instead, the commit range is determined by searching the git log for a specific release-bump commit message.

**Step 3a — Search for the release-bump commit**

Run:
```
git log --oneline --all
```

Search for a commit whose message matches this exact literal pattern (these commits are applied en masse by Bioconductor and do not include the actual package version number):
```
bump x.y.z version to even y prior to creation of RELEASE_
```

For example, for the Bioconductor 3.18 release:
```
a1b2c3d bump x.y.z version to even y prior to creation of RELEASE_3_18 branch
```

**Step 3b — Find the devel-version bump commit that follows**

Immediately after the release-bump commit, Bioconductor applies a second en-masse commit that increments the `devel` branch back to an odd minor version. Its message matches the literal pattern:
```
bump x.y.z version to odd y following creation of RELEASE_
```

For example:
```
b2c3d4e bump x.y.z version to odd y following creation of RELEASE_3_18 branch
```

This second commit (`<devel-bump-sha>`) is the starting point for the commit range. Use `<devel-bump-sha>..HEAD` as the range.

To locate it, find the oldest commit returned by:
```
git log --oneline <release-bump-sha>..HEAD
```

**Step 3c — Handle new packages (no release-bump commit found)**

If no release-bump commit is found in the history:

1. Check the current `Version:` field from `DESCRIPTION`.
2. If the version is below `1.0.0` (e.g. `0.99.3`): treat the entire commit history as the range (i.e. `git log --oneline` from the first commit to `HEAD`) and note that this appears to be a new package submission.
3. If the version is `1.0.0` or higher but no release-bump commit is found: **do not guess**. Ask the user to supply a starting commit SHA (see Error Handling).

**Step 3d — Handle an existing NEWS entry for the upcoming release**

If the NEWS file already has a section heading for the upcoming release version, offer to **append** new commits since the last commit already covered rather than regenerating the entire block.

**Retrieve commits for the determined range**:
```
git log <range> --oneline
```

Also retrieve merge commits separately:
```
git log <range> --merges --format="%H %s %b"
```

### 4. Extract PR Titles from Merge Commits

For each merge commit in the log, attempt to extract the pull request title:

- GitHub-style merge commits have the format: `Merge pull request #NNN from <branch>` followed by the PR title on the next line
- Parse the commit body (from `git show <sha> --format="%b" -s`) to extract the PR title
- If a PR title is found, use it as the primary description for that merge commit; otherwise fall back to the merge commit subject line

For non-merge commits, use the commit subject line directly.

### 5. Classify Commits by Message Specificity

For each commit, evaluate its message for vagueness using these criteria — a commit is **vague** if it meets any of the following:

**Word count rule**: The commit message (after stripping conventional-commit type prefixes like `fix:`, `feat:`, `chore:`) contains **3 words or fewer**.

**Filler phrase rule**: The lowercased message matches any of these patterns:
- Single words: `fix`, `update`, `wip`, `cleanup`, `refactor`, `changes`, `misc`, `tweaks`, `improvements`
- Short phrases: `minor update`, `minor fix`, `minor changes`, `api update`, `small fix`, `small update`, `bug fix`, `quick fix`, `more fixes`, `various fixes`, `various changes`

Split all commits into two lists: **specific** and **vague**.

### 6. Inspect Diffs for Vague Commits

For each vague commit, run:
```
git show <sha> --stat --patch -- R/ src/ DESCRIPTION NAMESPACE
```

Limiting the diff to code-bearing paths avoids noise from unrelated files.

From the diff, summarise:
- **Files changed**: list each changed file and whether it was added, deleted, or modified
- **Functions affected**: scan `+` and `-` diff lines for patterns such as `function(`, `setGeneric(`, `setClass(`, `setMethod(`, `setRefClass(`, `R6Class(`, `export(` — note added (`+`) vs removed (`-`) occurrences; this list is representative and agents may extend it based on what they observe in the diff
- **Scale of change**: lines added and removed

If a diff is very large (> 500 changed lines total), summarise by file rather than by line to avoid context overflow.

Combine the diff summary with the original vague commit message to produce an enriched description to use in subsequent steps.

### 7. Detect Existing NEWS Categories

If the NEWS file already exists, read its content and extract all unique category/section headings currently in use. Examples vary by package — typical headings include `NEW FEATURES`, `BUG FIXES`, `SIGNIFICANT USER-VISIBLE CHANGES`, `DEPRECATED AND DEFUNCT`, `INTERNAL CHANGES`, and others.

Use these detected headings as the allowed category set for the new entries. If no headings can be detected (e.g. the file is new or has no previous entries), present a default set for the user to choose from and allow custom headings.

### 8. Categorise All Changes

For each commit (using the enriched description for previously vague commits), assign it to one of the detected categories:

- Assign based on the content of the message and diff:
  - New exported functions/classes/methods/vignettes → `NEW FEATURES` (or equivalent)
  - Bug/error/warning fixes, test changes → `BUG FIXES` (or equivalent)
  - Removal of exports, `Deprecated`/`defunct` patterns → `DEPRECATED AND DEFUNCT` (or equivalent)
  - Breaking changes, renamed arguments, changed defaults → `SIGNIFICANT USER-VISIBLE CHANGES` (or equivalent)
  - Non-exported code, CI, documentation-only, `DESCRIPTION`-only → `INTERNAL CHANGES` (or equivalent)
- If a commit is ambiguous and cannot be confidently classified, assign it to the most conservative applicable category — typically `INTERNAL CHANGES` or `MISCELLANEOUS` if that heading exists — and always mark it with a `# TODO: verify category` annotation so the user can reclassify it during the preview step

### 9. Draft NEWS Entries

Group entries by category under the upcoming release version heading.

Format entries according to the detected NEWS file format:

**NEWS.md** (markdown):
```markdown
# Changes in version 1.20.0

## NEW FEATURES

- Description of new feature (#abc1234)

## BUG FIXES

- Description of fix (#def5678)
```

**NEWS** (plain text, Bioconductor-style):
```
        Changes in version 1.20.0 (YYYY-MM-DD)
        + NEW FEATURES
        o Description of new feature (commit abc1234)

        + BUG FIXES
        o Description of fix (commit def5678)
```

**NEWS.Rd** (R documentation format):
```
\section{Changes in version 1.20.0}{
  \subsection{NEW FEATURES}{
    \itemize{
      \item Description of new feature (commit abc1234)
    }
  }
  \subsection{BUG FIXES}{
    \itemize{
      \item Description of fix (commit def5678)
    }
  }
}
```

Each bullet/item:
- Is a concise one-liner derived from the commit message (or enriched description for previously vague commits)
- Ends with a short SHA reference or PR number in parentheses for traceability
- Uses `# TODO: verify category` (NEWS.md/NEWS) or a comment equivalent to flag uncertain entries

### 10. Show Preview and Confirm

Display the complete drafted NEWS block in the chat. Also provide a brief summary:
- Total commits processed
- Number of commits that needed diff inspection
- Breakdown of entries by category
- Any entries flagged for manual review

Ask for confirmation before writing:
```
Does this NEWS draft look correct?
  [yes] - write to <filename>
  [edit] - specify which entries to revise
  [abort] - discard and exit
```

If the user requests edits, apply them interactively and show the updated preview again before writing.

**Do not write to disk until the user confirms.**

### 11. Write NEWS File

Once confirmed:
- **Prepend** the new version block to the existing NEWS file (new releases go at the top)
- If no NEWS file existed, create it with just the new block
- Confirm with: `✅ NEWS updated for version X.Y.Z — N entries across K categories written to <filename>`

## Output Format

- A drafted NEWS block displayed in the chat for review prior to any file writes
- Upon user confirmation, the updated (or newly created) `NEWS.md`, `NEWS`, or `NEWS.Rd` file on disk

## Error Handling

- **Not an R package directory** (`DESCRIPTION` missing): abort with "No DESCRIPTION file found — run this skill from an R package root"
- **Not a git repository**: abort with "No git repository found — initialise git first"
- **`git` not on PATH**: abort with "git is not available — install git and ensure it is on your PATH"
- **No commits in range**: report "No new commits since `<starting-commit>` — NEWS is already up to date"
- **No release-bump commit and version ≥ 1.0.0**: prompt the user to supply a starting commit SHA; do not guess
- **No release-bump commit and version < 1.0.0**: use full history and note this appears to be a new package submission
- **Multiple NEWS files found**: list them and ask user which to update
- **Diff too large** (> 500 changed lines for a single commit): summarise by file, note the limitation

## Examples

### Example 1: Clean Commit History

**Invocation**: "Update the NEWS file from recent commits"

**Scenario**: Package with prior releases; all commits since the previous release have descriptive messages.

**Process**:
1. Finds `NEWS.md`, detects existing headings `NEW FEATURES` and `BUG FIXES`
2. Derives release version `1.20.0` from current devel `1.19.4`
3. Finds release-bump commit `"bump x.y.z version to even y prior to creation of RELEASE_3_18 branch"`, then locates the subsequent devel-bump commit `"bump x.y.z version to odd y following creation of RELEASE_3_18 branch"` (`b2c3d4e`)
4. Retrieves 12 commits in range `b2c3d4e..HEAD` — none are vague
5. Categorises and drafts 12 entries
6. Shows preview, user confirms
7. Prepends block to `NEWS.md`

---

### Example 2: Vague Commits Needing Diff Inspection

**Invocation**: "Generate a changelog based on git commits"

**Scenario**: Several commits have messages like "API update", "fix", and "wip".

**Process**:
1. Finds `NEWS.md`; locates release-bump and subsequent devel-bump commit
2. Retrieves 8 commits in range: 5 specific, 3 vague
3. For "API update" (commit `a1b2c3d`): inspects diff, finds `returnSamples()` signature changed — classifies as `SIGNIFICANT USER-VISIBLE CHANGES`
4. For "fix" (commit `e4f5a6b`): inspects diff, finds test file edit — classifies as `BUG FIXES`
5. For "wip" (commit `c7d8e9f`): diff shows only internal helper changes — classifies as `INTERNAL CHANGES`
6. Drafts preview noting 3 commits were diff-inspected
7. User confirms; file updated

---

### Example 3: New Package Submission (version < 1.0.0)

**Invocation**: "Add a NEWS entry for the upcoming release"

**Scenario**: New package submission; `DESCRIPTION` shows `Version: 0.99.3`; no release-bump commit exists.

**Process**:
1. No NEWS file found; asks user which format to create → user selects `NEWS.md`
2. No release-bump commit found; version is `0.99.3` (below `1.0.0`) — treat entire commit history as the range
3. Drafts first-ever NEWS block noting this is a new package submission
4. Shows preview, user confirms
5. Creates `NEWS.md` with the new block

---

### Example 4: No Release-Bump Commit but Version ≥ 1.0.0

**Invocation**: "Update the NEWS file"

**Scenario**: Package is at `1.3.2` on devel but has no release-bump commit (e.g. history was rewritten or imported without full history).

**Process**:
1. Searches git log — no commit matching the release-bump pattern is found
2. Version is `1.3.2` (≥ 1.0.0) — cannot determine range safely
3. Tells the user: "No release-bump commit was found and the version is ≥ 1.0.0. Please specify a commit SHA to use as the starting point for the diff and NEWS entry generation."
4. User provides `f9e8d7c`; skill uses `f9e8d7c..HEAD` as the range and proceeds normally

---

### Example 5: PR Titles Used

**Invocation**: "Draft NEWS entries from git history"

**Scenario**: Repository uses GitHub pull requests merged with squash-merge.

**Process**:
1. Locates release-bump and devel-bump commits to establish range
2. Merge commits parsed; PR titles extracted (e.g. "Add support for TreeSummarizedExperiment input" from PR #45)
3. PR title used in place of merge commit subject "Merge pull request #45 from feature-branch"
4. Richer, human-readable entries appear in draft with `(#45)` reference

## Notes

- This skill assumes the Bioconductor convention where the `devel` branch carries odd-numbered minor versions and each release has an even minor version; no git tags are used or required
- The commit range is derived from the release-bump commit pattern ("bump x.y.z version to even y prior to creation of RELEASE_..."); if that pattern is absent and the version is ≥ 1.0.0, the user must supply a starting commit SHA
- Category headings are inferred from the existing NEWS file; no new heading names are introduced unless the file is new or the user requests them
- Diff inspection is scoped to `R/`, `src/`, `DESCRIPTION`, and `NAMESPACE` to avoid irrelevant noise from documentation or test-only commits
- The skill does not run R or install packages; it relies entirely on `git` and file reads
- For large repositories with hundreds of commits, consider narrowing the range manually if the preview is unwieldy

---

**Related**: See [analyze-r-package](../analyze-r-package/SKILL.md) for package structure analysis. See [SKILL_STANDARD.md](../../SKILL_STANDARD.md) for skill format details.
