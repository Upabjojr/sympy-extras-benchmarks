"""The expressions of holpy, read through Maxima's syntax."""
from __future__ import annotations

from sympy import Catalan, Symbol, exp, pi, sqrt, oo

from sympy_extras_benchmarks.parsers.holpy import condition, integral, sides, to_maxima, value


def test_names_become_maximas() -> None:
    assert to_maxima('Gamma(1/4) ^ 2 / (2 * sqrt(pi)) + B(m, n) - oo') == \
        'gamma(1/4) ^ 2 / (2 * sqrt(%pi)) + beta(m, n) - inf'


def test_a_name_that_merely_contains_pi_or_oo_is_left_alone() -> None:
    assert to_maxima('pioneer') == 'pioneer'
    assert to_maxima('book') == 'book'


def test_values_and_catalans_constant() -> None:
    assert value('pi/2') == pi/2
    assert value('oo') == oo
    assert value('sqrt(pi)') == sqrt(pi)
    assert value('G') == Catalan            # ``G`` is holpy's name for Catalan's constant
    assert value('INT x:[0,1]. x') is None  # an integral is not a closed form


def test_an_integral_and_its_parts() -> None:
    t = Symbol('t')
    read = integral('INT t:[0, pi/4]. exp(-t)')
    assert read is not None
    integrand, variable, low, high = read
    assert integrand == exp(-t) and variable == t
    assert low == 0 and high == pi/4
    assert integral('(INT t:[0,1]. t)') is not None      # also when bracketed
    assert integral('SUM n. 1/n') is None


def test_the_two_sides_of_a_goal() -> None:
    assert sides('(INT x:[0,1]. x) = 1/2') == ('(INT x:[0,1]. x) ', ' 1/2')
    assert sides('a >= b') is None
    assert sides('a != b') is None


def test_conditions_become_relations() -> None:
    k = Symbol('k')
    assert condition('k > 0') == (k > 0)
    assert condition('k != 0') is not None
    assert condition('k is odd') is None
