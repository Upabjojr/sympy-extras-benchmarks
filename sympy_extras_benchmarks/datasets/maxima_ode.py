"""The Kamke and Murphy collections of ordinary differential equations, as
transcribed in the test suite of Maxima's ``contrib_ode`` package.

The collections
===============

E. Kamke, *Differentialgleichungen: Lösungsmethoden und Lösungen* (1961)
lists about 1500 ordinary differential equations with their solutions;
G. M. Murphy, *Ordinary Differential Equations and Their Solutions* (1960)
about 2300. Maxima's ``share/contrib/diffequations/tests`` transcribes the
first order equations of both (``rtestode_kamke_1_*.mac``,
``rtestode_murphy_1_*.mac``, chapters 1 of the books), the second order
equations of Kamke (``rtestode_kamke_2_*.mac``) and the first order
equations of higher degree of Murphy (``rtestode_murphy_2_*.mac``,
chapter 2 of Murphy: equations polynomial in ``y'``). The same directory
holds Maxima's own regression files for Abel and Riccati equations,
symmetries and ``odelin``, in the same format.

Every entry of a test file has the form ::

    /* 12 */
    (pn_(12),ans:contrib_ode(eqn:'diff(y,x)+a*y-b*sin(c*x),y,x));
    [y = ...];
    [method,ode_check(eqn,ans[1])];
    [linear,0];

Only the equation ``eqn`` (a mathematical fact from the books) and the
one-word classification of the method are read; Maxima's solutions and
code are not used.

Source and licence
==================

Maxima is distributed under the **GNU General Public License, version 2**.
Its test files are kept in this repository under that licence, in
``data/maxima/`` with Maxima's ``COPYING`` beside them (see
``data/README.md``), and are read from there; a local Maxima installation
named by ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS`` is read instead, and a
file which is in neither is fetched into the cache (a sparse checkout of
Maxima's git repository on SourceForge, or the files of the GitHub
mirror). Only the equations — facts from Kamke's and Murphy's books — and
the one-word method classification are read.

The parser
==========

The equations are read by the Maxima expression parser of
:mod:`~sympy_extras_benchmarks.parsers.maxima`: the dependent variable
becomes ``y(x)`` and Maxima's names become SymPy's. This module reads the
structure of the test files around it: the ``pn_(n)`` entries, the
``contrib_ode`` call and the method classification.

Examples
========

>>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_file
>>> entries, skipped = parse_file("(pn_(1),ans:contrib_ode(eqn:'diff(y,x)^2 + a*y*'diff(y,x) = a*x,y,x));", 'demo')
>>> entries
[ODEEntry(demo.1, -a*x + a*y(x)*Derivative(y(x), x) + Derivative(y(x), x)**2)]
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
import urllib.request
from typing import Callable, Optional, Sequence

from sympy import Symbol
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef, UndefinedFunction

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.maxima import (
    MaximaSyntaxError, call_arguments, derivative_order, parse_expression, undefined_function, x, y)

__all__ = ['ODEEntry', 'COLLECTIONS', 'FILES', 'fetch', 'load', 'parse_file']

#: Maxima's git repository (SourceForge) and the directory of the tests
REPOSITORY = "https://git.code.sf.net/p/maxima/code"
SUBDIRECTORY = "share/contrib/diffequations/tests"
#: Maxima's own regression tests, read by
#: :mod:`~sympy_extras_benchmarks.datasets.polynomial_solving`
TESTS_SUBDIRECTORY = "tests"
#: the raw files of the GitHub mirror and of SourceForge's browser, as fallbacks
MIRRORS = (
    "https://raw.githubusercontent.com/calyau/maxima/master/%s/%s.mac",
    "https://sourceforge.net/p/maxima/code/ci/master/tree/%s/%s.mac?format=raw",
)
#: a local directory with the ``.mac`` files (a Maxima installation)
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS'

#: the test files of each collection
FILES: dict[str, tuple[str, ...]] = {
    'kamke1': tuple('rtestode_kamke_1_%d' % k for k in range(1, 7)),
    'kamke2': tuple('rtestode_kamke_2_%d' % k for k in range(1, 6)),
    'murphy1': tuple('rtestode_murphy_1_%d' % k for k in range(1, 7)),
    'murphy2': tuple('rtestode_murphy_2_%d' % k for k in range(1, 6)),
    'abel': ('rtest_ode1_abel',),
    'riccati': ('rtest_ode1_riccati',),
    'odelin': ('rtestode_odelin',),
}
#: the collections used in the benchmarks of sympy-extras, in order
COLLECTIONS: tuple[str, ...] = ('kamke1', 'kamke2', 'murphy1', 'murphy2')


class ODEEntry:
    """One equation of a collection.

    Attributes
    ==========

    collection : str
        ``'kamke1'``, ``'kamke2'``, ``'murphy1'`` or ``'murphy2'``.
    number : int
        The number of the equation in the book (and in Maxima's file).
    name : str
        ``collection.number``, with a letter appended when the file has
        several equations under the same number.
    source : str
        The Maxima text of the equation.
    equation : Expr
        The equation as ``lhs - rhs``, in ``y(x)``.
    order : int
        The order of the highest derivative of ``y(x)``.
    method : str
        Maxima's one-word classification of the equation (``'linear'``,
        ``'riccati'``, ``'abel'``, ...), or ``''`` when the file does not
        state it.
    """

    def __init__(self, collection: str, number: int, name: str, source: str,
                 equation: Expr, method: str = '') -> None:
        self.collection = collection
        self.number = number
        self.name = name
        self.source = source
        self.equation = equation
        self.order = derivative_order(equation, y(x))
        self.method = method

    @property
    def function(self) -> AppliedUndef:
        """The dependent variable, ``y(x)``."""
        return y(x)

    @property
    def variable(self) -> Symbol:
        """The independent variable, ``x``."""
        return x

    @property
    def parameters(self) -> list[Symbol]:
        """The symbolic parameters of the equation, sorted by name."""
        return sorted((s for s in self.equation.free_symbols if isinstance(s, Symbol) and s != x),
                      key=lambda s: s.name)

    @property
    def arbitrary_functions(self) -> list[UndefinedFunction]:
        """The undefined functions other than ``y`` (``f(x)``, ``g(x)``, ...)."""
        found: dict[str, UndefinedFunction] = {}
        for applied in self.equation.atoms(AppliedUndef):
            head = applied.func
            if isinstance(head, UndefinedFunction) and head != y:
                found[str(head)] = head
        return [found[k] for k in sorted(found)]

    def __repr__(self) -> str:
        return "ODEEntry(%s, %s)" % (self.name, self.equation)


# ---------------------------------------------------------------------------
# the test files

_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_ENTRY = re.compile(r"pn_\(\s*(\d+)\s*\)\s*,\s*ans\s*:\s*contrib_ode\s*\(\s*eqn\s*:")
_METHOD = re.compile(r"\[\s*method\s*,\s*ode_check\s*\(.*?\]\s*;\s*\[\s*([A-Za-z_0-9]+)\s*,", re.S)


def parse_file(text: str, collection: str) -> tuple[list[ODEEntry], list[tuple[str, str]]]:
    """The entries of a test file, and the ``(number, source)`` pairs which
    could not be translated (a reference to another equation, a function the
    parser does not know, ...).

    Examples
    ========

    >>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_file
    >>> text = '''
    ... /* 3 */
    ... (pn_(3),ans:contrib_ode(eqn:'diff(y,x)=x+y,y,x));
    ... [y = %e^x*(-x-1)*%e^-x+%c];
    ... [method,ode_check(eqn,ans[1])];
    ... [linear,0];
    ... '''
    >>> entries, skipped = parse_file(text, 'demo')
    >>> entries
    [ODEEntry(demo.3, -x - y(x) + Derivative(y(x), x))]
    >>> entries[0].method, skipped
    ('linear', [])
    """
    text = _COMMENT.sub('', text)
    entries: list[ODEEntry] = []
    skipped: list[tuple[str, str]] = []
    names: dict[str, int] = {}
    for match in _ENTRY.finditer(text):
        number = match.group(1)
        parsed = call_arguments(text, match.end())
        if parsed is None:
            skipped.append((number, text[match.end():match.end() + 80]))
            continue
        args, end = parsed
        if len(args) != 3:
            skipped.append((number, ','.join(args)))
            continue
        source, dependent, independent = (a.strip() for a in args)
        try:
            equation = parse_expression(source, dependent, independent)
        except (MaximaSyntaxError, ValueError, TypeError, ZeroDivisionError):
            skipped.append((number, source))
            continue
        if dependent != 'y' or independent != 'x':
            equation = as_expr(equation.subs({Symbol(independent): x}).subs(
                {undefined_function(dependent)(x): y(x)}))
        if derivative_order(equation, y(x)) == 0:
            skipped.append((number, source))
            continue
        method = ''
        after = text[end:end + 400]
        next_entry = _ENTRY.search(after)
        method_match = _METHOD.search(after[:next_entry.start()] if next_entry else after)
        if method_match:
            method = method_match.group(1)
        name = "%s.%s" % (collection, number)
        count = names.get(name, 0)
        names[name] = count + 1
        if count:
            name += chr(ord('a') + count)
        entries.append(ODEEntry(collection, int(number), name, source, equation, method))
    return entries, skipped


def _local_directory() -> Optional[pathlib.Path]:
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    return None


def _clone(target: pathlib.Path, subdirectory: str = SUBDIRECTORY) -> bool:
    """A sparse checkout of the test directories of Maxima's repository."""
    if (target / subdirectory).is_dir():
        return True
    try:
        if not (target / '.git').is_dir():
            subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                            REPOSITORY, str(target)], check=True, capture_output=True, timeout=900)
        subprocess.run(['git', '-C', str(target), 'sparse-checkout', 'set',
                        SUBDIRECTORY, TESTS_SUBDIRECTORY],
                       check=True, capture_output=True, timeout=900)
    except (subprocess.SubprocessError, OSError):
        return False
    return (target / subdirectory).is_dir()


