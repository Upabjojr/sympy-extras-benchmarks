"""Tests of the mathlib4 tactic-test parser on samples written here in
Lean syntax (nothing is copied from mathlib)."""
from __future__ import annotations

from sympy import Abs, And, Eq, Implies, Ne, Not, S, Symbol, true

from sympy_extras.assumptions import Exists, ForAll

from sympy_extras_benchmarks.datasets.lean_tactics import LeanGoal, goals


def _one(text: str) -> LeanGoal:
    found = goals(text, 'sample')
    assert len(found) == 1
    return found[0]


def test_a_rational_goal_becomes_a_universal_implication() -> None:
    goal = _one("example (x : ℚ) (h : 0 < x) : 0 < 2 * x := by linarith")
    x = Symbol('x')
    assert goal.domain is S.Reals
    assert goal.variables == [x]
    assert goal.expected is True
    assert goal.statement == ForAll([x], Implies(And(S.Zero < x), S.Zero < 2*x))


def test_a_false_conclusion_becomes_an_existential_expected_false() -> None:
    goal = _one("example (a : ℤ) (h1 : 2 < a) (h2 : a < 1) : False := by linarith")
    a = Symbol('a', integer=True)
    assert goal.domain is S.Integers
    assert goal.expected is False
    assert goal.statement == Exists([a], And(S(2) < a, a < 1))


def test_lean_notation_is_read() -> None:
    goal = _one("example (x y : ℝ) (h : x ≤ y) (h2 : x ≠ y) : ¬ (y ≤ x) := by linarith")
    x, y = Symbol('x'), Symbol('y')
    assert goal.hypotheses == [x <= y, Ne(x, y)]
    assert goal.goal == Not(y <= x)


def test_implicit_binders_declare_variables_too() -> None:
    # positivity states most of its goals with ``{a : ℤ}``
    goal = _one("example {a : ℤ} (ha : 3 < a) : 0 < a := by positivity")
    assert [s.name for s in goal.variables] == ['a']
    assert all(s.is_integer for s in goal.variables)


def test_a_hypothesis_with_nested_parentheses_is_kept() -> None:
    # the whole point of refusing rather than skipping: dropping this
    # hypothesis would turn a valid goal into a false counterexample
    goal = _one("example (x y : ℚ) (h : 6 + ((x + 1) * x + (2 + y) * y) = 3)"
                " (h2 : (x + 1) * x ≥ 0) : False := by linarith")
    assert len(goal.hypotheses) == 2
    assert Eq(6 + ((Symbol('x') + 1)*Symbol('x') + (2 + Symbol('y'))*Symbol('y')), 3) \
        in goal.hypotheses


def test_an_arbitrary_ordered_ring_is_read_at_the_reals() -> None:
    # ℝ is a model of every class listed, so the goal holds of ℝ too
    goal = _one("example {α : Type*} [CommRing α] [LinearOrder α] [IsStrictOrderedRing α]"
                " (a : α) (h : 0 < a) : 0 ≤ a := by positivity")
    assert goal.domain is S.Reals
    assert [s.name for s in goal.variables] == ['a']


def test_a_polymorphic_binder_is_refused() -> None:
    assert goals("example {α : Type*} (a : α) (h : 0 < a) : 0 ≤ a := by positivity") == []


def test_a_type_outside_the_arithmetic_ones_is_refused() -> None:
    assert goals("example (a : EReal) (h : 0 < a) : 0 ≤ a := by positivity") == []


def test_two_different_types_are_refused() -> None:
    assert goals("example (a : ℤ) (b : ℝ) (h : 0 < a) : 0 ≤ a := by positivity") == []


def test_an_undeclared_name_is_refused() -> None:
    # ``a`` comes from a ``variable`` command earlier in the file, whose
    # type this parser does not follow
    assert goals("example (h : 0 < a) : 0 ≤ a := by positivity") == []


def test_a_variable_denominator_is_refused() -> None:
    # Lean defines ``x / 0 = 0``, so the goal does not mean over ℝ what
    # it means in Lean
    assert goals("example (a b : ℚ) (h : 0 ≤ a) (h2 : 0 ≤ b) : 0 ≤ a / b := by positivity") == []


def test_division_over_the_integers_is_refused() -> None:
    # integer division truncates
    assert goals("example (a : ℤ) (h : 0 < a) : 0 ≤ a / 2 := by positivity") == []


def test_a_rational_coefficient_over_the_rationals_is_kept() -> None:
    goal = _one("example (a : ℚ) (h : 0 < a) : 0 < a / 2 := by positivity")
    assert goal.statement == ForAll([Symbol('a')], Implies(And(S.Zero < Symbol('a')),
                                                           S.Zero < Symbol('a')/2))


def test_a_real_exponent_is_refused() -> None:
    assert goals("example (a b : ℝ) (h : 0 < a) : 0 < a ^ b := by positivity") == []


def test_an_integer_exponent_is_kept() -> None:
    goal = _one("example (a : ℚ) (h : a ≠ 0) : 0 < a ^ 4 := by positivity")
    assert goal.goal == (S.Zero < Symbol('a')**4)


def test_a_ground_goal_takes_its_domain_from_the_ascription() -> None:
    goal = _one("example : (0 : ℚ) ≤ 3 := by positivity")
    assert goal.variables == []
    assert goal.domain is S.Reals
    assert goal.statement == (S.Zero <= 3)


def test_a_ground_goal_naming_no_domain_is_read_over_the_integers() -> None:
    # a numeral with no ascription is ℕ in Lean, and ℕ agrees with ℤ on
    # every formula that neither subtracts nor divides
    goal = _one("example : 0 ≤ 3 := by positivity")
    assert goal.domain is S.Integers


