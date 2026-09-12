"""Indefinite integrals from the test suites of Maxima and FriCAS, as SymPy
expressions.

The dataset
===========

Two sources, about 1400 calls, each an integrand and a variable, with the
facts in force and, where the source records one, a reference
antiderivative:

* Maxima's ``tests/rtest_integrate.mac``, the general integration file
  (the bulk: exponentials, logarithms, radicals, trigonometric and
  hyperbolic functions, the cases of its Risch and rational routines),
  ``rtestint.mac`` (the indefinite part of the definite-integration
  regression file: rational functions and algebraic radicals),
  ``rtest14.mac`` (Airy and Bessel functions), ``rtest7.mac``, and the
  indefinite integrals of M. Wester's *Critique of the Mathematical
  Abilities of CA Systems* (``wester_problems/test_indefinite_integrals.mac``,
  a demonstration without recorded values). The definite calls of these
  files belong to :mod:`~sympy_extras_benchmarks.datasets.maxima_integrals`;
  this module reads the two-argument ones it skips;
* FriCAS's ``src/input/integ.input``: the ``testIntegrate(f, x, issue)``
  assertions, most of them regression cases of FriCAS's integrator named by
  the issue they fixed (the transcendental Risch cases, the algebraic ones
  after Trager, the Abel and the Masser–Zannier examples), each of which
  asserts that the integral is found and that its derivative is the
  integrand; and the ``testEquals("integrate(f, x)", "F")`` statements,
  which record ``F``. The ``xf1testIntegrate``/``xf2testIntegrate``
  variants mark cases FriCAS itself cannot do; they assert nothing and are
  not read.

What is read, and what is not
=============================

The Maxima files are read as in
:mod:`~sympy_extras_benchmarks.datasets.maxima_integrals`: the context
(``assume``, ``declare``, ``assume_pos``, assigned values) is followed
through the file, calls inside binding constructs and under assumptions
the reader does not translate are refused, and the recorded value is kept
only when the statement is the call itself, possibly under a
value-preserving simplification. A recorded antiderivative is a **third
opinion**: the source's own system computed it, it may differ from another
correct one by a constant, and it may be wrong. A driver checks a result
by differentiation, never against the recorded value.

Source and licence
==================

Maxima is distributed under the **GNU General Public License, version 2**
(Wester's problems under the same licence by their author); FriCAS under
the **modified (3-clause) BSD licence**. Nothing of either is stored in this
repository: the files are fetched on first use into the cache directory
(or read from ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS`` and
``$SYMPY_EXTRAS_BENCHMARKS_FRICAS``). Only the calls, the facts and the
recorded values are read; the systems' code and their test harnesses are
not used.

Examples
========

>>> from sympy_extras_benchmarks.datasets.indefinite_integrals import maxima_indefinite, fricas_indefinite
>>> entry, = maxima_indefinite("integrate(cos(u), u);\\nsin(u)$\\n", 'demo')
>>> entry
IndefiniteIntegral(demo:1, cos(u) in u, recorded sin(u))
>>> entry.integral()
Integral(cos(u), u)
>>> found = fricas_indefinite('testIntegrate("(x+1)*exp(x)", "x", "rde")\\n'
...                           'testEquals("integrate(cos(x)/(1 + cos(x)), x)", "-sin(x)/(1 + cos(x)) + x")\\n', 'demo')
>>> [e.integrand for e in found], found[1].recorded
([(x + 1)*exp(x), cos(x)/(cos(x) + 1)], x - sin(x)/(cos(x) + 1))
"""
from __future__ import annotations

import pathlib
import re
from typing import Optional, Sequence

from sympy import Gt, Integral, Symbol, sympify
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.datasets import fricas_integrals
from sympy_extras_benchmarks.datasets.integrals import group, parse, relation, split_arguments
from sympy_extras_benchmarks.datasets.maxima_integrals import (
    _BINDING, _CALL, _LOOP, _PRESERVING, _PRINCIPAL, _Context, _application, _enclosing, _items, _peeled,
    licence_files as maxima_licence_files, statements)
from sympy_extras_benchmarks.datasets.maxima_ode import TESTS_SUBDIRECTORY, fetch as fetch_maxima

