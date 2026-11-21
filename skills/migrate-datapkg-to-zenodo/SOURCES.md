# Sources for migrate-datapkg-to-zenodo

Read this file when updating the skill, not when running it.

## Reference implementations

The skill's code lives in these packages, not in the skill. Re-read the newest
one before changing the guidance in steps 2 to 9:

- [curatedBladderData](https://github.com/lima1/curatedBladderData): the
  refactor took the source tarball from 75 MB to 1.4 MB.
- [curatedOvarianData](https://github.com/waldronlab/curatedOvarianData)
- [curatedCRCData](https://github.com/waldronlab/curatedCRCData)

The manifest row in the skill's example was copied from curatedBladderData's
`inst/extdata/zenodo-manifest.csv` on 2026-11-20 (Zenodo record 23192472).

## Design rationale

- **Motivation.** Legacy ExperimentData packages store serialized datasets
  inside the package, which bloats the source tarball to tens or hundreds of MB
  and makes every user download every dataset at install time.
- **Zenodo rather than ExperimentHub.** A citable DOI, md5-verified hosting
  with a public API, and no dependence on a submission pipeline.
  `BiocFileCache` still provides the local caching users expect from Hub
  packages.
- **Checksums refer to the uploaded files.** The xz re-serialization changes
  the bytes (usually shrinking them), so object-level equality to the old
  release is what the integrity report proves, and the manifest md5s cover the
  uploads.
- **Immutable records.** A published Zenodo record cannot be edited, so users
  always get exactly the verified bytes; the cost is a new record version and
  record ID to fix a file.
- **Fixtures.** They exist only so examples, tests, the vignette, and
  `R CMD check` run offline.
- **Zenodo record limits.** 50 GB and 100 files per record. Size quotas can be
  raised by request; the file cap generally cannot.
