"""Tests of the quadrature oracle and of the checks of the
``definite_integrals`` driver, on integrals whose values are known."""
from __future__ import annotations

import random

from sympy import I, Integer, Integral, Symbol, exp, oo, pi, sqrt
from sympy.core.expr import Expr

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.drivers.definite_integrals import assumed_symbols, check
from sympy_extras_benchmarks.oracles.quadrature import agree, numerical, quadrature, sample

x, z, a, s, n = (Symbol(name) for name in ('x', 'z', 'a', 's', 'n'))


def test_the_quadrature_of_a_convergent_integral() -> None:
    entry = DefiniteIntegral('t:1', exp(-a*x), x, 0, oo, facts=[a > 0])
    assert agree(quadrature(entry, {a: Integer(2)}), 0.5)


def test_the_quadrature_along_a_complex_segment() -> None:
    entry = DefiniteIntegral('t:2', 1/z, z, 1, I)
    assert agree(quadrature(entry, {}), complex(0, float(pi)/2))


def test_a_divergent_integral_is_not_trusted() -> None:
    assert quadrature(DefiniteIntegral('t:3', 1/x, x, 0, 1), {}) is None


def test_samples_satisfy_the_facts_and_properties() -> None:
    entry = DefiniteIntegral('t:4', x**n*exp(-s*x)*a, x, 0, oo, facts=[s - 2*a > 0],
                             properties=[(n, 'integer')])
    rng = random.Random(3)
    for _ in range(20):
        values = sample(entry, rng)
        assert values is not None
        assert values[s] - 2*values[a] > 0
        assert values[n].is_integer


def test_unsatisfiable_facts_give_no_sample() -> None:
    entry = DefiniteIntegral('t:5', exp(-a*x), x, 0, oo, facts=[a > 0, a < 0])
    assert sample(entry, random.Random(0), attempts=50) is None


def test_numerical_values() -> None:
    assert agree(numerical(sqrt(a), {a: Integer(2)}), 2**0.5)
    assert numerical(Integral(exp(x**3), (x, 0, a)), {a: Integer(1)}) is None
    assert numerical(oo + a, {a: Integer(1)}) is None


def test_sign_facts_become_assumptions() -> None:
    entry = DefiniteIntegral('t:6', x**n*exp(-a*x), x, 0, oo, facts=[a > 0],
                             properties=[(n, 'integer')])
    replacement = assumed_symbols(entry)
    assert replacement[a].is_positive
    assert replacement[n].is_integer


def test_a_right_result_and_a_right_recorded_value() -> None:
    entry = DefiniteIntegral('t:7', exp(-a*x), x, 0, oo, facts=[a > 0], recorded=1/a)
    result = check(entry, random.Random(1), 30.0)
    assert result['verdict'] == 'ok'
    assert result['source'] == 'agrees'


def test_a_wrong_result_is_caught() -> None:
    entry = DefiniteIntegral('t:8', exp(-a*x), x, 0, oo, facts=[a > 0])

    def wrong(integrand: Expr, limits: tuple[Symbol, Expr, Expr]) -> Expr:
        # twice the value, in the positive symbol the driver integrates with
        parameter, = integrand.free_symbols - {limits[0]}
        return 2/as_expr(parameter)

    assert check(entry, random.Random(1), 30.0, wrong)['verdict'] == 'WRONG'


def test_a_wrong_recorded_value_is_a_finding_about_the_source() -> None:
    entry = DefiniteIntegral('t:9', exp(-a*x), x, 0, oo, facts=[a > 0], recorded=2/a)
    result = check(entry, random.Random(1), 30.0)
    assert result['verdict'] == 'ok'
    assert result['source'] == 'SOURCE'


def test_an_unevaluated_result_and_no_answer() -> None:
    entry = DefiniteIntegral('t:10', exp(-x**4), x, 0, 1)

    def unevaluated(integrand: Expr, limits: tuple[Symbol, Expr, Expr]) -> Expr:
        return Integral(integrand, limits)

    def gives_up(integrand: Expr, limits: tuple[Symbol, Expr, Expr]) -> Expr:
        raise NotImplementedError

    assert check(entry, random.Random(1), 30.0, unevaluated)['verdict'] == 'unevaluated'
    assert check(entry, random.Random(1), 30.0, gives_up)['verdict'] == 'no answer'
