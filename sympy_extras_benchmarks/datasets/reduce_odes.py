"""Ordinary differential equations from the test suite of REDUCE's
``ODESolve`` package, as SymPy expressions.

The dataset
===========

REDUCE ships a test file per part of its ODE solver. Three of them —
``zimmer.tst``, ``zimmerop.tst`` and ``zimopbas.tst`` — are the
**Postel–Zimmermann** collection, the equations of

    F. Postel and P. Zimmermann, *A Review of the ODE Solvers of AXIOM,
    Derive, Maple, Mathematica, Macsyma, MuPAD and Reduce* (1996),

assembled to compare computer algebra systems against one another. The
rest (``odesolve.tst``, ``misc.tst``, ``extend.tst``) are REDUCE's own
regression equations.

This is the point of the module: every other ODE dataset here comes from
Kamke and Murphy, so a solver could be tuned to those two books and look
good. Postel–Zimmermann is an independent selection, and it was chosen to
be discriminating between systems.

Only the equations are read — they are the mathematical content, and the
same equations appear in the paper. REDUCE's solutions and code are not
used; a solution found here is checked with ``checkodesol`` and against
Mathematica, not against REDUCE.

Source and licence
==================

REDUCE is distributed under the *Reduce License*, a **BSD 2-clause**
style licence (see the ``LICENSE`` file of the repository; GitHub does not
recognise it as a standard SPDX identifier). The package directory is kept
under it in ``data/reduce/`` with that ``LICENSE`` beside it (see
``data/README.md``) and read from there, or from a local checkout named by
``$SYMPY_EXTRAS_BENCHMARKS_REDUCE``; if neither is there it is cloned
sparsely into the cache.

The parser
==========

REDUCE's syntax needs a preprocessor before the Maxima expression parser
of :mod:`~sympy_extras_benchmarks.datasets.maxima_ode` can read it:

* ``df(y,x)`` and ``df(y,x,2)`` are derivatives, written ``'diff(...)``
  in Maxima;
* multiplication is implicit between a number and a name, and between a
  number and a call: ``2x``, ``4df(y,x)``, ``(3+6x)``;
* a function of one argument may be written without brackets: ``sin x``,
  ``log y``;
* ``e`` is Euler's number and ``**`` and ``^`` are both exponentiation.

Anything left that the Maxima parser refuses is skipped rather than
guessed at.

Examples
========

>>> from sympy_extras_benchmarks.datasets.reduce_odes import equations
>>> text = "odesolve(df(y,x,2) - 2x*df(y,x) + 2y = 3, y, x);"
>>> entry, = equations(text, 'demo')
>>> entry
ReduceODE(demo:1, order 2)
>>> entry.equation
-2*x*Derivative(y(x), x) + 2*y(x) + Derivative(y(x), (x, 2)) - 3
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy import Function, Symbol
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef

from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.maxima import (
    MaximaSyntaxError, derivative_order, parse_expression, split_arguments)
from sympy_extras_benchmarks.parsers.reduce import strip_comments, to_maxima

__all__ = ['ReduceODE', 'REPOSITORY', 'SUBTREE', 'FILES', 'fetch', 'load', 'equations',
           'to_maxima', 'package_directory']

REPOSITORY = "https://github.com/reduce-algebra/reduce-algebra"
SUBTREE = 'packages/odesolve'
#: a local checkout of REDUCE
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_REDUCE'
#: the test files read; the first three are Postel-Zimmermann
FILES: tuple[str, ...] = ('zimmer.tst', 'zimmerop.tst', 'zimopbas.tst',
                          'odesolve.tst', 'misc.tst', 'extend.tst')


_CALL = re.compile(r'\bodesolve\s*\(', re.S)


class ReduceODE:
    """One ``odesolve`` call of a REDUCE test file.

    Attributes
    ==========

    name : str
        The file and the position of the call in it.
    equation : Expr
        The equation as an expression equal to zero, in ``y(x)``.
    function : AppliedUndef
        The unknown, ``y(x)``.
    order : int
        The highest derivative that occurs.
    """

    def __init__(self, name: str, equation: Expr, function: AppliedUndef, order: int) -> None:
        self.name = name
        self.equation = equation
        self.function = function
        self.order = order

    def __repr__(self) -> str:
        return "ReduceODE(%s, order %d)" % (self.name, self.order)


def equations(text: str, name: str = '') -> list[ReduceODE]:
    """Every ``odesolve`` call of a REDUCE test file that can be read."""
    body = strip_comments(text)
    found: list[ReduceODE] = []
    for index, match in enumerate(_CALL.finditer(body), start=1):
        depth, end = 0, match.end() - 1
        while end < len(body):
            if body[end] == '(':
                depth += 1
            elif body[end] == ')':
                depth -= 1
                if depth == 0:
                    break
            end += 1
        else:
            continue
        arguments = split_arguments(body[match.end():end])
        if not arguments:
            continue
        dependent, independent = 'y', 'x'
        if len(arguments) >= 3:
            dependent, independent = arguments[1].strip(), arguments[2].strip()
        if not (dependent.isidentifier() and independent.isidentifier()):
            continue
        try:
            equation = parse_expression(to_maxima(arguments[0]), dependent, independent)
        except (MaximaSyntaxError, RecursionError, ValueError, TypeError):
            continue
        function = Function(dependent)(Symbol(independent))
        order = derivative_order(equation, function)
        if order < 1 or not equation.has(function):
            continue
        found.append(ReduceODE('%s:%d' % (name, index), equation, function, order))
    return found


def package_directory(subtree: str = SUBTREE) -> Optional[pathlib.Path]:
    """The directory ``subtree`` of REDUCE's sources: under
    ``$SYMPY_EXTRAS_BENCHMARKS_REDUCE`` (a checkout, or the directory itself),
    or in a sparse clone in the cache, to which a missing subtree is added.
    ``None`` when unobtainable."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        root = pathlib.Path(override)
        return root / subtree if (root / subtree).is_dir() else root
    kept = bundled('reduce', subtree)
    if kept is not None:
        return kept
    clone = cache_directory() / 'reduce'
    if not (clone / subtree).is_dir():
        try:
            if not (clone / '.git').is_dir():
                subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                                REPOSITORY, str(clone)],
                               check=True, capture_output=True, timeout=1800)
                subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', subtree],
                               check=True, capture_output=True, timeout=1800)
            else:
                subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'add', subtree],
                               check=True, capture_output=True, timeout=1800)
        except (subprocess.SubprocessError, OSError):
            return None
    return clone / subtree if (clone / subtree).is_dir() else None


def fetch() -> list[pathlib.Path]:
    """The test files: from ``$SYMPY_EXTRAS_BENCHMARKS_REDUCE``, or a
    sparse clone in the cache. An empty list when unobtainable."""
    directory = package_directory(SUBTREE)
    if directory is None:
        return []
    return [directory / f for f in FILES if (directory / f).is_file()]


def load() -> list[ReduceODE]:
    """Every readable equation of the fetched files."""
    found: list[ReduceODE] = []
    for path in fetch():
        try:
            text = path.read_text(errors='replace')
        except OSError:
            continue
        found.extend(equations(text, path.stem))
    return found
