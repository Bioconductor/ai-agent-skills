---
name: update-r-news
description: Draft or update an R package NEWS file from git commit history, examining diffs when commit messages are vague
metadata:
  version: 1.3.1
  category: r-packages
  author: bioconductor
  tags: r-packages, documentation, git, changelog, news, bioconductor
---

# update-r-news

Draft or update an R package NEWS file (`NEWS.md`, `NEWS`, or `NEWS.Rd`) from the git commit history since the last release. The skill is designed for Bioconductor packages on the `devel` branch; CRAN and GitHub-only packages are supported with different version and commit-range rules (Step 2).

## Usage

- "Update the NEWS file from recent commits"
- "Add a NEWS entry for the upcoming release"
- "Generate a changelog based on git commits"

## Prerequisites

- Working directory is an R package root (contains `DESCRIPTION`) in a git repository
- Optional: the GitHub CLI (`gh`) and network access, to credit contributors

## Process

### 1. Detect the NEWS File and Format

Look for `NEWS.md`, `NEWS`, and `NEWS.Rd` in the package root and in `inst/`. If more than one exists, ask the user which to update. If none exists, ask which format to create (default: `NEWS.md`).

### 2. Determine the Version Heading

**Package type**: the package is a Bioconductor package if `DESCRIPTION` has a `biocViews` or `BiocType` field.

**CRAN or GitHub package** (neither field): Bioconductor's version rules and release-bump commits don't apply.
- **Heading**: ask the user which version the entries are for. Offer the next version they plan to release, or a `(development version)` heading if the NEWS file already uses one.
- **Commit range**: start from the most recent release tag (e.g. `v1.2.3`) if there is one; otherwise ask the user for a starting commit.

Then continue with Step 4.

**Bioconductor package**: the heading is the upcoming release version, derived from `Version:`. The `devel` branch carries an odd `y` in `x.y.z` and each release an even `y`:
- devel `1.19.4` → `1.20.0`
- devel `0.99.3` or `0.0.14` → `1.0.0`

Any version below `1.0.0` maps to `1.0.0`, the version Bioconductor assigns to a package's first release. Never derive a heading from the pre-release version (`0.99.4`, `0.100.0`), and do not create one heading per pre-release version.

### 3. Determine the Commit Range (Bioconductor packages)

Bioconductor does not tag releases. At each release it applies two commits to every package, with these messages. `x.y.z` and `y` are literal text, not placeholders; only the release number varies:

```
bump x.y.z version to even y prior to creation of RELEASE_3_18 branch
bump x.y.z version to odd y following creation of RELEASE_3_18 branch
```

The most recent "odd y" commit is the start of the range:

```
git log -1 --format=%h --grep="bump x.y.z version to odd y following creation of RELEASE_"
```

Use `<sha>..HEAD`. If no such commit exists:
- Version below `1.0.0`: this is a new package; use the entire history.
- Version `1.0.0` or higher: do not guess. Ask the user for a starting commit.

**Existing entries.** If the NEWS file already has a heading for the upcoming release version, offer to append the commits not yet covered instead of regenerating the block. For a package below `1.0.0` whose NEWS file has pre-release headings (e.g. `0.99.2` or `(development version)`), offer to merge those entries into the `1.0.0` block and remove the pre-release headings.

### 4. Collect Changes and Credit Authors

For a merge commit, use the PR title from the commit body in place of the `Merge pull request #NNN` subject line.

Credit the person who wrote the change. When a change came through a PR (a merge commit, or a squash commit whose subject ends in `(#N)`), cite the PR number and its author, even if the PR fixes an issue someone else reported. When a commit references only an issue, cite the issue and the person who opened it. Look up the username with the call below, taking the repository from `BugReports` or `URL` in `DESCRIPTION` and falling back to the `origin` remote. The `issues` endpoint returns PRs as well:

```
gh api repos/<owner>/<repo>/issues/<number> --jq .user.login
```

If the lookup fails, keep the number without a username and flag the entry in Step 8.

### 5. Inspect Diffs for Vague Commits

When a commit message doesn't say what changed for users (e.g. `fix`, `wip`, `API update`, `minor changes`), read its diff, limited to the paths that carry user-visible changes:

```
git show <sha> --stat --patch -- R/ src/ vignettes/ DESCRIPTION NAMESPACE
```

