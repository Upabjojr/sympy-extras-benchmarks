# Guidance for AI agents and contributors

This repository **translates the benchmark collections of
[sympy-extras](https://github.com/Upabjojr/sympy-extras) into SymPy
expressions**: parsers for the external collections the library is
evaluated on, the tables of published results translated into SymPy
expressions, and the drivers which run the algorithms of sympy-extras over
them. The measurements a run produces are not part of the repository. The
conventions of sympy-extras (`AGENTS.md` there) apply here too; the points
specific to this repository follow.

## What goes where

```
sympy_extras_benchmarks/
    cache.py                 the cache directory of the downloaded data
    datasets/
        maxima_ode.py        parser of Maxima's contrib_ode test files: Kamke and Murphy collections
        smtlib.py            SMT-LIB 2 parser (QF_NRA): the Meti-Tarski family
        solver_regressions.py  SMT-LIB 2 over the integers and with quantifiers: the cvc5 and Z3 regression suites
        prover_syntax.py     the arithmetic grammar the proof-assistant parsers share, and its refusals
                             (chained relations, abs, and the guards for total arithmetic, which
                             read an *unevaluated* parse because SymPy settles arithmetic as it reads)
        lean_tactics.py      the linarith/positivity tests of Lean's mathlib4
        coq_micromega.py     the lia/nia/psatz tests of the Rocq/Coq standard library
        tptp_arithmetic.py   the ARI domain of the TPTP problem library (TFF parser)
        reduce_odes.py       the Postel-Zimmermann ODEs, from REDUCE's ODESolve tests
        pde_symmetries.py    12 classical PDEs with the dimension of their symmetry algebra
        polynomial_systems.py  Katsura and cyclic systems with their invariants
        polynomial_solving.py  systems of polynomial equations: Maxima's algsys regression file
        tests/               parser tests on inline samples (no network, fast)
    oracles/                 independent oracles a driver can check against
        wolfram.py           Mathematica behind a command given with --wolfram
    drivers/                 one module per benchmark, each with main(argv) -> int
    __main__.py              python -m sympy_extras_benchmarks DRIVER [options]
results/                     runs written by --output, ignored by git
.cache/                      downloaded data, ignored by git
```

## Data and licenses

- **Nothing downloaded is committed.** Every dataset is fetched on first use
  into `.cache/` (or `$SYMPY_EXTRAS_BENCHMARKS_CACHE`), which is gitignored.
  The upstream projects and their licences, each read from the licence file
  in the source tree:

  | Source | Upstream | Licence | Local override |
  |---|---|---|---|
  | Kamke/Murphy collections (`maxima_ode`) | Maxima, SourceForge git, mirror `calyau/maxima` | GPL-2.0 | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
  | `algsys` regression file (`polynomial_solving`) | Maxima, `tests/` | GPL-2.0 | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
  | Meti-Tarski `QF_NRA` (`smtlib`) | `dreal/benchmarks` (mirror) | no licence file; SMT-LIB's own terms | `$SYMPY_EXTRAS_BENCHMARKS_SMTLIB` |
  | cvc5 regressions (`solver_regressions`) | `cvc5/cvc5` | modified BSD | — |
  | Z3 regressions (`solver_regressions`) | `Z3Prover/z3test` | MIT | — |
  | mathlib4 tactic tests (`lean_tactics`) | `leanprover-community/mathlib4` | Apache-2.0 | `$SYMPY_EXTRAS_BENCHMARKS_MATHLIB` |
  | Rocq micromega tests (`coq_micromega`) | `rocq-prover/stdlib` | LGPL-2.1 | `$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB` |
  | TPTP `ARI` domain (`tptp_arithmetic`) | tptp.org, official distribution | TPTP's own terms; problems credited in their headers | `$SYMPY_EXTRAS_BENCHMARKS_TPTP` |
  | Postel-Zimmermann ODEs (`reduce_odes`) | `reduce-algebra/reduce-algebra` | Reduce License (BSD 2-clause style) | `$SYMPY_EXTRAS_BENCHMARKS_REDUCE` |

  Only the mathematical content is read: the equations of Kamke's and
  Murphy's books, the formulas and the `:status` of the SMT-LIB problems,
  the binders/hypotheses/conclusion of a Lean or Rocq goal. **Maxima's
  solutions and code are not used, and neither are the assistants'
  proofs.**
- **A new dataset must record its source and licence** in the table above
  and in the `## Sources and licenses` table of `README.md`, together with
  what is read and what is deliberately not read. A source that is looked
  at and rejected goes in the "Surveyed and not used" table of `README.md`,
  with the reason, so that the ground is not covered twice.
- **Published results are facts and may be transcribed** (the dimension of
  a symmetry algebra, the number of solutions of cyclic-7), with the
  reference in the module docstring. Code of other systems must not be
  copied.
- **A dataset in a parsable format gets a parser**, tested on samples
  written for the test (in the syntax of the format, not copied from the
  files). A dataset which only exists as code is translated into SymPy
  expressions in a module of `datasets/`.
- **Read only what the suite actually asserts.** Both proof assistants and
  Maxima record entries that are *not* claims: mathlib marks a goal its
  tactic should fail on with `#guard_msgs`, an `/-- error -/` docstring,
  `fail_if_success`, a deliberately false local `axiom` or `test_sorry`;
  Rocq closes one with `Abort` or `Admitted`; Maxima comments the call out
  entirely. Reading any of them as an oracle produces a false bug report,
  so each parser refuses them and says so in its refusal reason.

## Drivers

- Every driver has `main(argv: Optional[list[str]] = None) -> int`, an
  `argparse` interface documented in the module docstring, prints one line
  per case and a summary, returns 1 when a **wrong** result was found (a
  failure or a timeout is not wrong) and writes a JSON file with `--output`.
- Every call into SymPy or sympy-extras which may not terminate runs under
  `sympy_extras._timeout.attempt` with the `--timeout` of the driver.
- Results are checked against the recorded answers or an independent
  oracle, never against the code's own output; a driver which can use a
  second oracle takes it as a command (``--wolfram``) so that no external
  system is a dependency of this repository; a wrong result is reported
  as `WRONG`/`MISMATCH` and is a bug of sympy-extras (or of the oracle) to
  be fixed there, not worked around here.
- **Runs are never committed.** A run measures one version of sympy-extras
  on one machine under one time limit; it is not part of the datasets and
  goes stale as soon as either side moves. `results/` is ignored by git, and
  neither logs, JSON nor tables of numbers belong in `README.md`. Report a
  run where it is needed, with the exact command line, the SymPy and
  sympy-extras versions and the time limit, which is all that is required to
  reproduce it.

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
