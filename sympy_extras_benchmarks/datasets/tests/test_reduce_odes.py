"""Tests of the REDUCE ODE parser on samples written here in REDUCE syntax
(nothing is copied from REDUCE)."""
from __future__ import annotations

from sympy import Function, Symbol

from sympy_extras_benchmarks.datasets.reduce_odes import ReduceODE, equations, to_maxima


def _one(text: str) -> ReduceODE:
    found = equations(text, 'sample')
    assert len(found) == 1
    return found[0]


def test_a_first_order_equation() -> None:
    entry = _one("odesolve(df(y,x) - y, y, x);")
    x, y = Symbol('x'), Function('y')
    assert entry.name == 'sample:1'
    assert entry.order == 1
    assert entry.equation == y(x).diff(x) - y(x)


def test_an_equation_with_an_equals_sign() -> None:
    entry = _one("odesolve(df(y,x,2) + y = 3, y, x);")
    x, y = Symbol('x'), Function('y')
    assert entry.order == 2
    assert entry.equation == y(x).diff(x, 2) + y(x) - 3


def test_implicit_multiplication_between_a_number_and_a_name() -> None:
    entry = _one("odesolve(df(y,x,2) - 2x*df(y,x) + 2y, y, x);")
    x, y = Symbol('x'), Function('y')
    assert entry.equation == y(x).diff(x, 2) - 2*x*y(x).diff(x) + 2*y(x)


def test_implicit_multiplication_before_a_call() -> None:
    # ``4df(y,x)`` is 4 times the derivative
    entry = _one("odesolve(df(y,x,2) + 4df(y,x) + 3y, y, x);")
    x, y = Symbol('x'), Function('y')
    assert entry.equation == y(x).diff(x, 2) + 4*y(x).diff(x) + 3*y(x)


def test_a_bracketless_function_call() -> None:
    entry = _one("odesolve(df(y,x) - sin x, y, x);")
    from sympy import sin
    x, y = Symbol('x'), Function('y')
    assert entry.equation == y(x).diff(x) - sin(x)


def test_other_variable_names() -> None:
    entry = _one("odesolve(df(z,w) - z, z, w);")
    w, z = Symbol('w'), Function('z')
    assert entry.function == z(w)
    assert entry.equation == z(w).diff(w) - z(w)


def test_a_comment_is_ignored() -> None:
    text = "% odesolve(df(y,x) - 1, y, x);\nodesolve(df(y,x) - y, y, x);"
    entry = _one(text)
    x, y = Symbol('x'), Function('y')
    assert entry.equation == y(x).diff(x) - y(x)


def test_an_algebraic_equation_is_refused() -> None:
    # no derivative: not an ODE
    assert equations("odesolve(y - x, y, x);", 'sample') == []


def test_several_calls_are_numbered_in_order() -> None:
    text = "odesolve(df(y,x) - y, y, x);\nodesolve(df(y,x) - 2y, y, x);"
    first, second = equations(text, 'file')
    assert (first.name, second.name) == ('file:1', 'file:2')


def test_to_maxima_leaves_ordinary_products_alone() -> None:
    assert to_maxima('a*x + b*y') == 'a*x + b*y'


def test_to_maxima_rewrites_the_power_operator() -> None:
    assert to_maxima('x**2 + y**3') == 'x^2 + y^3'
