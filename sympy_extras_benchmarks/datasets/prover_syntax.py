"""The small arithmetic language the proof-assistant test suites are read
in, shared by the mathlib4 and the Rocq/Coq parsers.

Lean and Rocq write their arithmetic goals in nearly the same notation
once the unicode is spelled out: numerals, ``+ - * / ^``, the six
relations, ``/\\``-style connectives and parentheses. This module holds
that common grammar, and — more importantly — the two refusals which keep
a translated goal honest:

* :func:`expression` and :func:`proposition` accept only the operators
  listed above and only identifiers the caller declared, so a goal using
  a function, a coercion or a variable from an enclosing command is
  refused rather than guessed at;
* :func:`representable` refuses the goals whose meaning in the proof
  assistant is not the meaning the same formula has over ℝ or ℤ.

Both assistants make arithmetic total: ``x / 0`` is ``0`` in Lean and in
Rocq's ``R``, integer division truncates, and a real exponent is real
exponentiation. Translating those conventions would make the benchmark
test the translation rather than the algorithms, so a goal that uses them
is dropped.

Examples
========

>>> from sympy import Symbol
>>> from sympy_extras_benchmarks.datasets.prover_syntax import proposition
>>> x = Symbol('x')
>>> proposition('0 < x -> x != 1', {'x': x})
Implies(0 < x, Ne(x, 1))
>>> proposition('x * (x + 1) >= 0', {'x': x})
x*(x + 1) >= 0
"""
from __future__ import annotations

import re
from tokenize import TokenError
from typing import Optional

from sympy import Abs, And, Eq, Implies, Ne, Not, Or, Pow, Symbol, preorder_traversal
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean
from sympy.parsing.sympy_parser import parse_expr

from sympy_extras._typing import as_boolean, as_expr

__all__ = ['SyntaxRefused', 'balanced', 'bars_to_abs', 'expression', 'proposition',
           'representable', 'split_top']

#: an identifier of either assistant (Lean admits greek letters and primes)
IDENTIFIER = re.compile(r"[A-Za-z_Ͱ-Ͽ][A-Za-z_0-9Ͱ-Ͽ']*")
#: everything the expression grammar allows, once identifiers are removed
_ALLOWED = set(' \t\n0123456789+-*/^().')
#: the one function the expression grammar knows
_FUNCTIONS = {'abs': Abs}
#: the relations, longest first so that ``<=`` is not read as ``<``
_RELATIONS: tuple[tuple[str, str], ...] = (
    ('<=', 'le'), ('>=', 'ge'), ('!=', 'ne'), ('<', 'lt'), ('>', 'gt'), ('=', 'eq'))


class SyntaxRefused(ValueError):
    """The goal uses something beyond the arithmetic subset read here."""


def balanced(text: str) -> bool:
    """Whether every bracket of ``text`` is closed."""
    depth = 0
    for character in text:
        if character in '([{':
            depth += 1
        elif character in ')]}':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def split_top(text: str, token: str) -> Optional[tuple[str, str]]:
    """``text`` split at the first ``token`` outside brackets, or ``None``.

    A token made of letters must stand alone, so that the ``and`` of
    ``android`` is not an operator.
    """
    depth = 0
    index = 0
    while index < len(text):
        character = text[index]
        if character in '([{':
            depth += 1
        elif character in ')]}':
            depth -= 1
        elif depth == 0 and text.startswith(token, index):
            if token.isalpha():
                after = index + len(token)
                if (index and text[index - 1].isalnum()) or (after < len(text)
                                                             and text[after].isalnum()):
                    index += 1
                    continue
            return text[:index], text[index + len(token):]
        index += 1
    return None


def expression(text: str, variables: dict[str, Symbol], integers: bool = False) -> Expr:
    """One arithmetic expression, refusing anything outside the subset.

    ``integers`` says the expression is read over ℤ, where a non-integer
    rational means truncating division and so is refused.

    The refusals of :func:`representable` are applied to an *unevaluated*
    parse of the same text, because SymPy settles the arithmetic while it
    reads: ``(0:ℝ) ^ (-1/3) = 0`` becomes ``False`` before anything can
    notice that the exponent was never an integer.
    """
    body = text.strip()
    if not body:
        raise SyntaxRefused("empty expression")
    for name in set(IDENTIFIER.findall(body)):
        if name not in variables and name not in _FUNCTIONS:
            raise SyntaxRefused("unknown name %s" % name)
    if set(IDENTIFIER.sub('', body)) - _ALLOWED:
        raise SyntaxRefused("unexpected characters in %r" % body)
    try:
        names: dict[str, object] = dict(variables)
        names.update(_FUNCTIONS)
        source = body.replace('^', '**')
        literal = parse_expr(source, local_dict=names, evaluate=False)
        value = parse_expr(source, local_dict=names, evaluate=True)
    except (SyntaxError, TokenError, TypeError, ValueError, AttributeError,
            RecursionError, OverflowError):
        raise SyntaxRefused("cannot parse %r" % body)
    if not isinstance(value, Expr) or not isinstance(literal, Expr):
        raise SyntaxRefused("not an expression: %r" % body)
    if not representable(literal, integers):
        raise SyntaxRefused("total arithmetic in %r (x/0, a truncated or real power)" % body)
    return as_expr(value)


