"""``satisfiable``, ``simplify`` and ``refine`` of
``sympy_extras.assumptions`` on every problem of SMT-LIB ``QF_NRA``, and
``resolve`` on every problem of ``NRA``, in parallel processes.

Usage::

    python -m sympy_extras_benchmarks smtlib_release --logic QF_NRA
        [--families meti-tarski,kissing] [--workers N] [--timeout S]
        [--rewrite-timeout S] [--memory MB] [--output results/qf_nra.jsonl]

For a ``QF_NRA`` problem, ``satisfiable(formula, domain=S.Reals)`` is
compared with the recorded ``:status``; a model is checked by exact
evaluation of the formula at it. Unless ``satisfiable`` ran out of time,
``simplify`` and ``refine`` of the formula over the reals follow: they
must give ``False`` only for an unsatisfiable problem and ``True`` only
for a satisfiable one, and a formula they return must agree with the
input at random rational points. For an ``NRA`` problem, ``resolve`` of
the closed formula (the free variables quantified existentially) must
give the recorded status. A problem recorded ``unknown`` gets the verdict
``sat`` or ``unsat``, to be checked with another oracle.

The problems run smallest file first. Every call has a time limit, and
the outcomes are kept apart: ``timeout``, ``unsupported``
(``NotImplementedError``), ``refused`` (``ValueError`` or ``TypeError``,
which sympy-extras raises for input outside what it accepts -- and which
a bug can raise too, so they are listed) and ``crash`` (anything else,
with the traceback). The results go to a JSON Lines file, one line per
problem, and a run resumes from it.
"""
from __future__ import annotations

import argparse
import pathlib
import random
import re
import sys
import time
import traceback
from typing import Callable, Optional, Sequence, TypeVar

from sympy import S, Rational, true, false
from sympy.core.basic import Basic
from sympy.core.relational import Relational
from sympy.logic.boolalg import Boolean

from sympy_extras.assumptions import Exists, satisfiable, simplify, refine, resolve
from sympy_extras._timeout import TimeLimitExceeded, time_limit
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.datasets import smtlib, solver_regressions, tarski_tests
from sympy_extras_benchmarks.datasets.smtlib_release import family, load
from sympy_extras_benchmarks.runner import JSON, Result, Task, run

T = TypeVar('T')

#: the time limit on reading one file
PARSE_TIMEOUT = 60.0


class Outcome:
    """How a call ended: ``kind`` is ``'value'``, ``'timeout'``,
    ``'unsupported'``, ``'refused'``, ``'memory'`` or ``'crash'``."""

    def __init__(self, kind: str, value: object = None, detail: str = '') -> None:
        self.kind = kind
        self.value = value
        self.detail = detail

    def label(self) -> str:
        return self.kind if not self.detail else '%s: %s' % (self.kind, self.detail)


def call(f: Callable[[], T], seconds: float) -> Outcome:
    """``f()`` under a time limit, with the way it ended."""
    try:
        with time_limit(seconds):
            return Outcome('value', f())
    except TimeLimitExceeded:
        return Outcome('timeout')
    except NotImplementedError as error:
        return Outcome('unsupported', detail=str(error)[:200])
    except (ValueError, TypeError) as error:
        return Outcome('refused', detail='%s: %s' % (type(error).__name__, str(error)[:200]))
    except MemoryError:
        return Outcome('memory')
    except RecursionError:
        return Outcome('crash', detail='RecursionError')
    except Exception as error:
        tail = traceback.format_exc().strip().splitlines()[-6:]
        return Outcome('crash', detail='%s: %s | %s' % (type(error).__name__, str(error)[:200], ' / '.join(tail)))


def evaluate(formula: Boolean, point: dict[Basic, Basic]) -> Optional[bool]:
    """The formula at a point, when it comes out decided."""
    try:
        value = formula.xreplace(point)
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    if value is true:
        return True
    if value is false:
        return False
    return None


