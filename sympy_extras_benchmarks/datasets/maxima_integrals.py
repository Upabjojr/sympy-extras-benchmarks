"""Definite integrals and Laplace transforms from Maxima's test suite, as
SymPy expressions.

The dataset
===========

Five files of Maxima's test suite, together about 800 calls:

* ``rtestint.mac`` — the regression file of Maxima's definite integration
  code (``defint``): rational functions over the whole line, Fourier and
  Mellin type integrals, branch points, integrals that once came out
  wrong;
* ``rtest_integrate.mac`` — the general integration file, read for its
  definite integrals;
* ``wester_problems/test_definite_integrals.mac`` — the definite integrals
  of M. Wester's *A Critique of the Mathematical Abilities of CA Systems*
  (1999): principal values, branch choices, contour integrals, each with
  its reference. A demonstration file, so no value is recorded;
* ``rtest_laplace.mac`` — Laplace transforms;
* ``rtest_hypgeo.mac`` — Laplace transforms of special functions computed
  by ``specint``, beginning with the table of Abramowitz and Stegun 29.3.

A transform is a definite integral and is read as one:
``laplace(f, t, s)`` is the integral of ``f*exp(-s*t)`` over ``(0, oo)``,
and ``specint(g, t)`` the integral of ``g`` over ``(0, oo)`` — its argument
already carries the kernel.

What is read, and what is not
=============================

Each call, the facts in force when it runs, and the value recorded after
it:

* the context is followed through the file: ``assume``, ``forget``,
  ``kill``, ``killcontext``, and ``declare`` for the properties
  ``integer``, ``noninteger``, ``even``, ``odd`` and ``real``. With
  ``assume_pos: true`` Maxima takes every parameter to be positive, which
  is read as ``p > 0`` for each;
* a variable given a value (``R: c*x^2 + b*x + a``) is replaced by it,
  since that is what Maxima integrates.

Refused:

* a call inside a construct that binds names — ``block``, ``makelist``,
  ``lambda``, ``sum``, ``subst``, ``at``, ``ev``, a loop, a function
  definition — whose symbols are then not free;
* a call made with ``intanalysis`` false, under which Maxima returns the
  principal value of a divergent integral;
* a call under an assumption or a declaration this module does not read,
  and anything with a name the expression parser does not translate.

The recorded value is kept only when the statement *is* the call, possibly
under a simplification that does not change the value (``ratsimp``,
``radcan``, ``factor``, ``float``, ...); after ``round``, ``is``, ``diff``
or ``errcatch`` the file records a value of something else. It is a
**third opinion**, not the answer key (see
:mod:`~sympy_extras_benchmarks.datasets.integrals`).

Source and licence
==================

Maxima is distributed under the **GNU General Public License, version 2**;
Wester's problems were released under the same licence by their author
(``wester-gpl-permission-message.txt`` beside the file). Nothing of Maxima
is stored in this repository: the files are fetched on first use into the
cache directory, or read from ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``.
Only the calls, the facts and the recorded values are read; Maxima's code
is not used.

Examples
========

>>> from sympy_extras_benchmarks.datasets.maxima_integrals import integrals
>>> text = "assume(k > 0)$\\n[k > 0]$\\nintegrate(exp(-k*u), u, 0, inf);\\n1/k$\\n"
>>> entry, = integrals(text, 'demo')
>>> entry
DefiniteIntegral(demo:2, u from 0 to oo, recorded 1/k)
>>> entry.integrand, entry.facts
(exp(-k*u), (k > 0,))
>>> transform, = integrals("laplace(sinh(w), w, p);\\n1/(p^2-1)$\\n", 'demo')
>>> transform.integrand, transform.recorded
(exp(-p*w)*sinh(w), 1/(p**2 - 1))
"""
from __future__ import annotations

import pathlib
import re
from typing import Optional, Sequence

from sympy import Gt, Symbol, exp, oo
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.integrals import (
    PROPERTIES, DefiniteIntegral, group, parse, relation, split_arguments)
from sympy_extras_benchmarks.datasets.maxima_limits import strip_comments
from sympy_extras_benchmarks.datasets.maxima_ode import TESTS_SUBDIRECTORY, fetch as fetch_maxima

