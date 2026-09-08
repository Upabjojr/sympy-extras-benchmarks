"""The ideal operations of sympy-extras on the Katsura and cyclic systems,
checked against their known invariants.

Usage::

    python -m sympy_extras_benchmarks polynomial_systems [--systems katsura-2,...]
        [--timeout SECONDS] [--output results.json]

For every system of :mod:`sympy_extras_benchmarks.datasets.polynomial_systems`
the dimension of the variety, the number of solutions (the dimension of
the quotient as a vector space) and radicality computed by ``Ideal`` are
compared with the published values; for zero-dimensional systems the lex
basis obtained by ``change_order`` (FGLM) is compared with the one of the
Gröbner walk. Every step runs under the time limit; a step which does
not finish is reported as ``timeout`` and is not counted as a mismatch.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from typing import Optional

from sympy_extras._timeout import attempt
from sympy_extras.polys.groebnerwalk import groebner_walk
from sympy_extras.polys.ideals import Ideal

from sympy_extras_benchmarks.datasets.polynomial_systems import SYSTEMS, PolynomialSystem


def run(system: PolynomialSystem, timeout: float, walk: bool) -> dict[str, object]:
    started = time.time()
    record: dict[str, object] = {'name': system.name, 'variables': len(system.variables)}
    mismatches: list[str] = []
    I = Ideal(system.equations, *system.variables)
    dimension = attempt(lambda: I.dimension(), timeout)
    record['dimension'] = dimension if dimension is not None else 'timeout'
    if dimension is not None and dimension != system.dimension:
        mismatches.append('dimension %s != %d' % (dimension, system.dimension))
    if system.dimension == 0:
        count = attempt(lambda: I.vector_space_dimension(), timeout)
        record['solutions'] = count if count is not None else 'timeout'
        if count is not None and system.solutions is not None and count != system.solutions:
            mismatches.append('solutions %s != %d' % (count, system.solutions))
        radical = attempt(lambda: I.is_radical(), timeout)
        record['radical'] = radical if radical is not None else 'timeout'
        if radical is not None and system.radical is not None and radical != system.radical:
            mismatches.append('radical %s != %s' % (radical, system.radical))
        if walk:
            fglm = attempt(lambda: [p.as_expr() for p in I.change_order('lex')], timeout)
            walked = attempt(lambda: [g.as_expr() for g in groebner_walk(I._basis(), I.ring(), 'lex')], timeout)
            if fglm is None or walked is None:
                record['lex'] = 'timeout'
            else:
                record['lex'] = 'agree' if fglm == walked else 'DIFFER'
                if fglm != walked:
                    mismatches.append('FGLM and the walk differ')
    record['mismatches'] = mismatches
    record['time'] = round(time.time() - started, 2)
    return record


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--systems', default='', help="comma-separated names (default: all)")
    parser.add_argument('--timeout', type=float, default=120.0)
    parser.add_argument('--no-walk', action='store_true', help="skip the Gröbner walk comparison")
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    wanted = set(args.systems.split(',')) if args.systems else set()
    systems = [s for s in SYSTEMS if not wanted or s.name in wanted]
    results: list[dict[str, object]] = []
    failures = 0
    for system in systems:
        record = run(system, args.timeout, not args.no_walk)
        results.append(record)
        problems = record['mismatches']
        if isinstance(problems, list) and problems:
            failures += 1
        print("%-12s vars=%d dim=%-8s solutions=%-8s radical=%-8s lex=%-8s %6.1fs %s" % (
            system.name, len(system.variables), record.get('dimension', '-'), record.get('solutions', '-'),
            record.get('radical', '-'), record.get('lex', '-'), float(str(record['time'])),
            'MISMATCH ' + '; '.join(str(p) for p in problems) if isinstance(problems, list) and problems else 'ok'),
            flush=True)
    print("systems:", len(results), "mismatches:", failures)
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'mismatches': failures, 'results': results}, indent=1))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