def check_model(formula: Boolean, variables: Sequence[Basic], model: object) -> str:
    """Whether a model returned by ``satisfiable`` satisfies the formula."""
    if not isinstance(model, dict):
        return 'not a model'
    point: dict[Basic, Basic] = {}
    for symbol, value in model.items():
        if isinstance(symbol, Basic) and isinstance(value, Basic):
            point[symbol] = value
    for v in variables:
        if isinstance(v, Basic) and v not in point:
            # a variable left out of the model may take any value
            point[v] = Rational(0)
    value = evaluate(formula, point)
    return 'verified' if value is True else ('fails' if value is False else 'uncheckable')


def rewrite_verdict(formula: Boolean, variables: Sequence[Basic], status: str, outcome: Outcome,
                    rng: random.Random) -> str:
    """The verdict on the result of ``simplify`` or ``refine``."""
    if outcome.kind != 'value':
        return outcome.label()
    result = outcome.value
    if result is true:
        return 'WRONG (True for an unsat problem)' if status == 'unsat' else ('ok' if status == 'sat' else 'sat')
    if result is false:
        return 'WRONG (False for a sat problem)' if status == 'sat' else ('ok' if status == 'unsat' else 'unsat')
    if not isinstance(result, Boolean):
        return 'WRONG (not a Boolean: %s)' % (str(result)[:100],)
    for _ in range(20):
        point: dict[Basic, Basic] = {v: Rational(rng.randint(-20, 20), rng.randint(1, 5))
                                     for v in variables if isinstance(v, Basic)}
        a, b = evaluate(formula, point), evaluate(result, point)
        if a is not None and b is not None and a != b:
            return 'WRONG (differs at %s)' % ({str(k): str(v) for k, v in point.items()},)
    return 'ok'


def _float(task: Task, key: str) -> float:
    value = task[key]
    return float(value) if isinstance(value, (int, float)) else 0.0


def _qf_nra(text: str, name: str, task: Task, result: Result) -> None:
    parsed = call(lambda: smtlib.translate(text, name), PARSE_TIMEOUT)
    problem = parsed.value
    if parsed.kind != 'value' or not isinstance(problem, smtlib.Problem):
        result['verdict'] = 'untranslated' if parsed.kind == 'value' else 'parse ' + parsed.label()
        return
    formula, variables, status = problem.formula, list(problem.variables), problem.status
    override = task.get('expected_status')
    if isinstance(override, str):
        status = override
    result.update({'status': status, 'variables': len(variables),
                   'relations': len(formula.atoms(Relational))})
    started = time.monotonic()
    outcome = call(lambda: satisfiable(formula, domain=S.Reals), _float(task, 'timeout'))
    result['sat_time'] = round(time.monotonic() - started, 2)
    if outcome.kind != 'value':
        verdict = outcome.label()
    elif outcome.value is False:
        verdict = 'ok' if status == 'unsat' else ('WRONG (unsat for a sat problem)' if status == 'sat' else 'unsat')
    elif isinstance(outcome.value, dict):
        check = check_model(formula, variables, outcome.value)
        result['model'] = {str(k): str(v)[:200] for k, v in outcome.value.items()}
        if check == 'fails':
            verdict = 'WRONG (the model does not satisfy the formula)'
        elif status == 'unsat':
            verdict = 'WRONG (a %s model for an unsat problem)' % check
        else:
            verdict = ('ok' if status == 'sat' else 'sat') + ('' if check == 'verified' else ' (model uncheckable)')
    else:
        verdict = 'undecided (%s)' % (str(outcome.value)[:60],)
    result['satisfiable'] = verdict
    if outcome.kind == 'timeout' or task.get('rewrite') is False:
        result['simplify'] = result['refine'] = 'skipped'
        return
    rng = random.Random(name)
    limit = _float(task, 'rewrite_timeout')
    result['simplify'] = rewrite_verdict(formula, variables, status,
                                         call(lambda: simplify(formula, domain=S.Reals), limit), rng)
    result['refine'] = rewrite_verdict(formula, variables, status,
                                       call(lambda: refine(formula, domain=S.Reals), limit), rng)