def proposition(text: str, variables: dict[str, Symbol],
                integers: bool = False) -> Boolean:
    """One proposition: the connectives, then a relation between
    expressions.

    ``text`` is expected in ASCII — ``and``, ``or``, ``not``, ``->``,
    ``!=`` — which is what each assistant's own notation is rewritten to
    before it gets here. ``integers`` is passed down to
    :func:`expression`, which needs it for the division refusal.
    """
    body = text.strip()
    if not body:
        raise SyntaxRefused("empty proposition")
    if body.startswith('(') and body.endswith(')') and balanced(body[1:-1]):
        return proposition(body[1:-1], variables, integers)
    if body in ('True', 'true'):
        return as_boolean(S.true)
    if body in ('False', 'false'):
        return as_boolean(S.false)
    for token, connective in (('or', Or), ('and', And)):
        split = split_top(body, ' %s ' % token)
        if split is not None:
            return as_boolean(connective(proposition(split[0], variables, integers),
                                         proposition(split[1], variables, integers)))
    split = split_top(body, '->')
    if split is not None:
        return as_boolean(Implies(proposition(split[0], variables, integers),
                                  proposition(split[1], variables, integers)))
    if body.startswith('not '):
        return as_boolean(Not(proposition(body[4:], variables, integers)))
    found = _relations_in(body)
    if not found:
        raise SyntaxRefused("no relation in %r" % body)
    if len(found) > 1:
        # a chain, ``0 <= x < n``, is the conjunction both assistants read
        # it as; without this the middle term would be parsed as a value
        parts: list[Boolean] = []
        for index, (begin, stop, kind) in enumerate(found):
            left = body[found[index - 1][1]:begin] if index else body[:begin]
            right = body[stop:found[index + 1][0]] if index + 1 < len(found) else body[stop:]
            if not left.strip() or not right.strip():
                raise SyntaxRefused("empty side in the chain %r" % body)
            parts.append(_relate(kind, left, right, variables, integers))
        return as_boolean(And(*parts))
    begin, stop, kind = found[0]
    return _relate(kind, body[:begin], body[stop:], variables, integers)


def _relations_in(text: str) -> list[tuple[int, int, str]]:
    """``(start, end, kind)`` of every relation of ``text`` outside
    brackets, left to right, the two-character ones read first."""
    found: list[tuple[int, int, str]] = []
    depth = 0
    index = 0
    while index < len(text):
        character = text[index]
        if character in '([{':
            depth += 1
        elif character in ')]}':
            depth -= 1
        elif depth == 0:
            for token, kind in _RELATIONS:
                if text.startswith(token, index):
                    found.append((index, index + len(token), kind))
                    index += len(token)
                    break
            else:
                index += 1
            continue
        index += 1
    return found


def _relate(kind: str, left: str, right: str, variables: dict[str, Symbol],
            integers: bool = False) -> Boolean:
    """One relation between two already-split sides."""
    first, second = expression(left, variables, integers), expression(right, variables, integers)
    if kind == 'le':
        return as_boolean(first <= second)
    if kind == 'ge':
        return as_boolean(first >= second)
    if kind == 'lt':
        return as_boolean(first < second)
    if kind == 'gt':
        return as_boolean(first > second)
    if kind == 'ne':
        return as_boolean(Ne(first, second))
    return as_boolean(Eq(first, second))


def bars_to_abs(text: str) -> str:
    """Lean's ``|x|`` rewritten as ``abs(x)``.

    The bars are matched in pairs from the left; an odd number of them, or
    a nested pair, is left alone for the caller to refuse.
    """
    if text.count('|') % 2:
        return text
    out, depth = [], 0
    for character in text:
        if character == '|':
            out.append('abs(' if depth == 0 else ')')
            depth = 1 - depth
        else:
            out.append(character)
    return "".join(out)


def representable(formula: Basic, integers: bool) -> bool:
    """Whether the formula means over its domain what it means in the
    proof assistant.

    Both assistants make arithmetic total, and two of their total
    definitions are not the ones a formula over ℝ or ℤ carries: division
    is defined at zero, with ``x / 0 = 0``, and ``a ^ b`` with a real
    ``b`` is real exponentiation. Over ℤ, division truncates as well.

    So the exponent of every power must be a nonnegative integer, unless
    the base is a nonzero numeral and the domain is not ℤ — which rules
    out a variable denominator, written ``b**-1`` here, while leaving
    ``a / 2`` alone — and over ℤ no non-integer rational may appear.
    """
    for node in preorder_traversal(formula):
        if isinstance(node, Pow):
            exponent, base = node.exp, node.base
            if exponent.is_Integer and bool(exponent.is_nonnegative):
                continue
            # dividing by a nonzero numeral is ordinary arithmetic; it is a
            # denominator that can vanish, or a non-integer exponent, that
            # the assistants define differently from ℝ
            if (exponent.is_Integer and base.is_number
                    and base.is_nonzero and not integers):
                continue
            return False
        if integers and node.is_Rational and not node.is_Integer:
            return False
    return True
