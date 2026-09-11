"""Numerical quadrature as an independent oracle for definite integrals.

Once its parameters are numbers, a definite integral is a number, so a
closed form can be checked by computing the integral numerically at sample
values of the parameters. The quadrature is done twice, with mpmath's
tanh-sinh and Gauss-Legendre rules at 30 digits, and trusted only when the
two agree: an oscillatory integrand over an infinite range, a divergent
integral, or a singularity inside the range makes them disagree, and the
integral is then left unchecked rather than judged. A pair of rules agreeing
on a wrong value is possible but needs both to fail the same way, which is
why a driver checks more than one sample.

An integral between complex endpoints is computed along the straight
segment joining them.

* :func:`sample` draws values of the parameters satisfying the facts and
  properties of an entry;
* :func:`quadrature` computes the integral at those values;
* :func:`numerical` evaluates a closed form there;
* :func:`agree` compares two numbers with a relative tolerance.

Examples
========

>>> from sympy import Symbol, exp, oo
>>> from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
>>> from sympy_extras_benchmarks.oracles.quadrature import agree, quadrature
>>> x, a = Symbol('x'), Symbol('a')
>>> entry = DefiniteIntegral('demo:1', exp(-a*x), x, 0, oo, facts=[a > 0])
>>> agree(quadrature(entry, {a: 2}), 0.5)
True
"""
from __future__ import annotations

import random
import re
from typing import Callable, Optional

import mpmath

from sympy import Integer, Integral, Rational, S, Symbol, lambdify, oo, zoo
from sympy.core.evalf import PrecisionExhausted
from sympy.core.expr import Expr

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral

__all__ = ['DIGITS', 'TOLERANCE', 'sample', 'quadrature', 'numerical', 'agree']

#: the working precision of the quadrature and of the evaluations
DIGITS = 30
#: the relative disagreement tolerated between two values of one integral
TOLERANCE = 1e-8
#: the relative disagreement tolerated between the two quadrature rules
_RULES_AGREE = 1e-10
#: the most digits ``evalf`` may work with to reach :data:`DIGITS`
_MAXN = 1000

#: what goes wrong numerically: a function mpmath does not have, a
#: domain error, an overflow
_NUMERICAL_ERRORS = (ValueError, TypeError, ZeroDivisionError, OverflowError, NameError,
                     AttributeError, NotImplementedError, KeyError)


def sample(entry: DefiniteIntegral, rng: random.Random, attempts: int = 200
           ) -> Optional[dict[Symbol, Expr]]:
    """Rational values of the parameters of ``entry`` satisfying its facts
    and properties, or ``None`` when none is found in ``attempts`` draws.

    A parameter no fact mentions is drawn positive, since that is where the
    integrals of these collections converge; one a fact mentions is drawn
    with either sign.
    """
    declared: dict[Symbol, set[str]] = {}
    for symbol, prop in entry.properties:
        declared.setdefault(symbol, set()).add(prop)
    constrained = {s for fact in entry.facts for s in fact.free_symbols}
    for _ in range(attempts):
        values: dict[Symbol, Expr] = {}
        for parameter in entry.parameters:
            props = declared.get(parameter, set())
            sign = -1 if parameter in constrained and rng.random() < 0.3 else 1
            if props & {'integer', 'even', 'odd'}:
                n = rng.randint(1, 4)
                n = 2*n if 'even' in props else 2*n - 1 if 'odd' in props else n
                values[parameter] = Integer(sign*n)
            else:
                value = Rational(rng.randint(3, 30), rng.randint(2, 7))
                if 'noninteger' in props and value.is_integer:
                    value += Rational(1, 3)
                values[parameter] = as_expr(sign*value)
        if all(fact.xreplace(values) is S.true for fact in entry.facts):
            return values
    return None


def _number(value: Expr) -> Optional[object]:
    """``value`` as an mpmath number, infinities included."""
    if value == oo:
        return mpmath.inf
    if value == -oo:
        return -mpmath.inf
    if value.free_symbols or value.has(zoo):
        return None
    try:
        return mpmath.mpmathify(complex(value.evalf(DIGITS)))
    except _NUMERICAL_ERRORS:
        return None


def quadrature(entry: DefiniteIntegral, values: dict[Symbol, Expr]) -> Optional[complex]:
    """The integral of ``entry`` at ``values`` of its parameters, or
    ``None`` when the two quadrature rules do not agree on it."""
    integrand = entry.integrand.xreplace(values)
    if integrand.free_symbols - {entry.variable}:
        return None
    lower = _number(as_expr(entry.lower.xreplace(values)))
    upper = _number(as_expr(entry.upper.xreplace(values)))
    if lower is None or upper is None:
        return None
    try:
        f: Callable[[object], object] = lambdify(entry.variable, integrand, modules='mpmath')
        with mpmath.workdps(DIGITS):
            first = mpmath.quad(f, [lower, upper], method='tanh-sinh')
            second = mpmath.quad(f, [lower, upper], method='gauss-legendre')
            if not (mpmath.isfinite(first) and mpmath.isfinite(second)):
                return None
            if abs(first - second) > _RULES_AGREE*max(1, abs(first)):
                return None
            return complex(first)
    except _NUMERICAL_ERRORS:
        return None


def _evaluated(value: Expr) -> Optional[complex]:
    """``value`` to :data:`DIGITS` digits, or ``None`` when that accuracy is
    out of reach.

    A closed form can cancel catastrophically — ``exp(400)*(1 - erf(20))``
    loses about 175 digits — and a plain ``evalf`` then returns a zero
    whose error is larger than the value, printed ``0.e+31``. ``evalf`` is
    asked for guaranteed digits first, with room to work at many more; when
    it cannot guarantee them, the value either cancels to zero or is lost,
    and only a zero known to be tiny is accepted.
    """
    try:
        return complex(value.evalf(DIGITS, strict=True, maxn=_MAXN))
    except PrecisionExhausted:
        pass
    loose = value.evalf(DIGITS, maxn=_MAXN)
    for part in loose.as_real_imag():
        zero = re.fullmatch(r"-?0\.e([+-]\d+)", str(part))
        if zero is not None and int(zero.group(1)) > -10:
            return None
    return complex(loose)


def numerical(value: Expr, values: dict[Symbol, Expr]) -> Optional[complex]:
    """``value`` at ``values``, or ``None`` when it is not a finite number
    there (an unevaluated integral, a symbol left, an infinity) or cannot be
    evaluated accurately."""
    substituted = value.xreplace(values)
    if not isinstance(substituted, Expr) or substituted.has(Integral) or substituted.free_symbols:
        return None
    try:
        number = _evaluated(substituted)
    except _NUMERICAL_ERRORS:
        return None
    if number is None:
        return None
    if number != number or abs(number) == float('inf'):
        return None
    return number


def agree(first: Optional[complex], second: Optional[complex],
          tolerance: float = TOLERANCE) -> bool:
    """Whether two numbers agree to ``tolerance``, relative to the larger
    (or absolute, near zero)."""
    if first is None or second is None:
        return False
    return abs(first - second) <= tolerance*max(1.0, abs(first), abs(second))
