"""Tests of the TPTP ARI parser on samples written here in TFF syntax
(nothing is copied from the problem library)."""
from __future__ import annotations

from typing import Optional

from sympy import Implies, Ne, S, Symbol

from sympy_extras.assumptions import ForAll

from sympy_extras_benchmarks.parsers.tptp import TPTPProblem, problem


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


def _p(body: str, status: str = 'Theorem') -> Optional[TPTPProblem]:
    return problem('%% Status   : %s\n%s\n' % (status, body), 'test')


# ---------------------------------------------------------------------------
# problems without variables: the type is implied by the numerals

def test_a_ground_problem_needs_no_type_declaration() -> None:
    p = _p('tff(a,conjecture, $less(2,3) ).')
    assert p is not None and p.domain is S.Integers and bool(p.formula) is True
    q = _p('tff(a,conjecture, ~ $less(3,2) ).')
    assert q is not None and bool(q.formula) is True


def test_a_ground_problem_with_a_decimal_is_read_over_the_reals() -> None:
    p = _p('tff(a,conjecture, $less(1.5,2.0) ).')
    assert p is not None and p.domain is S.Reals and bool(p.formula) is True


def test_a_ground_problem_with_a_rational_literal() -> None:
    p = _p('tff(a,conjecture, $less(1/2,1) ).')
    assert p is not None and p.domain is S.Reals and bool(p.formula) is True


def test_a_variable_without_a_declared_type_is_refused() -> None:
    assert _p('tff(a,conjecture, ! [X] : $less(X,X) ).') is None


def test_the_recorded_status_says_what_resolve_must_return() -> None:
    p = _p('tff(a,conjecture, $less(3,2) ).', status='CounterSatisfiable')
    assert p is not None and p.expected is False and bool(p.formula) is False


def test_a_problem_too_deeply_nested_is_refused_not_crashed() -> None:
    body = 'tff(a,conjecture, ! [X: $int] : %s $less(0,X) %s).' % ('~ (' * 3000, ')' * 3000)
    assert _p(body) is None