__all__ = ['FILES', 'COLLECTIONS', 'LICENCE', 'LICENCE_FILES', 'statements', 'integrals', 'fetch',
           'load', 'licence_files']

#: each collection: the file, where it lives in Maxima's repository, and
#: whether a recorded value follows every statement (the ``rtest`` format)
#: or the file is a demonstration without values
FILES: dict[str, tuple[str, str, bool]] = {
    'rtestint': ('rtestint', TESTS_SUBDIRECTORY, True),
    'rtest_integrate': ('rtest_integrate', TESTS_SUBDIRECTORY, True),
    'wester': ('test_definite_integrals', TESTS_SUBDIRECTORY + '/wester_problems', False),
    'laplace': ('rtest_laplace', TESTS_SUBDIRECTORY, True),
    'specint': ('rtest_hypgeo', TESTS_SUBDIRECTORY, True),
}
COLLECTIONS: tuple[str, ...] = tuple(FILES)
#: the licence, and the files of Maxima's repository that carry it: the GPL
#: itself and Wester's permission to release his problems under it. The
#: sparse clone keeps both beside the tests.
LICENCE = 'GPL-2.0'
LICENCE_FILES: tuple[str, ...] = ('COPYING', TESTS_SUBDIRECTORY + '/wester_problems/wester-gpl-permission-message.txt')

#: the calls read; a leading quote is the noun form, left unevaluated
_CALL = re.compile(r"(?<![\w%'])('?)(integrate|defint|laplace|specint)\s*\(")
#: constructs whose body sees names bound by the construct itself
_BINDING = frozenset({
    'block', 'makelist', 'create_list', 'lambda', 'sum', 'product', 'lsum', 'map', 'maplist',
    'subst', 'psubst', 'ratsubst', 'at', 'ev', 'buildq', 'assuming', 'apply', 'define',
    'funmake', 'sublist', 'every', 'some', 'tellsimp', 'tellsimpafter', 'defrule'})
#: functions and evaluation flags that do not change the value of their argument
_PRESERVING = frozenset({
    'ratsimp', 'fullratsimp', 'radcan', 'factor', 'expand', 'ratexpand', 'multthru',
    'trigsimp', 'trigreduce', 'trigexpand', 'logcontract', 'rootscontract', 'rectform',
    'demoivre', 'exponentialize', 'float', 'bfloat', 'numer'})
#: ``name: value``, but not ``name:: value`` or ``name := body``
_ASSIGNMENT = re.compile(r"([A-Za-z_%][\w%]*)\s*:(?![:=])(.*)", re.S)
#: ``name(arguments)`` spanning a whole item
_APPLICATION = re.compile(r"([A-Za-z_]\w*)\s*\(", re.S)
_LOOP = re.compile(r"\b(for|do|thru|while|unless)\b")
_PRINCIPAL = re.compile(r"intanalysis\s*[=:]\s*false")


def statements(text: str) -> list[str]:
    """The statements of a Maxima file, comments removed, without their
    ``;`` or ``$``.

    >>> statements('a: 1$ /* not ; here */ f(x; y); "s;t";')
    ['a: 1', 'f(x; y)', '"s;t"']
    """
    body = strip_comments(text)
    found: list[str] = []
    depth, start, quoted = 0, 0, False
    for index, character in enumerate(body):
        if character == '"' and (index == 0 or body[index - 1] != '\\'):
            quoted = not quoted
        elif quoted:
            continue
        elif character in '([{':
            depth += 1
        elif character in ')]}':
            depth = max(0, depth - 1)
        elif character in ';$' and depth == 0:
            statement = body[start:index].strip()
            if statement:
                found.append(statement)
            start = index + 1
    return found


def _application(item: str) -> Optional[tuple[str, list[str]]]:
    """``(name, arguments)`` when ``item`` is one call and nothing else."""
    match = _APPLICATION.match(item)
    if match is None:
        return None
    closed = group(item, match.end() - 1)
    if closed is None or closed[1] != len(item):
        return None
    return match.group(1), split_arguments(closed[0])


