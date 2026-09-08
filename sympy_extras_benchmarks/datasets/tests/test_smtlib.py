"""The SMT-LIB parser on problems written here (no network)."""
from __future__ import annotations

from sympy import Symbol, Rational, And, Or, Not, Implies, Eq, Ne, Le, Xor, Piecewise, true, false
from sympy.logic.boolalg import ITE
from sympy.testing.pytest import raises

from sympy_extras_benchmarks.datasets.smtlib import tokenize, parse, translate, SMTLibError

x, y, z = Symbol('x'), Symbol('y'), Symbol('z')


def test_tokenize() -> None:
    assert tokenize('(assert (<= (* x x) 1))') == ['(', 'assert', '(', '<=', '(', '*', 'x', 'x', ')', '1', ')', ')']
    assert tokenize('(set-info :source |multi\nline|) ; comment\n(check-sat)') == [
        '(', 'set-info', ':source', '|multi\nline|', ')', '(', 'check-sat', ')']
    assert tokenize('(set-info :category "industrial")') == ['(', 'set-info', ':category', '"industrial"', ')']
    raises(SMTLibError, lambda: tokenize('(a |b)'))
    raises(SMTLibError, lambda: tokenize('(a "b)'))


def test_parse() -> None:
    assert parse(tokenize('(a (b c) d)')) == [['a', ['b', 'c'], 'd']]
    assert parse(tokenize('() (x)')) == [[], ['x']]
    raises(SMTLibError, lambda: parse(tokenize('(a')))
    raises(SMTLibError, lambda: parse(tokenize('a)')))


def _problem(body: str, declarations: str = '(declare-fun x () Real) (declare-fun y () Real)',
             status: str = 'sat') -> str:
    return '(set-logic QF_NRA) (set-info :status %s) %s %s (check-sat) (exit)' % (status, declarations, body)


def test_terms() -> None:
    p = translate(_problem('(assert (= (+ x (* 2 y) (- 3)) (/ 1 2)))'), 'terms')
    assert p is not None
    assert p.formula == Eq(x + 2*y - 3, Rational(1, 2))
    assert p.variables == [x, y]
    assert p.status == 'sat'
    assert p.name == 'terms'
    assert repr(p) == 'Problem(terms, sat, 2 variables)'
    p = translate(_problem('(assert (< (- x y 1) (* x x x)))'))
    assert p is not None and p.formula == (x - y - 1 < x**3)
    p = translate(_problem('(assert (> (/ x 4 2) 0.25))'))
    assert p is not None and p.formula == (x/8 > Rational(1, 4))
    p = translate(_problem('(assert (>= (ite (< x 0) (- x) x) 1))'))
    assert p is not None and p.formula == (Piecewise((-x, x < 0), (x, True)) >= 1)


def test_connectives() -> None:
    p = translate(_problem('(assert (and (< x 1) (or (> y 0) (not (= x y))) (=> (> x 0) (> y 0))))'))
    assert p is not None
    assert p.formula == And(x < 1, Or(y > 0, Not(Eq(x, y))), Implies(x > 0, y > 0))
    p = translate(_problem('(assert (xor (< x 0) (< y 0)))'))
    assert p is not None and p.formula == Xor(x < 0, y < 0)
    p = translate(_problem('(assert (distinct x y 1))'))
    assert p is not None and p.formula == And(Ne(x, y), Ne(x, 1), Ne(y, 1))
    p = translate(_problem('(assert (<= 0 x y 1))'))
    assert p is not None and p.formula == And(Le(0, x), Le(x, y), Le(y, 1))
    p = translate(_problem('(assert (ite (< x 0) (< y 0) (> y 0)))'))
    assert p is not None and p.formula == ITE(x < 0, y < 0, y > 0)
    p = translate(_problem('(assert (=> (> x 0) (> y 0) (> x y)))'))
    assert p is not None and p.formula == Implies(x > 0, Implies(y > 0, x > y))
    p = translate(_problem('(assert true) (assert (< x 0))'))
    assert p is not None and p.formula == (x < 0)
    p = translate(_problem('(assert false)'))
    assert p is not None and p.formula is false


def test_let_and_define_fun() -> None:
    p = translate(_problem('(assert (let ((?v_0 (* x x)) (?v_1 (< y 0))) (and (< ?v_0 1) ?v_1 (let ((?v_0 y)) (> ?v_0 0)))))'))
    assert p is not None
    assert p.formula == And(x**2 < 1, y < 0, y > 0)
    p = translate(_problem('(define-fun c () Real (/ 22 7)) (assert (< x c))'))
    assert p is not None and p.formula == (x < Rational(22, 7))
    p = translate(_problem('(assert (= (> x 0) (> y 0)))'))
    assert p is not None
    assert p.formula.subs({x: 1, y: 1}) is true and p.formula.subs({x: 1, y: -1}) is false


def test_status_and_conjunction() -> None:
    p = translate(_problem('(assert (< x 0)) (assert (> x 1))', status='unsat'))
    assert p is not None
    assert p.status == 'unsat'
    assert p.formula == And(x < 0, x > 1)
    p = translate('(declare-const x Real) (assert (< x 0))')
    assert p is not None and p.status == 'unknown' and p.variables == [x]


def test_rejected() -> None:
    assert translate(_problem('(assert (< x 0))', '(declare-fun x () Int)')) is None
    assert translate(_problem('(assert (< (f x) 0))', '(declare-fun x () Real) (declare-fun f (Real) Real)')) is None
    assert translate(_problem('(assert (< x 0))', '(declare-const x Bool)')) is None
    assert translate(_problem('(assert (< x w))')) is None
    assert translate(_problem('(assert (foo x 1))')) is None
    assert translate(_problem('')) is None
    assert translate(_problem('(assert (< x 0)) (push 1)')) is None
    assert translate('(assert (< x') is None
    assert translate(_problem('(assert (exists ((z Real)) (< z x)))')) is None
