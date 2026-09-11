r"""The formula language of QEPCAD B and Tarski, parsed to SymPy.

Both systems (C. W. Brown, https://github.com/chriswestbrown/qepcad and
https://github.com/chriswestbrown/tarski) write

* polynomials with implicit multiplication (``2 x y^2``, ``-1(x - y)``),
  ``*`` allowed too, ``^`` for powers and rational constants ``p/q``;
* relations ``=``, ``/=``, ``<``, ``>``, ``<=``, ``>=``;
* connectives ``~``, ``/\\``, ``\\/``, ``==>``, ``<==`` and ``<==>`` (in
  decreasing order of precedence), with ``[ ]`` grouping formulas -- and,
  in formulas Tarski prints, ``( )`` as well;
* quantifiers ``(E x)`` and ``(A x)`` (also ``(Ex)``) in front of a
  formula (QEPCAD), or ``ex x, y [ ... ]`` and ``all x [ ... ]`` (Tarski).

QEPCAD's extended quantifiers (``F`` "infinitely many", ``G`` "all but
finitely many", ``C`` "connected", ``X k`` "exactly k") and the extended
Tarski atoms ``x < _root_k p`` have no counterpart in sympy-extras and
raise :class:`UnsupportedSyntax`.

A QEPCAD *input* is the dialogue the program runs: an informal description
in brackets, the variable list in parentheses, the number of free
variables (the first ones of the list), the prenex formula ending with a
period, then commands, of which only ``assume [ ... ]`` changes the
question. :func:`parse_inputs` finds every such input in a text, also in
the transcript of a session (the prompts are skipped).

Examples
========

>>> from sympy_extras_benchmarks.datasets.qepcad_syntax import parse_formula
>>> parse_formula('(E y)[ y^2 = x /\\ 2 y x - 1/2 > 0 ]')
Exists(y, Eq(y**2, x) & (2*x*y - 1/2 > 0))
>>> parse_formula('all x, y [ x^2 + b x y + c > 0 ]')
ForAll((x, y), b*x*y + c + x**2 > 0)
"""
from __future__ import annotations

import re
from typing import Optional

from sympy import Eq, Integer, Ne, Symbol, Rational, true, false
from sympy.core.expr import Expr
from sympy.logic.boolalg import And, Boolean, Equivalent, Implies, Not, Or

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean, as_expr

__all__ = ['QEPCADSyntaxError', 'UnsupportedSyntax', 'QEPCADInput', 'InputFailure', 'Example', 'blocks',
           'tokenize', 'parse_formula',
           'parse_inputs']


class QEPCADSyntaxError(ValueError):
    """The text is not a formula of the language."""


class UnsupportedSyntax(QEPCADSyntaxError):
    """The formula uses a construct with no counterpart in sympy-extras."""


_TOKEN = re.compile(r'\s*(?:(<==>|==>|<==|/=|<=|>=|/\\|\\/|[-+*^/=<>()\[\],~.])'
                    r'|(\d+)|([A-Za-z_][A-Za-z0-9_]*))')

_RELATIONS = ('=', '/=', '<', '>', '<=', '>=')
_KEYWORDS = ('ex', 'all', 'true', 'false', 'TRUE', 'FALSE')
_EXTENDED = ('F', 'G', 'C')


def tokenize(text: str) -> list[str]:
    """The tokens of a formula.

    >>> from sympy_extras_benchmarks.datasets.qepcad_syntax import tokenize
    >>> tokenize('(Ex)[x^2 /= 1/2]')
    ['(', 'Ex', ')', '[', 'x', '^', '2', '/=', '1', '/', '2', ']']
    """
    tokens: list[str] = []
    position = 0
    text = text.rstrip()
    while position < len(text):
        match = _TOKEN.match(text, position)
        if match is None or match.end() == position:
            raise QEPCADSyntaxError("unexpected character %r at %d" % (text[position], position))
        tokens.append(match.group(1) or match.group(2) or match.group(3))
        position = match.end()
        while position < len(text) and text[position].isspace():
            position += 1
    return tokens


def _is_name(token: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token))


