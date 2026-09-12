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
| `smtlib_release` | **Every** problem of the SMT-LIB logics `QF_NRA` (16 families: Meti-Tarski, hycomp, LassoRanker, Sturm-MBO, Pine, Uncu, zankl, Economics-Mulligan, Geogebra, ...) and `NRA` (KeYmaera and two small families), each with its `:status` | SMT-LIB 2 files, parsed by `smtlib` (`QF_NRA`) and `solver_regressions` (`NRA`); the 2025 release on Zenodo (record 16740866), checked against its MD5 sums and unpacked with `tar --zstd` | `QF_NRA` 12154 problems (5257 sat, 5536 unsat, 1361 unknown); `NRA` 3819 (3806 unsat, 5 sat, 8 unknown) |
| `qepcad_syntax` | The formula language of QEPCAD B and Tarski (implicit multiplication, `/\\`, `\\/`, `==>`, `(E x)`, `ex x [ ]`, ...) and QEPCAD's input dialogue | parser to SymPy formulas with the quantifiers of sympy-extras; QEPCAD's extended quantifiers (`F`, `G`, `C`, `X k`) and Tarski's `_root_` atoms are refused rather than approximated | — |
| `bath_cad` | The **Bath CAD example bank** (Wilson, Bradford, Davenport, England): the classical QE problems (Collins, Hong, Davenport–Heintz, Kahan, Solotareff, the X-axis ellipse, motion planning, TTICAD, ...) with their suggested variable order and Maple's best cell count | QEPCAD inputs, a Maple file and a PDF, from the University of Bath Research Data Archive | 78 inputs (four malformed in the file itself, one repeated), 50 polynomial lists, 24 cell counts read from the PDF |
| `qepcad_tests` | The regression tests and worked examples of **QEPCAD B** | QEPCAD inputs with QEPCAD's `sol T` answers; sparse clone of `chriswestbrown/qepcad` | 7 application problems (6 with an answer), 1000 random `(E y)[p(x, y) = 0]` of degree 6 (two of them corrupted in the file; the 2D-CAD set repeats all 1000), 9 worked examples |
| `tarski_tests` | The tests of **Tarski**: GeoGebra Discovery's QE problems with Tarski's answers, the ISSAC 2015 NuCAD conjunctions, the formulas and unit tests of the interpreter, and the Brown–Vale-Enriquez conjunctions (disjuncts of Meti-Tarski problems) | Tarski formulas and SMT-LIB files; sparse clone of `chriswestbrown/tarski` | 181 GeoGebra (165 with an answer), 225 ISSAC (repeated in the 2017 suite), 8 interpreter, 19555 + 119395 Brown–Vale-Enriquez |
| `lean_tactics` | The tactic tests of Lean's **mathlib4** for arithmetic (`linarith`, `positivity`), polynomial identities (`linear_combination`, `ring`) and numeral evaluation (`norm_num`), each with a machine-checked proof | Lean 4 `example` blocks, parsed to SymPy formulas by the grammar of `prover_syntax`; sparse clone of `leanprover-community/mathlib4` on GitHub | 13 files, 1573 examples, 443 usable goals of which 323 are not settled by SymPy's own evaluation |
| `coq_micromega` | The **micromega** test suite of the Rocq/Coq standard library (`lia`, `nia`, `lra`, `psatz`): mostly nonlinear goals over `Z`, `Q`, `R` and `nat`, one file per historical bug, each closed by `Qed` | Rocq `Lemma`/`Goal` statements, parsed to SymPy formulas by the grammar of `prover_syntax`; sparse clone of `rocq-prover/stdlib` on GitHub | 38 files, 285 statements, 119 usable goals (none of them trivial), 105 over the integers |
| `polynomial_solving` | The systems of Maxima's `algsys` regression file (`tests/rtest_algsys.mac`): the examples of Beyer (1984) and Morgan (1983), plus the ones that later broke `algsys` — positive-dimensional components, solutions real in the paper and complex in fact, and one where the published answer is wrong | Maxima `.mac`, read with the expression parser of `maxima_ode`; the recorded solutions are counted but are not the answer key | 51 systems, 1 to 13 equations, 1 to 6 unknowns |
| `tptp_arithmetic` | The arithmetic (`ARI`) domain of the **TPTP** problem library: several hundred TFF problems over `$int` and `$real`, each with the `Status` its authors recorded. Written to be hard for provers rather than to exercise a tactic | TFF, parsed by a recursive descent parser for the arithmetic fragment; `Problems/ARI` extracted from the official distribution | 700 problems, 189 usable (179 `Theorem`, 10 `CounterSatisfiable`), 122 over the integers |
| `reduce_odes` | The ODE test suite of **REDUCE**'s `ODESolve`, whose core is the **Postel–Zimmermann** collection — the equations of their 1996 review of the ODE solvers of seven computer algebra systems, chosen to tell systems apart | REDUCE `.tst`, rewritten into Maxima syntax (implicit multiplication, bracketless calls, `df`) and read with the parser of `maxima_ode` | 6 files, 233 `odesolve` calls, 88 usable equations of order 1 to 7 |
| `maxima_limits` | Maxima's four limit regression files: the main one (a bug per entry), a larger collection, the examples of **Gruntz's 1996 thesis** — the algorithm modern CAS limits come from — and the limit problems of **Wester's** *Critique of the Mathematical Abilities of CA Systems* | Maxima `.mac`, read with the expression parser of `maxima_ode`; a call while an `assume` is in force is refused, as are `und` and `ind` | 4 files, ~1070 calls, 354 usable limits (300 with a recorded value) |
| `pde_symmetries` | Twelve classical PDEs (heat, Burgers, KdV, wave, nonlinear diffusion, Fisher, Boussinesq, Liouville, sine-Gordon, potential Burgers, Black-Scholes) with the dimension of their point symmetry algebra from Olver, Bluman-Kumei and Ibragimov's handbook | translated into SymPy expressions | 12 equations |
| `polynomial_systems` | The Katsura-m and cyclic-m systems with their known invariants (dimension, number of solutions, radicality) | generated as SymPy expressions | Katsura 2-6, cyclic 3-7 |
| `maxima_integrals` | Definite integrals and Laplace transforms from Maxima's test suite: the regression file of its definite integration (`rtestint`), the definite integrals of `rtest_integrate`, the definite integrals of **Wester's** *Critique*, and the Laplace transforms of `rtest_laplace` and of `specint` (`rtest_hypgeo`, from Abramowitz and Stegun 29.3 on: Bessel functions, incomplete gamma, `erf`, orthogonal polynomials), each with the facts in force when it runs | Maxima `.mac`, read with the expression parser of `maxima_ode`; the context (`assume`, `forget`, `kill`, `declare`, `assume_pos`, assigned variables) is followed through the file, and a transform is read as its integral over `(0, oo)` | 569 integrals: rtestint 194, rtest_integrate 50, wester 22, laplace 75, specint 228; 392 with a recorded value |
| `reduce_defint` | The test file of **REDUCE's DEFINT** package (K. Gaskell, ZIB 1993–94). DEFINT integrates products of Meijer G-functions — the Adamchik–Marichev method, which is also SymPy's `meijerint` — and its tests are integrals over `(0, oo)` and `(0, y)` of powers, exponentials, Bessel functions, `Ei`, `Si`, `Shi` and `erf` | REDUCE `.tst`, rewritten into Maxima syntax as for `reduce_odes` | 93 calls, 92 read (the Fresnel one is refused) |
| `fricas_integrals` | FriCAS's `mapleok.input`: definite integrals of logarithms, inverse hyperbolic functions, absolute values, real and imaginary parts, over infinite ranges and along complex segments | FriCAS input, rewritten into Maxima syntax; sparse clone of `fricas/fricas` | 252 statements, 231 distinct integrals |
| `holpy_integrals` | The worked examples of **holpy** (Xu, Li and Zhan, *Verified Interactive Computation of Definite Integrals*, CADE 2021): the MIT Integration Bee (2013, 2014, 2019, 2020), Schaum's Outline and UC Davis exercises, and proved identities (Ahmed, Frullani, Dirichlet, Catalan, Wallis, beta and gamma, log-sine) with their conditions | holpy's JSON; the last line of a checked computation, or the other side of a proved goal, is the recorded value; sparse clone of `bzhan/holpy` | 249 integrals, 218 with a recorded value |

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
python -m sympy_extras_benchmarks tptp_arithmetic --timeout 20
python -m sympy_extras_benchmarks reduce_odes --timeout 20
python -m sympy_extras_benchmarks maxima_limits --timeout 15 \
    --wolfram "ssh mathematica-host 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"