class _Context:
    """What Maxima knows about the names at a point of the file."""

    def __init__(self) -> None:
        self.facts: list[Boolean] = []
        self.properties: dict[Symbol, set[str]] = {}
        #: names declared with a property this module does not read
        self.opaque: set[Symbol] = set()
        #: assigned values; ``None`` for a value that did not translate
        self.values: dict[Symbol, Optional[Expr]] = {}
        #: an assumption that did not translate is in force
        self.unreadable = False
        #: ``assume_pos: true``
        self.positive = False
        #: ``intanalysis: false``
        self.principal = False

    def clear(self) -> None:
        self.facts, self.properties, self.opaque, self.values = [], {}, set(), {}
        self.unreadable = self.positive = self.principal = False

    def _forget_symbol(self, symbol: Symbol) -> None:
        self.values.pop(symbol, None)
        self.properties.pop(symbol, None)
        self.opaque.discard(symbol)
        self.facts = [f for f in self.facts if symbol not in f.free_symbols]

    def _declare(self, arguments: list[str], add: bool) -> None:
        for name, prop in zip(arguments[::2], arguments[1::2]):
            symbol = Symbol(name.strip())
            prop = prop.strip()
            if prop in PROPERTIES:
                if add:
                    self.properties.setdefault(symbol, set()).add(prop)
                else:
                    self.properties.get(symbol, set()).discard(prop)
            elif add:
                self.opaque.add(symbol)
            else:
                self.opaque.discard(symbol)

    def apply(self, item: str) -> bool:
        """Apply ``item`` when it changes the context; whether it does."""
        assignment = _ASSIGNMENT.fullmatch(item)
        if assignment is not None:
            name, value = assignment.group(1), assignment.group(2).strip()
            if name == 'assume_pos':
                self.positive = value == 'true'
            elif name == 'intanalysis':
                self.principal = value == 'false'
            else:
                self.values[Symbol(name)] = parse(value)
            return True
        application = _application(item)
        if application is None:
            return False
        name, arguments = application
        if name == 'assume':
            for argument in arguments:
                fact = relation(argument)
                if fact is None:
                    self.unreadable = True
                elif fact not in self.facts:
                    self.facts.append(fact)
        elif name == 'forget':
            for argument in arguments:
                fact = relation(argument)
                if fact in self.facts:
                    self.facts.remove(fact)
        elif name == 'declare':
            self._declare(arguments, True)
        elif name == 'remove':
            self._declare(arguments, False)
        elif name == 'kill':
            if any(a == 'all' or a.startswith('allbut') for a in arguments):
                self.clear()
            for argument in arguments:
                if argument == 'values':
                    self.values = {}
                elif re.fullmatch(r"[A-Za-z_%][\w%]*", argument):
                    self._forget_symbol(Symbol(argument))
        elif name == 'killcontext':
            self.facts, self.unreadable = [], False
        elif name == 'reset':
            self.positive = self.principal = False
        else:
            return False
        return True


def _enclosing(text: str, position: int) -> list[str]:
    """The names of the calls whose brackets enclose ``position``; a plain
    bracket or a list is ``''``."""
    stack: list[str] = []
    quoted = False
    for index in range(position):
        character = text[index]
        if character == '"':
            quoted = not quoted
        elif quoted:
            continue
        elif character in '([{':
            name = re.search(r"([A-Za-z_%][\w%]*)\s*$", text[:index]) if character == '(' else None
            stack.append(name.group(1) if name is not None else '')
        elif character in ')]}' and stack:
            stack.pop()
    return stack


def _peeled(item: str) -> str:
    """``item`` without the simplifications and brackets around it."""
    text = item.strip()
    while True:
        match = re.match(r"([A-Za-z_]\w*)?\s*\(", text)
        if match is None:
            return text
        closed = group(text, match.end() - 1)
        if closed is None or closed[1] != len(text):
            return text
        name, arguments = match.group(1) or '', split_arguments(closed[0])
        if len(arguments) != 1 or (name and name not in _PRESERVING):
            return text
        text = arguments[0]


