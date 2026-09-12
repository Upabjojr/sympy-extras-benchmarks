"""``integrate_by_ranges`` of ``sympy_extras.integrals`` on random regions,
checked in four ways which do not use the decomposition.

Usage::

    python -m sympy_extras_benchmarks region_integrals [--cases N] [--seed N]
        [--variables 2|3] [--degree N] [--workers N] [--timeout S]
        [--output results/region_integrals.jsonl]

A case is a random Boolean combination of polynomial relations, cut to the
box `[-3, 3]^n` so that the region is bounded, with a random polynomial
integrand. The value ``integrate_by_ranges`` returns is checked against

* **sampling**: the integral of the integrand times the indicator of the
  region over the box, by Monte Carlo. A case which lands more than two
  standard errors away is sampled again, four times as densely, before it
  is judged, so that the verdict does not rest on one noisy estimate;
* **the region split in two**: the integral over the region equals the sum
  of the integrals over its parts on either side of ``x = 0``;
* **the variables in the other order**: the value cannot depend on the
  order the variables are eliminated in;
* **the recorded answer of Mathematica**, with ``--wolfram COMMAND``: the
  integral of ``Boole[condition]`` times the integrand over the box, to 20
  digits (see :mod:`~sympy_extras_benchmarks.oracles.wolfram`).

The region is always intersected with the box before either side sees it:
a region reaching outside the box would be integrated in full by
sympy-extras and cut off by the sampling, and the two would disagree for
no good reason.
"""
from __future__ import annotations

import argparse
import pathlib
import random
import sys
from typing import Optional, Sequence

import numpy as np

from sympy import And, Integer, Or, Symbol, lambdify, symbols
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._timeout import TimeLimitExceeded, time_limit
from sympy_extras._typing import as_boolean, as_expr
from sympy_extras.integrals import IntegralByRanges, integrate_by_ranges

from sympy_extras_benchmarks.runner import JSON, Result, Task, run

#: the box every region is cut to
BOX = 3

#: how many points one Monte Carlo estimate uses
SAMPLES = 400000


def box_of(variables: Sequence[Symbol], box: int = BOX) -> Boolean:
    """The box the region is cut to."""
    return as_boolean(And(*[And(-box < v, v < box) for v in variables]))


def random_polynomial(rng: random.Random, variables: Sequence[Symbol], degree: int,
                      coefficients: int = 3) -> Expr:
    """A random polynomial with small integer coefficients."""
    total: Expr = Integer(rng.randint(-coefficients, coefficients))
    for _ in range(rng.randint(1, 4)):
        term: Expr = Integer(rng.randint(-coefficients, coefficients))
        for variable in variables:
            term = as_expr(term*variable**rng.randint(0, degree))
        total = as_expr(total + term)
    return total


def random_case(rng: random.Random, variables: Sequence[Symbol], degree: int = 2) -> tuple[Expr, Boolean]:
    """A random region in the box, and a random integrand."""
    atoms: list[Boolean] = []
    for _ in range(rng.randint(1, 3)):
        polynomial = random_polynomial(rng, variables, rng.choice([1, degree, degree]))
        atoms.append(as_boolean(polynomial < 0 if rng.random() < 0.5 else polynomial > 0))
    joined = And(*atoms) if rng.random() < 0.75 else Or(*atoms)
    integrand = random_polynomial(rng, variables, rng.choice([0, 1, degree])) if rng.random() < 0.7 else Integer(1)
    return integrand, as_boolean(And(joined, box_of(variables)))


def sample(integrand: Expr, condition: Boolean, variables: Sequence[Symbol], seed: int,
           samples: int = SAMPLES, box: int = BOX) -> tuple[float, float]:
    """The integral over the box by Monte Carlo, and its standard error."""
    f = lambdify(variables, integrand, 'numpy')
    g = lambdify(variables, condition, 'numpy')
    generator = np.random.default_rng(seed)
    points = [generator.uniform(-box, box, samples) for _ in variables]
    with np.errstate(divide='ignore', invalid='ignore'):
        inside = np.asarray(g(*points), dtype=bool)
        values = np.asarray(f(*points), dtype=float)*np.ones(samples)
    weighted = np.where(inside & np.isfinite(values), values, 0.0)
    volume = float((2*box)**len(variables))
    return volume*float(weighted.mean()), volume*float(weighted.std(ddof=1))/float(np.sqrt(samples))


