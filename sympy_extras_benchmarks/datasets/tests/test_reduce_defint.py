"""Tests of the reader of REDUCE's DEFINT tests, on samples written here in
REDUCE syntax (nothing is copied from REDUCE)."""
from __future__ import annotations

from sympy import Ei, Si, Symbol, besselj, exp, oo, pi, sin

from sympy_extras_benchmarks.datasets.reduce_defint import integrals

t = Symbol('t')


def test_names_ignore_case() -> None:
    entry, = integrals("int(BESSELJ(0,t)*E^(-t),t,0,INFINITY);\n", 'sample')
    assert entry.integrand == besselj(0, t)*exp(-t)
    assert (entry.lower, entry.upper) == (0, oo)


def test_a_bracketless_call_and_implicit_multiplication() -> None:
    entry, = integrals("int(sin t*e^(-1/2t),t,0,pi);\n", 'sample')
    assert entry.integrand == sin(t)*exp(-t/2)
    assert entry.upper == pi


def test_the_integral_functions() -> None:
    first, second = integrals("int(si(t)*e^(-t),t,0,infinity);\nint(ei(-t),t,0,infinity);\n",
                              'sample')
    assert first.integrand == Si(t)*exp(-t)
    assert second.integrand == Ei(-t)


def test_the_fresnel_integrals_are_refused() -> None:
    assert integrals("int(fresnel_s(t),t,0,1);\n", 'sample') == []


def test_indefinite_integrals_and_transforms_are_not_read() -> None:
    assert integrals("int(t^2,t);\nlaplace_transform(t,t);\n", 'sample') == []


def test_a_commented_call_is_skipped() -> None:
    entry, = integrals("% int(t,t,0,1);\nint(t^3,t,0,1);\n", 'sample')
    assert entry.name == 'sample:1'
    assert entry.integrand == t**3