class _Parser:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = 0
        self.symbols: dict[str, Symbol] = {}

    def peek(self, offset: int = 0) -> Optional[str]:
        index = self.position + offset
        return self.tokens[index] if index < len(self.tokens) else None

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise QEPCADSyntaxError("unexpected end of the formula")
        self.position += 1
        return token

    def expect(self, token: str) -> None:
        found = self.take()
        if found != token:
            raise QEPCADSyntaxError("expected %r, found %r" % (token, found))

    def symbol(self, name: str) -> Symbol:
        if name.startswith('_root_'):
            raise UnsupportedSyntax("the extended atom %s" % name)
        if name not in self.symbols:
            self.symbols[name] = Symbol(name)
        return self.symbols[name]

    # formulas

    def formula(self) -> Boolean:
        left = self.disjunction()
        token = self.peek()
        if token == '<==>':
            self.take()
            return as_boolean(Equivalent(left, self.formula()))
        if token == '==>':
            self.take()
            return as_boolean(Implies(left, self.formula()))
        if token == '<==':
            self.take()
            return as_boolean(Implies(self.formula(), left))
        return left

    def disjunction(self) -> Boolean:
        parts = [self.conjunction()]
        while self.peek() == '\\/':
            self.take()
            parts.append(self.conjunction())
        return parts[0] if len(parts) == 1 else as_boolean(Or(*parts))

    def conjunction(self) -> Boolean:
        parts = [self.unary()]
        while self.peek() == '/\\':
            self.take()
            parts.append(self.unary())
        return parts[0] if len(parts) == 1 else as_boolean(And(*parts))

    def _qepcad_quantifier(self) -> Optional[tuple[str, str, int]]:
        """``(kind, variable, tokens)`` when a QEPCAD quantifier starts here."""
        if self.peek() != '(':
            return None
        first, second, third = self.peek(1), self.peek(2), self.peek(3)
        if first is None or second is None:
            return None
        if first in ('E', 'A') + _EXTENDED and _is_name(second) and third == ')':
            return first, second, 4
        if re.fullmatch(r'X\d+', first) and _is_name(second) and third == ')':
            raise UnsupportedSyntax("the quantifier (%s %s)" % (first, second))
        match = re.fullmatch(r'([EAFGC])([A-Za-z_][A-Za-z0-9_]*)', first)
        if match is not None and second == ')' and third in ('[', '(', '~'):
            return match.group(1), match.group(2), 3
        match = re.fullmatch(r'X(\d+)[A-Za-z_][A-Za-z0-9_]*', first)
        if match is not None and second == ')':
            raise UnsupportedSyntax("the quantifier (%s)" % first)
        return None

    def unary(self) -> Boolean:
        token = self.peek()
        if token == '~':
            self.take()
            return as_boolean(Not(self.unary()))
        quantifier = self._qepcad_quantifier()
        if quantifier is not None:
            kind, name, length = quantifier
            if kind in _EXTENDED:
                raise UnsupportedSyntax("the quantifier (%s %s)" % (kind, name))
            self.position += length
            variable = self.symbol(name)
            body = self.unary()
            return as_boolean(Exists(variable, body) if kind == 'E' else ForAll(variable, body))
        if token in ('ex', 'all'):
            self.take()
            variables = [self.symbol(self.take())]
            while self.peek() == ',':
                self.take()
                variables.append(self.symbol(self.take()))
            body = self.unary()
            return as_boolean(Exists(variables, body) if token == 'ex' else ForAll(variables, body))
        if token in ('true', 'TRUE'):
            self.take()
            return true
        if token in ('false', 'FALSE'):
            self.take()
            return false
        if token == '[':
            self.take()
            inner = self.formula()
            self.expect(']')
            return inner
        if token == '(':
            # a parenthesised formula, or a relation whose left side
            # starts with a parenthesised polynomial
            saved = self.position
            try:
                self.take()
                inner = self.formula()
                self.expect(')')
                if self.peek() not in _RELATIONS and self.peek() not in ('+', '-', '*', '/', '^'):
                    return inner
            except UnsupportedSyntax:
                raise
            except QEPCADSyntaxError:
                pass
            self.position = saved
        return self.relation()

    def relation(self) -> Boolean:
        terms = [self.expression()]
        operators: list[str] = []
        while self.peek() in _RELATIONS:
            operators.append(self.take())
            terms.append(self.expression())
        if not operators:
            raise QEPCADSyntaxError("expected a relation, found %r" % (self.peek(),))
        parts: list[Boolean] = []
        for operator, left, right in zip(operators, terms, terms[1:]):
            if operator == '=':
                parts.append(as_boolean(Eq(left, right)))
            elif operator == '/=':
                parts.append(as_boolean(Ne(left, right)))
            elif operator == '<':
                parts.append(as_boolean(left < right))
            elif operator == '>':
                parts.append(as_boolean(left > right))
            elif operator == '<=':
                parts.append(as_boolean(left <= right))
            else:
                parts.append(as_boolean(left >= right))
        return parts[0] if len(parts) == 1 else as_boolean(And(*parts))

    # polynomials

    def expression(self) -> Expr:
        sign = Integer(1)
        while self.peek() in ('+', '-'):
            if self.take() == '-':
                sign = -sign
        total = as_expr(sign*self.term())
        while self.peek() in ('+', '-'):
            operator = self.take()
            term = self.term()
            total = as_expr(total + term if operator == '+' else total - term)
        return total

    def _starts_factor(self) -> bool:
        token = self.peek()
        if token is None:
            return False
        if token == '(':
            return self._qepcad_quantifier() is None
        return token.isdigit() or (_is_name(token) and token not in _KEYWORDS)

    def term(self) -> Expr:
        product = self.power()
        while True:
            token = self.peek()
            if token == '*':
                self.take()
                product = as_expr(product*self.power())
            elif token == '/':
                self.take()
                product = as_expr(product/self.power())
            elif self._starts_factor():
                product = as_expr(product*self.power())
            else:
                return product

    def power(self) -> Expr:
        base = self.atom()
        while self.peek() == '^':
            self.take()
            sign = 1
            if self.peek() in ('+', '-'):
                sign = -1 if self.take() == '-' else 1
            exponent = self.atom()
            if not exponent.is_Integer:
                raise QEPCADSyntaxError("the exponent %s is not an integer" % exponent)
            base = as_expr(base**(sign*exponent))
        return base

    def atom(self) -> Expr:
        token = self.take()
        if token.isdigit():
            return Integer(token)
        if token == '(':
            inner = self.expression()
            self.expect(')')
            return inner
        if _is_name(token) and token not in _KEYWORDS:
            return self.symbol(token)
        raise QEPCADSyntaxError("unexpected %r in a polynomial" % token)


