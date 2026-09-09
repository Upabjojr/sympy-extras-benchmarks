"""Tests of the solver-regression parser on samples written here in
SMT-LIB syntax (nothing is copied from the collections)."""
from __future__ import annotations

from sympy import And, Eq, Mod, Ne, Or, Symbol, S, true
from sympy.testing.pytest import raises

from sympy_extras.assumptions import Exists, ForAll

from sympy_extras_benchmarks.datasets.smtlib import SMTLibError
from sympy_extras_benchmarks.datasets.solver_regressions import (
    ARITHMETIC_LOGICS, ArithProblem, translate)


def test_integer_problem() -> None:
    text = """
    (set-logic QF_LIA)
    (set-info :status unsat)
    (declare-fun n () Int)
    (declare-fun m () Int)
    (assert (and (> n 0) (< n 1) (= m (+ n 2))))
    (check-sat)
    """
    problem = translate(text, 'integers')
    assert problem is not None
    assert problem.status == 'unsat'
    assert problem.logic == 'QF_LIA'
    assert problem.domain is S.Integers
    assert [s.name for s in problem.integers] == ['m', 'n']
    assert problem.reals == []
    assert all(s.is_integer for s in problem.integers)
    assert not problem.quantified


def test_real_problem_and_expect_header() -> None:
    # cvc5 records the answer in a header comment rather than in set-info
    text = """
    ; COMMAND-LINE: --quiet
    ; EXPECT: sat
    (set-logic QF_NRA)
    (declare-const x Real)
    (assert (> (* x x) 2))
    (check-sat)
    """
    problem = translate(text, 'reals')
    assert problem is not None
    assert problem.status == 'sat'
    assert problem.domain is S.Reals
    assert problem.integers == []
    x = Symbol('x')
    assert problem.formula == (x**2 > 2)


def test_status_prefers_set_info() -> None:
    text = """
    ; EXPECT: sat
    (set-logic QF_LIA)
    (set-info :status unsat)
    (declare-fun n () Int)
    (assert (< n n))
    (check-sat)
    """
    problem = translate(text, 'both')
    assert problem is not None
    assert problem.status == 'unsat'


def test_contradictory_expect_headers_are_unknown() -> None:
    text = """
    ; EXPECT: sat
    ; EXPECT: unsat
    (set-logic QF_LIA)
    (declare-fun n () Int)
    (assert (> n 0))
    (check-sat)
    """
    problem = translate(text, 'ambiguous')
    assert problem is not None
    assert problem.status == 'unknown'


def test_quantifiers() -> None:
    text = """
    (set-logic NRA)
    (set-info :status sat)
    (declare-fun a () Real)
    (assert (forall ((x Real)) (>= (+ (* x x) a) 0)))
    (check-sat)
    """
    problem = translate(text, 'quantified')
    assert problem is not None
    assert problem.quantified
    x, a = Symbol('x'), Symbol('a')
    assert problem.formula == ForAll(x, x**2 + a >= 0)
    assert [s.name for s in problem.reals] == ['a']


def test_nested_quantifiers_keep_their_order() -> None:
    text = """
    (set-logic LIA)
    (set-info :status sat)
    (assert (forall ((n Int)) (exists ((m Int)) (> m n))))
    (check-sat)
    """
    problem = translate(text, 'nested')
    assert problem is not None
    n, m = Symbol('n', integer=True), Symbol('m', integer=True)
    assert problem.formula == ForAll(n, Exists(m, m > n))
    assert problem.variables == []


def test_divisible() -> None:
    text = """
    (set-logic LIA)
    (set-info :status sat)
    (declare-fun n () Int)
    (assert ((_ divisible 3) (+ n 1)))
    (check-sat)
    """
    problem = translate(text, 'divisible')
    assert problem is not None
    n = Symbol('n', integer=True)
    assert problem.formula == Eq(Mod(n + 1, 3), 0)


def test_mod_and_div_with_a_positive_numeral() -> None:
    text = """
    (set-logic QF_NIA)
    (set-info :status sat)
    (declare-fun n () Int)
    (assert (and (= (mod n 4) 1) (= (div n 4) 2)))
    (check-sat)
    """
    problem = translate(text, 'euclidean')
    assert problem is not None
    n = Symbol('n', integer=True)
    assert problem.formula == And(Eq(Mod(n, 4), 1), Eq((n - Mod(n, 4))/4, 2))


def test_negative_divisor_is_refused() -> None:
    # SMT-LIB's div/mod are Euclidean: the remainder is non-negative even
    # for a negative divisor, which SymPy's Mod is not, so the file is
    # not translated rather than translated wrongly
    text = """
    (set-logic QF_NIA)
    (declare-fun n () Int)
    (assert (= (mod n (- 4)) 1))
    (check-sat)
    """
    assert translate(text, 'negative-divisor') is None


def test_variable_divisor_is_refused() -> None:
    text = """
    (set-logic QF_NIA)
    (declare-fun n () Int)
    (declare-fun m () Int)
    (assert (= (mod n m) 1))
    (check-sat)
    """
    assert translate(text, 'variable-divisor') is None


def test_mixed_sorts_are_refused() -> None:
    text = """
    (set-logic QF_LIRA)
    (declare-fun n () Int)
    (declare-fun x () Real)
    (assert (> (+ n x) 0))
    (check-sat)
    """
    assert translate(text, 'mixed') is None


