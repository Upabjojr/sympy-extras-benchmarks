"""Definite integrals from the test file of REDUCE's DEFINT package, as
SymPy expressions.

The dataset
===========

REDUCE's DEFINT package (K. Gaskell and W. Neun, ZIB, and S. L. Kameny)
evaluates a definite integral by writing each factor of the integrand as a
Meijer G-function and integrating their product with the Meijer G
integration formula — the method of Adamchik and Marichev, and the one
SymPy's ``meijerint`` implements. Its test file ``defint.tst`` is
therefore a test of exactly that method: mostly integrals over
``(0, infinity)`` of products of powers, exponentials, trigonometric and
hyperbolic functions, Bessel functions, the exponential, sine and
hyperbolic sine integrals and the error function, collected by Kerry
Gaskell at ZIB in 1993–94, then the same functions over ``(0, y)``, and
last a few Gaussian integrals the package could not do.

What is read, and what is not
=============================

The four-argument calls ``int(f, x, a, b)``. REDUCE's syntax is rewritten
into Maxima's (:func:`~sympy_extras_benchmarks.datasets.reduce_odes.to_maxima`)
and read with the Maxima expression parser; REDUCE ignores case, so
``BesselJ`` is ``besselj``.

Not read:

* the transforms the file also exercises (``laplace_transform``,
  ``hankel_transform``, ``fourier_sin``, ...): their kernels and
  normalisations are the package's own definitions;
* REDUCE's results (the ``defint.rlg`` log beside the test file) and its
  code;
* the Fresnel integrals, whose normalisation in REDUCE is not the one
  the translated names would assume; they are refused rather than guessed.

Source and licence
==================

REDUCE is distributed under the *Reduce License*, a **BSD 2-clause**
style licence. ``packages/defint`` is kept under it in ``data/reduce/``
with REDUCE's ``LICENSE`` beside it (see ``data/README.md``) and read from
there, or from ``$SYMPY_EXTRAS_BENCHMARKS_REDUCE``; if neither is there
it is added to the sparse clone of REDUCE in the cache.

Examples
========

>>> from sympy_extras_benchmarks.datasets.reduce_defint import integrals
>>> text = "% a comment\\nint(y^2*BesselK(1,y),y,0,infinity);\\nint(e^(-1/3t)*sin t,t,0,pi);\\n"
>>> first, second = integrals(text, 'demo')
>>> first
DefiniteIntegral(demo:1, y from 0 to oo, recorded None)
>>> first.integrand
y**2*besselk(1, y)
>>> second.integrand, second.upper
(exp(-t/3)*sin(t), pi)
"""
from __future__ import annotations

import pathlib
import re

from sympy import Symbol

from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.parsers.maxima import group, parse, split_arguments
from sympy_extras_benchmarks.datasets.reduce_odes import package_directory
from sympy_extras_benchmarks.parsers.reduce import strip_comments, to_maxima_names

__all__ = ['SUBTREE', 'FILES', 'LICENCE', 'LICENCE_FILES', 'integrals', 'fetch', 'load',
           'licence_files', 'to_maxima_names']

SUBTREE = 'packages/defint'
FILES: tuple[str, ...] = ('defint.tst',)
#: the licence, and the file at the root of REDUCE's repository carrying it,
#: which the sparse clone keeps
LICENCE = 'Reduce License (BSD 2-clause style)'
LICENCE_FILES: tuple[str, ...] = ('LICENSE',)

_CALL = re.compile(r"(?<![\w%])int\s*\(")


def integrals(text: str, name: str = '') -> list[DefiniteIntegral]:
    """Every four-argument ``int`` call of a REDUCE file that can be read."""
    body = strip_comments(text)
    found: list[DefiniteIntegral] = []
    for index, match in enumerate(_CALL.finditer(body), start=1):
        closed = group(body, match.end() - 1)
        if closed is None:
            continue
        arguments = split_arguments(closed[0])
        if len(arguments) != 4:
            continue
        parts = [parse(to_maxima_names(a)) for a in arguments]
        integrand, variable, lower, upper = parts
        if (integrand is None or lower is None or upper is None
                or not isinstance(variable, Symbol)):
            continue
        found.append(DefiniteIntegral('%s:%d' % (name, index), integrand, variable, lower, upper))
    return found


def licence_files() -> list[pathlib.Path]:
    """The licence files kept with the fetched package."""
    directory = package_directory(SUBTREE)
    if directory is None:
        return []
    root = directory.parent.parent if directory.name == SUBTREE.split('/')[-1] else directory
    return [root / name for name in LICENCE_FILES if (root / name).is_file()]


def fetch() -> list[tuple[str, str]]:
    """``(file name, text)`` of the test file, when it could be got."""
    directory = package_directory(SUBTREE)
    if directory is None:
        return []
    found: list[tuple[str, str]] = []
    for file in FILES:
        path = directory / file
        if path.is_file():
            found.append((file.split('.')[0], path.read_text(errors='replace')))
    return found


def load() -> list[DefiniteIntegral]:
    """Every readable definite integral of the test file."""
    found: list[DefiniteIntegral] = []
    for name, text in fetch():
        found.extend(integrals(text, name))
    return found
