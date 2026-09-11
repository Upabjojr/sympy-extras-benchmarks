"""The QEPCAD/Tarski formula parser on formulas written here (no network)."""
from __future__ import annotations

from sympy import Symbol, Rational, Eq, Ne, Le, And, Or, Not, Implies, Equivalent, true, false
from sympy.testing.pytest import raises

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras_benchmarks.datasets.qepcad_syntax import (
    QEPCADInput, QEPCADSyntaxError, UnsupportedSyntax, parse_formula, parse_inputs, tokenize)

a, b, c, x, y, z = [Symbol(n) for n in 'abcxyz']


def test_tokenize() -> None:
    assert tokenize('x <==> y ==> z <== w') == ['x', '<==>', 'y', '==>', 'z', '<==', 'w']
    assert tokenize('[a /\\ b \\/ ~c]') == ['[', 'a', '/\\', 'b', '\\/', '~', 'c', ']']
    raises(QEPCADSyntaxError, lambda: tokenize('x $ y'))


def test_polynomials() -> None:
    assert parse_formula('2 x y^2 - 3 = 0') == Eq(2*x*y**2 - 3, 0)
    assert parse_formula('-1(x - y) > 0') == (-(x - y) > 0)
    assert parse_formula('1/2 (x + y) <= a') == (Rational(1, 2)*(x + y) <= a)
    assert parse_formula('x * y /= 3/4') == Ne(x*y, Rational(3, 4))
    assert parse_formula('- - x < 2') == (x < 2)
    assert parse_formula('x^2 y^3 >= 0') == (x**2*y**3 >= 0)
    assert parse_formula('0 <= x <= 1') == And(Le(0, x), Le(x, 1))


def test_connectives() -> None:
    assert parse_formula('[x > 0 /\\ y > 0] \\/ z = 0') == Or(And(x > 0, y > 0), Eq(z, 0))
    assert parse_formula('~ x > 0 /\\ y > 0') == And(Not(x > 0), y > 0)
    assert parse_formula('x > 0 ==> y > 0') == Implies(x > 0, y > 0)
    assert parse_formula('x > 0 <== y > 0') == Implies(y > 0, x > 0)
    assert parse_formula('x > 0 <==> y > 0') == Equivalent(x > 0, y > 0)
    assert parse_formula('true /\\ FALSE \\/ x = 1') == Eq(x, 1)
    assert parse_formula('[true]') == true
    assert parse_formula('false') == false


def test_round_brackets() -> None:
    # Tarski prints parentheses around atoms and formulas as well
    assert parse_formula('(x > 0) /\\ (~((x + 1) y >= 0))') == And(x > 0, Not((x + 1)*y >= 0))
    assert parse_formula('(x + 1) (y - 1) > 0') == ((x + 1)*(y - 1) > 0)


def test_quantifiers() -> None:
    assert parse_formula('(E x)(A y)[x y = 1]') == Exists(x, ForAll(y, Eq(x*y, 1)))
    assert parse_formula('(Ex)[x^2 = a].') == Exists(x, Eq(x**2, a))
    assert parse_formula('ex x, y [ x + y = 1 /\\ x y > 0 ]') == Exists((x, y), And(Eq(x + y, 1), x*y > 0))
    assert parse_formula('all x [ a x^2 + b x + c >= 0 ]') == ForAll(x, a*x**2 + b*x + c >= 0)


def test_unsupported() -> None:
    raises(UnsupportedSyntax, lambda: parse_formula('(F x)[x > 0]'))
    raises(UnsupportedSyntax, lambda: parse_formula('(X2 x)[x^2 = 1]'))
    raises(UnsupportedSyntax, lambda: parse_formula('x > _root_1 x^2 - 2'))
    raises(QEPCADSyntaxError, lambda: parse_formula('x + > 1'))
    raises(QEPCADSyntaxError, lambda: parse_formula('x + 1'))
    raises(QEPCADSyntaxError, lambda: parse_formula('x^y > 1'))


def test_inputs() -> None:
    text = """#1: a made-up problem
[ Lower bound ]
(a,b,x)
2
(A x)[ x^2 + a x
  + b > 0 ].
go
go
sol T
[]
(x,y)
1
(E y)[ y^2 = x ].
assume [ x /= 2 ]
finish
"""
    inputs = parse_inputs(text)
    assert len(inputs) == 2
    first, second = inputs[0][1], inputs[1][1]
    assert isinstance(first, QEPCADInput) and isinstance(second, QEPCADInput)
    assert first.name == 'Lower bound'
    assert first.variables == [a, b, x] and first.free_variables == [a, b]
    assert first.formula == ForAll(x, x**2 + a*x + b > 0)
    assert first.assumptions is None
    assert second.formula == Exists(y, Eq(y**2, x))
    assert second.assumptions == Ne(x, 2)


def test_transcript() -> None:
    text = """Enter an informal description  between '[' and ']':
[ Quadratic ]
Enter a variable list:
(c,x)
Enter the number of free variables:
1
Enter a prenex formula:
(E x)[x^2 + c = 0].
"""
    inputs = parse_inputs(text)
    assert len(inputs) == 1
    problem = inputs[0][1]
    assert isinstance(problem, QEPCADInput)
    assert problem.formula == Exists(x, Eq(x**2 + c, 0))