Look for added, removed, or changed exports, generics, classes, methods, arguments, and defaults. For a commit with more than about 500 changed lines, summarise by file.

`NAMESPACE` can change in layout without changing in meaning: a new roxygen2 version may regroup or reorder directives. Compare the set of `export()`, `import*()`, and `S3method()` directives before and after, and treat a layout-only change as internal.

### 6. Choose Categories

Use the category headings the NEWS file already has, and match its version heading style (e.g. `# pkgname 1.18.0` or `# Changes in version 1.18.0`) and bullet marker. Introduce a new heading only if the user asks.

If the file has entries but no category headings, don't add any. If the file is new, propose this default set and let the user change it, including only headings that receive entries:

| Heading | Changes |
| --- | --- |
| `NEW FEATURES` | New exported functions, classes, methods, vignettes |
| `SIGNIFICANT USER-VISIBLE CHANGES` | Breaking changes, renamed arguments, changed defaults |
| `BUG FIXES AND MINOR IMPROVEMENTS` | Fixes, plus internal changes: dependencies, documentation, CI, tests |
| `DEPRECATED AND DEFUNCT` | Deprecated or removed exports |

Internal changes get an `INTERNAL CHANGES` heading only if the file already has one.

- Omit commits that only change `Version:` in `DESCRIPTION`, including the release-bump commits.
- Combine commits about the same change (e.g. a fix and its follow-up tests) into one entry.
- If the category is uncertain, use `BUG FIXES AND MINOR IMPROVEMENTS` (or the file's equivalent) and mark the entry `# TODO: verify category` (`% TODO: verify category` in `NEWS.Rd`) for the user to resolve in Step 8.

### 7. Draft the Entries

Each entry:
- Is one line written for package users: what changed in behaviour, not how the code changed
- Ends with the issue or PR number and the username from Step 4, only when the commit or PR references one. Use the order the file already uses, or `(#12, @username)` if it has none
- Has no commit SHA; the version heading already says which release the change is in

Bioconductor requires each change to be a list element; don't write prose paragraphs under a heading. For a file with no previous entries, use the `NEWS.md` layout in Example 1, or one of these:

**NEWS** (plain text):
```
        Changes in version 1.20.0 (YYYY-MM-DD)
        + NEW FEATURES
        o Description of new feature

        + BUG FIXES AND MINOR IMPROVEMENTS
        o Description of fix (#12, @username)
```

**NEWS.Rd**:
```
\section{Changes in version 1.20.0}{
  \subsection{NEW FEATURES}{
    \itemize{
      \item Description of new feature
    }
  }
}
```

### 8. Confirm, Then Write

Show the drafted block, with the entries flagged for review (uncertain category, vague commit, author not found). Do not write to disk until the user confirms. Then add the block above the previous release's block (in `NEWS.Rd`, after the `\name` and `\title` header), extend the existing block for the upcoming release, or create the file.

## Examples

### Example 1: Vague commits on a released Bioconductor package

`DESCRIPTION` has `Version: 1.19.4`. The range starts at the "odd y following creation of RELEASE_3_18" commit and holds three commits:

```
c7d8e9f wip
e4f5a6b API update
9a8b7c6 Merge pull request #45 from user/tse-input
```

The diff of `e4f5a6b` shows `returnSamples()` gained a required `assay` argument; the diff of `c7d8e9f` touches only a non-exported helper. The body of `9a8b7c6` gives the PR title "Add support for TreeSummarizedExperiment input", and the lookup for #45 returns `contributor`. The existing `NEWS.md` uses the default headings, `# Changes in version` version headings, and `-` bullets:

```markdown
# Changes in version 1.20.0

## NEW FEATURES

- `importData()` accepts `TreeSummarizedExperiment` input (#45, @contributor)

## SIGNIFICANT USER-VISIBLE CHANGES

- `returnSamples()` now requires an `assay` argument

## BUG FIXES AND MINOR IMPROVEMENTS

- Internal changes to sample lookup
```

The preview flags the last two entries as drafted from diffs, not commit messages.

### Example 2: New submission with pre-release headings

`DESCRIPTION` has `Version: 0.99.3` and `biocViews`, and `NEWS.md` has a `# pkgname 0.99.2` heading. No release-bump commit exists, so the range is the entire history and the heading is `# pkgname 1.0.0`. The skill offers to move the `0.99.2` entries into the `1.0.0` block and remove the `0.99.2` heading.
