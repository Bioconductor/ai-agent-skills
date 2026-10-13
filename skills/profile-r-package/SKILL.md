---
name: profile-r-package
description: Measure where an R/Bioconductor package spends its check time and memory, then reduce it against the 10-minute and 8 GB budgets without changing results
version: 1.0.0
category: r-packages
tags: [r-packages, bioconductor, performance, memory, profiling, benchmarking]
author: bioconductor
---

# profile-r-package

Find out where an R/Bioconductor package spends its `R CMD check` time and its peak memory, then
bring both under the Bioconductor expectations while proving the results did not change.
`BiocCheck` cannot measure either figure — they need a real build on a real machine, which
[bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) notes at step 6 before moving on.

The measurement is base R throughout, with GNU `time` for the one figure base R cannot reach.
Ordering matters more than any technique: measure the whole before profiling a part, profile before
editing, verify outputs after. R makes it easy to optimise a function worth 2% of the runtime while
one vignette chunk burns eight minutes.

## Usage

Invoke this skill when a package is too slow or too large to check, or before submission to confirm
it is not:

- "Why does R CMD check take so long on this package?"
- "This package runs out of memory when I build the vignettes"
- "Profile this package and tell me what to fix"

## Prerequisites

- An R package root (contains `DESCRIPTION`), with `R CMD build`/`check` available and the
  package's dependencies installed. Vignette timing additionally needs the package itself installed,
  since a vignette calling `library(<pkg>)` loads it like any user would
- The package already builds and checks without error — a package that fails is not yet a package
  that is slow
- An R build with memory profiling; confirm with `capabilities("profmem")`
- For peak memory, GNU `time` (`/usr/bin/time`, or `-l` rather than `-v` on macOS) — an operating
  system tool, not an R package

## Process

### 1. Establish the budget, and carry its modality forward

Two figures define success **for a Bioconductor package**: they are submission expectations, not R
rules, so a CRAN-only package is not measured against them and should be reported on its own terms.
Neither is a hard requirement, and they are hedged differently — the 10 minutes is a "should", the
8 GB a "recommended". Quote the wording from
[general-dev.md](../bioc-pkg-dev/knowledge/development/general-dev.md) rather than from this skill;
the matching bullets a reviewer ticks sit in the Package Review Checklist that
[bioc-pkg-review](../bioc-pkg-review/SKILL.md) fills.

Carry that modality into every later step, including the final table: a package over either figure
is not blocked from submission, and reporting it as blocked is a defect in the report. Record the
machine and the R and Bioconductor versions — a measurement with no machine attached cannot be
compared to the next one.

### 2. Measure everything in one run

One invocation yields the total, the peak memory and the per-step breakdown. Build first, then:

```
R CMD build .      # writes the tarball into the current directory
_R_CHECK_TIMINGS_=0 /usr/bin/time -v \
    R CMD check --no-build-vignettes --timings <pkg>_<version>.tar.gz
```

Each piece earns its place. `/usr/bin/time -v` supplies the elapsed total and the peak resident set
size, because `R CMD check` reports neither. `--timings` writes the per-example file read in step 3.
`_R_CHECK_TIMINGS_=0` is what makes the check annotate every step with `[user/elapsed]`; without the
variable the threshold is infinite and **nothing is annotated at any duration** (`--as-cran` sets it
to 10 seconds).

`--no-build-vignettes` does **not** exclude vignettes from the measured time: the check still runs
the R code in every vignette and skips only the re-building of vignette *outputs*, so the log shows
`checking running R code from vignettes ... [0s/6s] OK` beside
`checking re-building of vignette outputs ... SKIPPED`. `--no-vignettes` is the flag that skips the
code, reporting both steps `SKIPPED`. Vignette code is therefore inside the 10-minute figure and
vignette rendering is not — and the annotated line gives that split directly. Do not try to recover
it by running the check twice and subtracting: the check does network I/O, and its run-to-run spread
is easily larger than the quantity being measured.

Add `--no-manual` only if `texi2dvi` is missing, and say so — the budget is defined on the plain
command. Compare the total to the budget before going further; if the package is already at three
minutes and 2 GB, stop and say so.

### 3. Attribute the cost to a step, then to a file

The run above already splits the total by step; read those lines first, then drill into whichever
dominates. The log uses typographic quotes, so a pattern written with a straight apostrophe matches
nothing — match the word alone:

```
grep -aE "Running|checking (examples|tests|running R code from vignettes)" <pkg>.Rcheck/00check.log
```

**Examples.** `--timings` writes `<pkg>.Rcheck/<pkg>-Ex.timings`, a tab-separated table of `name`,
`user`, `system` and `elapsed`, one row per Rd topic. Every data row ends in a trailing tab, so it
has five fields against a four-field header, and the default reader silently shifts the columns and
returns `elapsed` as `NA`. Read it positionally:

