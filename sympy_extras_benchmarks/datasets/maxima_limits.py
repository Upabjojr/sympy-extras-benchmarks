"""Limits from Maxima's ``limit`` regression files, as SymPy expressions.

The dataset
===========

Maxima keeps four test files for its limit code, together about a
thousand calls:

* ``rtest_limit.mac`` — the main regression file, one entry per bug ever
  fixed;
* ``rtest_limit_extra.mac`` — a second, larger collection;
* ``rtest_limit_gruntz.mac`` — the examples of D. Gruntz, *On Computing
  Limits in a Symbolic Manipulation System* (1996), the thesis the modern
  algorithm comes from;
* ``rtest_limit_wester.mac`` — the limit problems of M. Wester's *A
  Critique of the Mathematical Abilities of CA Systems* (1999).

The last two are literature benchmarks assembled to be hard, which is why
they are worth more than their size suggests.

Each entry is an expression followed by the value Maxima records::

    limit(7^n/8^n,n,inf);
    0$

What is read, and what is not
=============================

The call and the recorded value. The value is a **third opinion**, not an
answer key: Maxima's limit code has its own bugs, so a disagreement is
reported for adjudication rather than counted as a defect. Mathematica
decides.

Refused:

* any call while an ``assume`` is in force — the context would change the
  answer, and tracking Maxima's assumption database is not attempted;
* ``und`` and ``ind``, Maxima's "undefined" and "indeterminate but
  bounded", which have no single SymPy counterpart;
* anything the Maxima expression parser cannot read.

Source and licence
==================

Maxima is distributed under the **GNU General Public License, version
2**. Nothing of it is stored in this repository: the files are fetched on
first use into the cache directory, or read from
``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``. Only the calls and the
recorded values are read; Maxima's code is not used.

Examples
========

>>> from sympy_extras_benchmarks.datasets.maxima_limits import limits
>>> text = "limit(7^n/8^n,n,inf);\\n0$\\nlimit(sin(x)/x,x,0);\\n1$\\n"
>>> first, second = limits(text, 'demo')
>>> first
MaximaLimit(demo:1, n -> oo, recorded 0)
>>> first.expression
7**n/8**n
>>> second.expression, second.point
(sin(x)/x, 0)
"""
from __future__ import annotations

import re
from typing import Optional

from sympy import Symbol, oo, zoo
from sympy.core.expr import Expr

from sympy_extras_benchmarks.datasets.maxima_ode import (
    TESTS_SUBDIRECTORY, MaximaSyntaxError, fetch as fetch_maxima, parse_expression)

__all__ = ['MaximaLimit', 'FILES', 'fetch', 'load', 'limits']

#: the regression files read
FILES: tuple[str, ...] = ('rtest_limit', 'rtest_limit_extra',
                          'rtest_limit_gruntz', 'rtest_limit_wester')

#: a name that cannot occur in the files, so the Maxima parser — written
#: for differential equations — leaves every name a plain symbol
_NO_FUNCTION = '__not_a_dependent_variable__'

#: Maxima's infinities, and what they are in SymPy
_INFINITIES = {'inf': oo, 'minf': -oo, 'infinity': zoo}
#: Maxima's non-values: no single SymPy counterpart, so they are refused
_REFUSED_VALUES = frozenset({'und', 'ind', 'unknown', 'false', 'true'})

_CALL = re.compile(r'^\s*limit\s*\(', re.M)
#: statements that put an assumption into Maxima's context, take one out,
#: or clear the whole context
_CONTEXT = re.compile(r'\b(assume|declare|forget|kill|domain\s*:)\s*\(?')


class MaximaLimit:
    """One ``limit`` call of a Maxima regression file.

    Attributes
    ==========

    name : str
        The file and the position of the call in it.
    expression : Expr
        The expression whose limit is taken.
    variable : Symbol
        The variable that moves.
    point : Expr
        Where it moves to.
    direction : str
        ``'+'``, ``'-'`` or ``'+-'`` (Maxima's ``plus``, ``minus``, or a
        two-sided limit when the call names no direction).
    recorded : Expr or None
        The value Maxima records, or ``None`` when the file records
        something this module does not read.
    """

    def __init__(self, name: str, expression: Expr, variable: Symbol, point: Expr,
                 direction: str, recorded: Optional[Expr]) -> None:
        self.name = name
        self.expression = expression
        self.variable = variable
        self.point = point
        self.direction = direction
        self.recorded = recorded

    def __repr__(self) -> str:
        arrow = '%s -> %s' % (self.variable, self.point)
        if self.direction != '+-':
            arrow += self.direction
        return "MaximaLimit(%s, %s, recorded %s)" % (self.name, arrow, self.recorded)


