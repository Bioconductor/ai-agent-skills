# Package Name

Covers: Chapter 2 - Choosing a package name.

## Core rules

- The package name must match the GitHub repository name and is case-sensitive.
- The name must be unique: it must not already exist in Bioconductor (checked
  case-insensitively) or on CRAN.
- The name should be descriptive of the package's purpose.
- Reusing archived or deprecated package names is strongly discouraged and often
  will not be allowed.

## How to check availability

- Try installing the proposed name; the install should FAIL if the name is free:

  ```r
  BiocManager::install("MyPackage")
  ```

- Alternatively, search the Bioconductor code base / package listings directly.
- Check for unintended meanings in other languages using a tool such as
  wordsafety.com.

## Names to avoid (forbidden / disallowed patterns)

- Names that create confusion with an existing package, function, or class name.
- Names implying temporal relationships (e.g., `ExistingPackage2`) or qualitative
  upgrades (e.g., `ExistingPackagePlus`).
- Hate speech, slurs, or profanity.
- References to historical, ethical, or political contexts.
- Names invoking well-known people, characters, brands, places, or icons.
- Names with unintended meanings in foreign languages.

## Renaming

- Bioconductor discourages renaming a package after acceptance.
- Renaming requires deprecating the old package and resubmitting for review, which
  is time-consuming. Choose carefully up front.

Source: [Package name](https://contributions.bioconductor.org/package-name.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