```r
f <- file.path(paste0(pkg, ".Rcheck"), paste0(pkg, "-Ex.timings"))
tm <- read.delim(f, header = FALSE, skip = 1,
                 col.names = c("name", "user", "system", "elapsed", ""))
head(tm[order(-tm$elapsed), ])
```

**Tests.** The per-file `Running 'file.R' [Us/Es]` lines resolve only as far as the files actually
in `tests/`. A framework driven by a single runner script — `tests/testthat.R` is the common case —
reports one line for the whole suite however many test files sit beneath it, and splitting that
further means asking the framework directly.

**Vignettes.** Measure what the check measures. `checking running R code from vignettes` tangles
each vignette and sources the result; it never weaves or renders. So time the tangled code, not a
full build:

```r
v <- tools::pkgVignettes(dir = ".")$docs[1]
tangled <- tools::buildVignette(v, weave = FALSE, tangle = TRUE)   # returns the .R file written
cat(system.time(source(tangled, echo = TRUE))[["elapsed"]], "s\n")
```

`tools::buildVignette(v)` on its own weaves and renders — exactly the work `--no-build-vignettes`
skips — so its elapsed time overstates the cost against this budget, on a render-heavy vignette by
orders of magnitude. Tangled code comments out `eval = FALSE` chunks and omits `purl = FALSE` ones,
so it is a close but not exact image of what the check runs.

These calls write their outputs into the package directory, as `R CMD build` and the profiler's
`prof.out` do into the working directory. Work on a scratch copy, or remove the generated files, so
the next `R CMD build` does not pick them up.

Name the single largest contributor before continuing. Everything after this applies to it alone.

### 4. Measure peak memory, not allocated memory

Peak and allocated are different questions, and R's own tools answer only the second well.

The 8 GB figure spans the vignettes, examples and tests together, so the number that answers it is
the peak of the whole check — already captured by the `/usr/bin/time -v` wrapper in step 2. To
attribute a peak that is too high, re-run one step alone under the same wrapper. Report it in the
units the tool prints, converting only to compare against the budget, and say which you did.

What that figure is not: GNU `time` reports the high-water mark of the single largest process, never
a sum. The parent process's retained memory is invisible beside a larger child, so the true system
peak can exceed the reported one even with no concurrency at all; across concurrent workers it is
worse, and can report less than the same work run serially. Treat it as a lower bound, and where
the margin matters measure the process tree as a group (a cgroup's `memory.peak`, or a sampler).
Confirm the step succeeded first: a step that errors or reports `SKIPPED` still prints a plausible
peak, and it is the peak of the failure.

`gc()` reports only R's own heap, blind to memory held by compiled code, external pointers and
forked workers — which for these packages is where most of the 8 GB lives. Use it for attribution
inside a session, never for the verdict, and read the megabyte columns positionally: the matrix
carries three columns all named `(Mb)`, so indexing `max used` by name returns a cell count. On
Linux, `readLines("/proc/self/status")` and its `VmHWM` line give the same high-water mark for the
current session in base R, which is useful in-session and useless for a child process.

### 5. Profile the hot path

Only now open the R code. Wrap the one expensive call identified in step 3:

```r
Rprof("prof.out", memory.profiling = TRUE, interval = 0.02)
## ... the expensive call, and nothing else ...
Rprof(NULL)
summaryRprof("prof.out", memory = "both")
```

Read `$by.self` first — time excluding callees, with a `mem.total` column giving allocation per
function. `mem.total` measures allocation *flow*, not occupancy: a function allocating 600 MB
cumulatively may never hold more than a few MB at once, so it locates copying but cannot produce
the 8 GB verdict. To confirm a copy that should not happen, `tracemem(x)` prints every copy of `x`
with the call stack, and `Rprofmem("mem.out", threshold = 1e6)` logs allocations over 1 MB.
`tracemem()` firing repeatedly inside a loop is the signature of the defect in step 6.

Two misreadings to avoid. In byte-compiled code — which installed package code is — time in native
routines is charged to the calling R closure, not to `.Call` (uncompiled code attributes it to
`.Call`, so the same function profiles differently before and after compilation). A thin wrapper
holding nearly all the self time is pointing at compiled code, which no R-level restructuring will
move. And a flat or empty `$by.self` usually means the work is shorter than the sampling interval:
`interval` clamps at a platform floor with a warning (`0.0001` warns and uses `0.01`), so run the
call in a loop and divide rather than lowering it further.

### 6. Classify the finding by cause

The fix follows from the cause. Loop growth, pre-allocation and the default core count are already
documented in
[bioc-pkg-dev/knowledge/development/r-code.md](../bioc-pkg-dev/knowledge/development/r-code.md);
read them there. `tracemem()` from step 5 additionally catches copy-on-modify — a slot of a large
S4 object reassigned in a loop copies the whole object each iteration.

**Parallelism multiplying peak memory** is the cause this skill owns, because it is more often the
origin of a memory failure than the cure for a timing one. Under a forking backend workers share
memory copy-on-write, so a worker that modifies a large shared object materialises its own copy;
under a socket backend every worker receives a full copy immediately. N workers can approach N
times the memory, on a build machine with less of it than yours. Subset large shared objects
*before* passing them to workers, not inside each worker.

**Bypassed infrastructure.** Where the package already depends on Bioconductor infrastructure,
using it generally beats reimplementing it — indexed range overlaps over nested loops, chunked
iteration over whole-file loads (see [bioc-howto](../bioc-howto/SKILL.md)), sparse or on-disk
representations for mostly-zero data. Do not add a dependency purely for speed; that is a design
change. Confirm any class or function against its own documentation, using
[bioc-pkg-finder](../bioc-pkg-finder/SKILL.md) when the right piece is not known.

### 7. Reduce, in order of measured cost

Work down the ranked list from step 3, largest first, one change at a time, re-measuring after
each. Stop as soon as the package is under budget. Where the cost is the data rather than the code,
shrinking an input to the smallest subset that still demonstrates the point is usually the cheapest
fix.

Three reductions carry constraints that are easy to miss, each owned elsewhere. Read the owner
before applying any of them:

- **Wrapping an example** changes how BiocCheck counts runnable examples, against a threshold that
  fails hard. See
  [documentation.md](../bioc-pkg-dev/knowledge/development/documentation.md) and
  [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) step 3.
- **Moving a slow test** out of `tests/` has a time threshold, a required configuration file without
  which the test silently stops running, a different cadence, and a step to take first — all in
  [tests.md](../bioc-pkg-dev/knowledge/development/tests.md), which also notes the mechanism does
  not apply to vignettes.
- **A slow vignette chunk** has its own sanctioned remedies in that same file, caching among them.

That last point needs one distinction: caching *computed results* is sanctioned there, whereas
caching *downloads* with `BiocFileCache` does not reduce a cold build — it makes your second run
fast and leaves the first exactly as slow.

### 8. Verify the results did not change

A performance change is acceptable only if it is provably behaviour-preserving: compare the changed
path's output before and after with `identical()` (or `all.equal()` where floating-point
reassociation is expected), confirm the full suite is green, and re-run step 2 beside the old
figures.

