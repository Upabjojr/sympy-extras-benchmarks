# The collections, in their own language

Every collection which may be redistributed is kept here in the language
it is written in — Maxima, REDUCE, SMT-LIB 2, Lean 4, Rocq, QEPCAD and
Tarski input, FriCAS input, holpy JSON — exactly as its upstream holds
it, with the licence of that upstream beside it. Nothing here is
translated: the parsers of `sympy_extras_benchmarks.parsers` read these
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
| `tptp/` | the `ARI` (arithmetic) domain of the TPTP, with the TPTP's `ReadMe` | [tptp.org](https://tptp.org) | v9.3.1 | TPTP terms: copyright G. Sutcliffe & C. Suttner, verbatim redistribution with attribution only (`tptp/NOTICE`) |

Only the trees a dataset reads are kept, not the whole of any upstream
repository — for `mathlib4`, whose suite is read file by file, only those
files. Two more things are left out on purpose:

* `solver-regressions-z3/regressions/nl/fastmul-unfolded-l-native-nl-wrapped.smt2`
  (13 MB) and `helperlemma-l-native-nl-wrapped.smt2` (9 MB), machine-generated
  files no benchmark can finish on. They are downloaded with the rest of
  the tree when the cache is used, and are on the Hub as
  [`Upabjojr/z3test-nl-large`](https://huggingface.co/datasets/Upabjojr/z3test-nl-large);
* the Brown–Vale-Enriquez data of `tarski` (`tests/dataset-Brown-V-E-2019`,
  139000 files, 623 MB), which `tarski_tests.brown_files` downloads into
  the cache on first use, and which is on the Hub as
  [`Upabjojr/tarski-brown-vale-enriquez-2019`](https://huggingface.co/datasets/Upabjojr/tarski-brown-vale-enriquez-2019).

## What is not kept here

One collection is still fetched on first use into `.cache/`, which is
never committed:

* the **SMT-LIB 2025 release** in full (`smtlib_release`, 3.3 GB unpacked)
  — too large to keep, and only the Meti-Tarski family of it is used often
  enough to be worth keeping, which is what `meti-tarski/` above is. Its
  archives are on the Hub as [`Upabjojr/smtlib-2025-nra`](https://huggingface.co/datasets/Upabjojr/smtlib-2025-nra).

**The TPTP is not under an open licence.** Its terms, in `Documents/ReadMe`
of the distribution and in `tptp/NOTICE` here, permit *verbatim*
redistribution of the TPTP and of parts of it, clearly attributed to the
TPTP, and require the permission of Geoff Sutcliffe and Christian Suttner
for anything modified. `tptp/` is kept under that permission: never edit its
files.

## The large collections on the Hugging Face Hub

The collections too large for `data/` are published on the Hugging Face Hub,
one dataset repository each, since each has its own licence:

| Hub dataset | Content | Licence | Size |
|---|---|---|---|
| [`Upabjojr/smtlib-2025-nra`](https://huggingface.co/datasets/Upabjojr/smtlib-2025-nra) | `QF_NRA.tar.zst` and `NRA.tar.zst` of the SMT-LIB 2025 release, byte for byte as on Zenodo | CC BY 4.0 | 202 MB |
| [`Upabjojr/tarski-brown-vale-enriquez-2019`](https://huggingface.co/datasets/Upabjojr/tarski-brown-vale-enriquez-2019) | Tarski's `tests/dataset-Brown-V-E-2019`: `smtlib-r1` and `smtlib-r2` as two `.tar.zst` (19555 and 119395 SMT-LIB files), `round1inputs`, `round2inputs`, `README` | ISC | 71 MB |
| [`Upabjojr/z3test-nl-large`](https://huggingface.co/datasets/Upabjojr/z3test-nl-large) | the two large files of `z3test`'s `regressions/nl`, at their own paths | MIT | 22 MB |
| [`Upabjojr/tptp-v9.3.1`](https://huggingface.co/datasets/Upabjojr/tptp-v9.3.1) | `TPTP-v9.3.1.tgz`, the whole TPTP distribution byte for byte: a **preservation copy**, so that this knowledge is not lost, whose card states that its copyright is restricted | TPTP terms (`other`) | 891 MB |

Every repository keeps the files in their source language, unchanged but for
the packing of the Brown–Vale-Enriquez trees (139000 loose files is more than a
Hub repository should hold), with the upstream licence text, a dataset card
giving the attribution, and `SHA256SUMS`. They are mirrors: the upstreams in
the tables above remain the sources.

**How the datasets use them.** A dataset reads `data/`, a local copy or the
cache before touching the network. When it has to download, it goes to the
upstream server first and falls back to the Hub mirror when the server cannot
be reached or gives something failing its check. The global option reverses
the order, Hub first and upstream as the fallback:

```
python -m sympy_extras_benchmarks --huggingface smtlib_release ...
SYMPY_EXTRAS_BENCHMARKS_HUGGINGFACE=1 python -m sympy_extras_benchmarks ...
```

It also adds the two large `z3test` files, which `data/` lacks, to
`solver_regressions`. Every file downloaded from the Hub is checked against
the `SHA256SUMS` of its repository; `sympy_extras_benchmarks.huggingface`
holds the names and the logic.

`scripts/huggingface_upload.py` built them. It stages into
`.cache/huggingface-staging/` and uploads only with `--upload`, creating
private repositories unless `--public` is given; rerun it to refresh a
repository after its upstream changes. The datasets download from the names
in `sympy_extras_benchmarks.huggingface`, so a mirror uploaded elsewhere has to
be named there too.

## Refreshing a collection

Delete the directory and let the dataset fetch its upstream again
(`python -m sympy_extras_benchmarks --list` names the drivers; every
dataset module also runs as a script), then copy back only the files the
dataset reads and update the version in the table above.
