Covers: Chapter 21 - .gitignore

# .gitignore

- Keep a single `.gitignore` file at the top level of the package. Do not nest
  multiple `.gitignore` files.
- Certain system/generated files must NOT be tracked. BiocCheck flags them if
  committed. They may exist locally but must be excluded.

## Files that must be excluded (BiocCheck-flagged)

Configuration and history:

- `.Renviron`, `.Rprofile`, `.Rhistory`, `.RApp.history`
- `.Rproj`, `.Rproj.user`
- `.seed`, `.exrc`, `.gdb.history`

Build artifacts and compiled objects:

- `.o`, `.sl`, `.so`, `.dylib`, `.a`, `.dll`, `.def`
- `.log`, `.aux`, `.backups`

System and IDE files:

- `.DS_Store` (macOS)
- `.project`, `.cproject`, `.settings`, `.tm_properties`
- `.directory`, `.dropbox`
- `unsrturl.bst`

Git metadata that should not be present:

- `.gitattributes`, `.gitmodules`, `.hgtags`

## Notes

- Do not commit build tarballs (`*.tar.gz`) or the `*.Rcheck/` directory.
- Do not commit large data files (see data chapter); they belong in a Hub.

Source: [.gitignore](https://contributions.bioconductor.org/gitignore.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
