"""``resolve`` of ``sympy_extras.assumptions`` on the arithmetic tactic
tests (``linarith``, ``nlinarith``, ``positivity``) of Lean's mathlib4.

Usage::

    python -m sympy_extras_benchmarks lean_tactics [--sample N] [--seed N]
        [--timeout S] [--max-variables N] [--max-size N]
        [--domain reals|integers|both] [--non-trivial]
        [--wolfram COMMAND] [--output results.json]

See :mod:`~sympy_extras_benchmarks.drivers.prover_goals` for what is run
and how a disagreement is reported, and
:mod:`~sympy_extras_benchmarks.datasets.lean_tactics` for how the goals
are read.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from sympy_extras_benchmarks.datasets.lean_tactics import load
from sympy_extras_benchmarks.drivers.prover_goals import add_arguments, run


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    return run(load(), parser.parse_args(argv))


if __name__ == '__main__':
    sys.exit(main())