def _assumed(text: str, position: int) -> bool:
    """Whether an assumption is in force at ``position``.

    ``assume`` and ``declare`` add to Maxima's context, ``forget`` takes
    one out and ``kill`` clears it. The count is approximate — a single
    ``forget`` may retract several facts — so it errs toward refusing.
    """
    active = 0
    for match in _CONTEXT.finditer(text, 0, position):
        word = match.group(1).split()[0]
        if word in ('assume', 'declare'):
            active += 1
        elif word == 'kill':
            active = 0
        else:
            active = max(0, active - 1)
    return active > 0


def _group(text: str, start: int) -> Optional[tuple[str, int]]:
    """The bracketed group beginning at ``start``, and the index after it."""
    depth, index = 0, start
    while index < len(text):
        if text[index] in '([':
            depth += 1
        elif text[index] in ')]':
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    return None


def _split_commas(text: str) -> list[str]:
    parts, depth, last = [], 0, 0
    for index, character in enumerate(text):
        if character in '([':
            depth += 1
        elif character in ')]':
            depth -= 1
        elif character == ',' and depth == 0:
            parts.append(text[last:index])
            last = index + 1
    parts.append(text[last:])
    return [p.strip() for p in parts if p.strip()]


def strip_comments(text: str) -> str:
    """``text`` with Maxima's ``/* ... */`` comments blanked, positions kept."""
    out = list(text)
    depth, index = 0, 0
    while index < len(text) - 1:
        if text[index:index + 2] == '/*':
            depth += 1
            out[index] = out[index + 1] = ' '
            index += 2
            continue
        if text[index:index + 2] == '*/' and depth:
            depth -= 1
            out[index] = out[index + 1] = ' '
            index += 2
            continue
        if depth and out[index] != '\n':
            out[index] = ' '
        index += 1
    return "".join(out)


def _answer_after(text: str, position: int) -> str:
    """The statement following the call: what Maxima records as the value.

    The call ends with ``;`` or ``$`` and the recorded value is the next
    statement, itself ended by one of the two.
    """
    index = position
    while index < len(text) and text[index] not in ';$':
        index += 1
    index += 1
    depth, start = 0, index
    while index < len(text):
        character = text[index]
        if character in '([':
            depth += 1
        elif character in ')]':
            depth -= 1
        elif character in ';$' and depth == 0:
            break
        index += 1
    return text[start:index]


def _value(text: str) -> Optional[Expr]:
    """The recorded value, or ``None`` when it is not one this module reads."""
    body = text.strip().rstrip('$;').strip()
    if not body or body in _REFUSED_VALUES:
        return None
    if body in _INFINITIES:
        return _INFINITIES[body]
    try:
        return parse_expression(body, _NO_FUNCTION, _NO_FUNCTION)
    except (MaximaSyntaxError, RecursionError, ValueError, TypeError):
        return None


def _point(text: str) -> Optional[Expr]:
    body = text.strip()
    if body in _INFINITIES:
        return _INFINITIES[body]
    try:
        return parse_expression(body, _NO_FUNCTION, _NO_FUNCTION)
    except (MaximaSyntaxError, RecursionError, ValueError, TypeError):
        return None


def limits(text: str, name: str = '') -> list[MaximaLimit]:
    """Every ``limit`` call of a Maxima regression file that can be read."""
    body = strip_comments(text)
    found: list[MaximaLimit] = []
    for index, match in enumerate(_CALL.finditer(body), start=1):
        # an assumption in force would change the answer, and Maxima's
        # assumption database is not modelled here; but one that has been
        # forgotten, or cleared by kill(all), is no longer in force
        if _assumed(body, match.start()):
            continue
        group = _group(body, match.end() - 1)
        if group is None:
            continue
        arguments = _split_commas(group[0])
        if len(arguments) < 3:
            continue                        # limit(expr) alone: no variable
        try:
            expression = parse_expression(arguments[0], _NO_FUNCTION, _NO_FUNCTION)
        except (MaximaSyntaxError, RecursionError, ValueError, TypeError):
            continue
        variable = _point(arguments[1])
        if not isinstance(variable, Symbol):
            continue
        point = _point(arguments[2])
        if point is None:
            continue
        direction = '+-'
        if len(arguments) >= 4:
            written = arguments[3].strip()
            if written == 'plus':
                direction = '+'
            elif written == 'minus':
                direction = '-'
            else:
                continue                    # an option this module does not read
        recorded = _value(_answer_after(body, group[1]))
        found.append(MaximaLimit('%s:%d' % (name, index), expression, variable,
                                 point, direction, recorded))
    return found


def fetch() -> list[tuple[str, str]]:
    """``(file name, text)`` for every regression file that could be got."""
    found: list[tuple[str, str]] = []
    for name in FILES:
        text = fetch_maxima(name, TESTS_SUBDIRECTORY)
        if text is not None:
            found.append((name, text))
    return found


def load() -> list[MaximaLimit]:
    """Every readable limit of the regression files."""
    found: list[MaximaLimit] = []
    for name, text in fetch():
        found.extend(limits(text, name))
    return found
