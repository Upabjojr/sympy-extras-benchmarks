"""Definite integrals: the record every integration dataset reads to.

Each collection of definite integrals here — Maxima's integration and
transform tests (:mod:`~sympy_extras_benchmarks.datasets.maxima_integrals`),
REDUCE's DEFINT tests (:mod:`~sympy_extras_benchmarks.datasets.reduce_defint`),
FriCAS's ``mapleok`` collection
(:mod:`~sympy_extras_benchmarks.datasets.fricas_integrals`) and holpy's
worked problems (:mod:`~sympy_extras_benchmarks.datasets.holpy_integrals`)
— is read to a list of :class:`DefiniteIntegral`: the integrand, the
variable, the two bounds, what the source assumes about the parameters,
and the value the source records when it records one.

A recorded value is a **third opinion**, never the answer key: it is what
the source's own system computed, and those systems have bugs. A driver
checks a result against numerical quadrature
(:mod:`~sympy_extras_benchmarks.oracles.quadrature`) and reports a recorded
value that quadrature contradicts as a finding about the source.

The helpers read the notation the sources share: Maxima's relations
(``a > 0``, ``a # 0``, ``notequal(a, 0)``) for the facts, and the
splitting of an argument list at its top-level commas.

Examples
========

>>> from sympy import Symbol, exp, oo
>>> from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral, relation
>>> x = Symbol('x')
>>> entry = DefiniteIntegral('demo:1', exp(-x), x, 0, oo, recorded=1)
>>> entry
DefiniteIntegral(demo:1, x from 0 to oo, recorded 1)
>>> entry.integral()
Integral(exp(-x), (x, 0, oo))
>>> relation('a+1 > 0')
a + 1 > 0
>>> relation('notequal(a, 0)')
Ne(a, 0)
"""
from __future__ import annotations

import re
from typing import Callable, Optional, Sequence

from sympy import Derivative, Eq, Ge, Gt, Integral, Le, Lt, Ne, Product, Sum, Symbol, nan, sympify
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.datasets.maxima_ode import MaximaSyntaxError, parse_expression

__all__ = ['DefiniteIntegral', 'NO_FUNCTION', 'PROPERTIES', 'readable', 'relation',
           'parse', 'split_arguments', 'group']

#: a name that cannot occur in the files, so the Maxima parser — written
#: for differential equations — leaves every name a plain symbol
NO_FUNCTION = '__not_a_dependent_variable__'

#: the properties a parameter may be declared to have, each the name of the
#: SymPy assumption it becomes
PROPERTIES: frozenset[str] = frozenset({'integer', 'noninteger', 'even', 'odd', 'real'})

#: the relational operators, the two-character ones first
_RELATIONS: tuple[tuple[str, Callable[[Expr, Expr], Boolean]], ...] = (
    ('>=', Ge), ('<=', Le), ('#', Ne), ('>', Gt), ('<', Lt), ('=', Eq))

_OPEN, _CLOSE = '([{', ')]}'


class DefiniteIntegral:
    """One definite integral of a collection.

    Attributes
    ==========

    name : str
        The collection and the position of the integral in it.
    integrand : Expr
    variable : Symbol
    lower, upper : Expr
        The bounds; ``oo`` and ``-oo`` for an infinite range.
    facts : tuple of Boolean
        Relations the source assumes while the integral is computed
        (``a > 0``), in terms of the parameters.
    properties : tuple of (Symbol, str)
        Declared properties of the parameters, each one of
        :data:`PROPERTIES` (``(n, 'integer')``).
    recorded : Expr or None
        The value the source records, or ``None`` when it records none
        this module reads.
    """

    def __init__(self, name: str, integrand: object, variable: Symbol, lower: object,
                 upper: object, facts: Sequence[Boolean] = (),
                 properties: Sequence[tuple[Symbol, str]] = (),
                 recorded: Optional[object] = None) -> None:
        self.name = name
        self.integrand = as_expr(sympify(integrand))
        self.variable = variable
        self.lower = as_expr(sympify(lower))
        self.upper = as_expr(sympify(upper))
        self.facts = tuple(facts)
        self.properties = tuple(properties)
        self.recorded = None if recorded is None else as_expr(sympify(recorded))

    @property
    def parameters(self) -> list[Symbol]:
        """The symbols other than the variable, sorted by name."""
        found: set[Symbol] = set()
        for expr in (self.integrand, self.lower, self.upper):
            found |= {s for s in expr.free_symbols if isinstance(s, Symbol)}
        found.discard(self.variable)
        return sorted(found, key=lambda s: s.name)

    def integral(self) -> Integral:
        """The unevaluated SymPy integral."""
        return Integral(self.integrand, (self.variable, self.lower, self.upper))

    def key(self) -> tuple[Expr, Symbol, Expr, Expr]:
        """What two entries share when they state the same integral."""
        return (self.integrand, self.variable, self.lower, self.upper)

    def __repr__(self) -> str:
        return "DefiniteIntegral(%s, %s from %s to %s, recorded %s)" % (
            self.name, self.variable, self.lower, self.upper, self.recorded)


