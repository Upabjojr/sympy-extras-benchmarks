"""The rewriting of REDUCE's syntax into Maxima's."""
from __future__ import annotations

from sympy_extras_benchmarks.parsers.reduce import strip_comments, to_maxima, to_maxima_names


def test_to_maxima_leaves_ordinary_products_alone() -> None:
    assert to_maxima('a*x + b*y') == 'a*x + b*y'


def test_to_maxima_rewrites_the_power_operator() -> None:
    assert to_maxima('x**2 + y**3') == 'x^2 + y^3'


def test_scientific_notation_is_not_a_multiplication() -> None:
    # ``1.5e-3`` is one number: splitting it would give ``1.5*e-3``, i.e. 3e/2 - 3
    assert to_maxima('1.5e-3') == '1.5e-3'
    assert to_maxima('2e3') == '2e3'
    assert to_maxima('1.5E+2') == '1.5E+2'
    assert to_maxima('2e3*x') == '2e3*x'


def test_implicit_multiplication_still_works() -> None:
    assert to_maxima('2x') == '2*x'
    assert to_maxima('4df(y,x)') == "4*'diff(y,x)"
    assert to_maxima('2(x+1)') == '2*(x+1)'
    assert to_maxima('3e') == '3*e'            # ``e`` with no exponent is a name


def test_bracketless_calls_and_derivatives() -> None:
    assert to_maxima('sin x') == 'sin(x)'
    assert to_maxima('sqrt x + 1') == 'sqrt(x) + 1'
    assert to_maxima('df(y,x,2)') == "'diff(y,x,2)"
    assert to_maxima('e^x') == '%e^x'


def test_reduce_names_become_maxima_names() -> None:
    assert to_maxima_names('BesselJ(0,x)') == 'bessel_j(0,x)'
    assert to_maxima_names('Si(pi*x)') == 'expintegral_si(%pi*x)'
    assert to_maxima_names('infinity') == 'inf'
    assert to_maxima_names('heaviside(x)') == 'unit_step(x)'


def test_comments_are_removed() -> None:
    assert strip_comments('x % commento\ny') == 'x \ny'
