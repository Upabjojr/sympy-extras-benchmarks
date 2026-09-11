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

holpy is distributed under the **BSD 3-Clause** licence (``LICENSE`` in
the repository); the problems are credited in its files to the MIT
Integration Bee, Schaum's Outline and UC Davis. Nothing of it is stored in
this repository: ``integral/examples`` is cloned sparsely on first use into
the cache directory, or read from ``$SYMPY_EXTRAS_BENCHMARKS_HOLPY`` (a
checkout of holpy, or the examples directory itself).

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
import re
import subprocess
from typing import Optional, Sequence, Union

from sympy import Catalan, Symbol
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.integrals import (
    DefiniteIntegral, group, parse, relation, split_arguments)

__all__ = ['REPOSITORY', 'SUBTREE', 'integrals', 'to_maxima', 'fetch', 'load']

REPOSITORY = "https://github.com/bzhan/holpy"
SUBTREE = 'integral/examples'
#: a checkout of holpy, or its examples directory
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_HOLPY'

#: a JSON value, as the example files hold it
JSONValue = Union[None, bool, int, float, str, list['JSONValue'], dict[str, 'JSONValue']]

#: holpy's names and Maxima's
_NAMES: dict[str, str] = {'Gamma': 'gamma', 'B': 'beta'}
_INTEGRAL = re.compile(r"INT\s+([A-Za-z_]\w*)\s*:\s*\[")


def to_maxima(text: str) -> str:
    """A holpy expression in Maxima's syntax and names.

    >>> to_maxima('Gamma(1/4) ^ 2 / (2 * sqrt(pi)) + B(m, n) - oo')
    gamma(1/4) ^ 2 / (2 * sqrt(%pi)) + beta(m, n) - inf
    """
    body = re.sub(r"(?<![\w%])pi(?!\w)", '%pi', text)
    body = re.sub(r"(?<![\w%])oo(?!\w)", 'inf', body)
    for name, maxima in _NAMES.items():
        body = re.sub(r"(?<![\w%])" + re.escape(name) + r"\s*\(", maxima + '(', body)
    return body


def _value(text: str) -> Optional[Expr]:
    """A closed-form holpy expression; ``G`` is Catalan's constant."""
    value = parse(to_maxima(text))
    if value is None:
        return None
    return as_expr(value.xreplace({Symbol('G'): Catalan}))


def _unbracketed(text: str) -> str:
    body = text.strip()
    while body.startswith('('):
        closed = group(body, 0)
        if closed is None or closed[1] != len(body):
            break
        body = closed[0].strip()
    return body


def _integral(text: str) -> Optional[tuple[Expr, Symbol, Expr, Expr]]:
    """``INT x:[a, b]. f`` as its parts, or ``None``."""
    body = _unbracketed(text)
    match = _INTEGRAL.match(body)
    if match is None:
        return None
    closed = group(body, match.end() - 1)
    if closed is None:
        return None
    bounds = split_arguments(closed[0])
    rest = body[closed[1]:].lstrip()
    if len(bounds) != 2 or not rest.startswith('.'):
        return None
    integrand = _value(rest[1:])
    lower, upper = _value(bounds[0]), _value(bounds[1])
    if integrand is None or lower is None or upper is None:
        return None
    return integrand, Symbol(match.group(1)), lower, upper


def _sides(goal: str) -> Optional[tuple[str, str]]:
    """The two sides of an equation at its top-level ``=``."""
    depth = 0
    for index, character in enumerate(goal):
        if character in '([':
            depth += 1
        elif character in ')]':
            depth -= 1
        elif (character == '=' and depth == 0 and goal[index - 1:index] not in ('<', '>', '!')
              and goal[index + 1:index + 2] != '='):
            return goal[:index], goal[index + 1:]
    return None


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
        fact = relation(to_maxima(text.replace('!=', '#')))
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
            read = _integral(problem)
            steps = item.get('calc')
            if isinstance(steps, list) and steps and isinstance(steps[-1], dict):
                last = steps[-1].get('text')
                if isinstance(last, str) and 'INT' not in last:
                    recorded = _value(last)
        elif isinstance(goal, str):
            sides = _sides(goal)
            if sides is None:
                continue
            for integral_side, other in (sides, sides[::-1]):
                read = _integral(integral_side)
                if read is not None:
                    if _integral(other) is None:
                        recorded = _value(other)
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
