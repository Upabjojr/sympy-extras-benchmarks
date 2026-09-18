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

Every source is read through the Maxima parser of
:mod:`~sympy_extras_benchmarks.parsers.maxima` (REDUCE, FriCAS and holpy
expressions rewritten into Maxima's syntax first), whose
:func:`~sympy_extras_benchmarks.parsers.maxima.relation` reads the facts.

Examples
========

>>> from sympy import Symbol, exp, oo
>>> from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
>>> from sympy_extras_benchmarks.parsers.maxima import relation
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

from typing import Optional, Sequence

from sympy import Integral, Symbol, sympify
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_expr

__all__ = ['DefiniteIntegral', 'PROPERTIES']


#: the properties a parameter may be declared to have, each the name of the
#: SymPy assumption it becomes
PROPERTIES: frozenset[str] = frozenset({'integer', 'noninteger', 'even', 'odd', 'real'})


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


