"""SMT-LIB 2 problems of the ``QF_NRA`` logic (quantifier-free nonlinear
real arithmetic) as SymPy formulas.

The dataset
===========

The Meti-Tarski family of the SMT-LIB benchmark library holds 7713 proof
obligations extracted from the MetiTarski theorem prover (Akbarpour and
Paulson, *MetiTarski: An automatic theorem prover for real-valued special
functions*, JAR 44, 2010): polynomial bounds of ``exp``, ``log``, ``sin``,
``atan``, ... in a few real variables, each with its recorded
``:status sat|unsat`` (they were submitted by Jovanovic and de Moura for
*Solving Non-Linear Arithmetic*, IJCAR 2012). The family is kept in this
repository, in ``data/meti-tarski/``, as the SMT-LIB 2025 release
publishes it; a local copy can be named by
``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB``, and the ``dreal/benchmarks`` mirror
on GitHub is cloned sparsely into the cache when neither is there.

The parser
==========

The files are read by :func:`~sympy_extras_benchmarks.parsers.smtlib.translate`
(:mod:`~sympy_extras_benchmarks.parsers.smtlib`); this module finds them.


Source and licence
==================

The problems are kept in this repository, in ``data/meti-tarski/``: the
7006 files of the family as the **SMT-LIB 2025 release** publishes them
(doi:10.5281/zenodo.16740866), under the **CC BY 4.0** licence that
release carries, with the attribution in ``data/meti-tarski/NOTICE``.
``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB`` names a directory to read instead; if
neither is there, the 7713 files of the
`dreal/benchmarks <https://github.com/dreal/benchmarks>`_ mirror are
cloned into the cache, a mirror which carries no licence of its own and
is therefore not kept here. Only the formulas and the recorded
``:status`` are read.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
from typing import Optional

from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.smtlib import Problem, translate

__all__ = ['REPOSITORY', 'SUBDIRECTORY', 'fetch', 'load', 'load_problems']

REPOSITORY = "https://github.com/dreal/benchmarks"
SUBDIRECTORY = "smt2/smt-lib/meti-tarski"
#: a local directory with the ``.smt2`` files
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_SMTLIB'


def fetch() -> Optional[pathlib.Path]:
    """The directory of the Meti-Tarski files: the one named by
    ``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB``, or the sparse clone in the cache
    (made on first use); ``None`` when it cannot be obtained."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    kept = bundled('meti-tarski')
    if kept is not None:
        return kept
    clone = cache_directory() / 'dreal-benchmarks'
    target = clone / SUBDIRECTORY
    if target.is_dir() and any(target.iterdir()):
        return target
    try:
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                        REPOSITORY, str(clone)], check=True, capture_output=True, timeout=900)
        subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', SUBDIRECTORY],
                       check=True, capture_output=True, timeout=900)
    except (subprocess.SubprocessError, OSError):
        return None
    return target if target.is_dir() else None


def load(limit: int = 0) -> list[pathlib.Path]:
    """The paths of the problem files, sorted by name (``limit`` of them
    when it is positive); empty when they cannot be fetched."""
    directory = fetch()
    if directory is None:
        return []
    paths = sorted(directory.rglob('*.smt2'))
    return paths[:limit] if limit else paths


def load_problems(limit: int = 0) -> list[Problem]:
    """The translated problems (files which cannot be translated are
    left out)."""
    problems: list[Problem] = []
    for path in load(limit):
        problem = translate(path.read_text(errors='replace'), path.stem)
        if problem is not None:
            problems.append(problem)
    return problems


if __name__ == '__main__':
    files = load()
    counts: dict[str, int] = {}
    sizes: dict[int, int] = {}
    for path in files:
        problem = translate(path.read_text(errors='replace'), path.stem)
        key = 'untranslated' if problem is None else problem.status
        counts[key] = counts.get(key, 0) + 1
        if problem is not None:
            sizes[len(problem.variables)] = sizes.get(len(problem.variables), 0) + 1
    print("files:", len(files), counts, "variables:", dict(sorted(sizes.items())))