def parse_formula(text: str) -> Boolean:
    """The formula written in ``text`` (a trailing period is allowed)."""
    tokens = tokenize(text)
    if tokens and tokens[-1] == '.':
        tokens.pop()
    parser = _Parser(tokens)
    result = parser.formula()
    if parser.peek() is not None:
        raise QEPCADSyntaxError("unexpected %r after the formula" % parser.peek())
    return result


class QEPCADInput:
    """One QEPCAD problem.

    Attributes
    ==========

    name : str
        The informal description (or the name given by the caller).
    variables : list[Symbol]
        The variable list, in QEPCAD's order.
    free : int
        How many of the variables, the first ones, are free.
    formula : Boolean
        The prenex formula.
    assumptions : Boolean or None
        The formula of an ``assume`` command, if there is one.
    """

    def __init__(self, name: str, variables: list[Symbol], free: int, formula: Boolean,
                 assumptions: Optional[Boolean] = None) -> None:
        self.name = name
        self.variables = variables
        self.free = free
        self.formula = formula
        self.assumptions = assumptions

    @property
    def free_variables(self) -> list[Symbol]:
        return self.variables[:self.free]

    def __repr__(self) -> str:
        return "QEPCADInput(%r, %d variables, %d free)" % (self.name, len(self.variables), self.free)


_BLOCK = re.compile(r'^[ \t]*\[(?P<name>[^\]\n]*)\][ \t]*\n\s*\((?P<variables>[^)\n]*)\)[ \t]*\n'
                    r'\s*(?P<free>\d+)[ \t]*\n(?P<formula>.*?)\.[ \t]*$', re.MULTILINE | re.DOTALL)
