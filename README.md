# sympy-extras-benchmarks

This repository **translates the benchmark collections of
[sympy-extras](https://github.com/Upabjojr/sympy-extras) into SymPy
expressions**. Every dataset the library is evaluated on reaches SymPy in
one of two ways:

- **parsers** for the collections which exist in a parsable format (they are
  downloaded on first use, nothing of the files is stored here), and
- **translations into SymPy expressions** of the tables which only existed
  as code.

A dataset, once translated, is an ordinary sequence of SymPy objects: the
equations, the formulas and the published answers, usable from any script.
The drivers here are one such use, running the algorithms of sympy-extras
over a dataset and checking the results against the recorded answers or an
independent oracle. The numbers a run produces are not part of the
repository (see [Results](#results)).

## Datasets

| Module (`sympy_extras_benchmarks.datasets`) | Data | Format and source | Size |
|---|---|---|---|
| `maxima_ode` | The Kamke collection of first and second order ODEs and the Murphy collection of first order ODEs (first degree and higher degree), as transcribed in the test suite of Maxima's `contrib_ode` | Maxima `.mac` test files, parsed by a recursive descent parser for Maxima expressions; sparse checkout of Maxima's git repository on SourceForge (GitHub mirror as fallback) | 1159 equations: kamke1 418, kamke2 422, murphy1 159, murphy2 160 |
| `smtlib` | The Meti-Tarski family of SMT-LIB `QF_NRA` (proof obligations on polynomial bounds of special functions, each with its `:status`) | SMT-LIB 2 files, parsed to SymPy formulas; sparse clone of the `dreal/benchmarks` mirror on GitHub | 7713 problems (5025 sat, 2688 unsat), 3 to 8 real variables |
| `solver_regressions` | The arithmetic problems of the cvc5 and Z3 regression suites: the cases which once broke a solver, over the **integers** as well as the reals and with quantifiers, each with the answer recorded in a `; EXPECT:` header or in `:status` | SMT-LIB 2 files, parsed to SymPy formulas (the s-expression reader of `smtlib` plus the integer sorts, `div`/`mod`/`abs`/`divisible` and the quantifiers); sparse clones of `cvc5/cvc5` and `Z3Prover/z3test` on GitHub | 1593 files, 316 arithmetic problems (166 with a recorded answer), 106 over the integers, 87 quantified |
| `lean_tactics` | The tactic tests of Lean's **mathlib4** for arithmetic (`linarith`, `positivity`), polynomial identities (`linear_combination`, `ring`) and numeral evaluation (`norm_num`), each with a machine-checked proof | Lean 4 `example` blocks, parsed to SymPy formulas by the grammar of `prover_syntax`; sparse clone of `leanprover-community/mathlib4` on GitHub | 13 files, 1573 examples, 443 usable goals of which 323 are not settled by SymPy's own evaluation |
| `coq_micromega` | The **micromega** test suite of the Rocq/Coq standard library (`lia`, `nia`, `lra`, `psatz`): mostly nonlinear goals over `Z`, `Q`, `R` and `nat`, one file per historical bug, each closed by `Qed` | Rocq `Lemma`/`Goal` statements, parsed to SymPy formulas by the grammar of `prover_syntax`; sparse clone of `rocq-prover/stdlib` on GitHub | 38 files, 285 statements, 119 usable goals (none of them trivial), 105 over the integers |
| `polynomial_solving` | The systems of Maxima's `algsys` regression file (`tests/rtest_algsys.mac`): the examples of Beyer (1984) and Morgan (1983), plus the ones that later broke `algsys` — positive-dimensional components, solutions real in the paper and complex in fact, and one where the published answer is wrong | Maxima `.mac`, read with the expression parser of `maxima_ode`; the recorded solutions are counted but are not the answer key | 51 systems, 1 to 13 equations, 1 to 6 unknowns |
| `pde_symmetries` | Twelve classical PDEs (heat, Burgers, KdV, wave, nonlinear diffusion, Fisher, Boussinesq, Liouville, sine-Gordon, potential Burgers, Black-Scholes) with the dimension of their point symmetry algebra from Olver, Bluman-Kumei and Ibragimov's handbook | translated into SymPy expressions | 12 equations |
| `polynomial_systems` | The Katsura-m and cyclic-m systems with their known invariants (dimension, number of solutions, radicality) | generated as SymPy expressions | Katsura 2-6, cyclic 3-7 |

The Maxima parser (`parse_expression`) understands the operators
`+ - * / ^ ** !`, the equality `=`, function calls, the noun form
`'diff(y, x, n)` and Maxima's names (`%e`, `%pi`, `bessel_j`,
`legendre_p`, ...); the dependent variable becomes `y(x)`, other applied
names undefined functions (`f(x)`) and other names symbols. The previous
translator of sympy-extras (regular expressions followed by
`parse_expr`) handled 722 of the 1160 equations; the parser handles 1159
(the one left is a cross-reference, `ode[394]`). The SMT-LIB parser
handles `let`, `ite`, `distinct`, `=>`, `xor`, `define-fun` constants and
chained relations; all 7713 files translate.

```python
>>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_equation
>>> parse_equation("x*'diff(y,x)^2 - y*'diff(y,x) + a = 0")
a + x*Derivative(y(x), x)**2 - y(x)*Derivative(y(x), x)
>>> from sympy_extras_benchmarks.datasets.smtlib import translate
>>> translate("(declare-fun x () Real) (assert (let ((?v (* x x))) (< ?v 2)))").formula
x**2 < 2

```

Loading a collection downloads it on first use into `.cache/`:

```python
from sympy_extras_benchmarks.datasets.maxima_ode import load
entries = load(('kamke1', 'murphy2'))
entries[0].equation, entries[0].order, entries[0].method
```

## Installation

```
pip install git+https://github.com/Upabjojr/sympy-extras
pip install -e .
```

## Running the benchmarks

```
python -m sympy_extras_benchmarks --list
python -m sympy_extras_benchmarks kamke_odes --collections kamke1 --limit 60 --timeout 15 --output results/kamke1.json
python -m sympy_extras_benchmarks linear_odes --limit 60 --timeout 10
python -m sympy_extras_benchmarks pde_symmetries
python -m sympy_extras_benchmarks qf_nra --sample 20 --seed 2 --timeout 20 --max-variables 3

# the integer and quantified problems, checked against Mathematica as well
python -m sympy_extras_benchmarks solver_regressions --sample 100 --domain integers \
    --wolfram "ssh mathematica-host 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"
# the goals of Lean's and Rocq's own tactic test suites
python -m sympy_extras_benchmarks lean_tactics --non-trivial \
    --wolfram "ssh mathematica-host 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"
python -m sympy_extras_benchmarks coq_micromega --domain integers --timeout 25
python -m sympy_extras_benchmarks polynomial_solving --timeout 30
python -m sympy_extras_benchmarks polynomial_systems
python -m sympy_extras_benchmarks solve_random --cases 150
python -m sympy_extras_benchmarks verify_random --sample 24 --seed 7 --timeout 15
python -m sympy_extras_benchmarks logic_random --cases 80 --seed 3
```

| Driver | Data | Checks |
|---|---|---|
| `kamke_odes` | Kamke and Murphy collections | `dsolve`, then the linear and first order solvers of sympy-extras ("extras"), then `dsolve_lie`; every solution verified with `checkodesol` under the time limit (or numerically for special function solutions) |
| `linear_odes` | the homogeneous linear equations of the collections | `dsolve_linear` (Kovacic, rational and hyperexponential solutions, Bessel/Whittaker/hypergeometric recognition); a full basis confirmed by `checkodesol` or numerically |
| `pde_symmetries` | the 12 PDEs | dimension of the algebra found with the stated ansatz; every symmetry verified by substitution |
| `qf_nra` | a random sample of the Meti-Tarski problems | `satisfiable` against the `:status` (models re-evaluated); `simplify` and `refine` over the reals against the status and random points |
| `solver_regressions` | the arithmetic problems of the cvc5 and Z3 regression suites | `satisfiable` (quantifier-free) or `resolve` (quantified) over the reals or the integers, against the recorded answer; with `--wolfram COMMAND` also against Mathematica, which makes a disagreement between the two an independent finding |
| `lean_tactics` | the `linarith`/`positivity` tests of mathlib4 | `resolve` on each closed goal against mathlib's verdict (`True` for a proved implication, `False` for contradictory hypotheses); the rationals are decided over the reals, so a disagreement with the suite that Mathematica confirms is reported as `SUSPECT` and only a disagreement with Mathematica is a finding |
| `coq_micromega` | the `lia`/`nia`/`psatz` tests of the Rocq standard library | the same, on the nonlinear half: Positivstellensatz examples, products of hypotheses and high powers over `Z`. Statements left `Abort`ed or `Admitted` are not read — they record that the tactic gives up, not that the goal is false |
| `polynomial_solving` | the systems of Maxima's `algsys` regression file | `solve` over the complexes; **every solution substituted back**, which is the hard check and the only one that counts as wrong; the number of solutions is compared with Mathematica's `Solve` and with the count Maxima records, and reported but not counted |
| `polynomial_systems` | Katsura and cyclic systems | `Ideal.dimension`, `vector_space_dimension`, `is_radical` against the known values; FGLM against the Gröbner walk |
| `solve_random` | random polynomial equations with sign assumptions; with `--transcendental N`, random equations in `exp`, `log`, `sin`, `cos`, `sqrt` | `solve` against `Poly.real_roots` or against sign changes on a fine grid refined with `nsolve` |
| `verify_random` | a random sample of the collections | `solve_ode`; every solution verified with `checkodesol` and numerically; a solution failing the numerical check is `WRONG` |
| `logic_random` | random Boolean combinations of polynomial relations with random assumptions | `simplify`, `refine`, `ask`, `satisfiable` against evaluation at random points; the CAD decides the equivalence for one variable |

A driver exits with status 1 only when a wrong result was found; failures
and timeouts are counted, not wrong.

## Results

Runs are not recorded here. What a given version of sympy-extras solved on
a given machine within a given time limit is a measurement, not part of the
datasets, and it goes stale as soon as either side changes; `results/` is
ignored by git. Write a run wherever you want it and compare it yourself:

```
python -m sympy_extras_benchmarks kamke_odes --collections kamke1 --limit 60 \
    --timeout 15 --output results/kamke1.json
```

A run is reproducible from three things: the command line above, the SymPy
version and the sympy-extras commit. Those belong next to the numbers, in
whatever report the numbers go into.

## Tests

```
python -m pytest        # parser tests on inline samples and doctests, no network
python -m mypy
python -m pyflakes sympy_extras_benchmarks conftest.py
```

## Sources and licenses

Every dataset is read from an upstream project. **Nothing from any of them is
committed to this repository**: each parser fetches on first use into `.cache/`
(or `$SYMPY_EXTRAS_BENCHMARKS_CACHE`), which is gitignored, and a local copy can
be pointed to with the environment variable in the last column.

| Source | Upstream | License (as published there) | What is read | Local override |
|---|---|---|---|---|
| Maxima `contrib_ode` tests — the Kamke and Murphy collections | [`git.code.sf.net/p/maxima/code`](https://git.code.sf.net/p/maxima/code), mirror [`calyau/maxima`](https://github.com/calyau/maxima) | GPL-2.0 (`COPYING`) | the equations and the one-word method classification. **Maxima's solutions and code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| Maxima `tests/rtest_algsys.mac` — the `algsys` regression file | as above | GPL-2.0 | the systems and the unknowns; the recorded solutions are *counted* as a third opinion and are not the answer key | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| SMT-LIB `QF_NRA` — the Meti-Tarski family | [`dreal/benchmarks`](https://github.com/dreal/benchmarks) (a mirror) | no license file in the mirror; the SMT-LIB benchmarks carry their own terms | the formulas and the `:status` | `$SYMPY_EXTRAS_BENCHMARKS_SMTLIB` |
| cvc5 regression suite | [`cvc5/cvc5`](https://github.com/cvc5/cvc5) | modified BSD (`COPYING`; the GPL notice there is about optional link-time dependencies, not the test files) | the formulas and the recorded `sat`/`unsat` | — |
| Z3 regression suite | [`Z3Prover/z3test`](https://github.com/Z3Prover/z3test) | MIT (`LICENSE.txt`, Microsoft Corporation) | the formulas and the recorded status | — |
| mathlib4 tactic tests (`linarith`, `positivity`, `linear_combination`, `ring`, `norm_num`) | [`leanprover-community/mathlib4`](https://github.com/leanprover-community/mathlib4) | Apache-2.0 (`LICENSE`) | the binders, hypotheses and conclusion of each `example`. **The proofs are not used** | `$SYMPY_EXTRAS_BENCHMARKS_MATHLIB` |
| Rocq/Coq `micromega` test suite (`lia`, `nia`, `lra`, `psatz`) | [`rocq-prover/stdlib`](https://github.com/rocq-prover/stdlib) | LGPL-2.1 (`LICENSE`) | the binders, hypotheses and conclusion of each `Lemma`/`Goal`. **The proofs are not used** | `$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB` |
| PDE symmetry dimensions | Olver, Bluman–Kumei, Ibragimov's handbook | published results, cited in the module docstring | the dimension of each symmetry algebra | — |
| Katsura and cyclic systems | the literature | published results, cited in the module docstring | the systems and their invariants | — |
| `algsys` literature systems | Beyer (1984), Morgan (1983), cited in `polynomial_solving` | published results | the systems and the number of solutions | — |

Two rules follow from the table, and are also in `AGENTS.md`:

* **Published results are facts** and may be transcribed, with the reference in
  the module docstring — the dimension of a symmetry algebra, the number of
  solutions of cyclic-7, the answer recorded beside an SMT-LIB problem.
* **Code of other systems is never copied.** The parsers are written against the
  *syntax* of each format and tested on samples written for the test, not on
  files taken from the collections.

### Surveyed and not used

Recorded so the ground is not covered twice:

| Source | License | Why not |
|---|---|---|
| [`vprover/vampire`](https://github.com/vprover/vampire) | BSD-3-Clause / "Vampire licence" | ships 9 TPTP `ARI` problems; `checks/theory` tests `let` and tuple parsing, not arithmetic |
| [`rocq-prover/rocq`](https://github.com/rocq-prover/rocq) | LGPL-2.1 | the micromega tests are no longer there; they live in `rocq-prover/stdlib`, which is what is read |
| TPTP `ARI` domain | TPTP's own terms | worth doing, but needs a TFF parser and the full distribution |
| Goedel-Prover / miniF2F / ProofNet | MIT (miniF2F), Apache-2.0 (Goedel-Prover) | olympiad and undergraduate problems, almost none in a decidable arithmetic fragment |
| mathlib4 `FieldSimp.lean` | Apache-2.0 | its goals are `P (expr)` assertions about mathlib's normal form, not truth claims |

## License

BSD 3-Clause, like sympy-extras — this covers the parsers, drivers and oracles
in this repository. The upstream collections keep their own licenses, listed
above, and are neither redistributed nor committed here.
