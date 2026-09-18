"""Tests of the record shared by the integration datasets."""
from __future__ import annotations

from sympy import Symbol, exp, oo

from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral

x, a, b = Symbol('x'), Symbol('a'), Symbol('b')


def test_parameters_and_key() -> None:
    entry = DefiniteIntegral('t:1', b*exp(-a*x), x, 0, oo)
    assert entry.parameters == [a, b]
    assert entry.key() == (b*exp(-a*x), x, 0, oo)
    assert entry.lower.is_zero