def _nra(text: str, name: str, task: Task, result: Result) -> None:
    parsed = call(lambda: solver_regressions.translate(text, name), PARSE_TIMEOUT)
    problem = parsed.value
    if parsed.kind != 'value' or not isinstance(problem, solver_regressions.ArithProblem):
        result['verdict'] = 'untranslated' if parsed.kind == 'value' else 'parse ' + parsed.label()
        return
    status = problem.status
    closed = problem.formula
    if problem.variables:
        closed = as_boolean(Exists(problem.variables, problem.formula))
    result.update({'status': status, 'variables': len(problem.variables),
                   'relations': len(problem.formula.atoms(Relational))})
    started = time.monotonic()
    outcome = call(lambda: resolve(closed, domain=problem.domain), _float(task, 'timeout'))
    result['resolve_time'] = round(time.monotonic() - started, 2)
    if outcome.kind != 'value':
        verdict = outcome.label()
    elif outcome.value is true or outcome.value is false:
        decided = 'sat' if outcome.value is true else 'unsat'
        verdict = decided if status == 'unknown' else (
            'ok' if decided == status else 'WRONG (%s for a %s problem)' % (decided, status))
    else:
        verdict = 'undecided (%s)' % (str(outcome.value)[:60],)
    result['resolve'] = verdict


def work(task: Task) -> Result:
    """Check one problem (the ``work`` function of the runner)."""
    path = pathlib.Path(str(task['path']))
    result: Result = {'family': task['family'], 'bytes': path.stat().st_size}
    if 'source_status' in task:
        result['source_status'] = task['source_status']
    text = path.read_text(errors='replace')
    if task['logic'] == 'QF_NRA':
        _qf_nra(text, path.stem, task, result)
    else:
        _nra(text, path.stem, task, result)
    return result


VERDICT_KEYS = ('verdict', 'satisfiable', 'simplify', 'refine', 'resolve')


def source_statuses() -> dict[str, str]:
    """The recorded status of every Meti-Tarski file of the release, by name."""
    statuses: dict[str, str] = {}
    for path in load('QF_NRA'):
        if family(path, 'QF_NRA') != 'meti-tarski':
            continue
        text = path.read_text(errors='replace')
        found = re.search(r':status\s+(sat|unsat|unknown)', text)
        statuses[path.name] = found.group(1) if found else 'unknown'
    return statuses


def _brown(args: argparse.Namespace) -> int:
    """``satisfiable`` on a round of the Brown--Vale-Enriquez conjunctions.

    A conjunction is a disjunct of the DNF of a Meti-Tarski problem (or a
    case of one, in round 2): it is expected ``unsat`` when its source is
    recorded ``unsat``, and is ``unknown`` otherwise, since one disjunct of
    a satisfiable formula may well be unsatisfiable.
    """
    statuses = source_statuses()
    paths = tarski_tests.brown_files(args.brown)
    if not paths:
        print("the Tarski test data could not be fetched")
        return 1
    if args.limit:
        paths = paths[:args.limit]
    tasks: list[Task] = []
    for path in paths:
        source = statuses.get(tarski_tests.brown_source(path), 'missing')
        tasks.append({'id': 'brown-r%d/%s' % (args.brown, path.name), 'path': str(path), 'logic': 'QF_NRA',
                      'family': 'brown-r%d' % args.brown, 'timeout': args.timeout, 'rewrite': False,
                      'source_status': source, 'expected_status': 'unsat' if source == 'unsat' else 'unknown',
                      'rewrite_timeout': 0.0})
    output = pathlib.Path(args.output or 'results/brown_r%d.jsonl' % args.brown)
    counter = [0]

    def report(result: Result) -> None:
        counter[0] += 1
        if counter[0] % 500 == 0 or 'WRONG' in str(result.get('satisfiable', '')) or 'crash' in str(result):
            print("%7d %-70s %s %s" % (counter[0], str(result['id'])[-70:], result.get('satisfiable', result.get('verdict')),
                                       str(result.get('satisfiable', ''))[:300] if 'WRONG' in str(result) else ''),
                  flush=True)

    results = run(tasks, 'sympy_extras_benchmarks.drivers.smtlib_release', output, workers=args.workers,
                  deadline=PARSE_TIMEOUT + args.timeout + 120, memory=args.memory, report=report)
    print()
    for key, row in summarise(results).items():
        print("%-12s %s" % (key, dict(sorted(row.items(), key=lambda kv: -kv[1]))))
    return 1 if any('WRONG' in str(r.get('satisfiable', '')) for r in results) else 0


