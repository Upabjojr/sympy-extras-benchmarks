"""Tests of the indefinite-integration driver's checks, offline."""
from __future__ import annotations

import random

from sympy import I, S, Symbol, besselk, cos, exp, log, meijerg, sin, sqrt
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.datasets.indefinite_integrals import IndefiniteIntegral
from sympy_extras_benchmarks.drivers.indefinite_integrals import check, verify

x, a = Symbol('x'), Symbol('a')


def _verify(integrand: object, result: object, parameters: tuple[Symbol, ...] = (),
            facts: tuple[Boolean, ...] = ()) -> str:
    verdict, _ = verify(as_expr(integrand), x, as_expr(result), list(parameters), list(facts),
                        random.Random(0), 10.0)
    return verdict


def test_the_derivative_is_checked_symbolically_and_numerically() -> None:
    assert _verify(cos(x), sin(x)) == 'correct'
    assert _verify(cos(x), sin(x) + 5) == 'correct'                 # a constant does not matter
    assert _verify(cos(x), cos(x)) == 'WRONG'
    # only numerically: the derivative is the integrand where both are real
    assert _verify(1/sqrt(1 - x**2), -I*log(I*x + sqrt(1 - x**2))) == 'correct'


def test_a_varying_imaginary_part_is_nonreal_and_a_constant_one_is_not() -> None:
    # I*log(x) has derivative I/x, wrong; log(x) + I*pi is a constant away
    # from log(x); I*log(-I*x + sqrt(1 - x**2)) is asin(x), real
    assert _verify(1/x, log(x) + I*3) == 'correct'
    assert _verify(2*x, x**2 + I*x) == 'WRONG'


def test_a_point_where_the_integrand_is_complex_is_no_test() -> None:
    # besselk(7, x) at x < 0 is a complex number with a tiny imaginary
    # part (-pi*besseli(7, x), 1e-28 of the real part), so an
    # antiderivative right for x > 0 (SymPy's G-function form) is not
    # wrong there: a relative tolerance on the imaginary part took the
    # point as real and reported it wrong
    G = -x*meijerg(((), (S(1)/2,)), ((-S(7)/2, -S(1)/2, S(7)/2), ()), x**2/4)/4
    assert _verify(besselk(7, x), G) == 'correct'
    assert _verify(besselk(7, x), -G) == 'WRONG'


def test_parameters_take_the_facts() -> None:
    assert _verify(exp(-a*x), -exp(-a*x)/a, (a,), (as_boolean(a > 0),)) == 'correct'
    assert _verify(exp(-a*x), exp(-a*x)/a, (a,), (as_boolean(a > 0),)) == 'WRONG'


def test_check_classifies() -> None:
    entry = IndefiniteIntegral('sample:1', cos(x), x, recorded=sin(x))
    result = check(entry, random.Random(0), 10.0)
    assert result['verdict'] == 'correct' and result['reference'] == 'sin(x)'
    unevaluated = check(IndefiniteIntegral('sample:2', exp(exp(exp(x))), x), random.Random(0), 10.0)
    assert unevaluated['verdict'] in ('unevaluated', 'no answer')
    crash = check(IndefiniteIntegral('sample:3', cos(x), x), random.Random(0), 10.0,
                  lambda f, v, facts: (_ for _ in ()).throw(ValueError('boom')))
    assert crash['verdict'] == 'crash' and 'boom' in str(crash['error'])
