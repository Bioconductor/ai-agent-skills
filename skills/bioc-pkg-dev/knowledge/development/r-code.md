Covers: Chapter 16 - R code

# R Code Style and Best Practices

## Formatting (hard rules)

- Use `<-` for assignment; `=` only for named function arguments.
- Indent with 4 spaces. No tabs.
- No lines longer than 80 characters.
- Space around binary operators: `a == b`. No space around `=` in named
  arguments: `somefunc(a=1, b=2)`.
- Full-line comments start with `##`, indented to surrounding code.

## Naming

- Functions and variables: camelCase starting lowercase (`myFunction`).
- Classes: CamelCase starting uppercase (`MyClass`).
- Do NOT put `.` in function names (avoids S3 dispatch collisions).
- Prefix non-exported/internal functions with a dot: `.internalFunc`.

## Vectorization and iteration

- Write `seq_len(n)` or `seq_along(x)`, NOT `1:n` or `1:length(x)`
  (the latter break when length is 0).
- Prefer vectorized code over explicit `for` loops.
- Use `vapply()` instead of `sapply()` (type-safe).
- Pre-allocate and fill (via `lapply()`/`vapply()`); never copy-and-append in a
  loop (that is O(n^2)).

## Booleans

- Use `TRUE`/`FALSE`, never `T`/`F`.

## Functions

- Write small functions; avoid functions longer than one screen.
- Give arguments defaults where sensible; validate with `stopifnot()` or checks.

## Forbidden patterns

- `set.seed()` inside package/internal code.
- `browser()` left in code.
- Direct slot access with `@` or `slot()` - use accessor methods instead.
- `<<-` (superassignment).
- `system()` without justification - use `system2()`.
- Nested function definitions.
- Commented-out code blocks and TODO comments in published packages.

## Messaging

- `message()` for diagnostic messages.
- `warning()` for unusual-but-handled situations.
- `stop()` for errors.
- `cat()`/`print()` only inside `show()` methods, not for general messaging.

## Classes and methods

- Prefer S4 over S3. Provide constructor functions and `show()` methods.
- Use accessors, not direct slot access.
- Only define methods for classes exported by your own package.
- Reuse existing Bioconductor core classes rather than inventing new ones.

## Web access, caching, parallelism

- Never write to the user home, working, or installed-package directory.
- Cache downloads via BiocFileCache or
  `tools::R_user_dir(package, which="cache")`; use `tempfile()` for scratch.
- Parallel operations should default to 1 or 2 cores.

Source: [R code](https://contributions.bioconductor.org/r-code.html)
Fetched 2026-08-14 from contributions.bioconductor.org (Bioconductor devel guide).
