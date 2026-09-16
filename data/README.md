# The collections, in their own language

Every collection which may be redistributed is kept here in the language
it is written in — Maxima, REDUCE, SMT-LIB 2, Lean 4, Rocq, QEPCAD and
Tarski input, FriCAS input, holpy JSON — exactly as its upstream holds
it, with the licence of that upstream beside it. Nothing here is
translated: the parsers of `sympy_extras_benchmarks.datasets` read these
files and produce SymPy objects when a dataset is loaded, so a checkout
of this repository runs every benchmark of the table below without
touching the network.

The licence of a directory is the licence of the files in it, not the
BSD 3-Clause of this repository's own code (`../LICENSE`). The copy is
verbatim: no file has been edited, and the licence file each project
ships is kept with it.

| Directory | Collection | Upstream | Version | Licence |
|---|---|---|---|---|
| `maxima/` | Kamke and Murphy ODEs (`contrib_ode`), and Maxima's regression files for integrals, limits and `algsys` | [Maxima](https://git.code.sf.net/p/maxima/code) | `d849baa` (2026-09-09) | GPL-2.0 (`maxima/repository/COPYING`) |
| `reduce/` | the Postel–Zimmermann ODE suite and REDUCE's `odesolve` and `defint` tests | [reduce-algebra](https://github.com/reduce-algebra/reduce-algebra) | `3d29908` (2026-09-09) | BSD-2-clause style (`reduce/LICENSE`) |
| `fricas/` | the integration inputs `integ.input` and `mapleok.input` | [fricas](https://github.com/fricas/fricas) | `46f4240` (2026-09-01) | modified BSD (`fricas/LICENSE.txt`) |
| `holpy/` | the integral examples | [bzhan/holpy](https://github.com/bzhan/holpy) | `f36c1f0` (2023-02-25) | BSD-3-Clause (`holpy/LICENSE`) |
| `rocq-stdlib/` | the `micromega` test suite | [rocq-prover/stdlib](https://github.com/rocq-prover/stdlib) | `1593d61` (2026-08-31) | LGPL-2.1 (`rocq-stdlib/LICENSE`) |
| `mathlib4/` | the tests of the arithmetic tactics | [mathlib4](https://github.com/leanprover-community/mathlib4) | `f5e9087` (2026-09-09) | Apache-2.0 (`mathlib4/LICENSE`) |
| `tarski/` | the regression, ISSAC and interpreter problems | [chriswestbrown/tarski](https://github.com/chriswestbrown/tarski) | `796962b` (2026-05-23) | ISC style (`tarski/interpreter/LICENSE`) |
| `qepcad/` | the regression tests and the published examples | [chriswestbrown/qepcad](https://github.com/chriswestbrown/qepcad) | `0f57079` (2021-03-09) | permissive, Hong & Brown (`qepcad/qesource/LICENSE`) |
| `bath-cad-examples/` | the CAD example bank | [Bath Research Data Archive](https://researchdata.bath.ac.uk/69/) | v4 (2013) | CC BY-SA 4.0 (`bath-cad-examples/NOTICE`) |
| `solver-regressions-z3/` | the arithmetic regressions of Z3 | [Z3Prover/z3test](https://github.com/Z3Prover/z3test) | `d43c5f7` (2026-09-05) | MIT (`solver-regressions-z3/LICENSE.txt`) |
| `solver-regressions-cvc5/` | the `nl`, `arith` and `quantifiers` regressions of cvc5 | [cvc5/cvc5](https://github.com/cvc5/cvc5) | `c881f61` (2026-09-09) | BSD-3-Clause (`solver-regressions-cvc5/COPYING`) |
| `meti-tarski/` | the 7006 Meti-Tarski `QF_NRA` problems | [SMT-LIB release 2025](https://doi.org/10.5281/zenodo.16740866) | 2025 release | CC BY 4.0 (`meti-tarski/NOTICE`) |

Only the trees a dataset reads are kept, not the whole of any upstream
repository — for `mathlib4`, whose suite is read file by file, only those
files. Two more things are left out on purpose:

* `solver-regressions-z3/regressions/nl/fastmul-unfolded-l-native-nl-wrapped.smt2`
  (13 MB) and `helperlemma-l-native-nl-wrapped.smt2` (9 MB), machine-generated
  files no benchmark can finish on. They are downloaded with the rest of
  the tree when the cache is used;
* the Brown–Vale-Enriquez data of `tarski` (`tests/dataset-Brown-V-E-2019`,
  139000 files, 623 MB), which `tarski_tests.brown_files` downloads into
  the cache on first use.

## What is not kept here

Two collections are still fetched on first use into `.cache/`, which is
never committed:

* the **SMT-LIB 2025 release** in full (`smtlib_release`, 3.3 GB unpacked)
  — too large to keep, and only the Meti-Tarski family of it is used often
  enough to be worth keeping, which is what `meti-tarski/` above is;
* the **TPTP** `ARI` domain (`tptp_arithmetic`). TPTP is distributed by
  Geoff Sutcliffe under its own terms and its problems are the work of
  their individual authors; those terms are not a grant to redistribute
  them here, so the domain is extracted from the official distribution
  instead.

## Refreshing a collection

Delete the directory and let the dataset fetch its upstream again
(`python -m sympy_extras_benchmarks --list` names the drivers; every
dataset module also runs as a script), then copy back only the files the
dataset reads and update the version in the table above.
