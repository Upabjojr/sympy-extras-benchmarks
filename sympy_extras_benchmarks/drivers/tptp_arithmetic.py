"""``resolve`` of ``sympy_extras.assumptions`` on the arithmetic (``ARI``)
domain of the TPTP problem library.

Usage::

    python -m sympy_extras_benchmarks tptp_arithmetic [--sample N] [--seed N]
        [--timeout S] [--max-variables N] [--max-size N]
        [--domain reals|integers|both] [--non-trivial]
        [--wolfram COMMAND] [--output results.json]

The largest of the cross-checking datasets, and the one written for
provers rather than for a tactic: several hundred problems over ``$int``,
``$rat`` and ``$real``, each carrying the ``Status`` its authors recorded.
See :mod:`~sympy_extras_benchmarks.drivers.prover_goals` for what is run
and :mod:`~sympy_extras_benchmarks.datasets.tptp_arithmetic` for what is
read and what is refused.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from sympy_extras_benchmarks.datasets.tptp_arithmetic import load
from sympy_extras_benchmarks.drivers.prover_goals import add_arguments, run


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    return run(load(), parser.parse_args(argv))


if __name__ == '__main__':
    sys.exit(main())