__all__ = ['IndefiniteIntegral', 'MAXIMA_FILES', 'FRICAS_FILES', 'COLLECTIONS', 'LICENCES',
           'maxima_indefinite', 'fricas_indefinite', 'fetch', 'load', 'licence_files']

#: each Maxima collection: the file, its subdirectory, and whether a
#: recorded value follows every statement
MAXIMA_FILES: dict[str, tuple[str, str, bool]] = {
    'rtest_integrate': ('rtest_integrate', TESTS_SUBDIRECTORY, True),
    'rtestint': ('rtestint', TESTS_SUBDIRECTORY, True),
    'rtest14': ('rtest14', TESTS_SUBDIRECTORY, True),
    'rtest7': ('rtest7', TESTS_SUBDIRECTORY, True),
    'wester': ('test_indefinite_integrals', TESTS_SUBDIRECTORY + '/wester_problems', False),
}
#: the FriCAS collections: the input file of each
FRICAS_FILES: dict[str, str] = {'fricas_integ': 'integ.input'}
COLLECTIONS: tuple[str, ...] = tuple(MAXIMA_FILES) + tuple(FRICAS_FILES)
#: the licence of each collection
LICENCES: dict[str, str] = {**{c: 'GPL-2.0' for c in MAXIMA_FILES},
                            **{c: fricas_integrals.LICENCE for c in FRICAS_FILES}}

#: a FriCAS assertion that the integral is found (``xf`` variants excluded)
_TEST_INTEGRATE = re.compile(r"(?<![\w])testIntegrate\s*\(")
_TEST_EQUALS = re.compile(r"(?<![\w])testEquals\s*\(")


class IndefiniteIntegral:
    """One indefinite integral of a collection.

    Attributes
    ==========

    name : str
        The collection and the position of the integral in it.
    integrand : Expr
    variable : Symbol
    facts : tuple of Boolean
        Relations the source assumes about the parameters.
    properties : tuple of (Symbol, str)
        Declared properties of the parameters (``(n, 'integer')``).
    recorded : Expr or None
        The antiderivative the source records, or ``None``.
    """

    def __init__(self, name: str, integrand: object, variable: Symbol,
                 facts: Sequence[Boolean] = (), properties: Sequence[tuple[Symbol, str]] = (),
                 recorded: Optional[object] = None) -> None:
        self.name = name
        self.integrand = as_expr(sympify(integrand))
        self.variable = variable
        self.facts = tuple(facts)
        self.properties = tuple(properties)
        self.recorded = None if recorded is None else as_expr(sympify(recorded))

    @property
    def parameters(self) -> list[Symbol]:
        """The symbols other than the variable, sorted by name."""
        found = {s for s in self.integrand.free_symbols if isinstance(s, Symbol)}
        found.discard(self.variable)
        return sorted(found, key=lambda s: s.name)

    def integral(self) -> Integral:
        """The unevaluated SymPy integral."""
        return Integral(self.integrand, self.variable)

    def key(self) -> tuple[Expr, Symbol]:
        return (self.integrand, self.variable)

    def __repr__(self) -> str:
        return "IndefiniteIntegral(%s, %s in %s, recorded %s)" % (
            self.name, self.integrand, self.variable, self.recorded)


#: the identifiers of an assumption the reader does not translate
_IDENTIFIER = re.compile(r"[A-Za-z_%][\w%]*")
#: names that are not parameters in an assumption
_NOT_PARAMETERS = frozenset({'notequal', 'equal', 'ratsimp', 'log', 'sqrt', 'exp', 'abs', 'sin', 'cos',
                             'tan', 'true', 'false', 'inf', 'minf', 'infinity', 'and', 'or', 'not'})