def _items(statement: str) -> tuple[list[str], list[str]]:
    """The expressions of a statement and its evaluation flags: a bracketed
    sequence ``(e1, ..., en)`` has no flags, and ``expr, flag, ...`` is
    ``ev`` shorthand."""
    if statement.startswith('('):
        closed = group(statement, 0)
        if closed is not None and closed[1] == len(statement):
            return split_arguments(closed[0]), []
    parts = split_arguments(statement)
    return parts[:1], parts[1:]


def _call(item: str, match: re.Match[str], context: _Context
          ) -> Optional[tuple[Expr, Symbol, Expr, Expr]]:
    """The integral a call states, with the context's values substituted."""
    closed = group(item, match.end() - 1)
    if closed is None or any(n in _BINDING for n in _enclosing(item, match.start())):
        return None
    arguments = split_arguments(closed[0])
    kind = match.group(2)
    parsed = [parse(a) for a in arguments]
    if any(p is None for p in parsed):
        return None
    values = [as_expr(p) for p in parsed]
    if kind in ('integrate', 'defint') and len(values) == 4:
        integrand, variable, lower, upper = values
    elif kind == 'laplace' and len(values) == 3:
        integrand, variable, lower, upper = (as_expr(values[0]*exp(-values[2]*values[1])),
                                             values[1], as_expr(0), oo)
        if not isinstance(values[2], Symbol):
            return None
    elif kind == 'specint' and len(values) == 2:
        integrand, variable, lower, upper = values[0], values[1], as_expr(0), oo
    else:
        return None
    if not isinstance(variable, Symbol) or variable in context.values:
        return None
    unknown = {s for s, v in context.values.items() if v is None}
    known = {s: v for s, v in context.values.items() if v is not None}
    parts = [as_expr(e.xreplace(known)) for e in (integrand, lower, upper)]
    if any(e.free_symbols & unknown for e in parts):
        return None
    return parts[0], variable, parts[1], parts[2]


def integrals(text: str, collection: str = '', values_follow: bool = True
              ) -> list[DefiniteIntegral]:
    """Every definite integral of a Maxima test file that can be read.

    With ``values_follow`` (the ``rtest`` format) every statement is
    followed by the value Maxima records for it; otherwise the file is a
    demonstration and every statement is an input.
    """
    parts = statements(text)
    context = _Context()
    found: list[DefiniteIntegral] = []
    step = 2 if values_follow else 1
    for number, index in enumerate(range(0, len(parts), step), start=1):
        statement = parts[index]
        expected = parts[index + 1] if values_follow and index + 1 < len(parts) else None
        if ':=' in statement:
            continue                        # a definition: its body runs later, if at all
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
                read = _call(item, match, context)
                if read is None or context.unreadable or context.principal:
                    continue
                integrand, variable, lower, upper = read
                entry = DefiniteIntegral('', integrand, variable, lower, upper)
                parameters = set(entry.parameters)
                if parameters & context.opaque:
                    continue
                # a fact about other names, or about the variable of
                # integration, constrains nothing the integral depends on
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
                ordinal += 1
                name = '%s:%d' % (collection, number) + ('.%d' % ordinal if ordinal > 1 else '')
                found.append(DefiniteIntegral(name, integrand, variable, lower, upper,
                                              facts, properties, recorded))
    return found


def licence_files() -> list[pathlib.Path]:
    """The licence files kept with the fetched tests (none for a copy
    fetched file by file from a mirror)."""
    root = cache_directory() / 'maxima' / 'repository'
    return [root / name for name in LICENCE_FILES if (root / name).is_file()]


def fetch(collections: Sequence[str] = COLLECTIONS) -> list[tuple[str, str]]:
    """``(collection, text)`` for every collection whose file could be got."""
    found: list[tuple[str, str]] = []
    for collection in collections:
        if collection not in FILES:
            raise ValueError("unknown collection %r; known: %s"
                             % (collection, ', '.join(COLLECTIONS)))
        name, subdirectory, _ = FILES[collection]
        text = fetch_maxima(name, subdirectory)
        if text is not None:
            found.append((collection, text))
    return found


def load(collections: Sequence[str] = COLLECTIONS) -> list[DefiniteIntegral]:
    """Every readable definite integral of the collections."""
    found: list[DefiniteIntegral] = []
    for collection, text in fetch(collections):
        found.extend(integrals(text, collection, FILES[collection][2]))
    return found
