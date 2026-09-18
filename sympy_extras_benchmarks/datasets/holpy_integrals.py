"""Definite integrals from the worked examples of holpy, as SymPy
expressions.

The dataset
===========

holpy (B. Zhan and others, Institute of Software, Chinese Academy of
Sciences) computes definite integrals interactively: the user chooses each
step — a substitution, an integration by parts, a trigonometric identity —
and the system checks it (R. Xu, L. Li and B. Zhan, *Verified Interactive
Computation of Definite Integrals*, CADE 2021). Its examples are of two
kinds:

* **problems**, ``INT x:[a, b]. f``, each with the worked computation:
  the MIT Integration Bee (2013, 2014, 2019, 2020), Schaum's Outline and
  the calculus exercises of UC Davis — undergraduate integrals, the kind a
  system should simply get right;
* **goals**, equations such as ``(INT x:[0,1]. atan(x)/x) = G`` proved in
  the system with the conditions they need: Ahmed's integral, Frullani and
  Dirichlet integrals, Catalan's constant, Euler's log-sine integral,
  Wallis, the beta and gamma functions, Bernoulli's ``x^x``.

What is read, and what is not
=============================

* a problem, and as its recorded value the last line of its computation
  when that line is in closed form;
* a goal one side of which is a definite integral, with the other side as
  its recorded value when that side is in closed form, and the goal's
  conditions (``a > 0``, ``m < 1``) as facts. A goal about the
  intermediate functions of a derivation (``I(a)``, ``D u. I(u)``), or
  whose other side is a series (``SUM``), is not read.

The recorded value is the result of a checked computation, but the
transcription of the problem is not checked, so it is still a **third
opinion** (see :mod:`~sympy_extras_benchmarks.datasets.integrals`).
holpy's steps and code are not used.

Source and licence
==================

holpy is distributed under the **BSD 3-Clause** licence; the problems are
credited in its files to the MIT Integration Bee, Schaum's Outline and UC
Davis. The examples are kept under that licence in ``data/holpy/`` with
holpy's ``LICENSE`` beside them (see ``data/README.md``) and read from
there, or from ``$SYMPY_EXTRAS_BENCHMARKS_HOLPY`` (a checkout of holpy, or
the examples directory itself); if neither is there,
``integral/examples`` is cloned sparsely into the cache.

Examples
========

>>> from sympy_extras_benchmarks.datasets.holpy_integrals import integrals
>>> problem = {"problem": "INT t:[0, pi/4]. sec(t)^2",
...            "calc": [{"text": "INT t:[0,pi / 4]. sec(t) ^ 2"}, {"text": "1"}]}
>>> goal = {"goal": "(INT t:[0,oo]. exp(-k * t)) = 1 / k", "conds": [{"cond": "k > 0"}]}
>>> first, second = integrals([problem, goal], 'demo')
>>> first
DefiniteIntegral(demo:1, t from 0 to pi/4, recorded 1)
>>> second.integrand, second.recorded, second.facts
(exp(-k*t), 1/k, (k > 0,))
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
from typing import Optional, Sequence, Union

from sympy import Symbol
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.parsers.holpy import condition as holpy_condition, integral, sides, value

__all__ = ['REPOSITORY', 'SUBTREE', 'integrals', 'fetch', 'load',
           'LICENCE', 'LICENCE_FILES', 'licence_files']

REPOSITORY = "https://github.com/bzhan/holpy"
SUBTREE = 'integral/examples'
#: the licence, and the file at the root of the repository carrying it,
#: which the sparse clone keeps
LICENCE = 'BSD-3-Clause'
LICENCE_FILES: tuple[str, ...] = ('LICENSE',)
#: a checkout of holpy, or its examples directory
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_HOLPY'

#: a JSON value, as the example files hold it
JSONValue = Union[None, bool, int, float, str, list['JSONValue'], dict[str, 'JSONValue']]


def _facts(conditions: JSONValue) -> Optional[list[Boolean]]:
    """The conditions of an entry as relations; ``None`` when one of them
    does not translate (the entry then cannot be read faithfully)."""
    if conditions is None:
        return []
    if not isinstance(conditions, list):
        return None
    facts: list[Boolean] = []
    for condition in conditions:
        text = condition.get('cond') if isinstance(condition, dict) else condition
        if not isinstance(text, str):
            return None
        fact = holpy_condition(text)
        if fact is None:
            return None
        facts.append(fact)
    return facts


def integrals(content: Sequence[JSONValue], name: str = '') -> list[DefiniteIntegral]:
    """Every definite integral of the entries of one example file."""
    found: list[DefiniteIntegral] = []
    for index, item in enumerate(content, start=1):
        if not isinstance(item, dict):
            continue
        recorded: Optional[Expr] = None
        read: Optional[tuple[Expr, Symbol, Expr, Expr]] = None
        problem, goal = item.get('problem'), item.get('goal')
        if isinstance(problem, str):
            read = integral(problem)
            steps = item.get('calc')
            if isinstance(steps, list) and steps and isinstance(steps[-1], dict):
                last = steps[-1].get('text')
                if isinstance(last, str) and 'INT' not in last:
                    recorded = value(last)
        elif isinstance(goal, str):
            sides_ = sides(goal)
            if sides_ is None:
                continue
            for integral_side, other in (sides_, sides_[::-1]):
                read = integral(integral_side)
                if read is not None:
                    if integral(other) is None:
                        recorded = value(other)
                    break
        if read is None:
            continue
        facts = _facts(item.get('conds'))
        if facts is None:
            continue
        integrand, variable, lower, upper = read
        entry = DefiniteIntegral('%s:%d' % (name, index), integrand, variable, lower, upper,
                                 recorded=recorded)
        parameters = set(entry.parameters)
        entry.facts = tuple(f for f in facts if f.free_symbols and f.free_symbols <= parameters)
        found.append(entry)
    return found


def _directory() -> Optional[pathlib.Path]:
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        root = pathlib.Path(override)
        return root / SUBTREE if (root / SUBTREE).is_dir() else root
    kept = bundled('holpy', SUBTREE)
    if kept is not None:
        return kept
    clone = cache_directory() / 'holpy'
    if not (clone / SUBTREE).is_dir():
        try:
            subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                            REPOSITORY, str(clone)], check=True, capture_output=True, timeout=1800)
            subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', SUBTREE],
                           check=True, capture_output=True, timeout=1800)
        except (subprocess.SubprocessError, OSError):
            return None
    return clone / SUBTREE if (clone / SUBTREE).is_dir() else None


def licence_files() -> list[pathlib.Path]:
    """The licence files kept with the fetched data."""
    directory = _directory()
    if directory is None:
        return []
    root = directory.parent.parent if directory.as_posix().endswith(SUBTREE) else directory
    return [root / name for name in LICENCE_FILES if (root / name).is_file()]


def fetch() -> list[tuple[str, list[JSONValue]]]:
    """``(collection, entries)`` for every example file, the collection
    being the file's path without ``.json`` (``MIT/2013``)."""
    directory = _directory()
    if directory is None:
        return []
    found: list[tuple[str, list[JSONValue]]] = []
    for path in sorted(directory.rglob('*.json')):
        try:
            data = json.loads(path.read_text(errors='replace'))
        except (OSError, ValueError):
            continue
        content = data.get('content') if isinstance(data, dict) else None
        if isinstance(content, list):
            found.append((path.relative_to(directory).with_suffix('').as_posix(), content))
    return found


def load() -> list[DefiniteIntegral]:
    """Every readable definite integral of the examples, each integral once."""
    found: list[DefiniteIntegral] = []
    seen: set[tuple[object, ...]] = set()
    for collection, content in fetch():
        for entry in integrals(content, collection):
            if entry.key() not in seen:
                seen.add(entry.key())
                found.append(entry)
    return found
