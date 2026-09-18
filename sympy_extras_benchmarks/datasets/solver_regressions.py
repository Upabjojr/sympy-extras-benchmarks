"""Arithmetic problems from the regression suites of the SMT solvers
cvc5 and Z3, as SymPy formulas.

The dataset
===========

Solvers keep the problems which once broke them, and those are exactly
the awkward cases: degenerate coefficients, empty and full solution
sets, deep quantifier alternations, divisibility constraints. The two
suites read here are

* the ``test/regress`` tree of `cvc5 <https://github.com/cvc5/cvc5>`_,
  whose files record the expected answer in a ``; EXPECT: sat`` header
  and often in ``(set-info :status ...)`` as well;
* the ``regressions`` tree of `z3test <https://github.com/Z3Prover/z3test>`_,
  which records it in ``(set-info :status ...)``.

The subtrees read are kept in this repository, in
``data/solver-regressions-z3/`` and ``data/solver-regressions-cvc5/``; a
local copy can be named by ``$SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS``,
and what is in neither is cloned sparsely into the cache. Only the
mathematical content is read: the formula, the sorts of the variables
and the recorded status.

The logics kept are the arithmetic ones, over the reals *and over the
integers*, quantified or not: ``QF_LIA``, ``QF_NIA``, ``LIA``, ``NIA``,
``QF_LRA``, ``QF_NRA``, ``LRA``, ``NRA`` and ``ALL`` when the file turns
out to use nothing else. The integer and quantified problems are what
this dataset adds to
:mod:`~sympy_extras_benchmarks.datasets.smtlib`, which reads the
quantifier-free real Meti-Tarski family.

The parser
==========

The files are read by
:func:`~sympy_extras_benchmarks.parsers.smtlib.translate_arithmetic`
(:mod:`~sympy_extras_benchmarks.parsers.smtlib`), which adds the integer
sorts and the quantifiers to the s-expression reader. What this module adds
is the convention of cvc5's suite: a file which records no ``:status``
states its expected answer in a ``; EXPECT: sat`` comment, and
:func:`translate` reads it.

Examples
========

>>> from sympy_extras_benchmarks.datasets.solver_regressions import translate
>>> text = '''
... ; EXPECT: unsat
... (set-logic QF_LIA)
... (declare-fun n () Int)
... (assert (and (> n 0) (< n 1)))
... (check-sat)
... '''
>>> problem = translate(text, 'demo')
>>> problem
ArithProblem(demo, QF_LIA, unsat, 1 integer, 0 real)
>>> problem.formula
(n > 0) & (n < 1)
>>> problem.domain
Integers


Source and licence
==================

cvc5 is distributed under a **modified BSD** licence, ``z3test`` under the
**MIT** licence. The subtrees read are kept under those licences in
``data/solver-regressions-cvc5/`` and ``data/solver-regressions-z3/``,
with each project's licence file beside them (see ``data/README.md``),
and are read from there; ``$SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS``
names a directory to read instead, and a subtree in neither is cloned
sparsely into the cache. Two machine-generated files of
``z3test``'s ``regressions/nl``, of 13 MB and 9 MB, are too large to keep:
they are in the clone, and are read from their Hugging Face mirror when
GitHub cannot be reached or, beside ``data/``, under the global option of
:mod:`~sympy_extras_benchmarks.huggingface`. The mirror is
`Upabjojr/z3test-nl-large
<https://huggingface.co/datasets/Upabjojr/z3test-nl-large>`_. Only the formulas and the recorded
``sat``/``unsat`` answers are read.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy_extras_benchmarks import huggingface
from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.smtlib import ArithProblem, translate_arithmetic

__all__ = ['SOURCES', 'fetch', 'load', 'translate']

#: the repositories and the subtrees taken from them
SOURCES: dict[str, tuple[str, tuple[str, ...]]] = {
    'cvc5': ("https://github.com/cvc5/cvc5",
             ('test/regress/cli/regress0/nl', 'test/regress/cli/regress1/nl',
              'test/regress/cli/regress0/arith', 'test/regress/cli/regress1/arith',
              'test/regress/cli/regress0/quantifiers')),
    'z3': ("https://github.com/Z3Prover/z3test",
           ('regressions/smt2', 'regressions/qsat', 'regressions/nl', 'regressions/mcsat_smt2')),
}

#: a local directory holding the ``.smt2`` files
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS'

_EXPECT = re.compile(r'^\s*;\s*EXPECT:\s*(sat|unsat)\s*$', re.MULTILINE)


def translate(text: str, name: str = '') -> Optional[ArithProblem]:
    """The problem of a regression file, as
    :func:`~sympy_extras_benchmarks.parsers.smtlib.translate_arithmetic`
    reads it, with the expected answer of cvc5's ``; EXPECT:`` comment when
    the file records no ``:status`` (and the comments agree)."""
    problem = translate_arithmetic(text, name)
    if problem is not None and problem.status == 'unknown':
        found = _EXPECT.findall(text)
        if len(set(found)) == 1:
            problem.status = found[0]
    return problem


def fetch() -> list[pathlib.Path]:
    """The directories holding the ``.smt2`` files: the one named by
    ``$SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS``, or the sparse clones
    in the cache (made on first use). Sources which cannot be obtained
    are skipped."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return [pathlib.Path(override)]
    directories: list[pathlib.Path] = []
    for key, (repository, subtrees) in SOURCES.items():
        kept = [p for p in (bundled('solver-regressions-' + key, s) for s in subtrees)
                if p is not None]
        if kept:
            directories.extend(kept)
            # data/ lacks the two large z3test files: the global option adds
            # them from their mirror
            if key == 'z3' and huggingface.preferred():
                directories.extend(_z3_large_from_hub())
            continue
        clone = cache_directory() / ('solver-regressions-' + key)
        present = [clone / s for s in subtrees if (clone / s).is_dir()]
        if present:
            directories.extend(present)
            continue
        try:
            subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                            repository, str(clone)], check=True, capture_output=True, timeout=1800)
            subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', *subtrees],
                           check=True, capture_output=True, timeout=1800)
        except (subprocess.SubprocessError, OSError):
            # the mirror holds only the two large files, so it replaces the
            # clone only when GitHub cannot be reached, never under the option
            if key == 'z3':
                directories.extend(_z3_large_from_hub())
            continue
        directories.extend(clone / s for s in subtrees if (clone / s).is_dir())
    return directories


#: the two files of ``z3test``'s ``regressions/nl`` too large for ``data/``
Z3_LARGE_FILES: tuple[str, ...] = ('fastmul-unfolded-l-native-nl-wrapped.smt2',
                                   'helperlemma-l-native-nl-wrapped.smt2')


def _z3_large_from_hub() -> list[pathlib.Path]:
    """The directory of the two large ``z3test`` files, downloaded from their
    Hugging Face mirror; empty when the Hub cannot be reached."""
    directory = cache_directory() / 'z3test-nl-large-huggingface' / 'regressions' / 'nl'
    for name in Z3_LARGE_FILES:
        if huggingface.download(huggingface.Z3TEST_NL_LARGE, 'regressions/nl/' + name,
                                directory / name) is None:
            return []
    return [directory]


def load() -> list[pathlib.Path]:
    """Every ``.smt2`` file of the fetched directories, sorted."""
    paths: list[pathlib.Path] = []
    for directory in fetch():
        paths.extend(sorted(directory.rglob('*.smt2')))
    return sorted(set(paths))
