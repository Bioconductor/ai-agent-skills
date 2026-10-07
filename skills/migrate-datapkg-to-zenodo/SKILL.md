---
name: migrate-datapkg-to-zenodo
description: Convert a legacy Bioconductor experiment data package that ships .rda files in data/ to on-demand download from Zenodo with BiocFileCache caching, keeping data() backward compatible and R CMD check offline
version: 1.1.1
category: r-packages
tags: [r-packages, bioconductor, experiment-data, zenodo, biocfilecache, data-hosting, refactoring]
author: bioconductor
---

# migrate-datapkg-to-zenodo

Legacy Bioconductor ExperimentData packages store serialized datasets (`data/*.rda`)
inside the package, bloating the source tarball to tens or hundreds of MB and
forcing every user to download every dataset at install time. This skill converts
such a package to the modern pattern: per-dataset files hosted on a citable Zenodo
record, downloaded individually on first use into a package-specific
`BiocFileCache`, verified against md5 checksums, with legacy `data()` access kept
working and `R CMD check` running entirely offline on small bundled fixtures.
Zenodo is the default host; step 8 covers substituting another hosting service
when the user asks for one.

Reference implementations (the canonical code; copy from the newest and keep
copies in sync):

- [curatedBladderData](https://github.com/lima1/curatedBladderData)
  (75 MB tarball to 1.4 MB)
- [curatedOvarianData](https://github.com/waldronlab/curatedOvarianData)
- [curatedCRCData](https://github.com/waldronlab/curatedCRCData)

## Usage

- "Convert this data package to Zenodo and BiocFileCache"
- "Move the datasets in this package out of data/ and host them on Zenodo"
- "Refactor this legacy experiment data package so it stops shipping .rda files"
- "Move this package's datasets to download-on-demand from
  [OSF / figshare / our institutional repository / an S3 bucket]"

## Prerequisites

- A checkout of the package with the full `data/*.rda` files present (if they were
  already removed, restore them from git history first).
- A Zenodo account that can create and publish records (upload itself is manual,
  through the web UI or Zenodo API). A single Zenodo record holds at most 50 GB
  and 100 files; if the compressed datasets exceed either limit, split them
  across several records (the manifest already carries one URL per file, so
  files may live on different records) or use another host (see "Using a host
  other than Zenodo" in step 8). Zenodo grants one-off size quota increases on
  request, but do not count on the 100-file cap moving, and zipping datasets
  together would defeat per-dataset download.
- The reference implementations above, for copying `R/getData.R` and
  `inst/scripts/`. Only the package name differs between their copies.
- Datasets in the references are `ExpressionSet`s, but the pattern is
  class-agnostic: each `.rda` holds one object whose name matches the file name.

## Process

### 1. Survey the package and tag the last data-shipping commit

- Enumerate `data/*.rda`: names, sizes, object classes. Confirm each file contains
  exactly one object named after the file.
- Find every consumer of `data(X)`: vignettes, examples, man pages, bundled
  analysis scripts (e.g. `inst/extdata/createEsetList.R` in the curated*Data
  family), and tests.
- Tag the current commit `pre-zenodo-refactor` and push the tag. The integrity
  report (step 8) checks out this tag in a git worktree to prove the uploaded
  objects are identical to what the package used to ship, so the tag is
  load-bearing, not cosmetic.

### 2. Add the regeneration scripts in inst/scripts/

Copy all three scripts from a reference implementation and change only the
package-specific parts (they detect the package name from `DESCRIPTION` where
possible):

- `make-data.R`: re-serializes every `data/*.rda` with `compress = "xz"` into a
  sibling directory `../<pkg>-zenodo-upload/`, and writes:
  - `zenodo-manifest.csv` with columns `dataset, filename, url, md5, size_bytes`
    (URLs contain the placeholder `RECORD_ID` until the record is published);
  - the `data/` stub files and `datalist` (step 4);
  - `upload-manifest.txt` for eyeball comparison against Zenodo's reported md5s.

  It must be idempotent: already-compressed files are left untouched, so
  re-running it with the record ID after publishing only rewrites the manifest.
  Never regenerate the `.rda` files after uploading; the manifest checksums must
  match the published bytes.
- `make-test-data.R`: builds small offline fixtures in `inst/extdata/testdata/`,
  one per dataset, subset to roughly the first 200 features and at most 100
  samples with full sample metadata retained. Also keep any specific features the
  vignette or examples reference by name (gene symbols, probe patterns), or the
  vignette will break on the fixtures.
- `data-integrity-report.Rmd`: see step 8.

### 3. Add the getter in R/getData.R

Copy `R/getData.R` from a reference implementation, changing `.pkgname` and the
exported function name (the getter is named after the package, the established
convention in this family). Its behavior:

- The manifest in `inst/extdata/zenodo-manifest.csv` is the only place download
  URLs live.
- Cache: `BiocFileCache::BiocFileCache(tools::R_user_dir(.pkgname, "cache"))`,
  package-specific so removing the package's cache cannot disturb anything else.
- Fresh downloads are verified against the manifest md5; on mismatch the corrupt
  entry is evicted and the download retried once, then errors informatively.
- Cache hits are verified with a cheap `size_bytes` comparison (a full md5 on
  every load would be slow); a wrong-sized cached file is evicted and
  re-downloaded. This is why `size_bytes` in the manifest must be exact: a wrong
  value silently evicts and re-downloads a good file on every call.
- Exported getter: no arguments lists dataset names (no download); one name
  returns the object; several names return a named list; `test = TRUE` loads the
  offline fixtures from `inst/extdata/testdata/` instead of downloading.
- `.stubLoad(name)` backs the `data()` stubs: it emits a once-per-session
  deprecation message, and under the package's own `R CMD check` it resolves to
  the offline fixture so checking needs no network, while checks of reverse
  dependencies get the real data:

  ```r
  if (identical(Sys.getenv("_R_CHECK_PACKAGE_NAME_"), .pkgname))
      return(.loadOne(name, test = TRUE))
  ```

### 4. Replace data/ with stubs

- Delete every `data/*.rda` (git preserves them at the `pre-zenodo-refactor` tag).
- Install the stub files generated by `make-data.R`, one `data/<name>.R` per
  dataset, so `data(X)` keeps working lazily:

  ```r
  delayedAssign("GSE89_eset",
      curatedBladderData:::.stubLoad("GSE89_eset"),
      assign.env = environment())
  ```

- Keep (or create) `data/datalist` listing one dataset name per line. Without it,
  installation executes the stubs, downloading everything at install time.
- In `DESCRIPTION`, add `BuildResaveData: no` so `R CMD build` does not execute
  the stubs and re-save the downloads as `.rda`, and remove `LazyData` if present.

### 5. Update DESCRIPTION and NAMESPACE

- `Imports: BiocFileCache, tools, utils` (plus whatever the data class needs,
  e.g. `Depends: Biobase` for `ExpressionSet`s).
- `NAMESPACE`: export the getter; `importFrom(BiocFileCache, BiocFileCache,
  bfcrpath, bfcquery, bfcremove)`, `importFrom(tools, md5sum, R_user_dir)`,
  `importFrom(utils, read.csv)`.
- Mention the hosting and caching in `Description:`, bump the version, and add a
  `NEWS.md` entry covering: data moved to Zenodo, the new getter, deprecated but
  working `data()`, the cache location, and the tarball size change.

### 6. Update documentation and bundled scripts

- Add a man page for the getter (copy the reference `man/<pkg>.Rd`): arguments,
  return value for each calling pattern, cache location and how to clear it, and
  examples that use `test = TRUE`.
- Fix the package-level man page if it still describes the old access pattern.
- Vignette: add a short "Data access and caching" section (where the data lives,
  cache directory, deprecation of `data()`), switch all loads to the getter, and
  run the whole vignette on the fixtures (`test = TRUE`) so building it is
  offline. Note in prose that real analyses should omit `test = TRUE`.
- Bundled analysis scripts that load all datasets (e.g. `createEsetList.R`) should
  loop over the getter's dataset listing, with a `test.mode` switch so the
  vignette can drive them offline.

### 7. Add tests

Copy `tests/testthat/test-getData.R` from a reference implementation and adapt:

- Hard-code the expected dataset names in the test file; this guards the manifest
  against silently losing rows.
- Manifest well-formedness: filenames are `<dataset>.rda`, md5s match
  `^[0-9a-f]{32}$`, URLs match the Zenodo records pattern, sizes are positive.
- Lock-step check: manifest datasets == fixture files == `data()` stubs.
- Getter behavior on fixtures: single object, named list, class, informative
  error on unknown names.
- `data()` stub creates a working binding (force it with the
  `_R_CHECK_PACKAGE_NAME_` guard set so no network is needed).
- One opt-in live test (`skip_on_bioc()`, gated on an environment variable such
  as `RUN_FULL_DOWNLOAD_TESTS`, plus `skip_if_offline("zenodo.org")`) that
  downloads the smallest dataset and confirms the second call hits the cache.

### 8. Upload to Zenodo and finalize the manifest

1. Run `Rscript inst/scripts/make-data.R` (placeholder URLs) to produce
   `../<pkg>-zenodo-upload/`.
2. Create a new Zenodo record and upload the compressed `.rda` files. Metadata
   conventions from the reference records:
   - Title: `<pkg>: <short data description> for Bioconductor`.
   - Description: states these are the serialized objects for the Bioconductor
     package `<pkg>`, downloaded on demand by the package.
   - Creators: the package authors, with ORCIDs.
   - License: the terms the data are actually redistributable under, which is
     not automatically the package's software license. Verify that
     redistribution is permitted for every dataset and document each dataset's
     source; when the package has long shipped the data, the license it was
     already distributed under is usually correct, but source data can carry
     their own terms.
   - Related identifier: the package's GitHub URL, relation `isSupplementedBy`,
     resource type software.
3. Publish, note the record ID, and compare Zenodo's displayed checksums against
   `upload-manifest.txt`.
4. Re-run `Rscript inst/scripts/make-data.R <RECORD_ID>`; this rewrites only the
   manifest with real URLs. Copy `zenodo-manifest.csv` to `inst/extdata/`.

#### Using a host other than Zenodo

Zenodo is the default, but if the user names another service, the pattern
carries over: everything in `R/getData.R` is host-agnostic, because the
manifest is the only place URLs live. Any host works that serves stable,
versioned, direct-download HTTPS URLs without authentication: an institutional
repository, OSF, figshare, Dataverse, or a lab-controlled S3 bucket or web
server. Avoid hosts that cannot guarantee immutable content at a fixed URL,
and avoid the hosts Bioconductor review rejects for package data: GitHub
(including release assets), Dropbox, Google Drive, and personal homepages.
Adapt the Zenodo-specific pieces:

- `make-data.R`: change the URL template to the new host's download URL scheme.
- The manifest URL regex in the testthat suite: relax or retarget it.
- Integrity report section 2: replace the Zenodo API checksum comparison with
  the host's equivalent (its API, or downloading each file once and comparing
  md5s locally if the host exposes no checksums).
- Record metadata (step 8.2): apply the same conventions as far as the host
  supports them; prefer hosts that mint a DOI so the data remain citable.
- Name the manifest and scripts after the host (or neutrally, e.g.
  `data-manifest.csv`) so the code does not claim Zenodo while pointing
  elsewhere.

### 9. Verify with the data integrity report

Knit `inst/scripts/data-integrity-report.Rmd` from a package checkout. It must
pass all three sections before merging:

1. Every uploaded object is `all.equal` to the object shipped at the
   `pre-zenodo-refactor` tag (checked out via `git worktree`). Compare each
   component (for `ExpressionSet`s: exprs, pData, fData, annotation,
   experimentData), not just the whole object.
2. The manifest md5s and `size_bytes` match both the local upload files and what
   the Zenodo API reports for the record
   (`https://zenodo.org/api/records/<RECORD_ID>`).
3. A real download through the getter works and the second call hits the cache,
   using a throwaway cache (`R_USER_CACHE_DIR` pointed at a tempdir) so the
   user's real cache is untouched.

Because the manifest md5s equal the md5s of byte-identical uploads, sections 1
and 2 together prove every Zenodo file; only one download needs exercising end
to end.

Then run `R CMD check` (must pass with no network) and the full test suite with
the live-download test enabled.

### 10. Commit and propagate

- Agents follow the commit gates in
  [AGENTS.md § Agent Responsibilities](../../AGENTS.md#agent-responsibilities):
  show a draft commit message and obtain explicit approval before each commit,
  and acknowledge the AI agent with a co-author trailer.
- Two-commit convention from the references: first "Move datasets to Zenodo with
  BiocFileCache caching" (all code, placeholder URLs), then "Finalize Zenodo
  manifest for record NNNN" after publishing and verification.
- `R/getData.R`, the three `inst/scripts/` files, and the test file are
  intentionally duplicated across the sibling curated*Data packages. Each copy
  carries a header comment naming its siblings; when changing one, update the
  others and their header lists.

## Output Format

A pull request against the package containing: `R/getData.R` with the exported
getter, `inst/extdata/zenodo-manifest.csv` with published URLs,
`inst/extdata/testdata/` fixtures, `data/` stubs plus `datalist`, `inst/scripts/`
regeneration and verification scripts, testthat tests, updated DESCRIPTION,
NAMESPACE, NEWS, man pages, and vignette, and a published Zenodo record whose
checksums the integrity report has verified.

## Examples

**User**: "curatedPancreasData still ships 120 MB of .rda files; move it to
Zenodo like the other curated*Data packages"

**Agent**: Tags `pre-zenodo-refactor`; copies `R/getData.R`, `inst/scripts/`,
and the tests from curatedBladderData, renaming the getter
`curatedPancreasData`; runs `make-data.R` and `make-test-data.R`; converts
`data/` to stubs; updates DESCRIPTION, NAMESPACE, docs, and vignette; asks the
user to upload `../curatedPancreasData-zenodo-upload/` to a new Zenodo record;
after publication re-runs `make-data.R <RECORD_ID>`, installs the final
manifest, knits the integrity report, and runs check plus the live download
test.

## Notes

- Why Zenodo rather than ExperimentHub: a citable DOI, md5-verified hosting with
  a public API, and no dependence on a submission pipeline; `BiocFileCache`
  still provides the local caching users expect from Hub packages. The pattern
  suits legacy packages where a full ExperimentHub conversion is not worth the
  churn.
- The xz re-serialization changes the bytes (usually shrinking them), so all
  checksums refer to the uploaded files; object-level equality to the old
  release is what the integrity report proves.
- Zenodo records are immutable once published. Fixing a bad file means a new
  record version, a new record ID, and re-running `make-data.R <RECORD_ID>`;
  this is a feature (users always get exactly the verified bytes).
- Zenodo limits a single record to 50 GB total and 100 files. Check the
  compressed upload size and dataset count that `make-data.R` reports before
  creating the record; above either limit, split files across multiple records
  or switch hosts (step 8). Size quotas can be raised by request; the file cap
  generally cannot, and zipping would defeat per-dataset download.
- Keep the fixtures small (tens of KB each); they ship in the tarball and exist
  only so examples, tests, the vignette, and `R CMD check` run offline.
- If the package's git history is itself bloated by the old `.rda` files, that
  is a separate problem; do not rewrite history as part of this refactor, since
  the `pre-zenodo-refactor` tag and the integrity report depend on it.