def readable(expr: object) -> bool:
    """Whether ``expr`` is a value this package can reason about: an
    expression without undefined functions, derivatives, integrals, sums,
    products or ``nan`` — any of which means a name or construct of the
    source that did not translate."""
    if not isinstance(expr, Expr):
        return False
    if expr.has(nan):
        return False
    return not expr.atoms(AppliedUndef, Derivative, Integral, Sum, Product)


def parse(text: str) -> Optional[Expr]:
    """A Maxima expression as a readable SymPy expression, or ``None``."""
    try:
        value = parse_expression(text, NO_FUNCTION, NO_FUNCTION)
    except (MaximaSyntaxError, RecursionError, ValueError, TypeError, ZeroDivisionError):
        return None
    return value if readable(value) else None


def group(text: str, start: int) -> Optional[tuple[str, int]]:
    """The inside of the bracketed group opening at ``text[start]``, and the
    index after its closing bracket; ``None`` when it does not close."""
    depth, index, quoted = 0, start, False
    while index < len(text):
        character = text[index]
        if character == '"':
            quoted = not quoted
        elif not quoted and character in _OPEN:
            depth += 1
        elif not quoted and character in _CLOSE:
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    return None


def split_arguments(text: str) -> list[str]:
    """``text`` split at its top-level commas, each part stripped.

    >>> split_arguments('f(x, y), [a, b], "c, d"')
    ['f(x, y)', '[a, b]', '"c, d"']
    """
    parts: list[str] = []
    depth, last, quoted = 0, 0, False
    for index, character in enumerate(text):
        if character == '"':
            quoted = not quoted
        elif quoted:
            continue
        elif character in _OPEN:
            depth += 1
        elif character in _CLOSE:
            depth -= 1
        elif character == ',' and depth == 0:
            parts.append(text[last:index].strip())
            last = index + 1
    parts.append(text[last:].strip())
    return [p for p in parts if p]


def relation(text: str) -> Optional[Boolean]:
    """A Maxima relation (``a > 0``, ``a # b``, ``notequal(a, 0)``,
    ``equal(a, b)``) as a SymPy one, or ``None`` when it is not one."""
    body = text.strip()
    call = re.fullmatch(r'(not)?equal\s*\((.*)\)', body, re.S)
    if call is not None:
        arguments = split_arguments(call.group(2))
        if len(arguments) != 2:
            return None
        lhs, rhs = parse(arguments[0]), parse(arguments[1])
        if lhs is None or rhs is None:
            return None
        return as_boolean(Ne(lhs, rhs) if call.group(1) else Eq(lhs, rhs))
    depth = 0
    for index, character in enumerate(body):
        if character in _OPEN:
            depth += 1
        elif character in _CLOSE:
            depth -= 1
        elif depth == 0:
            for symbol, build in _RELATIONS:
                if body.startswith(symbol, index):
                    lhs, rhs = parse(body[:index]), parse(body[index + len(symbol):])
                    if lhs is None or rhs is None:
                        return None
                    return as_boolean(build(lhs, rhs))
    return None
