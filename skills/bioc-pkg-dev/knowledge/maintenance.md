# Covers: Chapters 24-30 - Bioconductor Package Maintenance

Overview: this knowledge base covers ongoing maintenance and development of packages
already accepted into Bioconductor - git workflow, version numbering, build-report
troubleshooting, C/C++ debugging, deprecation, end-of-life policy, and branch renaming.

## Chapter 24 - Git Version Control (post-acceptance workflow)

Setup after acceptance:

- Register your SSH public key at the BiocCredentials app: `https://git.bioconductor.org/BiocCredentials/`.
  Bioconductor initially seeds from your GitHub keys at `https://github.com/<github-id>.keys`.
- Add the Bioconductor server as the `upstream` remote; keep `origin` = your GitHub repo:

  ```bash
  git remote add upstream git@git.bioconductor.org:packages/<PKG>.git
  git remote -v   # origin -> GitHub, upstream -> git.bioconductor.org
  ```

Sync before editing (pull from BOTH remotes so they stay in step):

```bash
git fetch --all
git merge upstream/devel
git merge origin/devel
```

Commit and push to BOTH remotes (every commit must bump the `z` version - see ch25):

```bash
git add <files>
git commit -m "informative message"
git push upstream devel
git push origin devel
```

Push rules:

- Only two branches accept maintainer pushes: `devel` and the current release branch
  (e.g. `RELEASE_3_6`). New branches CANNOT be created/pushed to the Bioconductor server.
- Use SSH exclusively for developer (read/write) access.

Backport a bug fix from devel to release with cherry-pick:

```bash
git checkout RELEASE_3_6
git cherry-pick <commit-hash>
git push upstream RELEASE_3_6
```

Builds: run once per day and take roughly 24 hours. A valid version bump is required
for any change to propagate; broken packages are not published to users.

## Chapter 25 - Version Numbering

Format is `x.y.z`:

- New (unaccepted) packages start at `0.99.0` in DESCRIPTION. Upstream: "New packages submitted
  to Bioconductor should set Version: 0.99.0 in the DESCRIPTION file." Stated as a "should", but
  it is what reviewers and the build system expect - set it, and treat a wrong version as a
  warning rather than as a reason someone cannot submit.
- `y` (middle): must be ODD in devel, EVEN in release. Maximum value is 99.
- `z` (patch): increment by 1 for EACH git commit in the devel branch.
- `x` (major): only ever changed by the Bioconductor team.

Release transition mechanics:

- At release, a `0.99.z` package becomes `1.0.0` (first official release), and devel
  continues from `1.1.0`.
- Generally, a package at `x.99.z` is bumped to `(x+1).0.0` in release and `(x+1).1.0` in devel.
- For a regular devel version like `1.1.25`, the team creates the release branch at `1.2.0`
  and bumps devel to `1.3.0`.

Critical: commits pushed WITHOUT a corresponding version bump do NOT propagate to the
repository seen by `BiocManager::install()`.

## Chapter 26 - Troubleshooting the Build Report

Propagation timeline:

- The Bioconductor Build System (BBS) pulls code daily around 2:30 PM EST; reports appear
  around 11:30 AM EST next day. Commits after the cutoff slip to the following day
  (36-48h lag possible).
- A valid version bump is ALWAYS required to propagate; broken packages are not published.

Reproduce build failures locally:

1. Match the R version shown at the top of the relevant (devel/release) build report.
2. Update dependencies: `BiocManager::valid()` then `BiocManager::install()`.
3. Apply the build system's environment variables (Renviron.bioc).
4. Consider the official Bioconductor Docker images for a pre-configured environment.

Common error categories:

- R 4.3+: vectors in `if`/`&&`/`||` conditions now error - reduce with `any()`/`all()`.
- R 4.0: missing S3 method registration in NAMESPACE; partial arg matching no longer
  tolerated; `matrix` now extends `array` (use `is()`/`inherits()`, not `class(x) == ...`);
  `data.frame()`/`read.table()` default `stringsAsFactors = FALSE`.
- Dependencies: CRAN binaries may lag a new R version; packages removed from CRAN/Bioc
  force code restructuring; missing system libraries need a GitHub issue report.

## Chapter 27 - Debugging C/C++ Code

Setup:

