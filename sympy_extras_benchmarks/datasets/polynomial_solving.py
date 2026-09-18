"""Systems of polynomial equations from the ``algsys`` regression file of
Maxima, as SymPy expressions.

The dataset
===========

Maxima's ``tests/rtest_algsys.mac`` collects the systems an early paper on
``algsys`` worked through, together with the ones that later broke it:

* W. A. Beyer, *Solution of Simultaneous Polynomial Equations by
  Elimination in MACSYMA*, Proceedings of the 1984 MACSYMA Users'
  Conference, 110-120;
* A. P. Morgan, *A Method for Computing All Solutions to Systems of
  Polynomial Equations*, ACM TOMS 9:1-17 (1983).

They are small but awkward on purpose: positive-dimensional components,
solutions that are real in the paper and complex in fact, systems whose
Bézout number is far above the number of solutions, and a few where the
published answer is wrong (the file says so).

What is read, and what is not
=============================

Only the **equations and the variables** are read. The solutions Maxima
records are read too, but as a *count* and nothing more — they are a third
opinion, not the answer key, because several of them are floating point,
some carry Maxima's arbitrary constants (``%r1``) and at least one is
marked in the file as disagreeing with the paper. A driver checks its own
solutions by substituting them back, and asks Mathematica how many there
should be.

Source and licence
==================

Maxima is distributed under the **GNU General Public License, version 2**.
The file is kept under it in ``data/maxima/`` (see ``data/README.md``) and
read from there, or from ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``, or
from the cache, like the collections read by
:mod:`~sympy_extras_benchmarks.datasets.maxima_ode`, whose Maxima
expression parser this module reuses. **Maxima's code is not used**, and
its recorded solutions are only counted.

Examples
========

>>> from sympy_extras_benchmarks.datasets.polynomial_solving import systems
>>> text = '''
... /* a small one */
... algsys([x^2+x*y-1,y^2+x-5],[x,y]);
... [[x = 1,y = 2],[x = 3,y = 4]];
... '''
>>> system, = systems(text, 'demo')
>>> system
PolynomialSystem(demo:1, 2 equations, 2 unknowns, 2 recorded)
>>> system.equations
[x**2 + x*y - 1, x + y**2 - 5]
>>> system.variables
[x, y]
"""
from __future__ import annotations

import re
from typing import Optional

from sympy import Symbol
from sympy.core.expr import Expr

from sympy_extras_benchmarks.datasets.maxima_ode import TESTS_SUBDIRECTORY, fetch as fetch_maxima
from sympy_extras_benchmarks.parsers.maxima import (
    MaximaSyntaxError, group, parse_expression, split_arguments, strip_comments)

__all__ = ['PolynomialSystem', 'FILE', 'fetch', 'load', 'systems']

#: the Maxima regression file read
FILE = 'rtest_algsys'

#: a name that cannot occur in the file, so that the Maxima parser of
#: :mod:`~sympy_extras_benchmarks.datasets.maxima_ode` — which is written
#: for differential equations — leaves every name a plain symbol
_NO_FUNCTION = '__not_a_dependent_variable__'

_CALL = re.compile(r'\balgsys\s*\(', re.S)
#: ``name : expression;`` at the start of a line, which the file uses to
#: name an equation before passing it to ``algsys``
_ASSIGNMENT = re.compile(r"^([A-Za-z_][A-Za-z_0-9]*)\s*:(?!=)\s*(.+?)[;$]\s*$", re.M)


