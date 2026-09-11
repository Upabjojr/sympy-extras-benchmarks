"""``resolve`` and ``satisfiable`` of ``sympy_extras.assumptions`` on the
CAD test collections: the Bath CAD example bank, the tests of QEPCAD B and
the tests of Tarski, in parallel processes.

Usage::

    python -m sympy_extras_benchmarks cad_examples
        [--collections bath,qepcad-application,...] [--workers N]
        [--timeout S] [--cells] [--output results/cad_examples.jsonl]

Each problem is parsed from its QEPCAD or Tarski text. A ``resolve``
question gets ``resolve(formula, assumptions=...)`` over the reals: a truth
value when every variable is quantified, a quantifier-free formula in the
free variables otherwise. A ``satisfiable`` question (the quantifier-free
conjunctions of the ISSAC data) gets ``satisfiable``, whose model is
checked by exact evaluation.

When the collection records an answer (QEPCAD's ``sol T`` output, Tarski's
``.out`` files, the targets of Tarski's unit tests), the result is compared
with it: truth values directly, formulas at random rational points (inside
the ``assume`` region of the problem). A mismatch is reported as
``DISAGREES``, not as wrong -- the recorded answer comes from another
program and may be the wrong one; ``wolfram_check`` settles it. The exact
result is kept (``result_srepr``) for that check, and so is the problem
text. A problem repeated in another collection is run once.

With ``--cells``, the polynomials of the Maple file of the Bath bank are
decomposed instead, with the variable order Maple's best count was
achieved with, and the number of cells is reported beside Maple's.
"""
from __future__ import annotations

import argparse
import pathlib
import random
import sys
import time
from typing import Optional

from sympy import S, Rational, Symbol, srepr, true, false
from sympy.core.basic import Basic
from sympy.logic.boolalg import Boolean

from sympy_extras.assumptions import resolve, satisfiable
from sympy_extras.polys.cad import CAD, cylindrical_algebraic_decomposition

from sympy_extras_benchmarks.datasets import bath_cad, qepcad_tests, tarski_tests
from sympy_extras_benchmarks.datasets.qepcad_syntax import (
    Example, InputFailure, QEPCADSyntaxError, UnsupportedSyntax, parse_formula, parse_inputs)
from sympy_extras_benchmarks.drivers.smtlib_release import call, category, check_model, evaluate
from sympy_extras_benchmarks.runner import Result, Task, run

#: the number of random points a formula is compared at
POINTS = 200


def problem(syntax: str, text: str) -> tuple[Boolean, list[Symbol], Optional[Boolean]]:
    """The formula, its free variables and its assumptions."""
    if syntax == 'qepcad':
        items = parse_inputs(text)
        if not items:
            raise QEPCADSyntaxError("no QEPCAD input")
        item = items[0][1]
        if isinstance(item, InputFailure):
            raise item.error
        bound = set(item.variables[item.free:])
        free = [v for v in item.variables[:item.free]]
        extra = sorted((s for s in item.formula.free_symbols
                        if isinstance(s, Symbol) and s not in bound and s not in free), key=str)
        return item.formula, free + extra, item.assumptions
    formula = parse_formula(text)
    free = sorted((s for s in formula.free_symbols if isinstance(s, Symbol)), key=str)
    return formula, free, None


def _points(variables: list[Symbol], rng: random.Random) -> list[dict[Basic, Basic]]:
    points: list[dict[Basic, Basic]] = []
    for index in range(POINTS):
        scale = 3 if index < POINTS//2 else 30
        points.append({v: Rational(rng.randint(-scale*6, scale*6), rng.randint(1, 6)) for v in variables})
    return points


