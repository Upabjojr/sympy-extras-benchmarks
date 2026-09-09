"""Tests of the Rocq micromega parser on samples written here in Rocq
syntax (nothing is copied from the standard library)."""
from __future__ import annotations

from sympy import And, Eq, Implies, Ne, Or, S, Symbol

from sympy_extras.assumptions import Exists, ForAll

from sympy_extras_benchmarks.datasets.coq_micromega import CoqGoal, goals


def _file(statement: str, header: str = 'Open Scope Z_scope.',
          proof: str = 'Proof. lia. Qed.') -> str:
    return "%s\n%s\n%s\n" % (header, statement, proof)


def _one(statement: str, **kwargs: str) -> CoqGoal:
    found = goals(_file(statement, **kwargs), 'sample')
    assert len(found) == 1
    return found[0]


def test_an_integer_lemma_becomes_a_universal_implication() -> None:
    goal = _one("Lemma mul_pos : forall (x y : Z), x > 0 -> y > 0 -> x * y > 0.")
    x, y = Symbol('x', integer=True), Symbol('y', integer=True)
    assert goal.name == 'sample:mul_pos'
    assert goal.scope == 'Z'
    assert goal.domain is S.Integers
    assert goal.variables == [x, y]
    assert goal.expected is True
    assert goal.statement == ForAll([x, y], Implies(And(x > 0, y > 0), x*y > 0))


def test_a_false_conclusion_becomes_an_existential_expected_false() -> None:
    goal = _one("Goal forall x : Z, x > 1 -> x < 0 -> False.")
    x = Symbol('x', integer=True)
    assert goal.expected is False
    assert goal.statement == Exists([x], And(x > 1, x < 0))


def test_an_unnamed_goal_is_numbered() -> None:
    goal = _one("Goal forall x : Z, x * x >= 0.")
    assert goal.name == 'sample:1'


def test_the_scope_gives_the_domain() -> None:
    goal = _one("Lemma l : forall x : R, x * x >= 0.",
                header='Open Scope R_scope.', proof='Proof. nra. Qed.')
    assert goal.scope == 'R'
    assert goal.domain is S.Reals
    assert not goal.variables[0].is_integer


def test_the_rationals_are_decided_over_the_reals() -> None:
    goal = _one("Lemma l : forall x : Q, x * x >= 0.",
                header='Open Scope Q_scope.', proof='Proof. nra. Qed.')
    assert goal.scope == 'Q'
    assert goal.domain is S.Reals


def test_bare_binders_take_the_scope_as_their_type() -> None:
    goal = _one("Lemma l : forall x y, x >= 0 -> y >= 0 -> x + y >= 0.")
    assert [s.name for s in goal.variables] == ['x', 'y']
    assert all(s.is_integer for s in goal.variables)


def test_a_named_hypothesis_binder_is_a_premise() -> None:
    goal = _one("Lemma l : forall (x : Z) (H : 0 <= x), 0 <= 2 * x.")
    x = Symbol('x', integer=True)
    assert goal.hypotheses == [S.Zero <= x]
    assert goal.statement == ForAll([x], Implies(And(S.Zero <= x), S.Zero <= 2*x))


def test_rocq_connectives_are_read() -> None:
    goal = _one("Lemma l : forall x y : Z, 0 = x + y /\\ 0 = x - y -> 0 = x \\/ x <> 1.")
    x, y = Symbol('x', integer=True), Symbol('y', integer=True)
    assert goal.hypotheses == [And(Eq(0, x + y), Eq(0, x - y))]
    assert goal.goal == Or(Eq(0, x), Ne(x, 1))


def test_an_aborted_statement_is_not_an_oracle() -> None:
    # the suite records goals the tactic gives up on; they say nothing
    # about whether the goal is true
    assert goals(_file("Goal forall x : Z, x > 0.", proof='Proof. Fail lia. Abort.'),
                 'sample') == []


def test_an_admitted_statement_is_not_an_oracle() -> None:
    assert goals(_file("Goal forall x : Z, x > 0.", proof='Proof. Admitted.'), 'sample') == []


