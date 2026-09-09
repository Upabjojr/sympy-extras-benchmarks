"""``solve`` of ``sympy_extras.assumptions`` on the systems of polynomial
equations of Maxima's ``algsys`` regression file.

Usage::

    python -m sympy_extras_benchmarks polynomial_solving [--sample N]
        [--timeout S] [--max-unknowns N] [--wolfram COMMAND]
        [--output results.json]

Two checks, of very different strength:

* every solution returned is **substituted back**. A tuple that does not
  satisfy the system is a wrong answer with no room for interpretation,
  and the driver exits 1 on it.
* the **number** of solutions is compared with Mathematica's ``Solve`` and
  with the count Maxima records. A disagreement is reported but not
  counted as a wrong answer: the three systems count differently on
  purpose — multiplicities, solutions at infinity, and the recorded
  answers are floating point in places and wrong in at least one (the
  file says so).

A system whose answer carries a free parameter describes infinitely many
solutions, so only the substitution check applies to it.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from typing import Optional

from sympy import S, Symbol, Tuple, simplify
from sympy.core.basic import Basic
from sympy.sets.sets import FiniteSet

from sympy_extras.assumptions import solve
from sympy_extras._timeout import attempt

from sympy_extras_benchmarks.datasets.polynomial_solving import PolynomialSystem, load
from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, to_wolfram

__all__ = ['main', 'satisfies', 'solutions_of']


def solutions_of(answer: Basic, system: PolynomialSystem) -> Optional[list[dict[Symbol, Basic]]]:
    """The answer as a list of assignments, or ``None`` when it is not a
    finite list of tuples (a conditional or an image set, say)."""
    if not isinstance(answer, FiniteSet):
        return None
    found: list[dict[Symbol, Basic]] = []
    for element in answer.args:
        values = element.args if isinstance(element, Tuple) else (element,)
        if len(values) != len(system.variables):
            return None
        found.append(dict(zip(system.variables, values)))
    return found


def satisfies(system: PolynomialSystem, point: dict[Symbol, Basic],
              timeout: float = 20.0) -> Optional[bool]:
    """Whether a solution satisfies every equation; ``None`` when
    simplification could not decide it.

    Every simplification is bounded: substituting a root of a quartic into
    a polynomial can produce an expression ``simplify`` will work on for
    minutes, and an unbounded check here would be reported as the solver
    being slow.
    """
    decided = True
    for equation in system.equations:
        residue = equation.xreplace(point)
        value = attempt(lambda: simplify(residue), timeout)
        if value is None:
            # fall back to the numeric test, which is cheap and decisive
            numeric = attempt(lambda: complex(residue.evalf(40)), timeout)
            if numeric is None:
                decided = False
            elif abs(numeric) > 1e-25:
                return False
            continue
        if value == 0:
            continue
        if value.is_number and value.is_zero is False:
            return False
        # a residue that is not visibly zero and not visibly nonzero: it
        # may be a form simplify cannot close, so the point is undecided
        # rather than wrong
        residue = attempt(lambda: simplify(value.rewrite('exp').expand()), 10)
        if residue is not None and residue == 0:
            continue
        if value.is_number:
            numeric = attempt(lambda: complex(value.evalf(40)), 10)
            if numeric is not None and abs(numeric) < 1e-25:
                continue
            if numeric is not None:
                return False
        decided = False
    return True if decided else None


def _report(system: PolynomialSystem, answer: Optional[Basic], elapsed: float,
            check_timeout: float = 20.0) -> tuple[str, Optional[int], list[str]]:
    """``(verdict, number of solutions, the ones that fail substitution)``."""
    if answer is None:
        return ('timeout' if elapsed > 25.0 else 'refused/undecided'), None, []
    points = solutions_of(answer, system)
    if points is None:
        return 'not a finite list (%s)' % type(answer).__name__, None, []
    bad: list[str] = []
    undecided = 0
    for point in points:
        verdict = satisfies(system, point, check_timeout)
        if verdict is False:
            bad.append(", ".join("%s=%s" % (k, v) for k, v in point.items())[:90])
        elif verdict is None:
            undecided += 1
    if bad:
        return 'WRONG (%d of %d do not satisfy the system)' % (len(bad), len(points)), len(points), bad
    if undecided:
        return 'ok (%d of %d unverified)' % (undecided, len(points)), len(points), []
    return 'ok', len(points), []


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=int, default=60)
    parser.add_argument('--timeout', type=float, default=30.0)
    parser.add_argument('--max-unknowns', type=int, default=6)
    parser.add_argument('--check-timeout', type=float, default=20.0,
                        help="time limit for verifying one solution by substitution")
    parser.add_argument('--wolfram', default='')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    systems = [s for s in load() if len(s.variables) <= args.max_unknowns][:args.sample]
    if not systems:
        print("the algsys regression file could not be fetched")
        return 1
    oracle = Wolfram(args.wolfram, args.timeout) if args.wolfram else None
    counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    results: list[tuple[str, Optional[int], list[str]]] = []
    for system in systems:
        started = time.time()
        answer = attempt(lambda: solve(system.equations, system.variables,
                                       domain=S.Complexes), args.timeout)
        verdict, found, bad = _report(system, answer, time.time() - started,
                                      args.check_timeout)
        results.append((verdict, found, bad))
        print("%-22s eqs=%-2d vars=%-2d recorded=%-5s found=%-5s %-44s %5.1fs" % (
            system.name, len(system.equations), len(system.variables),
            'param' if system.parametric else system.recorded,
            '-' if found is None else found, verdict, time.time() - started), flush=True)
        for line in bad:
            print("      does not satisfy the system: %s" % line, flush=True)
    oracle_counts: list[Optional[int]] = [None]*len(systems)
    if oracle is not None:
        askable, expressions = [], []
        for index, system in enumerate(systems):
            try:
                body = ", ".join("%s == 0" % to_wolfram(e) for e in system.equations)
                variables = ", ".join(to_wolfram(v) for v in system.variables)
            except WolframError:
                continue
            askable.append(index)
            expressions.append("Length[Solve[{%s}, {%s}]]" % (body, variables))
        print("\nasking Mathematica about %d of the %d systems..." % (len(askable), len(systems)),
              flush=True)
        try:
            answers = oracle.evaluate(expressions)
        except WolframError as error:
            print("the oracle failed: %s" % error)
            answers = ['$Aborted']*len(expressions)
        for index, value in zip(askable, answers):
            oracle_counts[index] = int(value) if value.lstrip('-').isdigit() else None
    print()
    for system, (verdict, found, bad), expected in zip(systems, results, oracle_counts):
        note = ''
        if expected is not None and found is not None and not system.parametric:
            note = ('agrees' if expected == found
                    else 'COUNT (mathematica finds %d, sympy-extras %d)' % (expected, found))
        key = verdict.split(' ')[0]
        counts[key] = counts.get(key, 0) + 1
        if note.startswith('COUNT'):
            counts['COUNT'] = counts.get('COUNT', 0) + 1
            print("%-22s %-30s %s" % (system.name, verdict, note), flush=True)
        records.append({'name': system.name, 'equations': [str(e) for e in system.equations],
                        'variables': [str(v) for v in system.variables],
                        'recorded': system.recorded, 'parametric': system.parametric,
                        'found': found, 'verdict': verdict, 'oracle': note,
                        'unsatisfied': bad})
    print()
    print(dict(sorted(counts.items())))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'counts': counts, 'results': records},
                                                        indent=1))
    return 1 if any(k.startswith('WRONG') for k in counts) else 0


if __name__ == '__main__':
    sys.exit(main())