- Compile without optimization and with debug symbols. Set `CFLAGS=-ggdb -O0`
  (and `CXXFLAGS`) in `~/.R/Makevars`.
- Write a minimal script `buggy.R` that triggers the crash quickly and reliably.

Tools:

- Valgrind (memory errors - invalid reads/writes, corruption behind segfaults):

  ```bash
  R -d valgrind -f buggy.R
  ```

- gdb / lldb (interactive):

  ```bash
  R -d gdb -f buggy.R
  ```

  Key commands: `r` run, `b <function>` breakpoint, `bt` backtrace/call stack,
  `p <var>` inspect a C variable, `call Rf_PrintValue(<Rvar>)` to print an R object at C level.

Workflow: locate the crash frame via `bt` (low-numbered frames are where execution
entered the bad code), inspect nearby state, test a hypothesized fix, rerun, confirm.
Debuggers reveal WHERE a crash happens; you deduce WHY.

## Chapter 28 - Deprecation Guidelines

Applies to functionality present in at least one official release; features added and
removed within the same devel cycle are exempt. Full lifecycle spans ~3 release cycles (~18 months).

Function deprecation - three steps across cycles:

1. Deprecate (this devel cycle): inside the function call `.Deprecated("newFunc")` to emit
   a warning; note the replacement in the man page.

   ```r
   myOldFunc <- function() { .Deprecated("myNewFunc") }
   ```

2. Defunct (next release cycle): replace `.Deprecated()` with `.Defunct()` so the function
   errors instead of running; remove its man page and add it to a `MyPkg-defunct` man page.
3. Remove (following cycle): delete the code and its NAMESPACE export; keep only the defunct
   man page so `help("MyPkg-defunct")` still works.

Datasets:

- S3: add a deprecation class + custom `print` method that warns; next cycle make it error, then remove.
- S4: `setClass()` a deprecation subclass of the original + a `show` method that warns; same timeline.

Whole packages: see the End-of-Life policy (ch29).

## Chapter 29 - Package End-of-Life Policy

The Core Team deprecates packages that:

- Fail to build/check cleanly on all platforms (maintainer gets a final ~2-week notice), or
- Have unresponsive maintainers (must answer support-site questions and package email, and
  keep a valid maintainer email address).

Timeline:

- Step I - Deprecation: ~6-month warning; users see deprecation notices and strikethrough on
  build reports.
- Step II - Defunct: after one devel cycle without a fix, removed from nightly builds and
  from `BiocManager::install()`.
- Final removal: package disappears in the following release cycle.

Recovery: a package can return to active status if fixed within the deprecation period -
contact `maintainer@bioconductor.org`. A fully defunct/removed package must go through full
new-package review again.

Maintainer-initiated: maintainers may voluntarily request deprecation (superseded, outdated,
unmaintainable) by notifying the bioc-devel mailing list.

Orphaned packages: unresponsive-maintainer packages are labeled "orphaned"; community members
can request takeover by emailing the original maintainer and the Bioconductor team.

## Chapter 30 - Branch Rename FAQs

Bioconductor uses `devel` as the default branch name. Only the central repo at
`git.bioconductor.org` is renamed by the core team; maintainers must update their own local
and GitHub clones. Developers/maintainers are affected; end users are not.

Rename a local branch to `devel`:

```bash
git branch -m master devel      # or: git branch -m main devel
git fetch origin
git branch -u origin/devel devel
git remote set-head origin -a
```

On GitHub: change the default branch at
`https://github.com/<username>/<repo>/branches` (edit pencil) to `devel`.

Then push to Bioconductor:

```bash
git checkout devel
git push upstream devel
```

Clean up stale references:

```bash
git remote prune origin --dry-run   # verify
git remote prune origin             # execute
```

Source: [Git version control](https://contributions.bioconductor.org/git-version-control.html) and [Version numbering](https://contributions.bioconductor.org/versionnum.html) and [Troubleshooting the build report](https://contributions.bioconductor.org/troubleshooting-build-report.html) and [Debugging C/C++ code](https://contributions.bioconductor.org/debugging-cc-code.html) and [Deprecation](https://contributions.bioconductor.org/deprecation.html) and [Package end of life policy](https://contributions.bioconductor.org/package-end-of-life-policy.html) and [Branch rename FAQs](https://contributions.bioconductor.org/branch-rename-faqs.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
