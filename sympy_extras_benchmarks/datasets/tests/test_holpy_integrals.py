"""Tests of the reader of holpy's examples, on entries written here in
holpy's format (nothing is copied from holpy)."""
from __future__ import annotations

from sympy import Catalan, Ne, Symbol, beta, exp, oo, pi, sec

from sympy_extras_benchmarks.datasets.holpy_integrals import JSONValue, integrals

t, k, m, n = (Symbol(s) for s in ('t', 'k', 'm', 'n'))


def test_a_problem_and_the_last_line_of_its_computation() -> None:
    problem: JSONValue = {"problem": "INT t:[0, pi/4]. sec(t)^2",
                          "calc": [{"text": "INT t:[0,pi / 4]. sec(t) ^ 2"}, {"text": "1"}]}
    entry, = integrals([problem], 'sample')
    assert entry.name == 'sample:1'
    assert (entry.integrand, entry.lower, entry.upper) == (sec(t)**2, 0, pi/4)
    assert entry.recorded == 1


def test_an_unfinished_computation_records_nothing() -> None:
    problem: JSONValue = {"problem": "INT t:[0, 1]. t",
                          "calc": [{"text": "INT t:[0,1]. t"}]}
    entry, = integrals([problem], 'sample')
    assert entry.recorded is None


def test_a_goal_with_the_integral_on_either_side() -> None:
    goal: JSONValue = {"goal": "1 / k = (INT t:[0,oo]. exp(-k * t))", "conds": ["k > 0"]}
    entry, = integrals([goal], 'sample')
    assert (entry.integrand, entry.upper) == (exp(-k*t), oo)
    assert entry.recorded == 1/k
    assert entry.facts == (k > 0,)


def test_a_goal_about_a_series_is_read_without_a_value() -> None:
    goal: JSONValue = {"goal": "(INT t:[0,1]. t ^ t) = SUM(j, 1, oo, j ^ -j)"}
    entry, = integrals([goal], 'sample')
    assert entry.integrand == t**t
    assert entry.recorded is None


def test_a_goal_about_an_intermediate_function_is_not_read() -> None:
    assert integrals([{"goal": "I(1) = 2 * (INT t:[0,1]. t)"}], 'sample') == []
    assert integrals([{"goal": "(INT k:[1,oo]. D k. I(k)) = pi"}], 'sample') == []


def test_conditions_and_names() -> None:
    goal: JSONValue = {"goal": "(INT t:[0,1]. t ^ (m - 1) * (1 - t) ^ (n - 1)) = B(m,n)",
                       "conds": [{"cond": "m > 0"}, {"cond": "n != 0"}]}
    entry, = integrals([goal], 'sample')
    assert entry.recorded == beta(m, n)
    assert entry.facts == (m > 0, Ne(n, 0))


def test_catalans_constant() -> None:
    entry, = integrals([{"goal": "(INT t:[0,1]. atan(t) / t) = G"}], 'sample')
    assert entry.recorded == Catalan


def test_a_condition_that_does_not_translate_refuses_the_entry() -> None:
    goal: JSONValue = {"goal": "(INT t:[0,1]. t ^ m) = 1 / (m + 1)", "conds": ["m is real"]}
    assert integrals([goal], 'sample') == []


def test_a_condition_on_the_variable_is_dropped() -> None:
    goal: JSONValue = {"goal": "(INT t:[0,1]. t) = 1/2", "conds": ["t > 0"]}
    entry, = integrals([goal], 'sample')
    assert entry.facts == ()
