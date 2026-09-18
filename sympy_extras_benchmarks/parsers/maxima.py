"""The expression language of Maxima, read into SymPy.

Maxima's regression files are the largest source of the collections, and
REDUCE, FriCAS and holpy expressions are rewritten into Maxima's syntax
(:mod:`~sympy_extras_benchmarks.parsers.reduce`,
:mod:`~sympy_extras_benchmarks.parsers.fricas`,
:mod:`~sympy_extras_benchmarks.parsers.holpy`) so that this one parser
reads all four.

Expressions
===========

:func:`parse_expression` is a small recursive descent parser: the
operators ``+ - * / ^`` and ``**``, unary minus, ``!``, the equality ``=``,
function calls and the noun form ``'diff(y, x, n)``. The dependent
variable becomes an applied undefined function (``y(x)``), the known
functions of Maxima are mapped to SymPy's (``%e`` to ``E``, ``bessel_j``
to ``besselj``, ``legendre_p`` to ``legendre``, ...; see
:data:`FUNCTIONS`), other applied names become undefined functions
(``f(x)``) and other names become symbols (including ``lambda``, which
Python's parser could not accept). Numbers are exact.
:func:`parse_equation` reads an ordinary differential equation in
``y(x)``; :func:`parse` reads a value, with :data:`NO_FUNCTION` as the
dependent variable so that every name stays a symbol, and refuses what
did not translate (:func:`readable`); :func:`relation` reads Maxima's
relations (``a > 0``, ``a # b``, ``notequal(a, 0)``).

Source text
===========

The helpers split Maxima source without evaluating it:
:func:`strip_comments` blanks the nested ``/* ... */`` comments keeping
positions, :func:`statements` splits a file at its top-level ``;`` and
``$``, :func:`group` reads a bracketed group, :func:`split_arguments` and
:func:`call_arguments` split argument lists at their top-level commas, and
:func:`application` reads an item that is one call.

Nothing here reads a file or knows which collection a text comes from.

Examples
========

>>> from sympy_extras_benchmarks.parsers.maxima import parse_equation, relation
>>> parse_equation("'diff(y,x)^2 + a*y*'diff(y,x) = a*x")
-a*x + a*y(x)*Derivative(y(x), x) + Derivative(y(x), x)**2
>>> parse_equation("x^2*'diff(y,x,2) + lambda*y")
lambda*y(x) + x**2*Derivative(y(x), (x, 2))
>>> relation('notequal(a, 0)')
Ne(a, 0)
"""
from __future__ import annotations

import re
from typing import Callable, Optional, Sequence

from sympy import (E, I, pi, oo, EulerGamma, Integer, Rational, Symbol, Function,
    Derivative, factorial, sin, cos, tan, cot, sec, csc, exp, log, sqrt, sinh,
    cosh, tanh, coth, sech, csch, asin, acos, atan, acot, asec, acsc, atan2, asinh,
    acosh, atanh, acoth, asech, acsch, Abs, im, conjugate, erf, erfc, erfi, gamma,
    loggamma, uppergamma, beta, zeta, Ei, Si, Ci, Shi, Chi, E1, expint, fresnels,
    fresnelc, elliptic_k, elliptic_e, elliptic_f, besselj, bessely, besseli, besselk,
    legendre, hermite, laguerre, assoc_laguerre, chebyshevt, chebyshevu, jacobi,
    LambertW, Heaviside, DiracDelta, sign, floor, ceiling, binomial, airyai, airybi,
    factorial2, jn, yn)
from sympy import Eq, Ge, Gt, Integral, Le, Lt, Ne, Product, Sum, nan
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef, UndefinedFunction
from sympy.functions.elementary.complexes import re as real_part
from sympy.logic.boolalg import Boolean

from sympy_extras._typing import as_boolean, as_expr

__all__ = ['MaximaSyntaxError', 'FUNCTIONS', 'NO_FUNCTION', 'Token', 'x', 'y', 'tokenize',
           'parse_expression', 'parse_equation', 'derivative_order', 'undefined_function',
           'parse', 'readable', 'relation', 'strip_comments', 'statements', 'group',
           'split_arguments', 'call_arguments', 'application']


# ---------------------------------------------------------------------------
# expressions