If a substitution changes behaviour at an edge case, say so rather than hiding it. The edge-case
consequences of the common idiom swaps are in [bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) step 7; a
behaviour change belongs in `NEWS`, via [update-r-news](../update-r-news/SKILL.md).

### 9. Report

Use the format below, preserving the modality from step 1. Give the after figures on the same
machine as the before figures, or do not compare them.

## Output Format

```
## Performance: [Package] [version]

Machine: [cores, RAM], R [version], Bioconductor [version]

### Budget vs measured

| Metric                             | Budget (modality)      | Before | After |
|------------------------------------|------------------------|--------|-------|
| R CMD check --no-build-vignettes   | < 10 m (should)        | [x]    | [y]   |
|   of which vignette code (step 3)  | —                      | [x]    | [y]   |
| Peak resident memory               | < 8 GB (recommended)   | [x]    | [y]   |

### Where the cost was

1. [example / vignette / test file] — [n]s, [n]% of total — [cause from step 6]

### Changes made

- [change] — [before] to [after], outputs verified [identical | all.equal]
- Not addressed: [finding] — [why: needs a human decision, or is in compiled code]

### Verdict

[Within both budgets | Above the <metric> expectation by <amount>; not a submission blocker]
```

## Error Handling

- **Not an R package directory** (`DESCRIPTION` missing): abort with "No DESCRIPTION file found —
  run this skill from an R package root"
- **Package fails `R CMD check`**: stop and report the failure. Profiling a broken package measures
  the failure path, not the package
- **Dependencies not installed**: report which. The check time of a package whose dependencies are
  missing is not its check time
- **`/usr/bin/time` unavailable** (minimal container; the absolute path already bypasses any shell
  builtin): on macOS the flag is `-l`, with a different label and units, so match its output rather
  than the GNU wording. The `/proc` reader is **not** a substitute — it sees only the current
  session, not the check's child processes. Without a process-tree measurement, report the memory
  figure as unobtained rather than guessing
- **`capabilities("profmem")` is `FALSE`**: fall back to `gc()` deltas and `tracemem()`
- **Profile is empty**: the call was shorter than the sampling interval. Run it in a loop and
  divide; do not keep lowering `interval`, which clamps at a platform floor
- **Timings vary between runs**: re-run idle and report the median, not the best run