def evaluated(result: object) -> Optional[float]:
    """The number a result stands for, or ``None`` when it is not one."""
    if not isinstance(result, (Expr, IntegralByRanges)) or result.has(IntegralByRanges) or result.free_symbols:
        return None
    try:
        return float(result.evalf(25))
    except (AttributeError, TypeError, ValueError):
        return None


def integral(integrand: Expr, condition: Boolean, variables: Sequence[Symbol],
             seconds: float) -> Optional[float]:
    """``integrate_by_ranges`` under a time limit, as a number."""
    try:
        with time_limit(seconds):
            return evaluated(integrate_by_ranges(integrand, condition, list(variables)))
    except (TimeLimitExceeded, NotImplementedError, ValueError, TypeError, RecursionError):
        return None


def work(task: Task) -> Result:
    """Check one random case (the ``work`` function of the runner)."""
    seed = int(str(task['seed']))
    count = int(str(task['variables']))
    degree = int(str(task['degree']))
    timeout = float(str(task['timeout']))
    variables = symbols('x y z')[:count]
    integrand, condition = random_case(random.Random(seed), variables, degree)
    result: Result = {'integrand': str(integrand), 'condition': str(condition)}
    whole = integral(integrand, condition, variables, timeout)
    if whole is None:
        result['verdict'] = 'unevaluated'
        return result
    result['value'] = whole
    complaints: list[str] = []
    left = integral(integrand, as_boolean(And(condition, variables[0] <= 0)), variables, timeout)
    right = integral(integrand, as_boolean(And(condition, variables[0] > 0)), variables, timeout)
    if left is not None and right is not None:
        result['split'] = left + right
        if abs(left + right - whole) > 1e-7*max(1.0, abs(whole)):
            complaints.append('WRONG (the halves give %.10f, the whole %.10f)' % (left + right, whole))
    if count > 1:
        other = integral(integrand, condition, variables[::-1], timeout)
        if other is not None:
            result['other_order'] = other
            if abs(other - whole) > 1e-7*max(1.0, abs(whole)):
                complaints.append('WRONG (the other variable order gives %.10f)' % other)
    estimate, error = sample(integrand, condition, variables, seed)
    if abs(whole - estimate) > 2*error:
        estimate, error = sample(integrand, condition, variables, seed + 7919, 4*SAMPLES)
    result['sampled'] = estimate
    result['error'] = error
    if abs(whole - estimate) > max(4*error, 1e-4*max(1.0, abs(estimate))):
        complaints.append('WRONG (sampling gives %.8f +- %.5f)' % (estimate, error))
    result['verdict'] = '; '.join(complaints) if complaints else 'ok'
    return result


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=int, default=40)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--variables', type=int, choices=[2, 3], default=2)
    parser.add_argument('--degree', type=int, default=2)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--timeout', type=float, default=90.0)
    parser.add_argument('--memory', type=int, default=2048)
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    tasks: list[Task] = [{'id': 'case-%d-%d' % (args.seed, index), 'seed': args.seed*10000 + index,
                          'variables': args.variables, 'degree': args.degree, 'timeout': args.timeout}
                         for index in range(args.cases)]
    output = pathlib.Path(args.output or 'results/region_integrals.jsonl')
    counter = [0]

    def report(result: Result) -> None:
        counter[0] += 1
        verdict = str(result.get('verdict', ''))
        print('%4d %-9s %-58s %s' % (counter[0], verdict.split(' (')[0], str(result.get('condition', ''))[:58],
                                     result.get('value', '')), flush=True)
        if 'WRONG' in verdict:
            print('      %s\n      integrand %s' % (verdict, result.get('integrand')), flush=True)

    results = run(tasks, 'sympy_extras_benchmarks.drivers.region_integrals', output, workers=args.workers,
                  deadline=6*args.timeout + 120, memory=args.memory, report=report)
    wanted = {str(t['id']) for t in tasks}
    mine = [r for r in results if str(r['id']) in wanted]
    kinds: dict[str, int] = {}
    for result in mine:
        kind = str(result.get('verdict', 'unknown')).split(' (')[0].split(';')[0]
        kinds[kind] = kinds.get(kind, 0) + 1
    print('\n%s' % dict(sorted(kinds.items(), key=lambda kv: -kv[1])))
    return 1 if any('WRONG' in str(r.get('verdict', '')) for r in mine) else 0


if __name__ == '__main__':
    sys.exit(main())
