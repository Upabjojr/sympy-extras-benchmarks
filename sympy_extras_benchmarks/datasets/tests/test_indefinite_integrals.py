"""Tests of the readers of indefinite integrals, on samples written here in
Maxima's and FriCAS's syntax (nothing is copied from either)."""
from __future__ import annotations

from sympy import I, Symbol, cos, exp, log, sin, sqrt

from sympy_extras_benchmarks.datasets.indefinite_integrals import (
    IndefiniteIntegral, fricas_indefinite, maxima_indefinite)

u, k, a, b, x = (Symbol(s) for s in ('u', 'k', 'a', 'b', 'x'))


def _one(text: str, values_follow: bool = True) -> IndefiniteIntegral:
    found = maxima_indefinite(text, 'sample', values_follow)
    assert len(found) == 1
    return found[0]


def test_a_call_and_its_recorded_antiderivative() -> None:
    entry = _one("integrate(cos(u), u);\nsin(u)$\n")
    assert entry.name == 'sample:1'
    assert (entry.integrand, entry.variable, entry.recorded) == (cos(u), u, sin(u))
    assert entry.integral().free_symbols == {u}
    assert entry.parameters == []


def test_definite_calls_are_left_to_the_other_reader() -> None:
    assert maxima_indefinite("integrate(cos(u), u, 0, 1);\nsin(1)$\n", 'sample') == []


def test_the_context_is_followed() -> None:
    text = ("assume(k > 0)$\n[k > 0]$\n"
            "integrate(exp(-k*u), u);\n-exp(-k*u)/k$\n"
            "forget(k > 0)$\n[k > 0]$\n"
            "integrate(exp(-k*u), u);\n-exp(-k*u)/k$\n")
    first, second = maxima_indefinite(text, 'sample')
    assert first.facts == (k > 0,) and second.facts == ()
    assert first.parameters == [k]


def test_an_untranslated_assumption_is_released_by_its_forget() -> None:
    # the assumption mentions a and b; the calls about them are refused
    # until the forget, those about other parameters never
    text = ("assume(notequal(ratsimp(a/b), -1))$\n[notequal(a/b, -1)]$\n"
            "integrate(a*u, u);\na*u^2/2$\n"
            "integrate(k*u, u);\nk*u^2/2$\n"
            "forget(notequal(a/b, -1))$\n[notequal(a/b, -1)]$\n"
            "integrate(a*u, u);\na*u^2/2$\n")
    found = maxima_indefinite(text, 'sample')
    assert [e.integrand for e in found] == [k*u, a*u]


def test_maxima_giving_up_is_no_reference() -> None:
    entry = _one("integrate(exp(exp(u)), u);\nintegrate(%e^%e^u, u)$\n")
    assert entry.recorded is None


def test_a_recorded_value_is_read_through_a_preserving_simplification_only() -> None:
    assert _one("ratsimp(integrate(2*u, u));\nu^2$\n").recorded == u**2
    assert _one("diff(integrate(2*u, u), u);\n2*u$\n").recorded is None


def test_a_demonstration_file_has_no_values() -> None:
    found = maxima_indefinite("integrate(sqrt(x), x);\nintegrate(2^x, x);\n", 'sample', values_follow=False)
    assert [e.integrand for e in found] == [sqrt(x), 2**x]
    assert all(e.recorded is None for e in found)


def test_fricas_assertions_and_references() -> None:
    text = ('testIntegrate("(x+1)*exp(x)", "x", "rde")\n'
            'xf1testIntegrate("1/(-3+v^3)*v/(-4+v^3)^(1/2)", "v", "#360")\n'
            'testIntegrate("log(1-z^3)*(I*z)^(1/2)", "z", "#440")\n'
            'testIntegrate("(x+1)*" _\n'
            '              "exp(x)", "x", "again")\n'
            'testEquals("integrate(cos(x)/(1 + cos(x)), x)", "-sin(x)/(1 + cos(x)) + x")\n'
            'testEquals("integrate(cos(x)/sqrt(x), x = 0..%plusInfinity)", "sqrt(%pi/2)")\n')
    found = fricas_indefinite(text, 'sample')
    z = Symbol('z')
    assert [e.integrand for e in found] == [(x + 1)*exp(x), log(1 - z**3)*sqrt(I*z), cos(x)/(1 + cos(x))]
    assert found[2].recorded == x - sin(x)/(cos(x) + 1)
    assert found[0].name == 'sample:1' and found[2].name == 'sample:4'
    assert all(e.facts == () for e in found)
