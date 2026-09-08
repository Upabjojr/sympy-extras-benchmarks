"""Point symmetry algebras of classical partial differential equations,
compared with the dimensions published in the literature.

Usage::

    python -m sympy_extras_benchmarks pde_symmetries [--output results.json]

For every equation of :mod:`sympy_extras_benchmarks.datasets.pde_symmetries`
the finite-dimensional part of the point symmetry algebra is computed with
``pde_symmetries`` and the polynomial ansatz of the degree given in the
table, its dimension compared with the reference, and every symmetry
verified by substitution in the invariance condition with
``check_symmetry``.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from typing import Optional

from sympy_extras.solvers import pde_symmetries, check_symmetry

from sympy_extras_benchmarks.datasets.pde_symmetries import TABLE, u


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    failures = 0
    results: list[dict[str, object]] = []
    print("%-46s %7s %5s %5s %s" % ("equation", "degree", "found", "ref", "time"))
    for entry in TABLE:
        started = time.time()
        syms = pde_symmetries(entry.equation, u, degree=entry.degree, basis=entry.basis)
        elapsed = time.time() - started
        verified = all(check_symmetry(entry.equation, u, s) for s in syms)
        status = "ok" if len(syms) == entry.expected and verified else "MISMATCH"
        if status != "ok":
            failures += 1
        print("%-46s %7d %5d %5d %5.1fs %s  %s" % (entry.name, entry.degree, len(syms), entry.expected,
                                                   elapsed, status, entry.reference))
        results.append({'name': entry.name, 'degree': entry.degree, 'found': len(syms),
                        'expected': entry.expected, 'verified': verified, 'status': status,
                        'time': round(elapsed, 2)})
    print("mismatches:", failures)
    if args.output:
        pathlib.Path(args.output).write_text(json.dumps({'mismatches': failures, 'results': results}, indent=1))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
