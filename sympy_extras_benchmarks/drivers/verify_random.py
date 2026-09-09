"""Draw random equations from the collections and verify the solutions
independently.

Usage::

    python -m sympy_extras_benchmarks verify_random.py [--sample N] [--seed N] [--timeout S]
        [--collections kamke1,kamke2]

For every sampled equation of the Kamke collection ``solve_ode`` (SymPy's
``dsolve`` first, the symmetry method when it fails) is run, and every
solution is verified twice: symbolically with ``checkodesol`` and
numerically, by evaluating the residual of the equation at random points
with random values of the constants and parameters (an implicit solution
`G(x, y) = 0` is differentiated implicitly and its points are found with
``nsolve``). A solution which fails the numerical check is reported as
WRONG; one which passes neither check is UNVERIFIED.
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from typing import Optional, Protocol, Union


from sympy import im, nan, oo, zoo, Basic, Derivative, Eq, Expr, Symbol, Rational, Integral, nsolve, diff, N
from sympy.solvers.ode import checkodesol

from sympy_extras._timeout import attempt
from sympy_extras._typing import as_expr
from sympy_extras.solvers import solve_ode

from sympy_extras_benchmarks.datasets.maxima_ode import load, x, y

__all__ = ['Equation', 'main', 'numeric_check', 'verify', 'x', 'y']


class Equation(Protocol):
    """What :func:`verify` needs of an equation, whichever collection it
    came from: the Kamke/Murphy entries of
    :mod:`~sympy_extras_benchmarks.datasets.maxima_ode` and the
    Postel-Zimmermann ones of
    :mod:`~sympy_extras_benchmarks.datasets.reduce_odes` both provide it."""

    name: str

    @property
    def equation(self) -> Expr:
        ...

    @property
    def order(self) -> int:
        ...

PRECISION = 30
TOLERANCE = Rational(1, 10)**12

#: values for the symbols of an equation
Point = dict[Union[Basic, complex], Union[Basic, complex]]


def _residual_explicit(equation: Expr, value: Expr, point: Point) -> Optional[Expr]:
    """The residual of the equation at an explicit solution ``y = value``."""
    e = equation.subs(y(x), value).doit()
    r = e.subs(point)
    r = N(r, PRECISION)
    return r if isinstance(r, Expr) and r.is_number else None


def _residual_implicit(equation: Expr, G: Expr, order: int, point: Point) -> Optional[Expr]:
    """The residual at a point of the curve ``G(x, y) = 0``: the derivatives
    of ``y`` come from implicit differentiation."""
    ysym = Symbol('y_value')
    g = G.subs(y(x), ysym)
    numeric = g.subs(point)
    x0 = point[x]
    y0: Optional[Basic] = None
    for guess in (Rational(1, 2), 1, -1, 2, Rational(-3, 2)):
        try:
            candidate = nsolve(numeric.subs(x, x0), ysym, guess, prec=PRECISION)
        except (ValueError, TypeError, ZeroDivisionError):
            continue
        if abs(N(numeric.subs({x: x0, ysym: candidate}), PRECISION)) < TOLERANCE:
            y0 = candidate
            break
    if y0 is None:
        return None
    derivatives: list[Expr] = [ysym]
    y1 = -diff(g, x)/diff(g, ysym)
    derivatives.append(y1)
    for _ in range(order - 1):
        last = derivatives[-1]
        derivatives.append(diff(last, x) + diff(last, ysym)*y1)
    e = equation
    for d in sorted(e.atoms(Derivative), key=lambda d: -sum(int(n) for _, n in d.variable_count)):
        if d.expr == y(x):
            k = sum(int(n) for _, n in d.variable_count)
            e = e.subs(d, derivatives[k])
    e = e.subs(y(x), ysym)
    r = N(e.subs(point).subs({x: x0, ysym: y0}), PRECISION)
    return r if isinstance(r, Expr) and r.is_number else None


def _has_symbolic_exponent(solution: Eq) -> bool:
    """Whether a power in the solution has an exponent that is not a
    number.

    Substituting a random rational for such an exponent picks a principal
    branch, and a correct solution can then leave a nonzero residual: the
    Bernoulli family ``(...)**(-1/(n - 1))`` verifies exactly at ``n = 2``
    and ``n = 3`` yet fails at a random rational ``n``. The numeric check
    cannot tell that from a wrong answer, so it declines to judge.
    """
    from sympy import Pow
    return any(not power.exp.is_number for power in solution.atoms(Pow))


def numeric_check(entry: Equation, solution: Eq, rng: random.Random, trials: int = 3) -> Optional[bool]:
    """``True`` if the residual vanishes at random points, ``False`` if it
    does not, ``None`` if it could not be evaluated."""
    if solution.has(Integral) or _has_symbolic_exponent(solution):
        return None
    parameters = sorted((solution.free_symbols | entry.equation.free_symbols) - {x}, key=str)
    outcomes: list[bool] = []
    for _ in range(trials):
        point: Point = {p: Rational(rng.randint(1, 9), rng.randint(1, 4)) for p in parameters}
        point[x] = Rational(rng.randint(1, 12), rng.randint(1, 5))
        if solution.lhs == y(x):
            r = _residual_explicit(entry.equation, as_expr(solution.rhs), point)
        else:
            r = _residual_implicit(entry.equation, as_expr(solution.lhs - solution.rhs), entry.order, point)
        if r is None or not r.is_finite:
            continue
        if not _real_here(solution, point):
            # the closed form is on a branch the equation is not: a real
            # solution written with log or a fractional power evaluates
            # complex outside its interval, and the residual there says
            # nothing about whether the solution is right
            continue
        outcomes.append(bool(abs(r) < TOLERANCE))
    if not outcomes:
        return None
    return all(outcomes)


def _real_here(solution: Eq, point: Point) -> bool:
    """Whether the solution takes a finite real value at the point.

    Only such a point can falsify a solution of a real equation. Without
    this the check reports a correct answer as wrong whenever the random
    point lands where a logarithm or a fractional power turns complex --
    ``exp(x*log(x - 1))/(x - 1)`` at ``x < 1``, say.
    """
    value = solution.rhs if solution.lhs == y(x) else solution.lhs - solution.rhs
    try:
        evaluated = N(value.subs(point), PRECISION)
    except (TypeError, ValueError, ZeroDivisionError, ArithmeticError):
        return False
    if not evaluated.is_number or evaluated.has(zoo, nan, oo):
        return False
    imaginary = im(evaluated)
    if not imaginary.is_number:
        return False
    return bool(abs(imaginary) < TOLERANCE)


def verify(entry: Equation, rng: random.Random, timeout: float) -> tuple[str, list[str]]:
    """``(status, one line per solution)`` for one equation.

    A stack overflow is contained here rather than left to end the sweep:
    ``sympy_extras._timeout.attempt`` does not catch ``RecursionError``
    (sympy-extras#49), and one equation deep inside SymPy would otherwise
    discard the results of every equation before it.
    """
    try:
        solutions = attempt(lambda: solve_ode(entry.equation, y(x), check=False, timeout=timeout),
                            4*timeout)
    except RecursionError:
        return 'failed (recursion)', []
    if not solutions:
        return 'failed', []
    verdicts: list[str] = []
    for sol in solutions:
        symbolic = attempt(lambda: checkodesol(entry.equation, sol, y(x)), timeout)
        symbolic_ok = symbolic is not None and bool(symbolic[0])
        numeric = attempt(lambda: numeric_check(entry, sol, rng), timeout)
        if numeric is False:
            verdicts.append('WRONG: %s' % sol)
        elif numeric or symbolic_ok:
            verdicts.append('verified: %s' % sol)
        else:
            verdicts.append('unverified: %s' % sol)
    if any(v.startswith('WRONG') for v in verdicts):
        status = 'WRONG'
    elif any(v.startswith('verified') for v in verdicts):
        status = 'verified'
    else:
        status = 'unverified'
    return status, verdicts


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=int, default=20)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--timeout', type=float, default=20.0)
    parser.add_argument('--collections', default='kamke1,kamke2')
    args = parser.parse_args(argv)
    rng = random.Random(args.seed)
    entries = load(tuple(args.collections.split(',')))
    if not entries:
        print("no equations could be loaded")
        return 1
    sample = rng.sample(entries, min(args.sample, len(entries)))
    counts: dict[str, int] = {}
    for entry in sample:
        started = time.time()
        status, verdicts = verify(entry, rng, args.timeout)
        counts[status] = counts.get(status, 0) + 1
        print("%-10s order %d %-10s %5.1fs  %s" % (entry.name, entry.order, status, time.time() - started, entry.equation), flush=True)
        for v in verdicts:
            print("    ", v)
    print()
    print("sample:", len(sample), dict(sorted(counts.items())))
    return 1 if counts.get('WRONG') else 0


if __name__ == '__main__':
    sys.exit(main())