class MaximaSyntaxError(ValueError):
    """The text is not a Maxima expression the parser understands."""


#: the variables of the collections: an equation is in ``y(x)``
x = Symbol('x')
y = Function('y')
assert isinstance(y, UndefinedFunction)


def derivative_order(expr: Basic, f: Expr) -> int:
    """The order of the highest derivative of ``f`` in ``expr``."""
    orders = [sum(int(as_expr(n)) for _, n in d.variable_count)
              for d in expr.atoms(Derivative) if d.expr == f]
    return max(orders, default=0)


#: a token: its kind (``number``, ``name``, ``op``) and text
Token = tuple[str, str]

_NUMBER = re.compile(r"\d+\.\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|\d+(?:[eE][+-]?\d+)?")
_NAME = re.compile(r"%?[A-Za-z_][A-Za-z_0-9]*")
_OPERATORS = ('**', ':=', '!!', '+', '-', '*', '/', '^', '=', '(', ')', ',', "'", '!', '[', ']', ':')


def tokenize(text: str) -> list[Token]:
    """The tokens of a Maxima expression.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.maxima import tokenize
    >>> tokenize("'diff(y,x)+%e^-x")
    [('op', "'"), ('name', 'diff'), ('op', '('), ('name', 'y'), ('op', ','), ('name', 'x'), ('op', ')'), ('op', '+'), ('name', '%e'), ('op', '^'), ('op', '-'), ('name', 'x')]
    """
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        m = _NUMBER.match(text, i)
        if m:
            tokens.append(('number', m.group(0)))
            i = m.end()
            continue
        m = _NAME.match(text, i)
        if m:
            tokens.append(('name', m.group(0)))
            i = m.end()
            continue
        for op in _OPERATORS:
            if text.startswith(op, i):
                tokens.append(('op', op))
                i += len(op)
                break
        else:
            raise MaximaSyntaxError("unexpected character %r at %d in %r" % (c, i, text))
    return tokens


#: Maxima's constants
_CONSTANTS: dict[str, Expr] = {
    '%e': E, '%i': I, '%pi': pi, '%gamma': EulerGamma, 'inf': oo, 'minf': -oo,
}

#: a function of SymPy applied to the translated arguments
Applier = Callable[[Sequence[Expr]], Expr]


def _unary(f: Callable[[Expr], Expr]) -> Applier:
    def apply(args: Sequence[Expr]) -> Expr:
        if len(args) != 1:
            raise MaximaSyntaxError("one argument expected, got %d" % len(args))
        return f(args[0])
    return apply


def _binary(f: Callable[[Expr, Expr], Expr]) -> Applier:
    def apply(args: Sequence[Expr]) -> Expr:
        if len(args) != 2:
            raise MaximaSyntaxError("two arguments expected, got %d" % len(args))
        return f(args[0], args[1])
    return apply


def _ternary(f: Callable[[Expr, Expr, Expr], Expr]) -> Applier:
    def apply(args: Sequence[Expr]) -> Expr:
        if len(args) != 3:
            raise MaximaSyntaxError("three arguments expected, got %d" % len(args))
        return f(args[0], args[1], args[2])
    return apply


def _quaternary(f: Callable[[Expr, Expr, Expr, Expr], Expr]) -> Applier:
    def apply(args: Sequence[Expr]) -> Expr:
        if len(args) != 4:
            raise MaximaSyntaxError("four arguments expected, got %d" % len(args))
        return f(args[0], args[1], args[2], args[3])
    return apply


def _integral(args: Sequence[Expr]) -> Expr:
    """Maxima's ``integrate(f, x)`` and ``integrate(f, x, a, b)``, unevaluated."""
    if len(args) == 2:
        return as_expr(Integral(args[0], args[1]))
    if len(args) == 4:
        return as_expr(Integral(args[0], (args[1], args[2], args[3])))
    raise MaximaSyntaxError("integrate takes two or four arguments, got %d" % len(args))


def _bound(builder: Callable[..., Basic]) -> Applier:
    """Maxima's ``sum(f, i, a, b)`` and ``product(f, i, a, b)``, unevaluated."""
    def apply(args: Sequence[Expr]) -> Expr:
        if len(args) != 4:
            raise MaximaSyntaxError("four arguments expected, got %d" % len(args))
        return as_expr(builder(args[0], (args[1], args[2], args[3])))
    return apply


