---
name: read-mass-spectrometry-data
description: Load raw mass spectrometry data from mzML files into a Bioconductor Spectra object
---

# Read Mass Spectrometry Data

Use the **Spectra** Bioconductor package to load raw mass spectrometry (MS) data
from mzML files. Spectra provides a flexible, memory-efficient representation
for MS data from multiple files.

## Required Packages

```r
BiocManager::install(c("Spectra", "mzR", "MsDataHub"))

library(Spectra)
library(mzR)
```

> **mzR** is required internally to parse mzML files but does not need to be
> called directly.

## Steps

### 1. Obtain mzML file paths

Use any local mzML files, or download example data from **MsDataHub**:

```r
library(MsDataHub)
fls <- c(
    X20171016_POOL_POS_1_105.134.mzML(),
    X20171016_POOL_POS_3_105.134.mzML()
)
fls  # character vector of local file paths
```

### 2. Load spectra from mzML files

```r
sp <- Spectra(fls)
sp

length(sp)  # total number of spectra across all files
```

The `Spectra` object uses an on-disk backend by default, reading data lazily
from the mzML files to keep memory usage low.

### 3. Access spectra metadata and data

```r
# Core spectrum metadata (as a DataFrame)
spectraData(sp)

# m/z and intensity values for a single spectrum
mz(sp)[[1]]
intensity(sp)[[1]]

# Filter spectra, e.g. keep only MS2 spectra
sp_ms2 <- filterMsLevel(sp, msLevel = 2L)
```

## Key Functions

- `Spectra(files)` — create a `Spectra` object from mzML/mzXML file paths
- `spectraData(sp)` — access per-spectrum metadata
- `mz(sp)` / `intensity(sp)` — access m/z and intensity values (as lists)
- `filterMsLevel(sp, msLevel)` — filter by MS level (1 = survey, 2 = fragmentation)
- `length(sp)` — total number of spectra

## Notes

- Spectra supports multiple backends (in-memory, on-disk, SQL) for different
  performance/memory trade-offs.
- Additional processing (peak picking, centroiding, annotation) is available
  through companion packages in the R for Mass Spectrometry ecosystem.

## Further Reading

- [R for Mass Spectrometry book](https://rformassspectrometry.github.io/book/)
- [Large-scale Spectra processing vignette](https://rformassspectrometry.github.io/Spectra/articles/Spectra-large-scale.html)
