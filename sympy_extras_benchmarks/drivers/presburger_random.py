"""``resolve`` over the integers on random linear formulas, against brute
force over a box.

Usage::

    python -m sympy_extras_benchmarks presburger_random [--cases N]
        [--seed N] [--timeout S] [--box N] [--variables N]
        [--output results.json]

This is the driver that found sympy-extras#51, and the one to run against
a fix for it. Presburger arithmetic is decidable, so a random formula has
a knowable truth value and no oracle is needed: three checks, each
decisive on its own, disagree with ``resolve`` or they do not.

Brute force over a box
    A point of ``[-box, box]^n`` where the matrix holds proves
    ``Exists``; one where it fails disproves ``ForAll``. Both directions
    are one-sided — the box cannot show the opposite — so a disagreement
    is always the procedure's, never the box's.

Duality
    ``resolve(ForAll(v, F))`` must be the negation of
    ``resolve(Exists(v, ~F))``. Nothing outside the package is involved,
    so a violation is an internal contradiction.

The real relaxation
    ℤ ⊆ ℝ, so a universal statement true over ℝ is true over ℤ. A
    ``ForAll`` that ``resolve`` calls false over ℤ while calling it true
    over ℝ, with no counterexample in the box, is reported as suspect.

Every disagreement is printed with the formula that produced it, and the
driver exits 1 if there was one.
"""
from __future__ import annotations

import argparse
import itertools
import json
import pathlib
import random
import sys
import time
from typing import Optional

from sympy import And, Eq, Integer, Ne, Or, S, Symbol, false, true
from sympy.logic.boolalg import Boolean

from sympy_extras.assumptions import Exists, ForAll, resolve
from sympy_extras._timeout import attempt
from sympy_extras._typing import as_boolean

__all__ = ['brute_force', 'main', 'random_formula']

#: the variables a formula may use
NAMES = ('x', 'y', 'z')


def random_formula(rng: random.Random, variables: list[Symbol]) -> Boolean:
    """A disjunction of conjunctions of linear relations.

    Equalities are weighted: they are what the elimination handles worst,
    and the reported defects all involve at least two of them.
    """
    def atom() -> Boolean:
        left = sum((rng.randint(-3, 3)*v for v in variables), S.Zero) + rng.randint(-4, 4)
        kind = rng.choice(['eq', 'eq', 'eq', 'ne', 'le', 'lt'])
        if kind == 'eq':
            return as_boolean(Eq(left, 0))
        if kind == 'ne':
            return as_boolean(Ne(left, 0))
        return as_boolean(left <= 0 if kind == 'le' else left < 0)

    disjuncts = [as_boolean(And(*[atom() for _ in range(rng.randint(1, 3))]))
                 for _ in range(rng.randint(1, 3))]
    return as_boolean(Or(*disjuncts))


def brute_force(matrix: Boolean, variables: list[Symbol], box: int) -> tuple[bool, bool]:
    """``(a point satisfies it, a point falsifies it)`` inside the box."""
    witness = counterexample = False
    for point in itertools.product(range(-box, box + 1), repeat=len(variables)):
        value = matrix.xreplace(dict(zip(variables, (Integer(c) for c in point))))
        if value is true:
            witness = True
        elif value is false:
            counterexample = True
        if witness and counterexample:
            break
    return witness, counterexample


def _decide(formula: Boolean, timeout: float, integers: bool = True) -> Optional[bool]:
    domain = S.Integers if integers else S.Reals
    answer = attempt(lambda: resolve(formula, domain=domain), timeout)
    if answer is true:
        return True
    if answer is false:
        return False
    return None


def _disagreement(matrix: Boolean, variables: list[Symbol], box: int,
                  timeout: float) -> Optional[tuple[str, dict[str, object]]]:
    """Why ``resolve`` is wrong about this formula, or ``None``."""
    from sympy import Not
    witness, counterexample = brute_force(matrix, variables, box)
    universal = _decide(as_boolean(ForAll(variables, matrix)), timeout)
    existential = _decide(as_boolean(Exists(variables, matrix)), timeout)
    negated = _decide(as_boolean(Exists(variables, Not(matrix))), timeout)
    facts: dict[str, object] = {'forall': universal, 'exists': existential,
                                'exists_not': negated}
    if existential is False and witness:
        return 'exists=False but the box holds a witness', facts
    if universal is True and counterexample:
        return 'forall=True but the box holds a counterexample', facts
    if universal is not None and negated is not None and universal == negated:
        return 'forall and exists-not agree; they must be opposite', facts
    if universal is False and not counterexample:
        if _decide(as_boolean(ForAll(variables, matrix)), timeout, integers=False) is True:
            return 'forall=False over Z while true over R, which transfers', facts
    return None


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=int, default=400)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=8.0)
    parser.add_argument('--box', type=int, default=6)
    parser.add_argument('--variables', type=int, default=3,
                        help="the most variables a formula may use (1 to 3)")
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    rng = random.Random(args.seed)
    pool = [Symbol(n, integer=True) for n in NAMES[:max(1, min(args.variables, 3))]]
    found: list[dict[str, object]] = []
    checked = 0
    started = time.time()
    for case in range(args.cases):
        variables = pool[:rng.randint(1, len(pool))]
        matrix = random_formula(rng, variables)
        if matrix in (true, false):
            continue
        checked += 1
        outcome = _disagreement(matrix, variables, args.box, args.timeout)
        if outcome is None:
            continue
        reason, facts = outcome
        found.append({'case': case, 'reason': reason, 'formula': str(matrix),
                      'variables': [str(v) for v in variables], **facts})
        print("[%d] %s\n     %s\n     forall=%s exists=%s exists-not=%s"
              % (case, reason, matrix, facts['forall'], facts['exists'],
                 facts['exists_not']), flush=True)
    print()
    print("checked %d formulas in %.0fs; %d disagreements"
          % (checked, time.time() - started, len(found)))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps(
            {'checked': checked, 'disagreements': found}, indent=1))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