def _unit_step(x: Expr) -> Expr:
    # Maxima's unit_step is 0 at 0
    return as_expr(Heaviside(x, 0))


def _sympy_function(f: object) -> Callable[..., Expr]:
    def apply(*args: Expr) -> Expr:
        assert callable(f)
        return as_expr(f(*args))
    return apply


_S = _sympy_function


#: Maxima's function names and their SymPy counterparts
FUNCTIONS: dict[str, Applier] = {
    'sin': _unary(_S(sin)), 'cos': _unary(_S(cos)), 'tan': _unary(_S(tan)),
    'cot': _unary(_S(cot)), 'sec': _unary(_S(sec)), 'csc': _unary(_S(csc)),
    'asin': _unary(_S(asin)), 'acos': _unary(_S(acos)), 'atan': _unary(_S(atan)),
    'arctan': _unary(_S(atan)), 'acot': _unary(_S(acot)), 'atan2': _binary(_S(atan2)),
    'sinh': _unary(_S(sinh)), 'cosh': _unary(_S(cosh)), 'tanh': _unary(_S(tanh)),
    'coth': _unary(_S(coth)), 'asinh': _unary(_S(asinh)), 'acosh': _unary(_S(acosh)),
    'atanh': _unary(_S(atanh)),
    'exp': _unary(_S(exp)), 'log': _unary(_S(log)), 'sqrt': _unary(_S(sqrt)),
    'abs': _unary(_S(Abs)), 'signum': _unary(_S(sign)), 'floor': _unary(_S(floor)),
    'ceiling': _unary(_S(ceiling)), 'erf': _unary(_S(erf)), 'erfc': _unary(_S(erfc)),
    'gamma': _unary(_S(gamma)), 'binomial': _binary(_S(binomial)),
    'bessel_j': _binary(_S(besselj)), 'bessel_y': _binary(_S(bessely)),
    'bessel_i': _binary(_S(besseli)), 'bessel_k': _binary(_S(besselk)),
    'legendre_p': _binary(_S(legendre)),
    'airy_ai': _unary(_S(airyai)), 'airy_bi': _unary(_S(airybi)),
    # the names below occur in the integration and transform tests; each is
    # the same function, with the same normalisation, in both systems
    'sech': _unary(_S(sech)), 'csch': _unary(_S(csch)), 'asec': _unary(_S(asec)),
    'acsc': _unary(_S(acsc)), 'acoth': _unary(_S(acoth)), 'asech': _unary(_S(asech)),
    'acsch': _unary(_S(acsch)),
    'realpart': _unary(_S(real_part)), 'imagpart': _unary(_S(im)), 'conjugate': _unary(_S(conjugate)),
    'erfi': _unary(_S(erfi)), 'log_gamma': _unary(_S(loggamma)),
    'gamma_incomplete': _binary(_S(uppergamma)), 'beta': _binary(_S(beta)),
    'zeta': _unary(_S(zeta)), 'lambert_w': _unary(_S(LambertW)),
    'expintegral_ei': _unary(_S(Ei)), 'expintegral_si': _unary(_S(Si)),
    'expintegral_ci': _unary(_S(Ci)), 'expintegral_shi': _unary(_S(Shi)),
    'expintegral_chi': _unary(_S(Chi)), 'expintegral_e1': _unary(_S(E1)),
    'expintegral_e': _binary(_S(expint)),
    'fresnel_s': _unary(_S(fresnels)), 'fresnel_c': _unary(_S(fresnelc)),
    'elliptic_kc': _unary(_S(elliptic_k)), 'elliptic_ec': _unary(_S(elliptic_e)),
    'elliptic_f': _binary(_S(elliptic_f)), 'elliptic_e': _binary(_S(elliptic_e)),
    'hermite': _binary(_S(hermite)), 'laguerre': _binary(_S(laguerre)),
    'gen_laguerre': _ternary(_S(assoc_laguerre)), 'chebyshev_t': _binary(_S(chebyshevt)),
    'chebyshev_u': _binary(_S(chebyshevu)), 'jacobi_p': _quaternary(_S(jacobi)),
    'unit_step': _unary(_unit_step), 'delta': _unary(_S(DiracDelta)),
    'factorial': _unary(_S(factorial)), 'factorial2': _unary(_S(factorial2)),
    'spherical_bessel_j': _binary(_S(jn)), 'spherical_bessel_y': _binary(_S(yn)),
    # the constructs with a bound variable, kept unevaluated
    'integrate': _integral, 'sum': _bound(Sum), 'product': _bound(Product),
}