class _IndefiniteContext(_Context):
    """The context of :class:`~sympy_extras_benchmarks.datasets.maxima_integrals._Context`,
    with an assumption the reader does not translate remembered by the
    names it mentions and released by the ``forget`` of an assumption
    about the same names, rather than refusing everything after it (the
    definite reader refuses the rest of the file; ``rtest_integrate``
    assumes ``notequal(ratsimp(...), -1)`` early and would lose 470
    integrals about other parameters)."""

    def __init__(self) -> None:
        super().__init__()
        self.untranslated: list[frozenset[str]] = []

    def clear(self) -> None:
        super().clear()
        self.untranslated = []

    def apply(self, item: str) -> bool:
        application = _application(item)
        if application is not None and application[0] in ('assume', 'forget'):
            name, arguments = application
            for argument in arguments:
                names = frozenset(_IDENTIFIER.findall(argument)) - _NOT_PARAMETERS
                if name == 'assume':
                    if relation(argument) is None:
                        self.untranslated.append(names)
                elif names in self.untranslated:
                    # Maxima prints the forgotten fact in its own form: the
                    # names it mentions identify it
                    self.untranslated.remove(names)
        changed = super().apply(item)
        if application is not None and application[0] in ('assume', 'forget', 'killcontext'):
            self.unreadable = False
        return changed

    def refuses(self, parameters: set[Symbol]) -> bool:
        """Whether an untranslated assumption mentions a parameter."""
        names = {p.name for p in parameters}
        return any(names & mentioned for mentioned in self.untranslated)


def _indefinite_call(item: str, match: re.Match[str], context: _Context
                     ) -> Optional[tuple[Expr, Symbol]]:
    """The integrand and the variable of a two-argument ``integrate`` call,
    with the context's values substituted."""
    if match.group(2) != 'integrate':
        return None
    closed = group(item, match.end() - 1)
    if closed is None or any(n in _BINDING for n in _enclosing(item, match.start())):
        return None
    arguments = split_arguments(closed[0])
    if len(arguments) != 2:
        return None
    integrand, variable = parse(arguments[0]), parse(arguments[1])
    if integrand is None or not isinstance(variable, Symbol) or variable in context.values:
        return None
    unknown = {s for s, v in context.values.items() if v is None}
    known = {s: v for s, v in context.values.items() if v is not None}
    substituted = as_expr(integrand.xreplace(known))
    if substituted.free_symbols & unknown:
        return None
    return substituted, variable


def maxima_indefinite(text: str, collection: str = '', values_follow: bool = True
                      ) -> list[IndefiniteIntegral]:
    """Every indefinite integral of a Maxima test file that can be read,
    the context followed as in
    :func:`~sympy_extras_benchmarks.datasets.maxima_integrals.integrals`."""
    parts = statements(text)
    context = _IndefiniteContext()
    found: list[IndefiniteIntegral] = []
    step = 2 if values_follow else 1
    for number, index in enumerate(range(0, len(parts), step), start=1):
        statement = parts[index]
        expected = parts[index + 1] if values_follow and index + 1 < len(parts) else None
        if ':=' in statement:
            continue
        items, flags = _items(statement)
        if any(_PRINCIPAL.fullmatch(f) for f in flags):
            continue
        flags_preserve = all(f in _PRESERVING for f in flags)
        loop = _LOOP.search(statement) is not None
        ordinal = 0
        for position, item in enumerate(items):
            if context.apply(item) or loop:
                continue
            for match in _CALL.finditer(item):
                read = _indefinite_call(item, match, context)
                if read is None or context.unreadable:
                    continue
                integrand, variable = read
                entry = IndefiniteIntegral('', integrand, variable)
                parameters = set(entry.parameters)
                if parameters & context.opaque or context.refuses(parameters):
                    continue
                known = {s: v for s, v in context.values.items() if v is not None}
                facts = [as_boolean(f.xreplace(known)) for f in context.facts]
                facts = [f for f in facts if f.free_symbols and f.free_symbols <= parameters]
                if context.positive:
                    facts += [as_boolean(Gt(p, 0)) for p in entry.parameters]
                properties = [(p, prop) for p in entry.parameters
                              for prop in sorted(context.properties.get(p, set()))]
                recorded = None
                call_end = group(item, match.end() - 1)
                if (expected is not None and not match.group(1) and flags_preserve
                        and position == len(items) - 1 and call_end is not None
                        and _peeled(item) == item[match.start():call_end[1]]):
                    recorded = parse(expected)
                    if recorded is not None and recorded.has(Integral):
                        recorded = None                     # Maxima gave up: no reference
                ordinal += 1
                name = '%s:%d' % (collection, number) + ('.%d' % ordinal if ordinal > 1 else '')
                found.append(IndefiniteIntegral(name, integrand, variable, facts, properties, recorded))
    return found


