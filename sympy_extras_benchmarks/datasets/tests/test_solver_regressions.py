"""The expected answers of cvc5's ``; EXPECT:`` comments, on samples written
here in SMT-LIB syntax (nothing is copied from the collections)."""
from __future__ import annotations

from sympy import S, Symbol

from sympy_extras_benchmarks.datasets.solver_regressions import translate


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