class _Parser:
    """Recursive descent parser for Maxima expressions.

    Precedence, from loosest to tightest: ``=``; ``+`` ``-``; ``*`` ``/``;
    unary ``-``; ``^`` (right associative, its exponent may carry a unary
    minus); ``!``; atoms. This matches Maxima for the expressions of the
    collections (``-x^2`` is ``-(x^2)``, ``%e^-x`` is ``exp(-x)``).
    """

    def __init__(self, tokens: list[Token], dependent: Symbol, independent: Symbol) -> None:
        self.tokens = tokens
        self.position = 0
        self.dependent = dependent
        self.independent = independent
        self.function: UndefinedFunction = y if dependent.name == 'y' else undefined_function(dependent.name)
        self.functions: dict[str, UndefinedFunction] = {}

    # -- token access

    def peek(self) -> Optional[Token]:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def take(self) -> Token:
        token = self.peek()
        if token is None:
            raise MaximaSyntaxError("unexpected end of expression")
        self.position += 1
        return token

    def accept(self, op: str) -> bool:
        token = self.peek()
        if token is not None and token == ('op', op):
            self.position += 1
            return True
        return False

    def expect(self, op: str) -> None:
        if not self.accept(op):
            raise MaximaSyntaxError("expected %r at token %d" % (op, self.position))

    # -- grammar

    def equation(self) -> Expr:
        """``lhs = rhs`` as ``lhs - rhs``, or a plain expression."""
        lhs = self.sum()
        if self.accept('='):
            rhs = self.sum()
            return as_expr(lhs - rhs)
        return lhs

    def sum(self) -> Expr:
        result = self.product()
        while True:
            if self.accept('+'):
                result = as_expr(result + self.product())
            elif self.accept('-'):
                result = as_expr(result - self.product())
            else:
                return result

    def product(self) -> Expr:
        result = self.unary()
        while True:
            if self.accept('*'):
                result = as_expr(result*self.unary())
            elif self.accept('/'):
                result = as_expr(result/self.unary())
            else:
                return result

    def unary(self) -> Expr:
        if self.accept('-'):
            return as_expr(-self.unary())
        if self.accept('+'):
            return self.unary()
        return self.power()

    def power(self) -> Expr:
        base = self.postfix()
        if self.accept('^') or self.accept('**'):
            exponent = self.unary()  # right associative, may start with a sign
            return as_expr(base**exponent)
        return base

    def postfix(self) -> Expr:
        result = self.atom()
        while True:
            if self.accept('!!'):
                # ``n!!`` is Maxima's double factorial (5!! = 15), not ``(n!)!``
                result = as_expr(factorial2(result))
            elif self.accept('!'):
                result = as_expr(factorial(result))
            else:
                return result

    def atom(self) -> Expr:
        kind, text = self.take()
        if kind == 'number':
            return _number(text)
        if kind == 'name':
            if self.accept('('):
                args = self.arguments()
                return self.call(text, args, quoted=False)
            return self.name(text)
        if text == '(':
            inner = self.equation()
            self.expect(')')
            return inner
        if text == "'":
            kind, name = self.take()
            if kind != 'name' or not self.accept('('):
                raise MaximaSyntaxError("a quoted name must be a function call")
            return self.call(name, self.arguments(), quoted=True)
        raise MaximaSyntaxError("unexpected token %r" % text)

    def arguments(self) -> list[Expr]:
        """The arguments after an opening parenthesis, through the closing one."""
        args: list[Expr] = []
        if self.accept(')'):
            return args
        while True:
            args.append(self.equation())
            if self.accept(')'):
                return args
            self.expect(',')

    # -- translation

    def name(self, text: str) -> Expr:
        if text in _CONSTANTS:
            return _CONSTANTS[text]
        if text == self.dependent.name:
            return as_expr(self.function(self.independent))
        if text == self.independent.name:
            return self.independent
        return Symbol(text)

    def call(self, name: str, args: list[Expr], quoted: bool) -> Expr:
        if name == 'diff':
            return self.derivative(args, quoted)
        if name in FUNCTIONS:
            return FUNCTIONS[name](args)
        if name == self.dependent.name:
            return as_expr(self.function(*args))
        if name in _CONSTANTS or name == self.independent.name:
            raise MaximaSyntaxError("%s is not a function" % name)
        if name not in self.functions:
            self.functions[name] = undefined_function(name)
        return as_expr(self.functions[name](*args))

    def derivative(self, args: list[Expr], quoted: bool) -> Expr:
        """``diff(expr, var, n, var2, n2, ...)``; the noun form stays a
        ``Derivative``, the verb form is evaluated (which leaves the
        derivatives of undefined functions alone)."""
        if len(args) < 2:
            raise MaximaSyntaxError("diff needs at least two arguments")
        expr = args[0]
        counts: list[tuple[Symbol, int]] = []
        rest = args[1:]
        i = 0
        while i < len(rest):
            var = rest[i]
            if not isinstance(var, Symbol):
                raise MaximaSyntaxError("differentiation with respect to %s" % var)
            n = 1
            if i + 1 < len(rest) and isinstance(rest[i + 1], Integer):
                n = int(rest[i + 1])
                i += 2
            else:
                i += 1
            counts.append((var, n))
        result = as_expr(Derivative(expr, *counts))
        if quoted:
            return result
        return as_expr(result.doit())


