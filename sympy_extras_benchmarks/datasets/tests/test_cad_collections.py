"""The readers of the CAD test collections (Bath, QEPCAD B, Tarski) on
texts written here (no network)."""
from __future__ import annotations

import pathlib

from sympy import Symbol

from sympy_extras_benchmarks.datasets import bath_cad, qepcad_tests, tarski_tests
from sympy_extras_benchmarks.datasets.qepcad_syntax import Example, blocks

x, y = Symbol('x'), Symbol('y')


def test_answers_after() -> None:
    lines = ['x > 1 /\\ y < 0', 'x > 1', 'FALSE', 'FALSE']
    assert qepcad_tests._answers_after('go\ngo\nsol E\nsol T\ncontinue\n', lines) == 'x > 1'
    assert qepcad_tests._answers_after('go\nsol T\n', lines) == 'FALSE'
    assert lines == ['FALSE']
    assert qepcad_tests._answers_after('q\n', lines) is None
    assert lines == ['FALSE']


def test_transcript_answer() -> None:
    text = """Before Solution >
sol E

An equivalent quantifier-free formula:

x > _root_1 x^2 - 2


Before Solution >
sol T

An equivalent quantifier-free formula:

x^2 - 2 > 0 /\\
x > 0


Before Solution >
quit
"""
    assert qepcad_tests._transcript_answer(text) == 'x^2 - 2 > 0 /\\ x > 0'
    assert qepcad_tests._transcript_answer('no session here') is None


def test_blocks() -> None:
    text = "[]\n(x,y)\n1\n(E y)[y^2 = x].\ngo\nsol T\n[]\n(x)\n0\n(E x)[x > 0].\nq\n"
    found = blocks(text)
    assert len(found) == 2
    assert found[0][0].group('formula').strip() == '(E y)[y^2 = x]'
    assert 'sol T' in found[0][1] and 'q' in found[1][1]


def test_bracket() -> None:
    text = '(def F [ ex x [ x > 0 ] /\\ [ y < 1 ] ]) (def G [ z = 0 ])'
    start = text.index('[')
    assert tarski_tests._bracket(text, start) == '[ ex x [ x > 0 ] /\\ [ y < 1 ] ]'
    assert tarski_tests._bracket('[ unclosed', 0) is None


def test_brown_source() -> None:
    assert tarski_tests.brown_source(pathlib.Path('/d/a-b-chunk-0001.smt2-3.smt2')) == 'a-b-chunk-0001.smt2'
    assert tarski_tests.brown_source(pathlib.Path('a-b-chunk-0001.smt2-3-12.smt2')) == 'a-b-chunk-0001.smt2'


def test_maple() -> None:
    symbols: dict[str, Symbol] = {}
    assert bath_cad._maple('x^2*y-3/2*x', symbols) == x**2*y - 3*x/2
    assert set(symbols) == {'x', 'y'}
    # a name SymPy defines (E, I, S, N, Q) is read as a variable
    e = bath_cad._maple('E*I+Q', {})
    assert {str(s) for s in e.free_symbols} == {'E', 'I', 'Q'}


def test_example() -> None:
    example = Example('bath', '01 Parabola', 'qepcad', '[P]\n(a,x)\n1\n(E x)[a x^2 = 1].')
    assert example.key == 'bath/01 Parabola'
    assert example.question == 'resolve' and example.expected is None and example.duplicate_of is None