def _download(name: str, target: pathlib.Path, subdirectory: str = SUBDIRECTORY) -> Optional[str]:
    for pattern in MIRRORS:
        try:
            with urllib.request.urlopen(pattern % (subdirectory, name), timeout=60) as response:
                text = response.read().decode('utf-8', errors='replace')
        except OSError:
            continue
        # a mirror answers a missing file with a web page, not Maxima source
        if '<html' not in text[:400].lower():
            target.write_text(text)
            return text
    return None


def fetch(name: str, subdirectory: str = SUBDIRECTORY) -> Optional[str]:
    """The text of the test file ``name`` (without extension): from the
    directory named by ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``, from the
    cache, from a sparse clone of Maxima's repository, or from the mirrors;
    ``None`` when none of them is reachable.

    ``subdirectory`` is where in the repository to look: the collections
    live under :data:`SUBDIRECTORY`, Maxima's own regression files under
    :data:`TESTS_SUBDIRECTORY`."""
    local = _local_directory()
    if local is not None and (local / (name + '.mac')).is_file():
        return (local / (name + '.mac')).read_text(errors='replace')
    kept = bundled('maxima', 'repository', subdirectory, name + '.mac')
    if kept is not None:
        return kept.read_text(errors='replace')
    cache = cache_directory() / 'maxima'
    cache.mkdir(parents=True, exist_ok=True)
    clone = cache / 'repository'
    path = clone / subdirectory / (name + '.mac')
    if path.is_file():
        return path.read_text(errors='replace')
    copy = cache / (name + '.mac')
    if copy.is_file():
        return copy.read_text(errors='replace')
    if _clone(clone, subdirectory) and path.is_file():
        return path.read_text(errors='replace')
    return _download(name, copy, subdirectory)


def load(collections: Sequence[str] = ('kamke1', 'kamke2'),
         report: Optional[Callable[[str], None]] = None) -> list[ODEEntry]:
    """The entries of the collections which could be fetched and parsed, in
    the order of the files. ``report`` receives a line for every file and
    every skipped entry."""
    entries: list[ODEEntry] = []
    for collection in collections:
        if collection not in FILES:
            raise ValueError("unknown collection %r; known: %s" % (collection, ', '.join(FILES)))
        for name in FILES[collection]:
            text = fetch(name)
            if text is None:
                if report is not None:
                    report("%s: could not be fetched" % name)
                continue
            parsed, skipped = parse_file(text, collection)
            entries.extend(parsed)
            if report is not None:
                report("%s: %d equations, %d skipped" % (name, len(parsed), len(skipped)))
                for number, source in skipped:
                    report("  skipped %s.%s: %s" % (collection, number, source.strip()[:100]))
    return entries


if __name__ == '__main__':
    loaded = load(COLLECTIONS, report=print)
    by_collection: dict[str, int] = {}
    for entry in loaded:
        by_collection[entry.collection] = by_collection.get(entry.collection, 0) + 1
    print(by_collection, sum(by_collection.values()))
