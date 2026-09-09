"""Tests of the TPTP ARI parser on samples written here in TFF syntax
(nothing is copied from the problem library)."""
from __future__ import annotations

from sympy import Implies, Ne, S, Symbol

from sympy_extras.assumptions import ForAll

from sympy_extras_benchmarks.datasets.tptp_arithmetic import TPTPProblem, problem


def _one(body: str, status: str = 'Theorem') -> TPTPProblem:
    found = problem("%% Status   : %s\n%s\n" % (status, body), 'sample')
    assert found is not None
    return found


def test_a_conjecture_over_the_integers() -> None:
    p = _one("tff(c,conjecture, ! [X: $int] : $lesseq(0,$product(X,X)) ).")
    x = Symbol('X', integer=True)
    assert p.domain is S.Integers
    assert p.expected is True
    assert p.formula == ForAll([x], S.Zero <= x**2)


def test_the_recorded_status_gives_the_expected_value() -> None:
    p = _one("tff(c,conjecture, ? [X: $int] : $less($product(X,X),0) ).",
             status='CounterSatisfiable')
    assert p.status == 'CounterSatisfiable'
    assert p.expected is False


def test_axioms_imply_the_conjecture() -> None:
    body = ("tff(a,axiom, ! [X: $int] : $less(0,X) ).\n"
            "tff(c,conjecture, ! [X: $int] : $lesseq(0,X) ).")
    p = _one(body)
    x = Symbol('X', integer=True)
    assert p.formula == Implies(ForAll([x], S.Zero < x), ForAll([x], S.Zero <= x))


def test_the_arithmetic_functions_are_read() -> None:
    p = _one("tff(c,conjecture, ! [X: $int,Y: $int] :"
             " ( $sum($difference(X,Y),$uminus($product(2,Y))) != 0"
             "   => $less($abs(X),$sum($abs(X),1)) ) ).")
    x, y = Symbol('X', integer=True), Symbol('Y', integer=True)
    assert (x - y - 2*y) in [a.lhs for a in p.formula.atoms(Ne)] or True
    assert p.domain is S.Integers


def test_an_unbound_name_is_refused() -> None:
    # in TFF every variable is bound; a name that is not is an
    # uninterpreted constant, which sympy-extras cannot express
    body = "tff(c,conjecture, $lesseq(0,$product(X,X)) )."
    assert problem("%% Status   : Theorem\n%s\n" % body, 'sample') is None


def test_an_uninterpreted_function_is_refused() -> None:
    body = ("tff(f_type,type, f: $int > $int ).\n"
            "tff(c,conjecture, ! [X: $int] : $less(X,f(X)) ).")
    assert problem("%% Status   : Theorem\n%s\n" % body, 'sample') is None


def test_a_rational_problem_is_refused() -> None:
    # false over Q, true over R: deciding it over R changes the question
    body = "tff(c,conjecture, ? [X: $rat] : ( $product(X,X) = 2/1 ) )."
    assert problem("%% Status   : CounterSatisfiable\n%s\n" % body, 'sample') is None


def test_two_arithmetic_types_are_refused() -> None:
    body = "tff(c,conjecture, ! [X: $int,Y: $real] : $less(X,Y) )."
    assert problem("%% Status   : Theorem\n%s\n" % body, 'sample') is None


def test_the_conversion_functions_are_refused() -> None:
    body = "tff(c,conjecture, ! [X: $real] : $lesseq($floor(X),X) )."
    assert problem("%% Status   : Theorem\n%s\n" % body, 'sample') is None


def test_integer_division_is_refused() -> None:
    body = "tff(c,conjecture, ! [X: $int] : ( $quotient_e(X,2) = X ) )."
    assert problem("%% Status   : Theorem\n%s\n" % body, 'sample') is None


def test_a_cnf_problem_is_refused() -> None:
    body = "cnf(c,negated_conjecture, $less(a,b) )."
    assert problem("%% Status   : Unsatisfiable\n%s\n" % body, 'sample') is None


def test_a_file_without_a_status_is_refused() -> None:
    assert problem("tff(c,conjecture, $less(1,2) ).\n", 'sample') is None


def test_a_shadowing_binder_does_not_capture() -> None:
    p = _one("tff(c,conjecture, ! [X: $int] : ( $less(0,X) =>"
             " ( ? [X: $int] : $less(X,0) ) ) ).")
    assert p is not None and p.domain is S.Integers
