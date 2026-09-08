"""Command line entry point: ``python -m sympy_extras_benchmarks DRIVER
[options]`` runs one of the drivers; ``--list`` names them."""
from __future__ import annotations

import importlib
import sys
from typing import Callable, Optional

#: the drivers, with one line each
DRIVERS: dict[str, str] = {
    'kamke_odes': "dsolve, the linear/first order solvers and dsolve_lie on the Kamke and Murphy collections",
    'linear_odes': "the linear ODE solvers on the homogeneous linear equations of the collections",
    'pde_symmetries': "point symmetry algebras of classical PDEs against the literature",
    'qf_nra': "satisfiable, simplify and refine on the SMT-LIB QF_NRA Meti-Tarski problems",
    'polynomial_systems': "ideal invariants of the Katsura and cyclic systems",
    'solve_random': "solve with assumptions on random polynomial and transcendental equations",
    'verify_random': "solve_ode on a random sample of the collections, verified numerically",
    'logic_random': "simplify, refine, ask, satisfiable on random Boolean combinations of relations",
}


def main(argv: Optional[list[str]] = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ('-h', '--help', '--list'):
        print("usage: python -m sympy_extras_benchmarks DRIVER [options]\n\ndrivers:")
        for name, line in DRIVERS.items():
            print("  %-20s %s" % (name, line))
        return 0 if args else 2
    name = args[0]
    if name not in DRIVERS:
        print("unknown driver %r; one of: %s" % (name, ', '.join(DRIVERS)))
        return 2
    module = importlib.import_module('sympy_extras_benchmarks.drivers.' + name)
    entry: Callable[[list[str]], int] = module.main
    return entry(args[1:])


if __name__ == '__main__':
    sys.exit(main())