def category(verdict: str) -> str:
    """The kind of a verdict, without its details."""
    for separator in (':', ' ('):
        if separator in verdict:
            verdict = verdict.split(separator)[0]
    return verdict


def summarise(results: list[Result]) -> dict[str, dict[str, int]]:
    """For each checked function, how many problems got each kind of verdict."""
    table: dict[str, dict[str, int]] = {}
    for result in results:
        for key in VERDICT_KEYS:
            verdict = result.get(key)
            if isinstance(verdict, str):
                row = table.setdefault(key, {})
                kind = category(verdict)
                row[kind] = row.get(kind, 0) + 1
    return table


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--logic', choices=['QF_NRA', 'NRA'], default='QF_NRA')
    parser.add_argument('--families', default='')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--timeout', type=float, default=30.0)
    parser.add_argument('--rewrite-timeout', type=float, default=20.0)
    parser.add_argument('--memory', type=int, default=2048)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--brown', type=int, default=0,
                        help='run satisfiable on round 1 or 2 of the Brown--Vale-Enriquez data of Tarski instead')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    if args.brown:
        return _brown(args)
    paths = load(args.logic)
    if not paths:
        print("the %s problems could not be fetched" % args.logic)
        return 1
    wanted = {f for f in args.families.split(',') if f}
    selected = [p for p in paths if not wanted or family(p, args.logic) in wanted]
    selected.sort(key=lambda p: (p.stat().st_size, str(p)))
    if args.limit:
        selected = selected[:args.limit]
    tasks: list[Task] = []
    for path in selected:
        relative = str(path).split('/non-incremental/', 1)[-1]
        tasks.append({'id': relative, 'path': str(path), 'logic': args.logic,
                      'family': family(path, args.logic), 'timeout': args.timeout,
                      'rewrite_timeout': args.rewrite_timeout})
    output = pathlib.Path(args.output or 'results/%s.jsonl' % args.logic.lower())
    deadline = PARSE_TIMEOUT + args.timeout + 2*args.rewrite_timeout + 120
    counter = [0]

    def report(result: Result) -> None:
        counter[0] += 1
        verdicts = ' '.join('%s=%s' % (k[:4], category(str(result[k]))) for k in VERDICT_KEYS if k in result)
        print("%6d %-60s %-7s %s %6.1fs" % (counter[0], str(result['id'])[-60:], result.get('status', ''),
                                            verdicts, float(str(result.get('time', 0)))), flush=True)
        for key in VERDICT_KEYS:
            if 'WRONG' in str(result.get(key, '')) or 'crash' in str(result.get(key, '')):
                print("       %s: %s" % (key, str(result[key])[:400]), flush=True)

    results = run(tasks, 'sympy_extras_benchmarks.drivers.smtlib_release', output, workers=args.workers,
                  deadline=deadline, memory=args.memory, report=report)
    wanted_ids = {str(t['id']) for t in tasks}
    mine = [r for r in results if str(r['id']) in wanted_ids]
    print()
    for key, row in summarise(mine).items():
        print("%-12s %s" % (key, dict(sorted(row.items(), key=lambda kv: -kv[1]))))
    wrong = any('WRONG' in str(r.get(k, '')) for r in mine for k in VERDICT_KEYS)
    return 1 if wrong else 0


if __name__ == '__main__':
    sys.exit(main())
