"""The expression language of holpy, read through Maxima's.

holpy writes definite integrals ``INT x:[a, b]. f``, ``pi`` and ``oo``
without a sigil, ``Gamma`` and ``B`` for the gamma and beta functions and
``G`` for Catalan's constant. :func:`to_maxima` rewrites the names so that
the expression parser of :mod:`~sympy_extras_benchmarks.parsers.maxima`
reads an expression; :func:`value` reads a closed-form value,
:func:`integral` the parts of an integral, :func:`sides` the two sides of
an equation and :func:`condition` a condition such as ``a > 0``.

Nothing here reads a file or knows which collection a text comes from.
"""
from __future__ import annotations

import re
from typing import Optional

from sympy import Catalan, Symbol
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.parsers.maxima import group, parse, relation, split_arguments

__all__ = ['to_maxima', 'value', 'integral', 'sides', 'condition']

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


def value(text: str) -> Optional[Expr]:
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


def integral(text: str) -> Optional[tuple[Expr, Symbol, Expr, Expr]]:
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
    integrand = value(rest[1:])
    lower, upper = value(bounds[0]), value(bounds[1])
    if integrand is None or lower is None or upper is None:
        return None
    return integrand, Symbol(match.group(1)), lower, upper


def sides(goal: str) -> Optional[tuple[str, str]]:
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


def condition(text: str) -> Optional[Boolean]:
    """A holpy condition (``k > 0``, ``a != 1``) as a SymPy relation, or
    ``None`` when it does not translate."""
    return relation(to_maxima(text.replace('!=', '#')))
