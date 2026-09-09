"""``resolve`` of ``sympy_extras.assumptions`` on the ``micromega`` test
suite (``lia``, ``nia``, ``lra``, ``psatz``) of the Rocq/Coq standard
library.

Usage::

    python -m sympy_extras_benchmarks coq_micromega [--sample N] [--seed N]
        [--timeout S] [--max-variables N] [--max-size N]
        [--domain reals|integers|both] [--non-trivial]
        [--wolfram COMMAND] [--output results.json]

These goals are the nonlinear half of the proof-assistant benchmarks:
Positivstellensatz examples, products of hypotheses and high powers over
``Z``, which is where a quantifier-elimination procedure is most likely
to give up. See :mod:`~sympy_extras_benchmarks.drivers.prover_goals` for
what is run and :mod:`~sympy_extras_benchmarks.datasets.coq_micromega`
for how the goals are read.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from sympy_extras_benchmarks.datasets.coq_micromega import load
from sympy_extras_benchmarks.drivers.prover_goals import add_arguments, run


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    return run(load(), parser.parse_args(argv))


if __name__ == '__main__':
    sys.exit(main())