def compare(result: Boolean, expected: Boolean, free: list[Symbol], assumptions: Optional[Boolean],
            rng: random.Random) -> str:
    """Whether two quantifier-free formulas agree at random points."""
    if result in (true, false) and expected in (true, false):
        return 'ok' if result == expected else 'DISAGREES (%s, recorded %s)' % (result, expected)
    variables = sorted(set(free) | {s for s in (result.free_symbols | expected.free_symbols)
                                    if isinstance(s, Symbol)}, key=str)
    checked = 0
    for point in _points(variables, rng):
        if assumptions is not None and evaluate(assumptions, point) is not True:
            continue
        a, b = evaluate(result, point), evaluate(expected, point)
        if a is None or b is None:
            continue
        checked += 1
        if a != b:
            return 'DISAGREES (at %s: %s, recorded %s)' % ({str(k): str(v) for k, v in point.items()}, a, b)
    return 'ok' if checked else 'not compared (no point decided both)'


def _resolve(task: Task, result: Result, formula: Boolean, free: list[Symbol],
             assumptions: Optional[Boolean], timeout: float) -> None:
    started = time.monotonic()
    outcome = call(lambda: resolve(formula, domain=S.Reals, assumptions=assumptions), timeout)
    result['resolve_time'] = round(time.monotonic() - started, 2)
    if outcome.kind != 'value' or not isinstance(outcome.value, Boolean):
        result['verdict'] = outcome.label() if outcome.kind != 'value' else 'not a Boolean'
        return
    value = outcome.value
    result['result'] = str(value)[:3000]
    result['result_srepr'] = srepr(value)[:400000]
    expected_text = task.get('expected')
    if not isinstance(expected_text, str) or not expected_text:
        result['verdict'] = 'decided' if value in (true, false) else 'eliminated'
        return
    try:
        expected = parse_formula(expected_text)
    except UnsupportedSyntax as error:
        result['verdict'] = 'eliminated (recorded answer unusable: %s)' % error
        return
    except QEPCADSyntaxError as error:
        result['verdict'] = 'eliminated (recorded answer unreadable: %s)' % error
        return
    outcome = call(lambda: compare(value, expected, free, assumptions, random.Random(str(task['id']))), 120.0)
    result['verdict'] = str(outcome.value) if outcome.kind == 'value' else 'compare ' + outcome.label()


def _satisfiable(result: Result, formula: Boolean, free: list[Symbol], timeout: float) -> None:
    started = time.monotonic()
    outcome = call(lambda: satisfiable(formula, domain=S.Reals), timeout)
    result['sat_time'] = round(time.monotonic() - started, 2)
    if outcome.kind != 'value':
        result['verdict'] = outcome.label()
    elif outcome.value is False:
        result['verdict'] = 'unsat'
    elif isinstance(outcome.value, dict):
        check = check_model(formula, free, outcome.value)
        result['model'] = {str(k): str(v)[:200] for k, v in outcome.value.items()}
        result['verdict'] = 'WRONG (the model does not satisfy the formula)' if check == 'fails' else (
            'sat' if check == 'verified' else 'sat (model uncheckable)')
    else:
        result['verdict'] = 'undecided (%s)' % (str(outcome.value)[:60],)


def _cells(task: Task, result: Result, timeout: float) -> None:
    for example in bath_cad.polynomial_examples():
        if '%s#%d' % (example.section, example.number) != task['name']:
            continue
        order = [str(v) for v in example.variables]
        recorded = task.get('maple_order')
        if isinstance(recorded, list) and sorted(str(v) for v in recorded) == sorted(order):
            order = [str(v) for v in recorded]
        symbols = {str(v): v for v in example.variables}
        gens = [symbols[name] for name in reversed(order)]
        started = time.monotonic()
        outcome = call(lambda: cylindrical_algebraic_decomposition(example.polynomials, gens), timeout)
        result['cad_time'] = round(time.monotonic() - started, 2)
        result['order'] = [str(g) for g in gens]
        if outcome.kind == 'value' and outcome.value is not None:
            count = len(outcome.value) if isinstance(outcome.value, CAD) else 0
            result['cells'] = count
            result['verdict'] = 'cells'
        else:
            result['verdict'] = outcome.label()
        return
    result['verdict'] = 'not found'