## Examples

### Example 1: A package already within budget (real run)

jsonlite 2.0.0 on R 4.6.1. The step 2 command gave 48.78s elapsed and a peak resident set size of
161900 kbytes (about 158 MiB), with examples 1.07s (`stream_in` largest at 0.83s) and tests 6s.
Both figures sit far inside the Bioconductor expectations, so the workflow stops after attribution
and reports. No profiling, no edits. This is the common outcome and the correct one.

Four things that run says about the environment rather than the package, all of which belong in the
report. A second run of the identical command on the identical tarball gave 30.63s against 48.78s —
a 59% swing with nothing changed, from network access during the dependency step, which is why two
runs cannot be subtracted to isolate anything smaller than that spread. Missing suggested packages
made the check ERROR until suggests were relaxed, after which both vignette steps reported
`SKIPPED`; a skipped step is not a fast step, so this is not the package's true check time. The 34
test files appear as one `testthat.R` line, so the 6s is the whole suite. And on the second run the
examples step itself reported `ERROR` — by this skill's own rule those numbers describe the failure
path, not the package.

---

### Example 2: Vignette code dominates the measured check

The annotated check reports 14 minutes total, of which
`checking running R code from vignettes ... [9m/10m]` — vignette code running *inside* the measured
check. Tangling each vignette and sourcing it attributes most of that to one, and then to a chunk
running over the full example dataset: data volume, not algorithm. Cut to one chromosome, outputs
keep their meaning, tests stay green, check drops to 5m. The sanctioned remedies for a slow chunk
are in `tests.md`.

---

### Example 3: Parallelism multiplying peak memory

Vignette building is killed on a 16 GB machine. The step is parallel, so GNU `time`'s figure is a
lower bound and the worker tree is measured as a group. `gc()` shows R's heap under 2 GB, so the
heap is not the problem: each worker receives a full copy of a large shared annotation object. The
object is subset *before* being passed to workers rather than inside them, and the worker count
brought back to the small default `r-code.md` calls for. Results `identical()`, tests green, peak
3.1 GB.

---

### Example 4: A slow test that should stay where it is

Check at 12m30s; the annotated log shows one integration test file at 6 minutes, and shrinking its
input would stop it testing what it tests. Before moving it, `tests.md` is consulted: the threshold
governing `tests/` is far higher than the whole-check figure in `general-dev.md`, so this test is
nowhere near it and moving it is not indicated. Those two numbers sit in tension upstream — this
skill reports that rather than deciding which governs, and a package caught between them is a
question for bioc-devel. The reduction is taken against the next-largest contributors instead:
nothing deleted, the test still running, and the report recording that it was left in place
deliberately.

## Notes

- The measurement workflow is base R. `profvis` adds a flame graph over the same sampler and
  `bench` adds repeated-iteration statistics, but no step requires either
- Profiling says where time goes, not whether the algorithm is right. A well-profiled nested loop
  over genomic ranges is still the wrong approach when an indexed overlap method exists
- This skill does not submit, check or review the package; run
  [build-check-bioccheck](../build-check-bioccheck/SKILL.md) for the gate. That gate's check uses
  different flags, so its elapsed time is not this figure. `bioc-pkg-review` reports check time and
  memory as needing a human, and this skill produces those figures for a person to carry across
  rather than feeding them to it

- Verified on R 4.6.1, 2026-10-13, against three released packages: jsonlite 2.0.0 (testthat, 3
  knitr vignettes), digest 0.6.39 (tinytest, 2 vignettes) and R6 2.6.1 (testthat, no vignettes).
  Steps 2 to 4 ran on all three, and the `-Ex.timings` reader trap reproduced on every one:
  `elapsed` came back all `NA` under the default reader in each case. (The row count varies with
  whether the examples step ran to completion, so it is not the thing to check.) Both test
  frameworks collapsed to a single runner line. Limits that bound what this proves: no vignette builder was installed for
  jsonlite or digest and R6 has no vignettes, so vignette code never ran inside a real check, and
  the flag behaviour in step 2 and the tangle-versus-build gap in step 3 were established on
  purpose-built packages instead; and all three were inside both budgets, so steps 5 to 8 were
  never exercised against a real over-budget package

---

**Related**: See [build-check-bioccheck](../build-check-bioccheck/SKILL.md) for the validation gate,
[bioc-pkg-dev](../bioc-pkg-dev/SKILL.md) for the submission workflow these budgets belong to,
[bioc-pkg-review](../bioc-pkg-review/SKILL.md) for the self-review that reports these two items as
needing a human, and [improve-code-coverage](../improve-code-coverage/SKILL.md) for test quality
once the suite is fast enough to run often. See [SKILL_STANDARD.md](../../SKILL_STANDARD.md) for skill format details.