def _joined(text: str) -> str:
    """A FriCAS input without its ``--`` comments and system commands, the
    continuation lines (ending in ``_``) joined."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(('--', ')')):
            lines.append('')
            continue
        lines.append(re.sub(r"\s--.*$", '', line))
    return re.sub(r"_\s*\n", '', "\n".join(lines))


def _quoted(argument: str) -> Optional[str]:
    """The text of a FriCAS string literal, or of adjacent literals over
    several lines joined; ``None`` for anything else.

    >>> from sympy_extras_benchmarks.datasets.indefinite_integrals import _quoted
    >>> _quoted('"(x+1)*"   "exp(x)"'), _quoted('f: String')
    ('(x+1)*exp(x)', None)
    """
    body = argument.strip()
    if '_"' in body or not re.fullmatch(r'(\s*"[^"]*"\s*)+', body):
        return None
    return ''.join(re.findall(r'"([^"]*)"', body))


def fricas_indefinite(text: str, collection: str = '') -> list[IndefiniteIntegral]:
    """Every indefinite integral asserted by a FriCAS test input:
    ``testIntegrate("f", "x", "issue")`` and ``testEquals("integrate(f, x)",
    "F")``, each integral once."""
    body = _joined(text)
    found: list[IndefiniteIntegral] = []
    seen: set[tuple[Expr, Symbol]] = set()
    number = 0
    calls: list[tuple[int, str, list[str]]] = []
    for pattern, kind in ((_TEST_INTEGRATE, 'integrate'), (_TEST_EQUALS, 'equals')):
        for match in pattern.finditer(body):
            closed = group(body, match.end() - 1)
            if closed is not None:
                calls.append((match.start(), kind, split_arguments(closed[0])))
    for _, kind, arguments in sorted(calls):
        recorded: Optional[Expr] = None
        if kind == 'integrate':
            if len(arguments) != 3:
                continue
            strings = [_quoted(a) for a in arguments[:2]]
            if any(s is None for s in strings):
                continue
            integrand_text, variable_text = str(strings[0]), str(strings[1])
        else:
            if len(arguments) != 2:
                continue
            call, answer = _quoted(arguments[0]), _quoted(arguments[1])
            if call is None or answer is None:
                continue
            inner = re.fullmatch(r"\s*integrate\s*\((.*)\)\s*", call, re.S)
            if inner is None:
                continue
            parts = split_arguments(inner.group(1))
            if len(parts) != 2:
                continue                                    # a definite integral
            integrand_text, variable_text = parts
            recorded = parse(fricas_integrals.to_maxima(answer))
        integrand = parse(fricas_integrals.to_maxima(integrand_text))
        variable = parse(variable_text)
        if integrand is None or not isinstance(variable, Symbol) or not integrand.has(variable):
            continue
        number += 1
        if (integrand, variable) in seen:
            continue
        seen.add((integrand, variable))
        found.append(IndefiniteIntegral('%s:%d' % (collection, number), integrand, variable,
                                        recorded=recorded))
    return found


def licence_files() -> list[pathlib.Path]:
    """The licence files kept with the fetched data of both sources."""
    return maxima_licence_files() + fricas_integrals.licence_files()


def fetch(collections: Sequence[str] = COLLECTIONS) -> list[tuple[str, str]]:
    """``(collection, text)`` for every collection whose file could be got."""
    found: list[tuple[str, str]] = []
    fricas_directory: Optional[pathlib.Path] = None
    for collection in collections:
        if collection in MAXIMA_FILES:
            name, subdirectory, _ = MAXIMA_FILES[collection]
            text = fetch_maxima(name, subdirectory)
            if text is not None:
                found.append((collection, text))
        elif collection in FRICAS_FILES:
            if fricas_directory is None:
                fricas_directory = fricas_integrals._directory()
            if fricas_directory is not None:
                path = fricas_directory / FRICAS_FILES[collection]
                if path.is_file():
                    found.append((collection, path.read_text(errors='replace')))
        else:
            raise ValueError("unknown collection %r; known: %s" % (collection, ', '.join(COLLECTIONS)))
    return found


def load(collections: Sequence[str] = COLLECTIONS) -> list[IndefiniteIntegral]:
    """Every readable indefinite integral of the collections."""
    found: list[IndefiniteIntegral] = []
    for collection, text in fetch(collections):
        if collection in MAXIMA_FILES:
            found.extend(maxima_indefinite(text, collection, MAXIMA_FILES[collection][2]))
        else:
            found.extend(fricas_indefinite(text, collection))
    return found
