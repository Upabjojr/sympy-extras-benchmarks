"""Tests of the reader of FriCAS's definite integrals, on samples written
here in FriCAS syntax (nothing is copied from FriCAS)."""
from __future__ import annotations

from sympy import I, Symbol, exp, im, legendre, oo

from sympy_extras_benchmarks.datasets.fricas_integrals import integrals

v = Symbol('v')


def test_a_range_and_the_nopole_option() -> None:
    entry, = integrals('a1 := integrate(1/(1+v^2), v = 0..%plusInfinity, "noPole")\n', 'sample')
    assert entry.name == 'sample:a1'
    assert entry.integrand == 1/(v**2 + 1)
    assert (entry.lower, entry.upper) == (0, oo)


def test_a_negative_infinity_and_a_complex_path() -> None:
    first, second = integrals('a2 := integrate(exp(v), v = %minusInfinity..0)\n'
                              'a3 := integrate(v, v = -%i..%i)\n', 'sample')
    assert (first.integrand, first.lower) == (exp(v), -oo)
    assert (second.lower, second.upper) == (-I, I)


def test_maples_imaginary_unit_and_a_repeat() -> None:
    entry, = integrals('b1 := integrate(v*I, v = 0..1)\nb2 := integrate(v*%i, v = 0..1)\n',
                       'sample')
    assert entry.name == 'sample:b1'
    assert entry.integrand == I*v


def test_comments_and_commands_are_skipped() -> None:
    text = (')set output off\n-- c1 := integrate(v, v = 0..1)\n'
            'c2 := integrate(v^2, v = 0..1) -- a note\n')
    entry, = integrals(text, 'sample')
    assert entry.name == 'sample:c2'


def test_another_option_or_no_range_is_refused() -> None:
    text = 'd1 := integrate(v, v = 0..1, "other")\nd2 := integrate(v, v)\n'
    assert integrals(text, 'sample') == []


def test_names() -> None:
    entry, = integrals('f1 := integrate(imag(v)*legendreP(2, v), v = 0..1)\n', 'sample')
    assert entry.integrand == im(v)*legendre(2, v)