def work(task: Task) -> Result:
    """Check one problem (the ``work`` function of the runner)."""
    result: Result = {'collection': task['collection'], 'name': task['name']}
    timeout = float(str(task['timeout']))
    if task['question'] == 'cells':
        _cells(task, result, timeout)
        return result
    result['syntax'] = task['syntax']
    result['text'] = task['text']
    try:
        formula, free, assumptions = problem(str(task['syntax']), str(task['text']))
    except UnsupportedSyntax as error:
        result['verdict'] = 'unsupported syntax: %s' % error
        return result
    except QEPCADSyntaxError as error:
        result['verdict'] = 'unreadable: %s' % error
        return result
    result['free'] = [str(v) for v in free]
    if task['question'] == 'satisfiable':
        _satisfiable(result, formula, free, timeout)
    else:
        _resolve(task, result, formula, free, assumptions, timeout)
    return result


def collections() -> list[Example]:
    """Every problem of the three collections."""
    return bath_cad.examples() + qepcad_tests.examples() + tarski_tests.examples()


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collections', default='')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--timeout', type=float, default=120.0)
    parser.add_argument('--memory', type=int, default=2048)
    parser.add_argument('--cells', action='store_true')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    tasks: list[Task] = []
    duplicates: list[Result] = []
    if args.cells:
        counts = bath_cad.cell_counts()
        for polynomial in bath_cad.polynomial_examples():
            recorded = counts.get(polynomial.title.lower())
            tasks.append({'id': 'bath-cells/%s#%d' % (polynomial.section, polynomial.number), 'collection': 'bath-cells',
                          'name': '%s#%d' % (polynomial.section, polynomial.number), 'title': polynomial.title,
                          'question': 'cells', 'timeout': args.timeout,
                          'maple_cells': recorded[0] if recorded else None,
                          'maple_order': list(recorded[1]) if recorded else None})
    else:
        wanted = {c for c in args.collections.split(',') if c}
        for example in collections():
            if wanted and example.collection not in wanted:
                continue
            if example.duplicate_of is not None:
                duplicates.append({'id': example.key, 'collection': example.collection, 'name': example.name,
                                   'verdict': 'duplicate', 'of': example.duplicate_of})
                continue
            tasks.append({'id': example.key, 'collection': example.collection, 'name': example.name,
                          'syntax': example.syntax, 'text': example.text, 'question': example.question,
                          'expected': example.expected, 'timeout': args.timeout})
    output = pathlib.Path(args.output or ('results/bath_cells.jsonl' if args.cells else 'results/cad_examples.jsonl'))
    counter = [0]

    def report(result: Result) -> None:
        counter[0] += 1
        extra = ''
        if 'cells' in result:
            extra = 'cells=%s' % result['cells']
        print("%5d %-55s %-50s %s %6.1fs" % (counter[0], str(result['id'])[-55:], str(result.get('verdict'))[:50],
                                             extra, float(str(result.get('time', 0)))), flush=True)
        verdict = str(result.get('verdict', ''))
        if 'WRONG' in verdict or 'DISAGREES' in verdict or verdict.startswith('crash'):
            print("      %s | result: %s" % (verdict[:400], str(result.get('result', ''))[:300]), flush=True)

    results = run(tasks, 'sympy_extras_benchmarks.drivers.cad_examples', output, workers=args.workers,
                  deadline=args.timeout + 300, memory=args.memory, report=report)
    everything = results + duplicates
    table: dict[str, dict[str, int]] = {}
    for result in everything:
        row = table.setdefault(str(result.get('collection')), {})
        kind = category(str(result.get('verdict')))
        row[kind] = row.get(kind, 0) + 1
    print()
    for collection, row in sorted(table.items()):
        print("%-28s %s" % (collection, dict(sorted(row.items(), key=lambda kv: -kv[1]))))
    return 1 if any('WRONG' in str(r.get('verdict', '')) for r in everything) else 0


if __name__ == '__main__':
    sys.exit(main())
