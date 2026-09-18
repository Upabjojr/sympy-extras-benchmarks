"""The rewriting of FriCAS input into Maxima's syntax."""
from __future__ import annotations

from sympy_extras_benchmarks.parsers.fricas import joined, quoted, to_maxima


def test_names_and_constants_become_maximas() -> None:
    assert to_maxima('imag(z)*%pi + real(z)') == 'imagpart(z)*%pi + realpart(z)'
    assert to_maxima('legendreP(2,z)**2') == 'legendre_p(2,z)^2'
    assert to_maxima('hermiteH(n,x) + laguerreL(n,x)') == 'hermite(n,x) + laguerre(n,x)'


def test_the_imaginary_unit_and_the_infinities() -> None:
    assert to_maxima('I') == '%i'
    assert to_maxima('exp(I*x)') == 'exp(%i*x)'
    assert to_maxima('%plusInfinity') == 'inf'
    assert to_maxima('%minusInfinity') == 'minf'


def test_a_name_that_merely_contains_i_is_left_alone() -> None:
    assert to_maxima('I*x + Illegal') == '%i*x + Illegal'
    assert to_maxima('Ideal') == 'Ideal'


def test_comments_commands_and_continuation_lines() -> None:
    text = ('-- a note\n'
             't1 := integrate(f, _\n'
             '   x = 0..1)\n'
             ')set output\n'
             't2 := 1  -- trailing\n')
    stripped = joined(text)
    assert 'a note' not in stripped and 'set output' not in stripped
    assert 'trailing' not in stripped
    assert 't1 := integrate(f,    x = 0..1)' in stripped


def test_string_literals() -> None:
    assert quoted('"(x+1)*"   "exp(x)"') == '(x+1)*exp(x)'
    assert quoted('"alone"') == 'alone'
    assert quoted('f: String') is None
    assert quoted('"con _\\"escape"') is None