class PolynomialSystem:
    """One ``algsys`` call of the regression file.

    Attributes
    ==========

    name : str
        The file and the position of the call in it.
    equations : list[Expr]
        The system, each equation as an expression equal to zero.
    variables : list[Symbol]
        The unknowns, in the order the call names them.
    recorded : int or None
        How many solutions Maxima records, or ``None`` when the recorded
        answer could not be counted. It is a third opinion and not an
        answer key: see the module docstring.
    parametric : bool
        Whether the recorded answer carries an arbitrary constant, so the
        solution set is positive-dimensional and counting is meaningless.
    """

    def __init__(self, name: str, equations: list[Expr], variables: list[Symbol],
                 recorded: Optional[int], parametric: bool) -> None:
        self.name = name
        self.equations = equations
        self.variables = variables
        self.recorded = recorded
        self.parametric = parametric

    def __repr__(self) -> str:
        return "PolynomialSystem(%s, %d equations, %d unknowns, %s recorded)" % (
            self.name, len(self.equations), len(self.variables),
            'parametric' if self.parametric else self.recorded)


def _recorded(text: str, start: int) -> tuple[Optional[int], bool]:
    """``(number of solutions, parametric)`` from the answer that follows
    the call, which ends at the next ``;`` outside brackets."""
    while start < len(text) and text[start] in ' \t\r\n);':
        if text[start] == ';':
            start += 1
            break
        start += 1
    while start < len(text) and text[start] in ' \t\r\n':
        start += 1
    if start >= len(text) or text[start] != '[':
        return None, False
    closed = group(text, start)
    if closed is None:
        return None, False
    body = closed[0]
    return len(split_arguments(body)), '%r' in body


def _assignments(text: str, upto: int) -> dict[str, str]:
    """The ``name : expression`` bindings in force at position ``upto``.

    The file names several systems before solving them, and an equation
    given to ``algsys`` may be one of those names rather than a
    polynomial. A name bound more than once takes its most recent value.
    """
    bindings: dict[str, str] = {}
    for match in _ASSIGNMENT.finditer(text):
        if match.start() >= upto:
            break
        bindings[match.group(1)] = match.group(2).strip()
    return bindings


def _resolve(source: str, bindings: dict[str, str]) -> str:
    """``source`` with a bound name replaced by what it stands for.

    Only a source that is exactly a name is substituted: the file never
    uses one inside a larger expression, and rewriting blindly would risk
    capturing a variable of the system.
    """
    body = source.strip()
    seen = 0
    while body in bindings and seen < 8:
        body = bindings[body].strip()
        seen += 1
    return body


def systems(text: str, name: str = '') -> list[PolynomialSystem]:
    """Every ``algsys`` call of the file that this module can read.

    Calls inside a comment are skipped: the file disables an entry by
    commenting it out, so those are not tests the suite runs.
    """
    text = strip_comments(text)
    found: list[PolynomialSystem] = []
    for index, match in enumerate(_CALL.finditer(text), start=1):
        arguments = group(text, match.end() - 1)
        if arguments is None:
            continue
        parts = split_arguments(arguments[0])
        if len(parts) != 2 or not parts[0].startswith('[') or not parts[1].startswith('['):
            continue
        bindings = _assignments(text, match.start())
        try:
            equations = [parse_expression(_resolve(e, bindings), _NO_FUNCTION, _NO_FUNCTION)
                         for e in split_arguments(parts[0][1:-1])]
            unknowns = [parse_expression(v, _NO_FUNCTION, _NO_FUNCTION)
                        for v in split_arguments(parts[1][1:-1])]
        except (MaximaSyntaxError, RecursionError, ValueError):
            continue
        if not equations or not all(isinstance(v, Symbol) for v in unknowns):
            continue
        # an equation mentioning none of the unknowns is a name this module
        # failed to resolve, not a system worth putting to a solver
        if not any(e.free_symbols & set(unknowns) for e in equations):
            continue
        variables = [v for v in unknowns if isinstance(v, Symbol)]
        count, parametric = _recorded(text, arguments[1])
        found.append(PolynomialSystem('%s:%d' % (name, index), equations, variables,
                                      count, parametric))
    return found


def fetch() -> Optional[str]:
    """The text of the regression file, or ``None`` when it cannot be
    obtained."""
    return fetch_maxima(FILE, TESTS_SUBDIRECTORY)


def load() -> list[PolynomialSystem]:
    """Every readable system of the regression file."""
    text = fetch()
    return systems(text, FILE) if text is not None else []
