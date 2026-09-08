# Guidance for AI agents and contributors

This repository holds the **benchmark datasets and drivers of
[sympy-extras](https://github.com/Upabjojr/sympy-extras)**: parsers for
the external collections the library is evaluated on, the tables of
published results translated into SymPy expressions, the drivers which run
the algorithms of sympy-extras on them, and the recorded results. The
conventions of sympy-extras (`AGENTS.md` there) apply here too; the points
specific to this repository follow.

## What goes where

```
sympy_extras_benchmarks/
    cache.py                 the cache directory of the downloaded data
    datasets/
        maxima_ode.py        parser of Maxima's contrib_ode test files: Kamke and Murphy collections
        smtlib.py            SMT-LIB 2 parser (QF_NRA): the Meti-Tarski family
        pde_symmetries.py    12 classical PDEs with the dimension of their symmetry algebra
        polynomial_systems.py  Katsura and cyclic systems with their invariants
        tests/               parser tests on inline samples (no network, fast)
    drivers/                 one module per benchmark, each with main(argv) -> int
    __main__.py              python -m sympy_extras_benchmarks DRIVER [options]
results/                     logs and JSON of the recorded runs (see README.md)
.cache/                      downloaded data, ignored by git
```

## Data and licenses

- **Nothing downloaded is committed.** Maxima's test files are GPL and
  the SMT-LIB files carry their own terms: the parsers fetch them on first
  use into `.cache/` (or the directory named by
  `$SYMPY_EXTRAS_BENCHMARKS_CACHE`) and only the mathematical content is
  read: the equations of Kamke's and Murphy's books, the formulas and the
  `:status` of the SMT-LIB problems. Maxima's solutions and code are not
  used. Local copies can be pointed to with
  `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` and `$SYMPY_EXTRAS_BENCHMARKS_SMTLIB`.
- **Published results are facts and may be transcribed** (the dimension of
  a symmetry algebra, the number of solutions of cyclic-7), with the
  reference in the module docstring. Code of other systems must not be
  copied.
- **A dataset in a parsable format gets a parser**, tested on samples
  written for the test (in the syntax of the format, not copied from the
  files). A dataset which only exists as code is translated into SymPy
  expressions in a module of `datasets/`.

## Drivers

- Every driver has `main(argv: Optional[list[str]] = None) -> int`, an
  `argparse` interface documented in the module docstring, prints one line
  per case and a summary, returns 1 when a **wrong** result was found (a
  failure or a timeout is not wrong) and writes a JSON file with `--output`.
- Every call into SymPy or sympy-extras which may not terminate runs under
  `sympy_extras._timeout.attempt` with the `--timeout` of the driver.
- Results are checked against the recorded answers or an independent
  oracle, never against the code's own output; a wrong result is reported
  as `WRONG`/`MISMATCH` and is a bug of sympy-extras (or of the oracle) to
  be fixed there, not worked around here.
- Recorded runs go into `results/` (log and JSON) and are summarised in
  `README.md` with the exact command line, the SymPy and sympy-extras
  versions and the time limit.

## Types and checks

Strict type stability as in sympy-extras: every function annotated, no
`Any`, `cast`, `getattr` or `# type: ignore`, SymPy values narrowed with
`sympy_extras._typing` (`as_expr`, `as_boolean`). Before committing:

```
python -m pytest              # parser tests and doctests, no network
python -m mypy                # Success: no issues found
python -m pyflakes sympy_extras_benchmarks conftest.py
```

The unit tests must stay fast and offline; the benchmarks themselves are
run by hand.
