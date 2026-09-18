"""Maple's polynomial notation."""
from __future__ import annotations

from sympy import Symbol

from sympy_extras_benchmarks.parsers.maple import polynomial

x, y = Symbol('x'), Symbol('y')


def test_polynomial() -> None:
    symbols: dict[str, Symbol] = {}
    assert polynomial('x^2*y-3/2*x', symbols) == x**2*y - 3*x/2
    assert set(symbols) == {'x', 'y'}
    # a name SymPy defines (E, I, S, N, Q) is read as a variable
    e = polynomial('E*I+Q', {})
    assert {str(s) for s in e.free_symbols} == {'E', 'I', 'Q'}
