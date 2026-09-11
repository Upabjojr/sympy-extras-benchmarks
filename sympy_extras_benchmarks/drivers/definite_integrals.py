"""``integrate`` on the definite integrals of Maxima, REDUCE, FriCAS and
holpy, checked by numerical quadrature.

Usage::

    python -m sympy_extras_benchmarks definite_integrals
        [--sources maxima,reduce,fricas,holpy] [--collections a,b]
        [--sample N] [--seed N] [--timeout S] [--meijerg]
        [--workers N] [--memory MB] [--output results.jsonl]

sympy-extras has no integrator of its own, so this driver measures SymPy's
``integrate``, which sympy-extras builds on: its default algorithm, or with
``--meijerg`` the Meijer G-function method alone — the method of REDUCE's
DEFINT and of Maxima's ``specint``, whose tests are two of the datasets.

Each integral is computed with its parameters carrying what the source
assumes about them (``a > 0`` becomes a positive symbol, a declared
integer an integer one), in parallel worker processes
(:mod:`~sympy_extras_benchmarks.runner`, resumable from ``--output``). The
result is evaluated at two random values of the parameters satisfying the
facts and compared with numerical quadrature
(:mod:`~sympy_extras_benchmarks.oracles.quadrature`):

``ok``
    the result agrees with the quadrature wherever the quadrature is
    trusted;
``WRONG``
    the result disagrees with a trusted quadrature. The driver exits 1;
``unevaluated``
    ``integrate`` returned the integral, or a ``Piecewise`` whose branch
    at the sample is still one;
``no answer``
    the time ran out or ``integrate`` gave up;
``unchecked``
    no sample satisfies the facts, or the quadrature is not trusted
    there (oscillation over an infinite range, divergence, a singularity
    inside the range).

The value the source records is compared with the same quadrature; a
disagreement is reported as ``SOURCE``, a finding about the source's own
answer (or its translation here), and not counted against ``integrate``.
Use a separate ``--output`` for each configuration: a run resumes from the
results already in the file.
"""
from __future__ import annotations

import argparse
import pathlib
import random
import sys
from typing import Callable, Optional

from sympy import Ge, Gt, Integral, Le, Lt, Ne, Symbol, integrate, oo, zoo
from sympy.core.expr import Expr

from sympy_extras._timeout import attempt
from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.datasets import (
    fricas_integrals, holpy_integrals, maxima_integrals, reduce_defint)
from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.oracles.quadrature import agree, numerical, quadrature, sample
from sympy_extras_benchmarks.runner import JSON, Result, Task, run

__all__ = ['SOURCES', 'assumed_symbols', 'check', 'work', 'main']

#: the datasets, each loading its integrals
SOURCES: dict[str, Callable[[], list[DefiniteIntegral]]] = {
    'maxima': maxima_integrals.load,
    'reduce': reduce_defint.load,
    'fricas': fricas_integrals.load,
    'holpy': holpy_integrals.load,
}

#: an integrator: the integrand and ``(variable, lower, upper)``
Integrator = Callable[[Expr, tuple[Symbol, Expr, Expr]], Expr]

#: the number of samples of the parameters a result is checked at
SAMPLES = 2


def _default(integrand: Expr, limits: tuple[Symbol, Expr, Expr]) -> Expr:
    return as_expr(integrate(integrand, limits))


def _meijerg(integrand: Expr, limits: tuple[Symbol, Expr, Expr]) -> Expr:
    return as_expr(integrate(integrand, limits, meijerg=True))


def assumed_symbols(entry: DefiniteIntegral) -> dict[Symbol, Symbol]:
    """Each parameter with the SymPy assumptions its facts and properties
    state: a sign fact ``p > 0`` (``p >= 0``, ``p < 0``, ``p <= 0``,
    ``p != 0``) and the declared properties. Other facts are left to the
    sample values."""
    signs = {Gt: 'positive', Ge: 'nonnegative', Lt: 'negative', Le: 'nonpositive',
             Ne: 'nonzero'}
    flipped = {Gt: 'negative', Ge: 'nonpositive', Lt: 'positive', Le: 'nonnegative',
               Ne: 'nonzero'}
    wanted: dict[Symbol, dict[str, bool]] = {}
    for fact in entry.facts:
        for kind in signs:
            if isinstance(fact, kind):
                lhs, rhs = fact.args
                if isinstance(lhs, Symbol) and rhs == 0:
                    wanted.setdefault(lhs, {})[signs[kind]] = True
                elif isinstance(rhs, Symbol) and lhs == 0:
                    wanted.setdefault(rhs, {})[flipped[kind]] = True
    for symbol, prop in entry.properties:
        wanted.setdefault(symbol, {})[prop] = True
    replacement: dict[Symbol, Symbol] = {}
    for symbol, assumptions in wanted.items():
        if symbol not in entry.parameters:
            continue
        try:
            replacement[symbol] = Symbol(symbol.name, **assumptions)
        except ValueError:
            continue                        # inconsistent: leave it plain
    return replacement


