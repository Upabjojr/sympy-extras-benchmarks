"""Tests of the reader of Maxima's integration and transform tests, on
samples written here in Maxima syntax (nothing is copied from Maxima)."""
from __future__ import annotations

from sympy import Rational, Symbol, cos, exp, oo, pi, sqrt

from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.datasets.maxima_integrals import integrals

u, k, p, w, n = (Symbol(s) for s in ('u', 'k', 'p', 'w', 'n'))


def _one(text: str, values_follow: bool = True) -> DefiniteIntegral:
    found = integrals(text, 'sample', values_follow)
    assert len(found) == 1
    return found[0]


def test_a_definite_integral_and_its_value() -> None:
    entry = _one("integrate(cos(u), u, 0, %pi/2);\n1$\n")
    assert entry.name == 'sample:1'
    assert (entry.integrand, entry.variable, entry.lower, entry.upper) == (cos(u), u, 0, pi/2)
    assert entry.recorded == 1


def test_an_indefinite_integral_is_not_read() -> None:
    assert integrals("integrate(cos(u), u);\nsin(u)$\n", 'sample') == []


def test_the_context_is_followed() -> None:
    text = ("assume(k > 0)$\n[k > 0]$\n"
            "integrate(exp(-k*u), u, 0, inf);\n1/k$\n"
            "forget(k > 0)$\n[k > 0]$\n"
            "integrate(exp(-k*u), u, 0, 1);\n(1-exp(-k))/k$\n")
    first, second = integrals(text, 'sample')
    assert first.facts == (k > 0,)
    assert first.upper == oo
    assert second.facts == ()


def test_kill_all_clears_the_context() -> None:
    text = ("(assume(k > 0), declare(n, integer), 0);\n0$\n(kill(all), 0);\n0$\n"
            "integrate(u^n*exp(-k*u), u, 0, 1);\nfoo$\n")
    entry = _one(text)
    assert entry.facts == () and entry.properties == ()


def test_a_fact_about_another_name_is_not_kept() -> None:
    entry = _one("assume(p > 0, k > p)$\n[p > 0, k > p]$\nintegrate(exp(-k*u), u, 0, inf);\n1/k$\n")
    assert entry.facts == ()


def test_declared_properties_are_read() -> None:
    entry = _one("declare(n, integer)$\ndone$\nintegrate(cos(n*u)^2, u, 0, %pi);\n%pi/2$\n")
    assert entry.properties == ((n, 'integer'),)


def test_a_declaration_this_module_does_not_read_refuses() -> None:
    text = "declare(n, scalar)$\ndone$\nintegrate(u^n, u, 0, 1);\n1/(n+1)$\n"
    assert integrals(text, 'sample') == []


def test_assume_pos_makes_every_parameter_positive() -> None:
    entry = _one("assume_pos: true$\ntrue$\nintegrate(p*exp(-k*u), u, 0, inf);\np/k$\n")
    assert set(entry.facts) == {k > 0, p > 0}


def test_a_variable_with_a_value_is_replaced() -> None:
    entry = _one("q: k^2 + 1$\nk^2 + 1$\nintegrate(1/q, u, 0, 1);\n1/(k^2 + 1)$\n")
    assert entry.integrand == 1/(k**2 + 1)


def test_a_call_inside_a_binding_construct_is_refused() -> None:
    text = "makelist(integrate(u^j, u, 0, 1), j, 1, 3);\n[1/2, 1/3, 1/4]$\n"
    assert integrals(text, 'sample') == []


def test_a_principal_value_is_refused() -> None:
    assert integrals("integrate(1/u, u, -1, 1), intanalysis = false;\n0$\n", 'sample') == []
    text = "intanalysis: false$\nfalse$\nintegrate(1/u^3, u, -1, 1);\n0$\n"
    assert integrals(text, 'sample') == []


def test_the_value_of_something_else_is_not_recorded() -> None:
    assert _one("round(100*integrate(u, u, 0, 1));\n50$\n").recorded is None
    assert _one("errcatch(integrate(1/u^2, u, -1, 1));\n[]$\n").recorded is None


def test_a_simplified_call_keeps_its_value() -> None:
    assert _one("ratsimp(integrate(u^2, u, 0, 3));\n9$\n").recorded == 9
    assert _one("integrate(u^2, u, 0, 3), ratsimp;\n9$\n").recorded == 9


def test_a_noun_form_records_no_value() -> None:
    assert _one("'integrate(u^2, u, 0, 3);\n'integrate(u^2, u, 0, 3)$\n").recorded is None


def test_a_definition_is_not_run() -> None:
    assert integrals("g(z) := integrate(z*u, u, 0, 1);\ng(z) := 0$\n", 'sample') == []


def test_transforms_are_integrals_over_the_positive_axis() -> None:
    entry = _one("laplace(cos(w), w, p);\np/(p^2 + 1)$\n")
    assert entry.integrand == exp(-p*w)*cos(w)
    assert (entry.lower, entry.upper) == (0, oo)
    assert entry.recorded == p/(p**2 + 1)
    entry = _one("(assume(p > 0), specint(exp(-p*w)*sqrt(w), w));\nsqrt(%pi)/(2*p^(3/2))$\n")
    assert entry.integrand == exp(-p*w)*sqrt(w)
    assert entry.facts == (p > 0,)
    assert entry.recorded == sqrt(pi)/(2*p**Rational(3, 2))


def test_a_demonstration_file_has_no_values() -> None:
    first, second = integrals("integrate(u, u, 0, 2);\nintegrate(u, u, 0, 3);\n",
                              'sample', values_follow=False)
    assert (first.upper, second.upper) == (2, 3)
    assert first.recorded is None and second.recorded is None
