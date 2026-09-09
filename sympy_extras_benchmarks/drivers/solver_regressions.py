"""``satisfiable`` and ``resolve`` of ``sympy_extras.assumptions`` on the
arithmetic problems of the cvc5 and Z3 regression suites, against the
answer recorded in each file and, optionally, against Mathematica.

Usage::

    python -m sympy_extras_benchmarks solver_regressions [--sample N]
        [--seed N] [--timeout S] [--max-variables N] [--max-size N]
        [--domain reals|integers|both] [--quantified only|skip|both]
        [--wolfram COMMAND] [--output results.json]

Each problem is decided with ``satisfiable(formula, domain=...)`` when it
is quantifier-free and with ``resolve(formula, domain=...)`` when it is
not (a closed quantified formula resolves to ``True`` or ``False``), and
the verdict is compared with the ``sat``/``unsat`` recorded in the file.
A model returned for a quantifier-free problem is substituted back, so a
``sat`` answer is checked and not merely counted.

The integer problems are the point of this driver: the Meti-Tarski family
read by :mod:`~sympy_extras_benchmarks.drivers.qf_nra` is quantifier-free
and over the reals, while these suites hold ``QF_LIA``, ``QF_NIA``,
``LIA``, ``NIA`` and quantified real problems as well.

With ``--wolfram COMMAND`` every problem is also put to Mathematica (see
:mod:`~sympy_extras_benchmarks.oracles.wolfram`), which gives a second,
independent verdict; a problem where sympy-extras and Mathematica differ
is reported whatever the recorded status says, and a problem where the
two agree *against* the recorded status is reported as ``SUSPECT`` — the
recorded answers of a regression suite are occasionally about a
different question (a solver option, a parse error) than the formula
alone.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
from typing import Optional

from sympy import Basic, S, count_ops, false, true
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, resolve, satisfiable
from sympy_extras._timeout import attempt
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.datasets.solver_regressions import ArithProblem, load, translate
from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, to_wolfram


def evaluate(formula: Boolean, model: dict[Basic, Basic]) -> Optional[bool]:
    """The formula at a model, when it comes out decided."""
    value = formula.xreplace(model)
    if value is true:
        return True
    if value is false:
        return False
    return None


def decide(problem: ArithProblem, timeout: float) -> tuple[Optional[bool], Optional[str]]:
    """``(verdict, note)``: whether the problem has a solution, and what
    went wrong when it has no verdict.

    ``sympy_extras._timeout.attempt`` returns ``None`` both when the time
    is up and when the call raised, so the two are told apart here: the
    call is timed, and a fast ``None`` is reported as ``refused`` (the
    formula is outside what the procedure accepts) rather than as a
    timeout, which would hide a coverage gap behind a performance
    number.
    """
    domain: Set = problem.domain
    if problem.quantified:
        # ``sat`` asks whether some assignment to the free variables makes
        # the formula true, so the free ones are quantified too
        closed = problem.formula
        if problem.variables:
            closed = as_boolean(Exists(problem.variables, problem.formula))
        started = time.time()
        answer = attempt(lambda: resolve(closed, domain=domain), timeout)
        if answer is None:
            return None, _gave_up(time.time() - started, timeout)
        if answer is true:
            return True, None
        if answer is false:
            return False, None
        return None, 'not decided (%s)' % (str(answer)[:40],)
    started = time.time()
    model = attempt(lambda: satisfiable(problem.formula, domain=domain), timeout)
    if model is None:
        return None, _gave_up(time.time() - started, timeout)
    if model is False:
        return False, None
    if isinstance(model, dict):
        point: dict[Basic, Basic] = {}
        for symbol, value in model.items():
            if not isinstance(value, Basic):
                return None, 'the model is not made of expressions'
            point[symbol] = value
        if evaluate(problem.formula, point) is False:
            return None, 'the model does not satisfy the formula'
        return True, None
    return None, 'undecided'


def _gave_up(elapsed: float, timeout: float) -> str:
    """Why a call came back with no answer: it ran out of time, or it
    refused the formula (or reported it undecided) at once."""
    return 'timeout' if elapsed > timeout*0.9 else 'refused/undecided'


def verdict_of(problem: ArithProblem, decided: Optional[bool], note: Optional[str]) -> str:
    """How the verdict compares with the recorded status."""
    if decided is None:
        return note or 'undecided'
    if problem.status == 'unknown':
        return 'sat' if decided else 'unsat'
    expected = problem.status == 'sat'
    if decided == expected:
        return 'ok'
    return 'WRONG (%s for a %s problem)' % ('sat' if decided else 'unsat', problem.status)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=int, default=60)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=20.0)
    parser.add_argument('--max-variables', type=int, default=3)
    parser.add_argument('--max-size', type=int, default=60)
    parser.add_argument('--domain', choices=('reals', 'integers', 'both'), default='both')
    parser.add_argument('--quantified', choices=('only', 'skip', 'both'), default='both')
    parser.add_argument('--wolfram', default='')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    rng = random.Random(args.seed)
    paths = load()
    if not paths:
        print("the regression suites could not be fetched")
        return 1
    rng.shuffle(paths)
    oracle = Wolfram(args.wolfram, args.timeout) if args.wolfram else None
    counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    problems: list[ArithProblem] = []
    for path in paths:
        if len(problems) >= args.sample:
            break
        try:
            problem = translate(path.read_text(errors='replace'), path.stem)
        except (OSError, RecursionError):
            continue
        if problem is None or problem.status == 'unknown':
            continue
        if len(problem.variables) > args.max_variables:
            continue
        if int(count_ops(problem.formula)) > args.max_size:
            continue
        if args.domain == 'reals' and problem.domain is S.Integers:
            continue
        if args.domain == 'integers' and problem.domain is not S.Integers:
            continue
        if args.quantified == 'only' and not problem.quantified:
            continue
        if args.quantified == 'skip' and problem.quantified:
            continue
        problems.append(problem)
    # sympy-extras first, printing as it goes, so that a slow oracle does
    # not hide the progress
    decisions: list[tuple[Optional[bool], Optional[str], str, float]] = []
    for problem in problems:
        started = time.time()
        decided, note = decide(problem, args.timeout)
        verdict = verdict_of(problem, decided, note)
        elapsed = time.time() - started
        decisions.append((decided, note, verdict, elapsed))
        print("%-34s %-8s %-9s %s%-6s ops=%-3d %-44s %5.1fs" % (
            problem.name[:34], problem.logic[:8],
            'integers' if problem.domain is S.Integers else 'reals',
            'Q' if problem.quantified else ' ', problem.status,
            int(count_ops(problem.formula)), verdict, elapsed), flush=True)
    # then the second oracle, on the problems it can be asked about
    wolfram_verdicts: list[Optional[bool]] = [None]*len(problems)
    if oracle is not None:
        askable: list[int] = []
        formulas: list[Boolean] = []
        domains: list[Set] = []
        for index, problem in enumerate(problems):
            try:
                to_wolfram(problem.formula)
            except WolframError:
                continue
            askable.append(index)
            formulas.append(as_boolean(problem.formula))
            domains.append(problem.domain)
        print("\nasking Mathematica about %d of the %d problems..." % (len(askable), len(problems)),
              flush=True)
        try:
            answers = oracle.satisfiable(formulas, domains)
        except WolframError as error:
            print("the oracle failed: %s" % error)
            answers = [None]*len(formulas)
        for index, answer in zip(askable, answers):
            wolfram_verdicts[index] = answer
    for problem, (decided, note, verdict, elapsed), oracle_verdict in zip(problems, decisions,
                                                                          wolfram_verdicts):
        against_oracle = ''
        if oracle_verdict is not None and decided is not None:
            if decided != oracle_verdict:
                against_oracle = 'DIFFER (mathematica says %s)' % ('sat' if oracle_verdict else 'unsat')
            elif 'WRONG' in verdict:
                verdict = 'SUSPECT (mathematica agrees with sympy-extras against the file)'
                against_oracle = 'agrees'
            else:
                against_oracle = 'agrees'
        elif oracle_verdict is not None:
            against_oracle = 'mathematica says %s' % ('sat' if oracle_verdict else 'unsat')
        key = verdict.split(' ')[0]
        counts[key] = counts.get(key, 0) + 1
        if against_oracle.startswith('DIFFER'):
            counts['DIFFER'] = counts.get('DIFFER', 0) + 1
            print("%-34s %-44s %s" % (problem.name[:34], verdict, against_oracle), flush=True)
        elif verdict.startswith('SUSPECT'):
            print("%-34s %s" % (problem.name[:34], verdict), flush=True)
        records.append({'name': problem.name, 'logic': problem.logic, 'status': problem.status,
                        'domain': 'integers' if problem.domain is S.Integers else 'reals',
                        'quantified': problem.quantified, 'variables': len(problem.variables),
                        'ops': int(count_ops(problem.formula)), 'verdict': verdict,
                        'oracle': against_oracle, 'time': round(elapsed, 2)})
    print()
    print(dict(sorted(counts.items())))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'counts': counts, 'results': records}, indent=1))
    return 1 if any(k.startswith('WRONG') or k == 'DIFFER' for k in counts) else 0


if __name__ == '__main__':
    sys.exit(main())