_PROMPT = re.compile(r'^\s*(Enter [^\n]*:|Before [^\n]*>|[^\n]*\[~/\]>[^\n]*)[ \t]*$', re.MULTILINE)


def _bracketed(text: str, start: int) -> Optional[str]:
    """The text of the bracket opening at or after ``start``, brackets included."""
    opening = text.find('[', start)
    if opening < 0:
        return None
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == '[':
            depth += 1
        elif text[index] == ']':
            depth -= 1
            if depth == 0:
                return text[opening:index + 1]
    return None


class InputFailure:
    """An input which could not be read, and why."""

    def __init__(self, name: str, error: QEPCADSyntaxError) -> None:
        self.name = name
        self.error = error

    def __repr__(self) -> str:
        return "InputFailure(%r, %s)" % (self.name, self.error)


def parse_inputs(text: str) -> list[tuple[str, 'QEPCADInput | InputFailure']]:
    """Every QEPCAD input in ``text``, in order, each with the text it was
    read from; an input which cannot be read gives an :class:`InputFailure`
    carrying the error."""
    cleaned = _PROMPT.sub('', text)
    found: list[tuple[str, QEPCADInput | InputFailure]] = []
    matches = list(_BLOCK.finditer(cleaned))
    for index, match in enumerate(matches):
        name = match.group('name').strip()
        source = match.group(0)
        try:
            names = [n.strip() for n in match.group('variables').split(',') if n.strip()]
            if not all(_is_name(n) for n in names):
                raise QEPCADSyntaxError("bad variable list %r" % match.group('variables'))
            variables = [Symbol(n) for n in names]
            free = int(match.group('free'))
            formula = parse_formula(match.group('formula'))
            end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
            commands = cleaned[match.end():end]
            assumptions: Optional[Boolean] = None
            place = commands.find('assume')
            if place >= 0:
                bracket = _bracketed(commands, place)
                if bracket is not None:
                    assumptions = parse_formula(bracket)
            found.append((source, QEPCADInput(name, variables, free, formula, assumptions)))
        except QEPCADSyntaxError as error:
            found.append((source, InputFailure(name, error)))
    return found


class Example:
    """A problem of a CAD test collection, written in QEPCAD or Tarski syntax.

    Attributes
    ==========

    collection : str
        The collection and set it comes from, e.g. ``'qepcad-application'``.
    name : str
        Its name in the collection.
    syntax : str
        ``'qepcad'`` when :attr:`text` is a QEPCAD input (read with
        :func:`parse_inputs`), ``'tarski'`` when it is a formula (read with
        :func:`parse_formula`).
    text : str
        The problem as written in the collection.
    question : str
        ``'resolve'``: eliminate the quantifiers (decide the formula when
        every variable is quantified); ``'satisfiable'``: whether the
        quantifier-free formula has a real solution.
    expected : str or None
        The answer the collection records, in Tarski syntax (a formula, or
        ``true``/``false``); ``None`` when it records none.
    duplicate_of : str or None
        The name of an earlier problem of the collections which is the same
        question, when there is one.
    """

    def __init__(self, collection: str, name: str, syntax: str, text: str, question: str = 'resolve',
                 expected: Optional[str] = None, duplicate_of: Optional[str] = None) -> None:
        self.collection = collection
        self.name = name
        self.syntax = syntax
        self.text = text
        self.question = question
        self.expected = expected
        self.duplicate_of = duplicate_of

    @property
    def key(self) -> str:
        return '%s/%s' % (self.collection, self.name)

    def __repr__(self) -> str:
        return "Example(%r, %r)" % (self.collection, self.name)


def blocks(text: str) -> list[tuple[re.Match[str], str]]:
    """The QEPCAD inputs of ``text`` (prompts removed), each with the
    commands which follow it."""
    cleaned = _PROMPT.sub('', text)
    matches = list(_BLOCK.finditer(cleaned))
    found: list[tuple[re.Match[str], str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
        found.append((match, cleaned[match.end():end]))
    return found
