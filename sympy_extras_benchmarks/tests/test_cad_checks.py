"""The checks of a decomposition in ``cad_examples`` catch a missing cell
and a cell with the wrong signs."""
from __future__ import annotations

import random

from sympy import symbols

from sympy_extras.polys.cad import cylindrical_algebraic_decomposition
from sympy_extras_benchmarks.drivers.cad_examples import check_cells

x, y = symbols('x y')
CIRCLE = [x**2 + y**2 - 1]


def test_correct_decomposition() -> None:
    cad = cylindrical_algebraic_decomposition(CIRCLE, [x, y])
    report = check_cells(cad, CIRCLE, [x, y], random.Random(0))
    assert report['missing'] == 0 and report['mislabelled'] == 0
    assert report['sign_conditions'] == 3 and report['rational_points'] == 13


def test_missing_cell() -> None:
    cad = cylindrical_algebraic_decomposition(CIRCLE, [x, y])
    # the only cell inside the circle
    cad.cells = [cell for cell in cad.cells if tuple(cell.signs) != (-1,)]
    report = check_cells(cad, CIRCLE, [x, y], random.Random(0), points=2000)
    assert report['missing'] != 0
    assert 'missing_point' in report


def test_mislabelled_cell() -> None:
    cad = cylindrical_algebraic_decomposition(CIRCLE, [x, y])
    outside = next(cell for cell in cad.cells if tuple(cell.signs) == (1,))
    outside.signs = (-1,)
    report = check_cells(cad, CIRCLE, [x, y], random.Random(0))
    assert report['mislabelled'] == 1
    assert report['recorded'] == '(-1,)' and report['actual'] == '(1,)'


def test_free_variables_of_a_qepcad_input() -> None:
    from sympy_extras_benchmarks.drivers.cad_examples import problem
    a, b = symbols('a b')
    # a declared count of 0 with no quantifier: every variable is free
    _, free, _ = problem('qepcad', '[T]\n(x,y)\n0\n[x y = 1 \\/ y < 0].')
    assert free == [x, y]
    # the free ones come first in QEPCAD's order, the bound ones are left out
    _, free, _ = problem('qepcad', '[Q]\n(b,a,x)\n2\n(E x)[a x^2 + b = 0].')
    assert free == [b, a]