def undefined_function(name: str) -> UndefinedFunction:
    f = Function(name)
    assert isinstance(f, UndefinedFunction)
    return f


def _number(text: str) -> Expr:
    if re.fullmatch(r"\d+", text):
        return Integer(int(text))
    return Rational(text)


def parse_expression(text: str, dependent: str = 'y', independent: str = 'x') -> Expr:
    """A Maxima expression as a SymPy expression; ``lhs = rhs`` becomes
    ``lhs - rhs``.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.maxima import parse_expression
    >>> parse_expression("bessel_j(n, x) + %pi*f(x)")
    pi*f(x) + besselj(n, x)
    >>> parse_expression("'diff(u,t,2) - a*u", 'u', 't')
    -a*u(t) + Derivative(u(t), (t, 2))
    """
    tokens = tokenize(text)
    parser = _Parser(tokens, Symbol(dependent), Symbol(independent))
    result = parser.equation()
    if parser.peek() is not None:
        raise MaximaSyntaxError("trailing tokens after %d in %r" % (parser.position, text))
    return result


def parse_equation(text: str) -> Expr:
    """A Maxima equation of the collections (in ``y`` and ``x``) as a SymPy
    expression equal to zero, or a ``MaximaSyntaxError`` when it is not an
    ordinary differential equation in ``y(x)``.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.maxima import parse_equation
    >>> parse_equation("(y+1)*'diff(y,x)=y+x")
    -x + (y(x) + 1)*Derivative(y(x), x) - y(x)
    """
    expr = parse_expression(text, 'y', 'x')
    if derivative_order(expr, y(x)) == 0:
        raise MaximaSyntaxError("not a differential equation in y(x): %r" % text)
    return expr


def call_arguments(text: str, start: int) -> Optional[tuple[list[str], int]]:
    """The comma-separated arguments of a call whose first argument starts
    at ``start`` (just after the opening parenthesis), split at depth zero,
    and the position after the closing parenthesis."""
    depth = 0
    args: list[str] = []
    begin = start
    i = start
    while i < len(text):
        c = text[i]
        if c == '(' or c == '[':
            depth += 1
        elif c == ')' or c == ']':
            if depth == 0:
                args.append(text[begin:i])
                return args, i + 1
            depth -= 1
        elif c == ',' and depth == 0:
            args.append(text[begin:i])
            begin = i + 1
        i += 1
    return None


#: a name that cannot occur in the files, so the Maxima parser — written
#: for differential equations — leaves every name a plain symbol
NO_FUNCTION = '__not_a_dependent_variable__'