def test_other_sorts_and_logics_are_refused() -> None:
    bitvector = """
    (set-logic QF_BV)
    (declare-fun b () (_ BitVec 8))
    (assert (= b b))
    (check-sat)
    """
    assert translate(bitvector, 'bitvector') is None
    uninterpreted = """
    (set-logic QF_UF)
    (declare-sort U 0)
    (declare-fun u () U)
    (assert (= u u))
    (check-sat)
    """
    assert translate(uninterpreted, 'uninterpreted') is None
    unary = """
    (set-logic QF_LIA)
    (declare-fun f (Int) Int)
    (assert (> (f 1) 0))
    (check-sat)
    """
    assert translate(unary, 'unary-function') is None


def test_no_assertion_is_refused() -> None:
    text = """
    (set-logic QF_LIA)
    (declare-fun n () Int)
    (check-sat)
    """
    assert translate(text, 'empty') is None


def test_let_and_define_fun() -> None:
    text = """
    (set-logic QF_NRA)
    (set-info :status sat)
    (declare-fun x () Real)
    (define-fun two () Real 2.0)
    (assert (let ((v (* x x))) (and (> v two) (< x 0))))
    (check-sat)
    """
    problem = translate(text, 'let')
    assert problem is not None
    x = Symbol('x')
    assert problem.formula == And(x**2 > 2, x < 0)


def test_connectives_and_distinct() -> None:
    text = """
    (set-logic QF_LIA)
    (set-info :status sat)
    (declare-fun n () Int)
    (declare-fun m () Int)
    (assert (distinct n m 0))
    (assert (=> (> n 0) (or (< m 0) (not (= m 1)))))
    (check-sat)
    """
    problem = translate(text, 'connectives')
    assert problem is not None
    n, m = Symbol('n', integer=True), Symbol('m', integer=True)
    assert problem.formula.has(Ne(n, m))
    assert problem.formula.subs({n: 1, m: 2}) is true


def test_division_by_zero_is_refused() -> None:
    text = """
    (set-logic QF_NRA)
    (declare-fun x () Real)
    (assert (> (/ x 0) 1))
    (check-sat)
    """
    assert translate(text, 'division-by-zero') is None


def test_repr_and_domain() -> None:
    problem = ArithProblem('demo', true, [Symbol('n', integer=True)], [], 'sat', 'QF_LIA', False)
    assert repr(problem) == 'ArithProblem(demo, QF_LIA, sat, 1 integer, 0 real)'
    assert problem.domain is S.Integers
    assert ArithProblem('d', true, [], [Symbol('x')], 'sat', 'QF_NRA', False).domain is S.Reals


def test_arithmetic_logics_cover_the_integer_ones() -> None:
    for logic in ('QF_LIA', 'QF_NIA', 'LIA', 'NIA', 'QF_NRA', 'NRA'):
        assert logic in ARITHMETIC_LOGICS


def test_smtlib_error_is_raised_by_the_shared_reader() -> None:
    from sympy_extras_benchmarks.datasets.smtlib import parse, tokenize
    raises(SMTLibError, lambda: parse(tokenize('(assert (> x 1)')))


def test_unknown_status_when_nothing_is_recorded() -> None:
    text = """
    (set-logic QF_NRA)
    (declare-fun x () Real)
    (assert (> x 1))
    (check-sat)
    """
    problem = translate(text, 'silent')
    assert problem is not None
    assert problem.status == 'unknown'


def test_or_of_relations_over_the_integers() -> None:
    text = """
    (set-logic QF_LIA)
    (set-info :status sat)
    (declare-fun n () Int)
    (assert (or (<= n (- 3)) (>= n 3)))
    (check-sat)
    """
    problem = translate(text, 'union')
    assert problem is not None
    n = Symbol('n', integer=True)
    assert problem.formula == Or(n <= -3, n >= 3)


def test_a_shadowing_binder_does_not_capture() -> None:
    # SymPy identifies symbols by name, so an inner binder of the same
    # name would capture the outer variable a let refers to: here ?y is
    # the OUTER x, and the formula is unsatisfiable
    text = """
    (set-logic ALL)
    (set-info :status unsat)
    (assert (exists ((x Real))
              (let ((?y x))
              (and (<= 0 x) (exists ((x Real)) (forall ((v Real)) (> 0 ?y)))))))
    (check-sat)
    """
    problem = translate(text, 'shadowed')
    assert problem is not None
    names = sorted({s.name for s in problem.formula.atoms(Symbol)})
    assert names == ['v', 'x', 'x__1']


def test_the_domain_follows_the_binders_of_a_closed_formula() -> None:
    # every variable is quantifier-bound, so there is no declaration to
    # read the sort from; the problem is still an integer one
    text = """
    (set-info :status sat)
    (assert (forall ((n Int)) (exists ((m Int)) (> m n))))
    (check-sat)
    """
    problem = translate(text, 'closed')
    assert problem is not None
    assert problem.variables == []
    assert problem.domain is S.Integers
    real = translate("""
    (set-info :status sat)
    (assert (forall ((x Real)) (exists ((y Real)) (> y x))))
    (check-sat)
    """, 'closed-real')
    assert real is not None
    assert real.domain is S.Reals


def test_a_file_mixing_the_sorts_in_binders_is_refused() -> None:
    text = """
    (set-info :status sat)
    (assert (forall ((n Int)) (exists ((x Real)) (> x n))))
    (check-sat)
    """
    assert translate(text, 'mixed-binders') is None