def test_a_failed_tactic_inside_a_finished_proof_is_fine() -> None:
    # ``Fail lia`` only records that lia does not close it; nia does, and
    # ``Qed`` accepts the proof, so the goal is true
    goal = _one("Lemma l : forall x : Z, x * x >= 0.", proof='Proof. Fail lia. nia. Qed.')
    assert goal.expected is True


def test_the_nat_scope_is_refused() -> None:
    # subtraction on nat is truncated
    assert goals(_file("Lemma l : forall x : nat, x - 1 <= x.",
                       header='Open Scope nat_scope.'), 'sample') == []


def test_a_machine_integer_scope_is_refused() -> None:
    assert goals(_file("Lemma l : forall x : int, x + 1 > x.",
                       header='Open Scope uint63_scope.'), 'sample') == []


def test_two_domains_in_one_statement_are_refused() -> None:
    assert goals(_file("Lemma l : forall (x : R) (y : nat), x >= 0 -> x >= 0.",
                       header='Open Scope R_scope.', proof='Proof. lra. Qed.'), 'sample') == []


def test_a_natural_binder_beside_an_integer_one_gains_its_nonnegativity() -> None:
    # nat and Z are both decided over ℤ, so they may be mixed; the ℕ
    # variable carries ``0 <= y`` and the goal must not subtract
    goal = _one("Lemma l : forall (x : Z) (y : nat), x >= y -> x >= 0.")
    assert (S.Zero <= Symbol('y', integer=True)) in goal.hypotheses


def test_subtraction_beside_a_natural_binder_is_refused() -> None:
    assert goals(_file("Lemma l : forall (x : Z) (y : nat), x >= y -> x - y >= 0."),
                 'sample') == []


def test_a_scope_annotation_is_dropped() -> None:
    goal = _one("Lemma l : forall z : Z, (0 <= z)%Z -> (0 <= 2 * z)%Z.")
    z = Symbol('z', integer=True)
    assert goal.hypotheses == [S.Zero <= z]


def test_a_chain_of_relations_is_a_conjunction() -> None:
    goal = _one("Lemma l : forall (a n : Z), 0 <= a < n -> 0 <= a.")
    a, n = Symbol('a', integer=True), Symbol('n', integer=True)
    assert goal.hypotheses == [And(S.Zero <= a, a < n)]


def test_an_undeclared_name_is_refused() -> None:
    assert goals(_file("Lemma l : forall x : Z, Z.abs x >= 0."), 'sample') == []


def test_a_ground_statement_without_binders_is_refused() -> None:
    assert goals(_file("Lemma l : 2 + 2 = 4."), 'sample') == []


def test_division_over_the_integers_is_refused() -> None:
    assert goals(_file("Lemma l : forall x : Z, x >= 0 -> x / 2 >= 0."), 'sample') == []


def test_a_variable_denominator_over_the_reals_is_refused() -> None:
    # Rocq defines ``/ 0`` as ``0``
    assert goals(_file("Lemma l : forall x y : R, y > 0 -> x / y >= 0.",
                       header='Open Scope R_scope.', proof='Proof. nra. Qed.'), 'sample') == []


def test_a_high_power_is_kept() -> None:
    goal = _one("Lemma l : forall x : Z, 1 <= x -> 0 <= x ^ 37.")
    assert goal.goal == (S.Zero <= Symbol('x', integer=True)**37)


def test_several_statements_are_read_in_order() -> None:
    text = ("Open Scope Z_scope.\n"
            "Lemma a : forall x : Z, x >= 0 -> x >= 0.\nProof. lia. Qed.\n"
            "Lemma b : forall y : Z, y >= 1 -> y >= 0.\nProof. lia. Qed.\n")
    first, second = goals(text, 'file')
    assert (first.name, second.name) == ('file:a', 'file:b')


def test_a_file_opening_no_arithmetic_scope_yields_nothing() -> None:
    assert goals("Lemma l : forall x : Z, x >= 0 -> x >= 0.\nProof. lia. Qed.\n", 'sample') == []
