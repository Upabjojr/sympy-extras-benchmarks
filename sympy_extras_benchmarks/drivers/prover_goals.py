"""``resolve`` on a collection of goals taken from a proof assistant's
test suite, against the assistant's verdict and, optionally, against
Mathematica.

Both the mathlib4 and the Rocq/Coq drivers are this run with a different
dataset: a goal of either is a closed formula whose truth value the
assistant has a machine-checked proof of, so ``resolve`` must return it.

The goals stated over the rationals are decided over the reals, which is
where ``resolve`` and ``Resolve`` both work. That is sound in the
direction these goals are used — they are the ones ``linarith``,
``positivity`` and ``micromega`` close, and their reasoning holds in
every ordered field — but not in general, so a goal where sympy-extras
disagrees with the assistant while Mathematica agrees with sympy-extras
is reported as ``SUSPECT`` rather than as a wrong answer: over ℝ it may
genuinely be the other way. Mathematica is the arbiter, and only a
disagreement between sympy-extras and Mathematica is counted as a
finding.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import time
from typing import Optional, Protocol, Sequence

from sympy import S, Symbol, count_ops, false, true
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import resolve
from sympy_extras._timeout import attempt
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, to_wolfram

__all__ = ['Goal', 'add_arguments', 'decide', 'run', 'verdict_of']


class Goal(Protocol):
    """What this driver needs of a goal, whichever suite it came from."""

    name: str

    @property
    def domain(self) -> Set:
        ...

    @property
    def variables(self) -> list[Symbol]:
        ...

    @property
    def statement(self) -> Boolean:
        ...

    @property
    def expected(self) -> bool:
        ...


def add_arguments(parser: argparse.ArgumentParser) -> None:
    """The options every prover-goal driver takes."""
    parser.add_argument('--sample', type=int, default=200)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=30.0)
    parser.add_argument('--max-variables', type=int, default=8)
    parser.add_argument('--max-size', type=int, default=200)
    parser.add_argument('--domain', choices=('reals', 'integers', 'both'), default='both')
    parser.add_argument('--non-trivial', action='store_true',
                        help="skip the goals whose statement is already True or False")
    parser.add_argument('--wolfram', default='')
    parser.add_argument('--output', default='')


def decide(goal: Goal, timeout: float) -> tuple[Optional[bool], Optional[str]]:
    """``(truth value, note)``: what ``resolve`` makes of the goal, and
    what went wrong when it makes nothing of it.

    ``sympy_extras._timeout.attempt`` returns ``None`` both when the time
    is up and when the call raised, so the call is timed and a fast
    ``None`` is reported as ``refused`` — a coverage gap, not a
    performance number.
    """
    domain: Set = goal.domain
    statement = goal.statement
    started = time.time()
    answer = attempt(lambda: resolve(statement, domain=domain), timeout)
    elapsed = time.time() - started
    if answer is None:
        return None, 'timeout' if elapsed > timeout*0.9 else 'refused/undecided'
    if answer is true:
        return True, None
    if answer is false:
        return False, None
    return None, 'not decided (%s)' % (str(answer)[:40],)


def verdict_of(goal: Goal, decided: Optional[bool], note: Optional[str]) -> str:
    """How the truth value compares with the assistant's."""
    if decided is None:
        return note or 'undecided'
    if decided == goal.expected:
        return 'ok'
    return 'WRONG (%s for a %s goal)' % (decided, 'valid' if goal.expected else 'unsatisfiable')


def _select(goals: Sequence[Goal], args: argparse.Namespace) -> list[Goal]:
    chosen: list[Goal] = []
    for goal in goals:
        if len(chosen) >= args.sample:
            break
        if len(goal.variables) > args.max_variables:
            continue
        if int(count_ops(goal.statement)) > args.max_size:
            continue
        if args.domain == 'reals' and goal.domain is S.Integers:
            continue
        if args.domain == 'integers' and goal.domain is not S.Integers:
            continue
        if args.non_trivial and goal.statement.atoms(Boolean) <= {true, false}:
            continue
        chosen.append(goal)
    return chosen


def run(goals: Sequence[Goal], args: argparse.Namespace) -> int:
    """Decide the goals, print a line each, and return 1 on a finding."""
    if not goals:
        print("the test suite could not be fetched")
        return 1
    shuffled = list(goals)
    random.Random(args.seed).shuffle(shuffled)
    chosen = _select(shuffled, args)
    oracle = Wolfram(args.wolfram, args.timeout) if args.wolfram else None
    counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    # sympy-extras first, printing as it goes, so a slow oracle does not
    # hide the progress
    decisions: list[tuple[Optional[bool], str, float]] = []
    for goal in chosen:
        started = time.time()
        decided, note = decide(goal, args.timeout)
        verdict = verdict_of(goal, decided, note)
        elapsed = time.time() - started
        decisions.append((decided, verdict, elapsed))
        print("%-28s %-8s %-14s vars=%-2d ops=%-4d %-40s %5.1fs" % (
            goal.name[:28], 'integers' if goal.domain is S.Integers else 'reals',
            'valid' if goal.expected else 'unsatisfiable', len(goal.variables),
            int(count_ops(goal.statement)), verdict, elapsed), flush=True)
    oracle_verdicts: list[Optional[bool]] = [None]*len(chosen)
    if oracle is not None:
        askable: list[int] = []
        formulas: list[Boolean] = []
        domains: list[Set] = []
        for index, goal in enumerate(chosen):
            try:
                to_wolfram(goal.statement)
            except WolframError:
                continue
            askable.append(index)
            formulas.append(as_boolean(goal.statement))
            domains.append(goal.domain)
        print("\nasking Mathematica about %d of the %d goals..." % (len(askable), len(chosen)),
              flush=True)
        try:
            answers = oracle.resolve(formulas, domains)
        except WolframError as error:
            print("the oracle failed: %s" % error)
            answers = [None]*len(formulas)
        for index, answer in zip(askable, answers):
            oracle_verdicts[index] = answer
    print()
    for goal, (decided, verdict, elapsed), oracle_verdict in zip(chosen, decisions,
                                                                 oracle_verdicts):
        against_oracle = ''
        if oracle_verdict is not None and decided is not None:
            if decided != oracle_verdict:
                against_oracle = 'DIFFER (mathematica says %s)' % oracle_verdict
            elif verdict.startswith('WRONG'):
                verdict = 'SUSPECT (mathematica agrees with sympy-extras against the suite)'
                against_oracle = 'agrees'
            else:
                against_oracle = 'agrees'
        elif oracle_verdict is not None:
            against_oracle = 'mathematica says %s' % oracle_verdict
        key = verdict.split(' ')[0]
        counts[key] = counts.get(key, 0) + 1
        if against_oracle.startswith('DIFFER'):
            counts['DIFFER'] = counts.get('DIFFER', 0) + 1
            print("%-28s %-40s %s" % (goal.name[:28], verdict, against_oracle), flush=True)
        elif verdict.startswith('SUSPECT'):
            print("%-28s %s" % (goal.name[:28], verdict), flush=True)
        records.append({'name': goal.name,
                        'domain': 'integers' if goal.domain is S.Integers else 'reals',
                        'expected': goal.expected, 'variables': len(goal.variables),
                        'ops': int(count_ops(goal.statement)), 'statement': str(goal.statement),
                        'verdict': verdict, 'oracle': against_oracle, 'time': round(elapsed, 2)})
    print()
    print(dict(sorted(counts.items())))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'counts': counts, 'results': records},
                                                        indent=1))
    return 1 if any(k.startswith('WRONG') or k == 'DIFFER' for k in counts) else 0
