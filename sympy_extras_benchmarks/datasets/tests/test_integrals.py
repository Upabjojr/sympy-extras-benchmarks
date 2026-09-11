"""Tests of the record and the helpers shared by the integration datasets."""
from __future__ import annotations

from sympy import Eq, Function, Ne, Symbol, exp, oo

from sympy_extras_benchmarks.datasets.integrals import (
    DefiniteIntegral, readable, relation, split_arguments)

x, a, b = Symbol('x'), Symbol('a'), Symbol('b')


def test_relations_of_every_kind() -> None:
    assert relation('a >= 2') == (a >= 2)
    assert relation('b - a < 1') == (b - a < 1)
    assert relation('a # b') == Ne(a, b)
    assert relation('equal(a, b)') == Eq(a, b)
    assert relation('notequal(a, 0)') == Ne(a, 0)


def test_not_a_relation() -> None:
    assert relation('a + b') is None
    # the comparison is inside a call, not at the top level
    assert relation('g(a > 0)') is None


def test_split_arguments_respects_brackets_and_strings() -> None:
    assert split_arguments('g(u, v), [1, 2], "p, q"') == ['g(u, v)', '[1, 2]', '"p, q"']


def test_readable_refuses_what_did_not_translate() -> None:
    assert readable(exp(x))
    assert not readable(Function('mystery')(x))


def test_parameters_and_key() -> None:
    entry = DefiniteIntegral('t:1', b*exp(-a*x), x, 0, oo)
    assert entry.parameters == [a, b]
    assert entry.key() == (b*exp(-a*x), x, 0, oo)
    assert entry.lower.is_zero