python -m sympy_extras_benchmarks polynomial_solving --timeout 30
# SymPy's integrate on the definite integrals, checked by quadrature; --meijerg forces
# the Meijer G method, the method of REDUCE's DEFINT
python -m sympy_extras_benchmarks definite_integrals --sources reduce,holpy --timeout 30 \
    --output results/definite_integrals.jsonl
python -m sympy_extras_benchmarks definite_integrals --sources reduce --meijerg \
    --output results/definite_integrals_meijerg.jsonl
# the definite integrator of sympy-extras instead of SymPy's integrate
python -m sympy_extras_benchmarks definite_integrals --extras --timeout 30 \
    --output results/definite_integrals_extras.jsonl
python -m sympy_extras_benchmarks definite_integrals --timeout 30 --output results/definite_integrals.jsonl \
    --wolfram "ssh mathematica-host 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"
python -m sympy_extras_benchmarks polynomial_systems
python -m sympy_extras_benchmarks solve_random --cases 150
python -m sympy_extras_benchmarks verify_random --sample 24 --seed 7 --timeout 15
python -m sympy_extras_benchmarks logic_random --cases 80 --seed 3
python -m sympy_extras_benchmarks presburger_random --cases 400 --seed 3
```

| Driver | Data | Checks |
|---|---|---|
| `kamke_odes` | Kamke and Murphy collections | `dsolve`, then the linear and first order solvers of sympy-extras ("extras"), then `dsolve_lie`; every solution verified with `checkodesol` under the time limit (or numerically for special function solutions) |
| `linear_odes` | the homogeneous linear equations of the collections | `dsolve_linear` (Kovacic, rational and hyperexponential solutions, Bessel/Whittaker/hypergeometric recognition); a full basis confirmed by `checkodesol` or numerically |
| `pde_symmetries` | the 12 PDEs | dimension of the algebra found with the stated ansatz; every symmetry verified by substitution |
| `qf_nra` | a random sample of the Meti-Tarski problems | `satisfiable` against the `:status` (models re-evaluated); `simplify` and `refine` over the reals against the status and random points |
| `solver_regressions` | the arithmetic problems of the cvc5 and Z3 regression suites | `satisfiable` (quantifier-free) or `resolve` (quantified) over the reals or the integers, against the recorded answer; with `--wolfram COMMAND` also against Mathematica, which makes a disagreement between the two an independent finding |
| `smtlib_release` | every problem of `QF_NRA` and `NRA`; with `--brown 1` or `--brown 2` the Brown–Vale-Enriquez conjunctions | in parallel worker processes (`runner`), smallest file first, resumable: `satisfiable` against the status (a model evaluated exactly), `simplify` and `refine` against the status and random points (`QF_NRA`), `resolve` of the closed formula (`NRA`); a Brown–Vale-Enriquez conjunction is expected unsat when its Meti-Tarski source is. Timeouts, refusals (`ValueError`/`TypeError`), `NotImplementedError` and crashes are kept apart |
| `cad_examples` | the Bath bank, the tests of QEPCAD B and of Tarski; with `--cells` the polynomial lists of the Bath bank | `resolve` (`satisfiable` for the ISSAC conjunctions); a recorded answer is compared at random rational points inside the `assume` region, and a mismatch is `DISAGREES` until Mathematica settles it; `--cells` reports the number of cells beside Maple's best (a comparison, not a check) |
| `wolfram_check` | the results of `smtlib_release` and `cad_examples` | Mathematica's `Resolve` on every answer no recorded answer confirms: unsat without a status, a closed decision or an elimination without a recorded answer (`ForAll[free, A ⇒ (R ⇔ F)]`), and every `WRONG` or `DISAGREES` |
| `region_integrals` | random regions: a Boolean combination of polynomial relations cut to a box, with a polynomial integrand | `integrate_by_ranges` against four checks which do not use the decomposition: Monte Carlo sampling of the integrand times the indicator (re-sampled four times as densely before a case is judged), the region split in two at `x = 0`, the variables in the other order, and with `--wolfram` the integral of `Boole[condition]` to 20 digits. The region is cut to the box before either side sees it, so that both integrate the same set |
| `lean_tactics` | the `linarith`/`positivity` tests of mathlib4 | `resolve` on each closed goal against mathlib's verdict (`True` for a proved implication, `False` for contradictory hypotheses); the rationals are decided over the reals, so a disagreement with the suite that Mathematica confirms is reported as `SUSPECT` and only a disagreement with Mathematica is a finding |
| `coq_micromega` | the `lia`/`nia`/`psatz` tests of the Rocq standard library | the same, on the nonlinear half: Positivstellensatz examples, products of hypotheses and high powers over `Z`. Statements left `Abort`ed or `Admitted` are not read — they record that the tactic gives up, not that the goal is false |
| `tptp_arithmetic` | the TPTP `ARI` domain | `resolve` on each closed problem against the recorded `Status`; the `$rat` problems are refused, since deciding them over ℝ changes the question |
| `reduce_odes` | the Postel–Zimmermann ODE collection | `solve_ode`, every solution verified with `checkodesol` and numerically; a solution whose residual does not vanish is `WRONG` |
| `maxima_limits` | Maxima's limit regression files | `limit` against Maxima's recorded value **and** Mathematica. Neither is an answer key — Maxima's limit code has its own bugs — so a `DIFFER` means sympy-extras and Mathematica disagree, and a `SUSPECT` means those two agree against Maxima. This is the driver that found #52 |
| `polynomial_solving` | the systems of Maxima's `algsys` regression file | `solve` over the complexes; **every solution substituted back**, which is the hard check and the only one that counts as wrong; the number of solutions is compared with Mathematica's `Solve` and with the count Maxima records, and reported but not counted |
| `definite_integrals` | the definite integrals of `maxima_integrals`, `reduce_defint`, `fricas_integrals` and `holpy_integrals` | SymPy's `integrate` (`--meijerg` forces the Meijer G method) or, with `--extras`, sympy-extras' `definite_integral` (the Marichev–Adamchik method, the facts of the source passed as statement assumptions, SymPy's `integrate` as its verified last resort) — with the facts of the source as assumptions, in parallel workers (`runner`). The result is evaluated at two samples of the parameters satisfying the facts and compared with numerical quadrature, trusted only when mpmath's tanh-sinh and Gauss-Legendre rules agree; a disagreement is `WRONG`. With `--wolfram COMMAND`, Mathematica's `NIntegrate` settles at the same sample every result the quadrature could not check, and every `WRONG` one. The source's recorded value is checked against the quadrature, and a wrong one is reported as `SOURCE`, a finding about the source. The licence of each dataset, and where its licence file is kept, is printed before the run |
| `polynomial_systems` | Katsura and cyclic systems | `Ideal.dimension`, `vector_space_dimension`, `is_radical` against the known values; FGLM against the Gröbner walk |
| `solve_random` | random polynomial equations with sign assumptions; with `--transcendental N`, random equations in `exp`, `log`, `sin`, `cos`, `sqrt` | `solve` against `Poly.real_roots` or against sign changes on a fine grid refined with `nsolve` |
| `verify_random` | a random sample of the collections | `solve_ode`; every solution verified with `checkodesol` and numerically; a solution failing the numerical check is `WRONG` |
| `presburger_random` | random linear formulas over ℤ — disjunctions of conjunctions of `=`, `!=`, `<=`, `<` | `resolve` against three oracles that each decide on their own: brute force over a box (one-sided both ways, so a disagreement is always the procedure's), the ∀/¬∃ duality (an internal contradiction, no outside oracle) and the real relaxation. **This is the driver that found #51 and the one to run against a fix** |
| `logic_random` | random Boolean combinations of polynomial relations with random assumptions | `simplify`, `refine`, `ask`, `satisfiable` against evaluation at random points; the CAD decides the equivalence for one variable |

A driver exits with status 1 only when a wrong result was found; failures
and timeouts are counted, not wrong.

## Results

### Definite integrals (`definite_integrals`)

SymPy 1.14's `integrate` and sympy-extras' `definite_integral` (commit 43f2064)
on the 1141 integrals of `maxima_integrals`, `reduce_defint`,
`fricas_integrals` and `holpy_integrals`, 30 s each, the unchecked results
settled by Mathematica's `NIntegrate`:

| | ok | ok (mathematica) | WRONG (mathematica) | unevaluated | no answer | crash |
|---|---|---|---|---|---|---|
| `integrate` | 533 | 149 | 34 | 221 | 74 | 1 |
| `--extras` | 565 | 176 | 1 | 358 | 21 | 0 |

The wrong answers of `integrate` are the branch cuts of its antiderivatives
on the complex-valued FriCAS integrands; `definite_integral` keeps an answer
of `integrate` only when the quadrature confirms it. Results in
`results/defint_sympy114.wolfram.log` and `results/defint_extras4.wolfram.log`.


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

The licence file of each upstream project is kept with its data: the sparse
clones keep the files at the root of each repository, where the licence is. A
dataset module names its licence and those files (`LICENCE`, `LICENCE_FILES`,
`licence_files()` in the integration datasets), and `definite_integrals` prints
them before a run.

| Source | Upstream | License (as published there) | What is read | Local override |
|---|---|---|---|---|
| Maxima `contrib_ode` tests — the Kamke and Murphy collections | [`git.code.sf.net/p/maxima/code`](https://git.code.sf.net/p/maxima/code), mirror [`calyau/maxima`](https://github.com/calyau/maxima) | GPL-2.0 (`COPYING`) | the equations and the one-word method classification. **Maxima's solutions and code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| Maxima `tests/rtest_limit*.mac` — the limit regression files | as above | GPL-2.0 | the calls and the recorded values, the latter as a third opinion only | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| Maxima `tests/rtest_algsys.mac` — the `algsys` regression file | as above | GPL-2.0 | the systems and the unknowns; the recorded solutions are *counted* as a third opinion and are not the answer key | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| Maxima `tests/rtestint.mac`, `rtest_integrate.mac`, `rtest_laplace.mac`, `rtest_hypgeo.mac` and `wester_problems/test_definite_integrals.mac` — definite integrals and Laplace transforms | as above | GPL-2.0; Wester's problems were released under it by their author (`wester-gpl-permission-message.txt`) | the calls, the facts in force when they run, and the recorded values, the latter as a third opinion only | `$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS` |
| TPTP `ARI` domain | [tptp.org](https://tptp.org) | distributed by Geoff Sutcliffe under TPTP's own terms; each problem is the work of the authors named in its header | the formulas and the recorded `Status` | `$SYMPY_EXTRAS_BENCHMARKS_TPTP` |
| REDUCE `ODESolve` tests — the Postel–Zimmermann collection | [`reduce-algebra/reduce-algebra`](https://github.com/reduce-algebra/reduce-algebra) | *Reduce License*, a BSD 2-clause style licence (`LICENSE`) | the equations only. **REDUCE's solutions and code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_REDUCE` |
| REDUCE DEFINT tests — Gaskell's collection | [`reduce-algebra/reduce-algebra`](https://github.com/reduce-algebra/reduce-algebra), `packages/defint` | *Reduce License*, a BSD 2-clause style licence (`LICENSE`) | the four-argument `int` calls. **REDUCE's results (`defint.rlg`), the transforms and the code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_REDUCE` |
| SMT-LIB `QF_NRA` — the Meti-Tarski family | [`dreal/benchmarks`](https://github.com/dreal/benchmarks) (a mirror) | no license file in the mirror; the SMT-LIB benchmarks carry their own terms | the formulas and the `:status` | `$SYMPY_EXTRAS_BENCHMARKS_SMTLIB` |
| cvc5 regression suite | [`cvc5/cvc5`](https://github.com/cvc5/cvc5) | modified BSD (`COPYING`; the GPL notice there is about optional link-time dependencies, not the test files) | the formulas and the recorded `sat`/`unsat` | — |
| Z3 regression suite | [`Z3Prover/z3test`](https://github.com/Z3Prover/z3test) | MIT (`LICENSE.txt`, Microsoft Corporation) | the formulas and the recorded status | — |
| SMT-LIB 2025 release — `QF_NRA` and `NRA`, every family | [Zenodo record 16740866](https://doi.org/10.5281/zenodo.16740866) (SMT-LIB non-incremental benchmarks, 2025) | CC BY 4.0, as stated on the Zenodo record; each family credits its submitters in the files | the formulas and the `:status` | `$SYMPY_EXTRAS_BENCHMARKS_SMTLIB_RELEASE` |
| The Bath CAD example bank, version 4 | [University of Bath Research Data Archive](https://doi.org/10.15125/BATH-00069) (D. Wilson, 2013) | CC BY-SA 4.0 | the QEPCAD inputs, the Maple polynomial lists and the best cell counts of the PDF | `$SYMPY_EXTRAS_BENCHMARKS_BATH_CAD` |
| QEPCAD B — regression tests and worked examples | [`chriswestbrown/qepcad`](https://github.com/chriswestbrown/qepcad) | ISC-style permission notice (`qesource/LICENSE`, H. Hong and C. W. Brown) | the inputs and QEPCAD's recorded `sol T` answers. **No code of QEPCAD is used** | `$SYMPY_EXTRAS_BENCHMARKS_QEPCAD` |
| Tarski — GeoGebra regression, ISSAC 2015/2017 data, interpreter examples, Brown–Vale-Enriquez 2019 data | [`chriswestbrown/tarski`](https://github.com/chriswestbrown/tarski) | ISC-style permission notice (`interpreter/LICENSE`, C. W. Brown) | the formulas and Tarski's recorded answers. **No code of Tarski is used** | `$SYMPY_EXTRAS_BENCHMARKS_TARSKI` |
| mathlib4 tactic tests (`linarith`, `positivity`, `linear_combination`, `ring`, `norm_num`) | [`leanprover-community/mathlib4`](https://github.com/leanprover-community/mathlib4) | Apache-2.0 (`LICENSE`) | the binders, hypotheses and conclusion of each `example`. **The proofs are not used** | `$SYMPY_EXTRAS_BENCHMARKS_MATHLIB` |
| Rocq/Coq `micromega` test suite (`lia`, `nia`, `lra`, `psatz`) | [`rocq-prover/stdlib`](https://github.com/rocq-prover/stdlib) | LGPL-2.1 (`LICENSE`) | the binders, hypotheses and conclusion of each `Lemma`/`Goal`. **The proofs are not used** | `$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB` |
| PDE symmetry dimensions | Olver, Bluman–Kumei, Ibragimov's handbook | published results, cited in the module docstring | the dimension of each symmetry algebra | — |
| Katsura and cyclic systems | the literature | published results, cited in the module docstring | the systems and their invariants | — |
| `algsys` literature systems | Beyer (1984), Morgan (1983), cited in `polynomial_solving` | published results | the systems and the number of solutions | — |
| FriCAS `src/input/mapleok.input` | [`fricas/fricas`](https://github.com/fricas/fricas) | modified BSD, 3-clause (`LICENSE.txt`) | the integrands, variables and endpoints. **FriCAS's answers, in the comments, and its code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_FRICAS` |
| holpy `integral/examples` — MIT Integration Bee, Schaum's Outline, UC Davis, proved identities | [`bzhan/holpy`](https://github.com/bzhan/holpy) | BSD-3-Clause (`LICENSE`); the problems are credited in the files to their competitions and books | the problems and goals with their conditions, and the final value of each computation as a third opinion. **holpy's steps and code are not used** | `$SYMPY_EXTRAS_BENCHMARKS_HOLPY` |

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
| Goedel-Prover / miniF2F / ProofNet | MIT (miniF2F), Apache-2.0 (Goedel-Prover) | olympiad and undergraduate problems, almost none in a decidable arithmetic fragment |
| mathlib4 `FieldSimp.lean` | Apache-2.0 | its goals are `P (expr)` assertions about mathlib's normal form, not truth claims |
| [IntegralBench](https://github.com/vegetable-yx/IntegralBench) — 317 graduate-level definite integrals with numerical answers | no licence file | no licence, and the problems are transcribed from a textbook and competitions whose rights are not theirs to give; LaTeX only. Its numerical answers would make a good oracle if its authors licensed it |
| N. Abbasi's *Computer Algebra Independent Integration Tests* (12000.org) | — | indefinite integrals only (Rubi's test suite); nothing definite to read |

## License

BSD 3-Clause, like sympy-extras — this covers the parsers, drivers and oracles
in this repository. The upstream collections keep their own licenses, listed
above, and are neither redistributed nor committed here.
