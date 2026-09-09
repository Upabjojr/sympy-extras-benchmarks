"""``solve_ode`` on the ODE test suite of REDUCE's ``ODESolve``, whose
core is the Postel-Zimmermann collection.

Usage::

    python -m sympy_extras_benchmarks reduce_odes [--sample N] [--seed N]
        [--timeout S] [--max-order N] [--output results.json]

Every equation is solved and every solution verified twice, with the same
checks as
:mod:`~sympy_extras_benchmarks.drivers.verify_random`: symbolically with
``checkodesol`` and numerically, by evaluating the residual at random
points. A solution whose residual does not vanish is ``WRONG`` and the
driver exits 1.

The point of this dataset is independence. Every other ODE benchmark here
is Kamke or Murphy, so a solver tuned to those two books would look good;
Postel and Zimmermann assembled their equations to tell computer algebra
systems apart.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
import time
from typing import Optional

from sympy_extras_benchmarks.datasets.reduce_odes import ReduceODE, load
from sympy_extras_benchmarks.drivers.verify_random import Equation, verify, x, y

def _verify_guarded(entry: Equation, rng: random.Random,
                    timeout: float) -> tuple[str, list[str]]:
    """:func:`verify`, with a stack overflow contained.

    ``sympy_extras._timeout.attempt`` does not catch ``RecursionError``
    (sympy-extras#49), so one equation deep in SymPy can end a sweep of
    hundreds and discard its results. Here it is one more equation with no
    answer.
    """
    try:
        return verify(entry, rng, timeout)
    except RecursionError:
        return 'failed (recursion)', []



def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=int, default=0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=20.0)
    parser.add_argument('--max-order', type=int, default=3)
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    rng = random.Random(args.seed)
    # ``verify`` is written against y(x); an equation in other letters is
    # the same mathematics but would need renaming, so it is left out
    entries: list[ReduceODE] = [e for e in load()
                                if e.function == y(x) and e.order <= args.max_order]
    if not entries:
        print("the REDUCE test files could not be fetched")
        return 1
    if args.sample:
        rng.shuffle(entries)
        entries = entries[:args.sample]
    counts: dict[str, int] = {}
    records: list[dict[str, object]] = []
    for entry in entries:
        started = time.time()
        status, verdicts = _verify_guarded(entry, rng, args.timeout)
        counts[status] = counts.get(status, 0) + 1
        print("%-16s order %d %-11s %5.1fs  %s" % (
            entry.name, entry.order, status, time.time() - started,
            str(entry.equation)[:70]), flush=True)
        for line in verdicts:
            print("     %s" % line[:150], flush=True)
        records.append({'name': entry.name, 'order': entry.order,
                        'equation': str(entry.equation), 'status': status,
                        'solutions': verdicts, 'time': round(time.time() - started, 2)})
    print()
    print(dict(sorted(counts.items())))
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'counts': counts, 'results': records},
                                                        indent=1))
    return 1 if counts.get('WRONG') else 0


if __name__ == '__main__':
    sys.exit(main())
