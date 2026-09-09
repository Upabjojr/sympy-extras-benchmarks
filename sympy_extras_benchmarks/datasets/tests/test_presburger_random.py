"""Tests of the random Presburger driver: the generator and the brute
force oracle, on formulas written here."""
from __future__ import annotations

import random

from sympy import And, Eq, Ne, Or, Poly, Symbol
from sympy.core.expr import Expr

from sympy_extras_benchmarks.drivers.presburger_random import (
    brute_force, main, random_formula)

x, y = Symbol('x', integer=True), Symbol('y', integer=True)


def test_brute_force_finds_a_witness() -> None:
    # (2, 0) satisfies it, and plenty of points do not
    matrix = And(Eq(y, 0), Eq(x - 3*y - 2, 0))
    witness, counterexample = brute_force(matrix, [x, y], 6)
    assert witness is True
    assert counterexample is True


def test_brute_force_reports_no_witness_when_there_is_none() -> None:
    # 2*x = 1 has no integer solution
    witness, counterexample = brute_force(Eq(2*x - 1, 0), [x], 6)
    assert witness is False
    assert counterexample is True


def test_brute_force_reports_no_counterexample_for_a_tautology() -> None:
    witness, counterexample = brute_force(Or(Eq(x, x), Ne(x, x)), [x], 4)
    assert witness is True
    assert counterexample is False


def test_brute_force_is_confined_to_the_box() -> None:
    # the only witness is at x = 20, outside a box of 6
    assert brute_force(Eq(x - 20, 0), [x], 6)[0] is False
    assert brute_force(Eq(x - 20, 0), [x], 25)[0] is True


def test_the_generator_only_makes_linear_relations() -> None:
    rng = random.Random(0)
    for _ in range(50):
        formula = random_formula(rng, [x, y])
        for atom in formula.atoms(Eq, Ne):
            for side in atom.args:
                assert isinstance(side, Expr)
                assert Poly(side, x, y).total_degree() <= 1


def test_the_generator_is_reproducible() -> None:
    first = [str(random_formula(random.Random(4), [x, y])) for _ in range(3)]
    second = [str(random_formula(random.Random(4), [x, y])) for _ in range(3)]
    assert first == second


def test_the_driver_runs_and_reports() -> None:
    # a handful of cases: the point is that it completes and returns a
    # status, not which formulas it happens to draw
    assert main(['--cases', '3', '--seed', '11', '--timeout', '5']) in (0, 1)
