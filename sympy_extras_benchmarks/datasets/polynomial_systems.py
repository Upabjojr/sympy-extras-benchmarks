"""Standard families of polynomial systems with known invariants: the
Katsura and cyclic systems.

These are the benchmark families used by the ``test_ideals_known.py``
tests of sympy-extras (as results, not code), extended to more members.
The invariants are classical: Katsura-m is zero-dimensional with ``2**m``
solutions counted with multiplicity (and radical, so ``2**m`` distinct
solutions); cyclic-m has finitely many solutions when ``m`` is
square-free, ``binomial(2m-2, m-1)`` of them for ``m`` prime (6 for
m = 3, 70 for m = 5, 924 for m = 7: U. Haagerup, *Cyclic p-roots of prime
lengths p and related complex Hadamard matrices*, 2008) and 156 for m = 6
(J. Backelin, R. Fröberg, *How we proved that there are exactly 924 cyclic
7-roots*, ISSAC 1991; G. Björck, R. Fröberg, *A faster way to count the
solutions of inhomogeneous systems of algebraic equations, with
applications to cyclic n-roots*, JSC 12, 1991), and positive dimension
otherwise (cyclic-4 has dimension 1, as do cyclic-8 and cyclic-9). The
Katsura systems come from S. Katsura, *Spin glass problem by the method of
integral equation of the effective field*, in *New Trends in Magnetism*
(1990); both families are the standard Gröbner basis benchmarks of
J.-C. Faugère, *A new efficient algorithm for computing Gröbner bases
(F4)*, JPAA 139 (1999).

Examples
========

>>> from sympy_extras_benchmarks.datasets.polynomial_systems import katsura, cyclic
>>> eqs, us = katsura(2)
>>> eqs
[u0 + 2*u1 + 2*u2 - 1, u0**2 - u0 + 2*u1**2 + 2*u2**2, 2*u0*u1 + 2*u1*u2 - u1]
>>> cyclic(3)[0]
[x0 + x1 + x2, x0*x1 + x0*x2 + x1*x2, x0*x1*x2 - 1]
"""
from __future__ import annotations

from math import factorial
from typing import Optional

from sympy import S, symbols
from sympy.core.expr import Expr
from sympy.core.symbol import Symbol

from sympy_extras._typing import as_expr

__all__ = ['PolynomialSystem', 'katsura', 'cyclic', 'SYSTEMS']


class PolynomialSystem:
    """A named system with its known invariants.

    Attributes
    ==========

    name : str
    equations : list[Expr]
    variables : tuple[Symbol, ...]
    dimension : int
        The dimension of the variety (0 for finitely many solutions).
    solutions : Optional[int]
        The number of solutions counted with multiplicity, when
        finite and known.
    radical : Optional[bool]
        Whether the ideal is radical, when known.
    """

    def __init__(self, name: str, equations: list[Expr], variables: tuple[Symbol, ...],
                 dimension: int, solutions: Optional[int], radical: Optional[bool]) -> None:
        self.name = name
        self.equations = equations
        self.variables = variables
        self.dimension = dimension
        self.solutions = solutions
        self.radical = radical

    def __repr__(self) -> str:
        return "PolynomialSystem(%s, %d equations)" % (self.name, len(self.equations))


def katsura(m: int) -> tuple[list[Expr], tuple[Symbol, ...]]:
    """The Katsura-m system in ``u_0, ..., u_m``: the linear equation
    ``u_0 + 2 (u_1 + ... + u_m) = 1`` and, for ``r = 0, ..., m-1``,
    ``sum_{i=-m}^{m} u_i u_{r-i} = u_r`` with ``u_{-i} = u_i`` and ``u_i = 0``
    beyond ``m``.

    Examples
    ========

    >>> from sympy_extras_benchmarks.datasets.polynomial_systems import katsura
    >>> eqs, us = katsura(3)
    >>> len(eqs), us
    (4, (u0, u1, u2, u3))
    """
    us = symbols('u0:%d' % (m + 1))

    def U(i: int) -> Expr:
        i = abs(i)
        return as_expr(us[i]) if i <= m else as_expr(S.Zero)

    eqs: list[Expr] = [as_expr(us[0] + 2*sum(us[1:]) - 1)]
    for r in range(m):
        total: Expr = as_expr(S.Zero)
        for i in range(-m, m + 1):
            total = as_expr(total + U(i)*U(r - i))
        eqs.append(as_expr(total - us[r]))
    return eqs, tuple(us)


def cyclic(m: int) -> tuple[list[Expr], tuple[Symbol, ...]]:
    """The cyclic-m system in ``x_0, ..., x_{m-1}``: the elementary cyclic
    sums of length ``1, ..., m-1`` and the product minus one.

    Examples
    ========

    >>> from sympy_extras_benchmarks.datasets.polynomial_systems import cyclic
    >>> cyclic(4)[0]
    [x0 + x1 + x2 + x3, x0*x1 + x0*x3 + x1*x2 + x2*x3, x0*x1*x2 + x0*x1*x3 + x0*x2*x3 + x1*x2*x3, x0*x1*x2*x3 - 1]
    """
    xs = symbols('x0:%d' % m)
    eqs: list[Expr] = []
    for length in range(1, m):
        total: Expr = as_expr(S.Zero)
        for start in range(m):
            term: Expr = as_expr(S.One)
            for k in range(length):
                term = as_expr(term*xs[(start + k) % m])
            total = as_expr(total + term)
        eqs.append(total)
    product: Expr = as_expr(S.One)
    for v in xs:
        product = as_expr(product*v)
    eqs.append(as_expr(product - 1))
    return eqs, tuple(xs)


#: the number of solutions of cyclic-m when it is finite and known
CYCLIC_SOLUTIONS: dict[int, int] = {3: 6, 5: 70, 6: 156, 7: 924}


def _cyclic_count(m: int) -> Optional[int]:
    if m in CYCLIC_SOLUTIONS:
        return CYCLIC_SOLUTIONS[m]
    if all(m % p for p in range(2, m) if p*p <= m):  # prime: Haagerup's count
        return factorial(2*m - 2)//factorial(m - 1)**2
    return None


def _katsura_system(m: int) -> PolynomialSystem:
    eqs, us = katsura(m)
    return PolynomialSystem('katsura-%d' % m, eqs, us, 0, 2**m, True)


def _cyclic_system(m: int) -> PolynomialSystem:
    eqs, xs = cyclic(m)
    if m in (4, 8, 9):
        return PolynomialSystem('cyclic-%d' % m, eqs, xs, 1, None, None)
    count = _cyclic_count(m)
    return PolynomialSystem('cyclic-%d' % m, eqs, xs, 0, count, True if count is not None else None)


#: the systems with their invariants, smallest first
SYSTEMS: list[PolynomialSystem] = (
    [_katsura_system(m) for m in range(2, 7)] + [_cyclic_system(m) for m in range(3, 8)])