def test_a_ground_goal_naming_no_domain_that_subtracts_is_refused() -> None:
    # ``5 - 20 = 0`` is a theorem of ℕ and false over ℤ
    assert goals("example : 5 - 20 = 0 := by norm_num") == []


def test_a_ground_goal_dividing_on_a_natural_type_is_refused() -> None:
    # ``5 / 2 = 2`` is a theorem of ℕ: division there truncates
    assert goals("example : (5 / 2 : ℕ) = 2 := by norm_num") == []


def test_a_real_power_with_a_fractional_exponent_is_refused() -> None:
    # Lean's rpow at a negative base is a junk value, not the real root
    assert goals("example : (-8 : ℝ) ^ (1 / 3 : ℝ) = -2 := by norm_num") == []


def test_a_natural_number_goal_gains_its_nonnegativity() -> None:
    goal = _one("example (n : ℕ) (h : 3 < n) : 0 < n := by positivity")
    n = Symbol('n', integer=True)
    assert goal.domain is S.Integers
    assert (S.Zero <= n) in goal.hypotheses
    assert goal.statement == ForAll([n], Implies(And(S.Zero <= n, S(3) < n), S.Zero < n))


def test_subtraction_on_a_nonnegative_type_is_refused() -> None:
    # ``1 - 2 = 0`` on ℕ: the formula would not mean what it says
    assert goals("example (n : ℕ) (h : 3 < n) : 0 < n - 1 := by positivity") == []


def test_a_goal_over_an_arbitrary_ordered_field_is_read_at_the_reals() -> None:
    goal = _one("example {α : Type*} [LinearOrderedField α] (a b : α) (h : a < b) :"
                " a ≤ b := by linarith")
    assert goal.domain is S.Reals
    assert [s.name for s in goal.variables] == ['a', 'b']


def test_an_instance_outside_the_vouched_classes_is_refused() -> None:
    assert goals("example {α : Type*} [Fintype α] (a : α) : a = a := by simp") == []


def test_a_chain_of_relations_is_a_conjunction() -> None:
    goal = _one("example (x n : ℤ) (h : 0 ≤ x ∧ x < n) : x < n := by linarith")
    x, n = Symbol('x', integer=True), Symbol('n', integer=True)
    assert goal.hypotheses == [And(S.Zero <= x, x < n)]


def test_absolute_value_bars_are_read() -> None:
    goal = _one("example (a : ℚ) (ha : a ≠ 0) : 0 < |a| := by positivity")
    assert goal.goal == (S.Zero < Abs(Symbol('a')))


def test_a_type_ascription_inside_a_proposition_is_dropped() -> None:
    goal = _one("example (x : ℚ) (h : (3 : ℚ) < x) : 0 < x := by linarith")
    assert goal.hypotheses == [S(3) < Symbol('x')]


def test_connectives_bind_looser_than_relations() -> None:
    goal = _one("example (x : ℚ) (h : 0 < x ∧ x < 1) : x < 2 := by linarith")
    x = Symbol('x')
    assert goal.hypotheses == [And(S.Zero < x, x < 1)]


def test_a_goal_without_hypotheses_is_the_conclusion_itself() -> None:
    goal = _one("example (x : ℚ) : 0 ≤ x ^ 2 := by positivity")
    assert goal.statement == ForAll([Symbol('x')], S.Zero <= Symbol('x')**2)


def test_several_examples_are_numbered_in_order() -> None:
    text = ("example (x : ℚ) (h : 0 < x) : 0 ≤ x := by linarith\n"
            "example (y : ℚ) (h : 0 < y) : 0 ≤ y := by linarith\n")
    first, second = goals(text, 'file')
    assert (first.name, second.name) == ('file:1', 'file:2')


def test_a_trivial_hypothesis_gives_a_trivially_true_statement() -> None:
    goal = _one("example (x : ℚ) (h : 0 < x) : 0 < x := by linarith")
    assert goal.statement == ForAll([Symbol('x')], true)


def test_an_example_guarded_as_an_error_is_not_an_oracle() -> None:
    # mathlib records goals its tactics are expected to fail on; the goal
    # itself need not be true
    text = ("/-- error: linarith failed -/\n"
            "#guard_msgs in\n"
            "example (x : ℚ) (h : 0 < x) : x < 0 := by linarith\n")
    assert goals(text, 'sample') == []


def test_an_example_proved_by_fail_if_success_is_not_an_oracle() -> None:
    text = "example (x : ℚ) (h : 0 < x) : x < 0 := by fail_if_success linarith\n"
    assert goals(text, 'sample') == []


def test_an_example_leaning_on_a_local_axiom_is_not_an_oracle() -> None:
    # these files declare false axioms on purpose, to exercise a tactic
    text = ("axiom bad (q : ℚ) : q = 0\n\n"
            "example (a b : ℚ) : a + b ^ 3 = 0 := by linear_combination bad a + b * bad (b * b)\n")
    assert goals(text, 'sample') == []


def test_an_ordinary_example_beside_an_axiom_is_still_read() -> None:
    text = ("axiom bad (q : ℚ) : q = 0\n\n"
            "example (a : ℚ) (h : 0 < a) : 0 ≤ a := by linarith\n")
    assert len(goals(text, 'sample')) == 1


def test_an_example_assuming_its_hypothesis_is_not_an_oracle() -> None:
    # ``test_sorry`` is mathlib's stand-in for ``sorry``: the ``have``
    # is assumed, so the goal is proved only under that assumption
    text = ("example (x : ℚ) : 0 ≤ x := by\n"
            "  have h : 0 ≤ x := test_sorry\n"
            "  linarith\n")
    assert goals(text, 'sample') == []
