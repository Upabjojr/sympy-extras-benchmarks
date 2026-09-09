"""``limit`` of ``sympy_extras.assumptions`` on Maxima's limit regression
files, against Maxima's recorded value and Mathematica.

Usage::

    python -m sympy_extras_benchmarks maxima_limits [--sample N] [--seed N]
        [--timeout S] [--files a,b] [--wolfram COMMAND] [--output results.json]

Neither party is an answer key. Maxima's limit code has its own bugs, and
so does everything else in this area, so the driver reports a
**disagreement** and lets Mathematica decide:

``DIFFER``
    sympy-extras and Mathematica give different values. This is the
    finding: two independent implementations of a decidable-ish question
    disagreeing.
``SUSPECT``
    sympy-extras and Mathematica agree with each other and differ from
    Maxima. Usually Maxima's entry is old or its conventions differ
    (``und``, ``ind``, complex infinity), so it is reported but not
    counted.

Only a value that both sides produce is compared; a limit either side
declines is left alone.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
from typing import Optional

from sympy import Basic, Limit, Symbol, nan, oo, simplify, zoo
from sympy.core.expr import Expr

from sympy_extras.assumptions.limits import limit
from sympy_extras._timeout import attempt

from sympy_extras_benchmarks.datasets.maxima_limits import MaximaLimit, load
from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, to_wolfram

__all__ = ['main', 'same', 'to_wolfram_limit']

#: the symbols an answer from Mathematica may legitimately contain; one
#: holding anything else is a token that did not translate
_KNOWN: frozenset[Symbol] = frozenset()

#: how close two values must be to count as the same. Loose enough for a
#: recorded 16-digit decimal to match the exact value it approximates,
#: far tighter than any real disagreement between limit algorithms.
TOLERANCE = 1e-12

#: Mathematica's spellings for the directions
_DIRECTION = {'+': 'Direction -> "FromAbove"', '-': 'Direction -> "FromBelow"'}


def same(first: Optional[Basic], second: Optional[Basic]) -> Optional[bool]:
    """Whether two limit values agree; ``None`` when it cannot be decided."""
    if first is None or second is None:
        return None
    if not isinstance(first, Expr) or not isinstance(second, Expr):
        return first == second
    if first == second:
        return True
    for value in (first, second):
        if value.has(nan):
            return None
    if {first, second} <= {oo, -oo, zoo} or first in (oo, -oo, zoo) or second in (oo, -oo, zoo):
        return first == second
    try:
        difference = attempt(lambda: simplify(first - second), 15)
    except RecursionError:
        return None
    if difference is None:
        return None
    if difference == 0:
        return True
    if difference.is_number:
        try:
            numeric = attempt(lambda: complex(difference.evalf(30)), 10)
            scale = attempt(lambda: max(abs(complex(first.evalf(30))),
                                        abs(complex(second.evalf(30))), 1.0), 10)
        except (RecursionError, TypeError, ValueError, OverflowError):
            return None
        if numeric is not None and scale is not None:
            # a *relative* tolerance, because the recorded value is often a
            # 16-digit decimal for an irrational: Maxima writes log(2) as
            # 0.6931471805599453, which differs from it by about 1e-17
            return abs(numeric) <= TOLERANCE*scale
    return None


def to_wolfram_limit(entry: MaximaLimit) -> str:
    """The Wolfram Language source for this limit."""
    body = to_wolfram(entry.expression)
    variable = to_wolfram(entry.variable)
    point = to_wolfram(entry.point)
    parts = ["%s -> %s" % (variable, point)]
    if entry.direction in _DIRECTION:
        parts.append(_DIRECTION[entry.direction])
    return "Limit[%s, %s]" % (body, ", ".join(parts))


def _ours(entry: MaximaLimit, timeout: float) -> Optional[Expr]:
    """sympy-extras' value, or ``None`` when it declines or the two sides
    of a two-sided limit disagree.

    ``RecursionError`` is contained here: ``sympy_extras._timeout.attempt``
    does not catch it (sympy-extras#49), and one entry deep inside SymPy
    would otherwise end the sweep and discard its results.
    """
    directions = ['+', '-'] if entry.direction == '+-' else [entry.direction]
    values = []
    for direction in directions:
        try:
            value = attempt(lambda: limit(entry.expression, entry.variable, entry.point,
                                          direction=direction), timeout)
        except RecursionError:
            return None
        if value is None:
            return None
        values.append(value)
    if len(values) == 2 and same(values[0], values[1]) is not True:
        return None                          # the two sides differ: no limit
    if values[0].has(Limit):
        return None                          # returned unevaluated: no answer
    return values[0]


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=int, default=0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=20.0)
    parser.add_argument('--files', default='')
    parser.add_argument('--wolfram', default='')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    entries = load()
    if args.files:
        wanted = set(args.files.split(','))
        entries = [e for e in entries if e.name.split(':')[0] in wanted]
    if not entries:
        print("the Maxima limit files could not be fetched")
        return 1
    if args.sample:
        random.Random(args.seed).shuffle(entries)
        entries = entries[:args.sample]
    oracle = Wolfram(args.wolfram, args.timeout) if args.wolfram else None
    ours: list[Optional[Expr]] = []
    for entry in entries:
        started = time.time()
        value = _ours(entry, args.timeout)
        ours.append(value)
        print("%-26s lim %s->%-6s %-40s ours=%-22s maxima=%-16s %5.1fs" % (
            entry.name[:26], entry.variable, entry.point,
            str(entry.expression)[:40], str(value)[:22], str(entry.recorded)[:16],
            time.time() - started), flush=True)
    theirs: list[Optional[Basic]] = [None]*len(entries)
    if oracle is not None:
        askable, expressions = [], []
        for index, entry in enumerate(entries):
            try:
                expressions.append(to_wolfram_limit(entry))
            except WolframError:
                continue
            askable.append(index)
        print("\nasking Mathematica about %d of the %d limits..." % (len(askable), len(entries)),
              flush=True)
        try:
            answers = oracle.evaluate(expressions)
        except WolframError as error:
            print("the oracle failed: %s" % error)
            answers = ['$Aborted']*len(expressions)
        from sympy.parsing.sympy_parser import parse_expr
        for index, text in zip(askable, answers):
            # anything Mathematica did not settle, and anything still
            # holding one of its own tokens, is no answer at all
            if not text or text.startswith('$') or 'Aborted' in text or 'Failed' in text:
                continue
            # ComplexInfinity first: replacing Infinity first would leave
            # the string "Complexoo", which parses as a symbol and then
            # disagrees with everything
            cleaned = (text.replace('ComplexInfinity', 'zoo')
                       .replace('DirectedInfinity', 'zoo')
                       .replace('Infinity', 'oo')
                       .replace('Indeterminate', 'nan')
                       .replace('[', '(').replace(']', ')'))
            value = attempt(lambda: parse_expr(cleaned), 10)
            if value is not None and not value.atoms(Symbol) - _KNOWN:
                theirs[index] = value
    counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    print()
    for entry, mine, other in zip(entries, ours, theirs):
        verdict = 'undecided'
        if mine is None:
            verdict = 'no answer'
        elif other is not None:
            agree = same(mine, other)
            if agree is True:
                verdict = 'ok'
                if same(mine, entry.recorded) is False:
                    verdict = 'SUSPECT (mathematica agrees with sympy-extras against maxima)'
            elif agree is False:
                verdict = 'DIFFER (mathematica says %s)' % other
        elif entry.recorded is not None:
            agree = same(mine, entry.recorded)
            verdict = 'ok (maxima only)' if agree is not False else 'differs from maxima only'
        counts[verdict.split(' ')[0]] = counts.get(verdict.split(' ')[0], 0) + 1
        if verdict.startswith(('DIFFER', 'SUSPECT')):
            print("%-26s %-40s ours=%s maxima=%s" % (entry.name[:26], verdict,
                                                     mine, entry.recorded), flush=True)
        records.append({'name': entry.name, 'expression': str(entry.expression),
                        'variable': str(entry.variable), 'point': str(entry.point),
                        'direction': entry.direction, 'ours': str(mine),
                        'maxima': str(entry.recorded), 'mathematica': str(other),
                        'verdict': verdict})
    print()
    print(dict(sorted(counts.items())))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'counts': counts, 'results': records},
                                                        indent=1))
    return 1 if counts.get('DIFFER') else 0


if __name__ == '__main__':
    sys.exit(main())