def check(entry: DefiniteIntegral, rng: random.Random, timeout: float,
          integrator: Integrator = _default) -> Result:
    """Compute ``entry`` with ``integrator`` and check the result."""
    replacement = assumed_symbols(entry)
    integrand = as_expr(entry.integrand.xreplace(replacement))
    limits = (entry.variable, as_expr(entry.lower.xreplace(replacement)),
              as_expr(entry.upper.xreplace(replacement)))
    try:
        value = attempt(lambda: integrator(integrand, limits), timeout)
    except RecursionError:
        value = None
    result: Result = {'result': None if value is None else str(value)[:2000]}
    if value is None:
        result['verdict'] = 'no answer'
        return result
    verdict = 'unevaluated' if value.has(Integral) else 'unchecked'
    checked: list[JSON] = []
    source: Optional[str] = None
    for _ in range(SAMPLES if entry.parameters else 1):
        values = sample(entry, rng)
        if values is None:
            break
        expected = attempt(lambda: quadrature(entry, values), timeout)
        if expected is None:
            continue
        assumed = {replacement.get(s, s): v for s, v in values.items()}
        ours = attempt(lambda: numerical(value, assumed), timeout)
        if entry.recorded is not None:
            recorded = entry.recorded
            theirs = attempt(lambda: numerical(recorded, values), timeout)
            if theirs is not None:
                source = 'agrees' if agree(theirs, expected) and source != 'SOURCE' else 'SOURCE'
        checked.append({'values': {str(s): str(v) for s, v in values.items()},
                        'quadrature': str(expected), 'result': str(ours)})
        if ours is None:
            if value in (oo, -oo, zoo):
                verdict = 'WRONG'           # divergent, says integrate; it converges
            continue
        if not agree(ours, expected):
            verdict = 'WRONG'
        elif verdict != 'WRONG':
            verdict = 'ok'
    result['verdict'] = verdict
    result['checked'] = checked
    result['source'] = source
    return result


_LOADED: dict[str, dict[str, DefiniteIntegral]] = {}


def _entry(source: str, name: str) -> Optional[DefiniteIntegral]:
    if source not in _LOADED:
        _LOADED[source] = {e.name: e for e in SOURCES[source]()}
    return _LOADED[source].get(name)


def work(task: Task) -> Result:
    """Check one integral (the ``work`` function of the runner)."""
    source, name = str(task['source']), str(task['name'])
    entry = _entry(source, name)
    if entry is None:
        return {'verdict': 'missing'}
    timeout = task['timeout']
    seed = task['seed']
    integrator = _meijerg if task['meijerg'] else _default
    rng = random.Random('%s/%s/%s' % (seed, source, name))
    return check(entry, rng, float(timeout) if isinstance(timeout, (int, float)) else 30.0,
                 integrator)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--sources', default=','.join(SOURCES))
    parser.add_argument('--collections', default='')
    parser.add_argument('--sample', type=int, default=0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=30.0)
    parser.add_argument('--meijerg', action='store_true')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--memory', type=int, default=2048)
    parser.add_argument('--output', default='results/definite_integrals.jsonl')
    args = parser.parse_args(argv)
    tasks: list[Task] = []
    wanted = set(args.collections.split(',')) if args.collections else set()
    for source in args.sources.split(','):
        if source not in SOURCES:
            print("unknown source %r; one of: %s" % (source, ', '.join(SOURCES)))
            return 2
        entries = SOURCES[source]()
        print("%s: %d integrals" % (source, len(entries)), flush=True)
        for entry in entries:
            if wanted and entry.name.split(':')[0] not in wanted:
                continue
            tasks.append({'id': '%s/%s' % (source, entry.name), 'source': source,
                          'name': entry.name, 'timeout': args.timeout, 'seed': args.seed,
                          'meijerg': args.meijerg})
    if not tasks:
        print("no integral could be fetched")
        return 1
    if args.sample:
        random.Random(args.seed).shuffle(tasks)
        tasks = tasks[:args.sample]

    def report(result: Result) -> None:
        line = "%-44s %-12s %6ss" % (str(result['id'])[:44], result.get('verdict'),
                                     result.get('time'))
        if result.get('source') == 'SOURCE':
            line += '  SOURCE'
        if result.get('verdict') == 'WRONG':
            line += '  %s  %s' % (str(result.get('result'))[:60], result.get('checked'))
        print(line, flush=True)

    ids = {str(t['id']) for t in tasks}
    results = [r for r in run(tasks, 'sympy_extras_benchmarks.drivers.definite_integrals',
                              pathlib.Path(args.output), workers=args.workers,
                              deadline=4*args.timeout + 60, memory=args.memory, report=report)
               if str(r['id']) in ids]
    counts: dict[str, int] = {}
    for result in results:
        verdict = str(result.get('verdict'))
        counts[verdict] = counts.get(verdict, 0) + 1
        if result.get('source') == 'SOURCE':
            counts['SOURCE'] = counts.get('SOURCE', 0) + 1
    print()
    print(dict(sorted(counts.items())))
    return 1 if counts.get('WRONG') else 0


if __name__ == '__main__':
    sys.exit(main())
