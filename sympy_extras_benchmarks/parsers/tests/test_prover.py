"""The arithmetic grammar Lean and Rocq share, and the two statement readers.
The refusals matter as much as the translations: reading as true a statement
which means something else in the proof assistant would produce a false bug
report."""
from __future__ import annotations

from sympy import Implies, Lt, Ne, S, Symbol
from sympy.testing.pytest import raises

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras_benchmarks.parsers.lean import LeanGoal, example
from sympy_extras_benchmarks.parsers.prover import (SyntaxRefused, balanced, bars_to_abs,
                                                    proposition, split_top)
from sympy_extras_benchmarks.parsers.rocq import CoqGoal, scope_of, statement

x, y = Symbol('x'), Symbol('y')
V = {'x': x, 'y': y}


# ---------------------------------------------------------------------------
# the shared grammar

def test_the_operators_the_grammar_accepts() -> None:
    assert proposition('0 < x', V) == Lt(0, x)
    assert proposition('x != y', V) == Ne(x, y)
    assert proposition('x^2 >= 0', V) == (x**2 >= 0)
    assert proposition('x*(y + 1) > 0', V) == (x*(y + 1) > 0)
    assert proposition('0 < x -> x != 0', V) == Implies(Lt(0, x), Ne(x, 0))
    assert proposition('x < y and y < x', V) == ((x < y) & (y < x))
    assert proposition('not (x < y)', V) == (x >= y)


def test_a_chained_relation_becomes_a_conjunction() -> None:
    assert proposition('x < y < 2', V) == ((x < y) & (y < 2))


def test_only_declared_names_are_accepted() -> None:
    raises(SyntaxRefused, lambda: proposition('x + z > 0', V))
    raises(SyntaxRefused, lambda: proposition('f(x) > 0', V))


def test_total_arithmetic_is_refused() -> None:
    # in Lean and in Rocq ``x / 0`` is 0: over R the same formula says something else
    raises(SyntaxRefused, lambda: proposition('1/x > 0', V))
    raises(SyntaxRefused, lambda: proposition('x / 0 = 0', V))
    raises(SyntaxRefused, lambda: proposition('2^x > 0', V))


def test_the_text_helpers() -> None:
    assert balanced('(a + b)') and not balanced('(a + b')
    assert split_top('a : b', ':') == ('a ', ' b')
    assert split_top('(a : b)', ':') is None
    assert bars_to_abs('|x| + 1') == 'abs(x) + 1'


# ---------------------------------------------------------------------------
# Lean

def test_a_lean_goal_and_its_statement() -> None:
    g = example('(x y : ℚ) (h1 : x < y) (h2 : 0 < x) : 0 < y', 'demo:1')
    assert isinstance(g, LeanGoal)
    assert g.domain is S.Reals and g.expected is True
    a, b = g.variables
    assert g.statement == ForAll((a, b), Implies(Lt(0, a) & Lt(a, b), Lt(0, b)))


def test_a_false_conclusion_means_the_hypotheses_are_contradictory() -> None:
    g = example('(a : ℚ) (h : a < 0) (h2 : 0 < a) : False', 'demo:2')
    assert isinstance(g, LeanGoal) and g.expected is False
    assert isinstance(g.statement, Exists)


def test_the_integer_type_gives_integer_symbols() -> None:
    g = example('(n : ℤ) (h : 0 < n) : n ≠ 0', 'demo:3')
    assert isinstance(g, LeanGoal) and g.domain is S.Integers
    assert all(v.is_integer for v in g.variables)


def test_lean_refuses_what_would_change_meaning() -> None:
    # on N subtraction is truncated (5 - 20 = 0) and division is integer division
    assert example('(n : ℕ) : n - 1 < n', 'd') == 'truncated subtraction on a nonnegative type'
    assert isinstance(example('(x : ℂ) : x = x', 'd'), str)
    assert isinstance(example('(x : ℝ) : x / 0 = 0', 'd'), str)
    assert isinstance(example('{α : Type} [Fintype α] (x : α) : x = x', 'd'), str)


def test_a_nonnegative_type_adds_its_hypothesis() -> None:
    g = example('(n : ℕ) : 0 <= n', 'd')
    assert isinstance(g, LeanGoal)
    assert any(h == (S.Zero <= v) for h in g.hypotheses for v in g.variables)


def test_a_polymorphic_goal_is_read_at_the_reals() -> None:
    g = example('{α : Type} [LinearOrderedField α] (x : α) : x ≤ x', 'd')
    assert isinstance(g, LeanGoal) and g.domain is S.Reals


# ---------------------------------------------------------------------------
# Rocq

def test_a_rocq_statement() -> None:
    g = statement('mul_pos : forall (x y : Z), x > 0 -> y > 0 -> x * y > 0', 'Z', 'demo', 1)
    assert isinstance(g, CoqGoal) and g.name == 'demo:mul_pos'
    assert g.scope == 'Z' and g.domain is S.Integers and g.expected is True


def test_rocq_reads_named_hypotheses_and_arrows() -> None:
    g = statement('forall (x : Z) (H : 0 < x), x <> 0', 'Z', 'demo', 1)
    assert isinstance(g, CoqGoal) and len(g.hypotheses) == 1


def test_rocq_drops_the_scope_marker() -> None:
    assert isinstance(statement('forall (x : Z), (0 <= x)%Z', 'Z', 'demo', 1), CoqGoal)


def test_rocq_refuses_another_domain_or_a_truncated_one() -> None:
    assert statement('forall x : R, x = x', 'Z', 'demo', 1) is None
    assert statement('forall (n : nat), n - 1 <= n', 'Z', 'demo', 1) is None


def test_the_scope_of_a_file() -> None:
    assert scope_of('Open Scope Z_scope.\nLemma l : forall x : Z, x = x.') == 'Z'
    assert scope_of('Require Import ZArith.\nLemma l : True.') == 'Z'
    assert scope_of('Open Scope nat_scope.') is None
