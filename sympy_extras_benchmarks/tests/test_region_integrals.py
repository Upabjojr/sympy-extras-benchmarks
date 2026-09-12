"""The checks of the region integral driver, on regions written here."""
from __future__ import annotations

import random

from sympy import Integer, pi, symbols

from sympy_extras_benchmarks.drivers.region_integrals import (box_of, evaluated, random_case, sample, work)

x, y = symbols('x y')


def test_box_and_random_case() -> None:
    integrand, condition = random_case(random.Random(3), (x, y))
    # the region is always cut to the box, so that it is bounded
    assert condition.has(x) and condition.atoms(type(x)) <= {x, y}
    assert random_case(random.Random(3), (x, y)) == (integrand, condition)      # the seed decides it
    assert box_of((x, y)).subs({x: 0, y: 0}) is not None


def test_sampling_a_known_region() -> None:
    # the unit disc has area pi
    value, error = sample(Integer(1), x**2 + y**2 < 1, (x, y), seed=1)
    assert abs(value - float(pi)) < 5*error
    # the integrand is used, not only the region: x**2 over the disc is pi/4
    value, error = sample(x**2, x**2 + y**2 < 1, (x, y), seed=1)
    assert abs(value - float(pi)/4) < 5*error


def test_evaluated() -> None:
    assert evaluated(Integer(3)) == 3.0
    assert evaluated(x) is None            # not a number
    assert evaluated(None) is None


def test_work_on_a_good_case() -> None:
    result = work({'id': 'k', 'seed': 5, 'variables': 2, 'degree': 2, 'timeout': 60.0})
    assert result['verdict'] in ('ok', 'unevaluated')
    if result['verdict'] == 'ok':
        assert isinstance(result['value'], float) and isinstance(result['sampled'], float)
