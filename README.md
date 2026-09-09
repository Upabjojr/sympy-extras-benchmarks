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

## License

BSD 3-Clause, like sympy-extras. The downloaded collections keep their own
licenses and are not redistributed here.