#: the relational operators, the two-character ones first
_RELATIONS: tuple[tuple[str, Callable[[Expr, Expr], Boolean]], ...] = (
    ('>=', Ge), ('<=', Le), ('#', Ne), ('>', Gt), ('<', Lt), ('=', Eq))


_OPEN, _CLOSE = '([{', ')]}'


def readable(expr: object) -> bool:
    """Whether ``expr`` is a value this package can reason about: an
    expression without undefined functions, derivatives, integrals, sums,
    products or ``nan`` — any of which means a name or construct of the
    source that did not translate."""
    if not isinstance(expr, Expr):
        return False
    if expr.has(nan):
        return False
    return not expr.atoms(AppliedUndef, Derivative, Integral, Sum, Product)


def parse(text: str) -> Optional[Expr]:
    """A Maxima expression as a readable SymPy expression, or ``None``."""
    try:
        value = parse_expression(text, NO_FUNCTION, NO_FUNCTION)
    except (MaximaSyntaxError, RecursionError, ValueError, TypeError, ZeroDivisionError):
        return None
    return value if readable(value) else None


def group(text: str, start: int) -> Optional[tuple[str, int]]:
    """The inside of the bracketed group opening at ``text[start]``, and the
    index after its closing bracket; ``None`` when it does not close."""
    depth, index, quoted = 0, start, False
    while index < len(text):
        character = text[index]
        if character == '"':
            quoted = not quoted
        elif not quoted and character in _OPEN:
            depth += 1
        elif not quoted and character in _CLOSE:
            depth -= 1
            if depth == 0:
                return text[start + 1:index], index + 1
        index += 1
    return None


def split_arguments(text: str) -> list[str]:
    """``text`` split at its top-level commas, each part stripped.

    >>> split_arguments('f(x, y), [a, b], "c, d"')
    ['f(x, y)', '[a, b]', '"c, d"']
    """
    parts: list[str] = []
    depth, last, quoted = 0, 0, False
    for index, character in enumerate(text):
        if character == '"':
            quoted = not quoted
        elif quoted:
            continue
        elif character in _OPEN:
            depth += 1
        elif character in _CLOSE:
            depth -= 1
        elif character == ',' and depth == 0:
            parts.append(text[last:index].strip())
            last = index + 1
    parts.append(text[last:].strip())
    return [p for p in parts if p]


def relation(text: str) -> Optional[Boolean]:
    """A Maxima relation (``a > 0``, ``a # b``, ``notequal(a, 0)``,
    ``equal(a, b)``) as a SymPy one, or ``None`` when it is not one."""
    body = text.strip()
    call = re.fullmatch(r'(not)?equal\s*\((.*)\)', body, re.S)
    if call is not None:
        arguments = split_arguments(call.group(2))
        if len(arguments) != 2:
            return None
        lhs, rhs = parse(arguments[0]), parse(arguments[1])
        if lhs is None or rhs is None:
            return None
        return as_boolean(Ne(lhs, rhs) if call.group(1) else Eq(lhs, rhs))
    depth = 0
    for index, character in enumerate(body):
        if character in _OPEN:
            depth += 1
        elif character in _CLOSE:
            depth -= 1
        elif depth == 0:
            for symbol, build in _RELATIONS:
                if body.startswith(symbol, index):
                    lhs, rhs = parse(body[:index]), parse(body[index + len(symbol):])
                    if lhs is None or rhs is None:
                        return None
                    return as_boolean(build(lhs, rhs))
    return None


#: ``name(arguments)`` spanning a whole item
_APPLICATION = re.compile(r"([A-Za-z_]\w*)\s*\(", re.S)


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


def application(item: str) -> Optional[tuple[str, list[str]]]:
    """``(name, arguments)`` when ``item`` is one call and nothing else."""
    match = _APPLICATION.match(item)
    if match is None:
        return None
    closed = group(item, match.end() - 1)
    if closed is None or closed[1] != len(item):
        return None
    return match.group(1), split_arguments(closed[0])


def strip_comments(text: str) -> str:
    """``text`` with Maxima's ``/* ... */`` comments blanked out.

    They are blanked rather than removed so that positions still line up,
    and they nest, as in Maxima: a test file uses that to disable whole
    entries, and what is inside a comment is not code.
    """
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
    if depth and index < len(text) and out[index] != '\n':
        out[index] = ' '
    return "".join(out)
