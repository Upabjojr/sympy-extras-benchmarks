"""Classical partial differential equations with the dimension of their
point symmetry algebra, as published in the literature.

This is the table used by ``benchmarks/pde_symmetries.py`` of sympy-extras,
translated into SymPy expressions: twelve equations in ``u(x, t)`` with,
for each, the degree of the polynomial ansatz under which
``pde_symmetries`` is run, extra basis functions when needed, and the
number of generators expected with that ansatz (the finite-dimensional
part; the symmetries which only add solutions of a linear equation are
excluded). The values come from P. J. Olver, *Applications of Lie Groups
to Differential Equations* (1993, chapter 2 and its exercises), G. W.
Bluman and S. Kumei, *Symmetries and Differential Equations* (1989), and
N. H. Ibragimov (ed.), *CRC Handbook of Lie Group Analysis of Differential
Equations*, vol. 1 (1994).

Source and licence
==================

Nothing is downloaded and nothing is redistributed: these are **published
results**, which are facts, transcribed with their references above and
written out as SymPy expressions in this module.

Examples
========

>>> from sympy_extras_benchmarks.datasets.pde_symmetries import TABLE
>>> len(TABLE)
12
>>> TABLE[0].name, TABLE[0].expected
('heat u_t = u_xx', 6)
>>> TABLE[0].equation
Derivative(u(x, t), t) - Derivative(u(x, t), (x, 2))
"""
from __future__ import annotations

from sympy import Function, symbols, exp, sin, log, Rational
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef

from sympy_extras._typing import as_expr

__all__ = ['PDEEntry', 'TABLE', 'x', 't', 'u']

x, t, m, a = symbols('x t m a')
_u = Function('u')(x, t)
assert isinstance(_u, AppliedUndef)
u: AppliedUndef = _u


class PDEEntry:
    """One equation of the table.

    Attributes
    ==========

    name : str
        A short name with the equation in words.
    equation : Expr
        The equation as an expression equal to zero, in ``u(x, t)``.
    degree : int
        The degree of the polynomial ansatz for the infinitesimals.
    basis : tuple[Expr, ...]
        Extra basis functions for the ansatz (``log(x)`` for the
        Black-Scholes-type equation).
    expected : int
        The dimension of the algebra found with this ansatz.
    reference : str
        Where the value comes from and what the generators are.
    """

    def __init__(self, name: str, equation: Expr, degree: int, basis: tuple[Expr, ...],
                 expected: int, reference: str) -> None:
        self.name = name
        self.equation = equation
        self.degree = degree
        self.basis = basis
        self.expected = expected
        self.reference = reference

    def __repr__(self) -> str:
        return "PDEEntry(%s, dimension %d)" % (self.name, self.expected)


def _e(expr: object) -> Expr:
    return as_expr(expr)


TABLE: list[PDEEntry] = [
    PDEEntry("heat u_t = u_xx", _e(u.diff(t) - u.diff(x, 2)), 3, (), 6,
             "Olver ex. 2.41: 6 generators plus the superposition ideal"),
    PDEEntry("Burgers u_t + u u_x = u_xx", _e(u.diff(t) + u*u.diff(x) - u.diff(x, 2)), 2, (), 5,
             "Olver ex. 2.43 (Galilean algebra)"),
    PDEEntry("KdV u_t + u u_x + u_xxx = 0", _e(u.diff(t) + u*u.diff(x) + u.diff(x, 3)), 2, (), 4,
             "Olver ex. 2.44"),
    PDEEntry("wave u_tt = u_xx", _e(u.diff(t, 2) - u.diff(x, 2)), 2, (), 7,
             "polynomial part of the conformal algebra: translations, boost, dilation, "
             "2 special conformal, u d/du"),
    PDEEntry("nonlinear diffusion u_t = (u^m u_x)_x", _e(u.diff(t) - (u**m*u.diff(x)).diff(x)), 2, (), 4,
             "Ovsiannikov's classification: 4 for generic m"),
    PDEEntry("nonlinear diffusion m = -4/3", _e(u.diff(t) - (u**Rational(-4, 3)*u.diff(x)).diff(x)), 2, (), 5,
             "the exceptional exponent: an extra projective symmetry"),
    PDEEntry("Fisher u_t = u_xx + u(1 - u)", _e(u.diff(t) - u.diff(x, 2) - u*(1 - u)), 2, (), 2,
             "translations only"),
    PDEEntry("Boussinesq u_tt + u u_xx + u_x^2 + u_xxxx = 0",
             _e(u.diff(t, 2) + u*u.diff(x, 2) + u.diff(x)**2 + u.diff(x, 4)), 2, (), 3,
             "translations and a scaling (Clarkson-Kruskal)"),
    PDEEntry("Liouville u_xt = exp(u)", _e(u.diff(x, t) - exp(u)), 2, (), 6,
             "infinite algebra f(x) d/dx + g(t) d/dt - (f' + g') d/du: 3 + 3 polynomials of degree <= 2"),
    PDEEntry("sine-Gordon u_xt = sin(u)", _e(u.diff(x, t) - sin(u)), 2, (), 3,
             "translations and the Lorentz-type scaling x d/dx - t d/dt"),
    PDEEntry("potential Burgers u_t = u_xx + u_x^2", _e(u.diff(t) - u.diff(x, 2) - u.diff(x)**2), 3, (), 6,
             "linearisable by u = log v: the heat algebra"),
    PDEEntry("Black-Scholes-type u_t + x^2 u_xx/2 = 0", _e(u.diff(t) + x**2*u.diff(x, 2)/2), 2,
             (_e(log(x)),), 5,
             "5 of the 6 generators of Gazizov-Ibragimov; the sixth needs t*log(x)**2 terms"),
]
