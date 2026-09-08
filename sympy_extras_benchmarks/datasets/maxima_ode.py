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
code are not used, and nothing of the GPL-licensed files is stored in this
repository: they are cloned on first use into the cache directory (a
sparse checkout of Maxima's git repository on SourceForge, or the files of
the GitHub mirror), or read from a local Maxima installation named by
``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``.

The parser
==========

Maxima expressions are parsed by a small recursive descent parser
(``parse_expression``): the operators ``+ - * / ^`` and ``**``, unary
minus, ``!``, the equality ``=``, function calls and the noun form
``'diff(y, x, n)``. The dependent variable becomes an applied undefined
function (``y(x)``), the known functions of Maxima are mapped to SymPy's
(``%e`` to ``E``, ``bessel_j`` to ``besselj``, ``legendre_p`` to
``legendre``, ...), other applied names become undefined functions
(``f(x)``) and other names become symbols (including ``lambda``, which
Python's parser could not accept). Numbers are exact.

Examples
========

>>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_equation
>>> entry = parse_equation("'diff(y,x)^2 + a*y*'diff(y,x) = a*x")
>>> entry
-a*x + a*y(x)*Derivative(y(x), x) + Derivative(y(x), x)**2
>>> parse_equation("x^2*'diff(y,x,2) + lambda*y")
lambda*y(x) + x**2*Derivative(y(x), (x, 2))
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import urllib.request
import os
from typing import Callable, Optional, Sequence

from sympy import (E, I, pi, oo, EulerGamma, Integer, Rational, Symbol, Function,
    Derivative, factorial, sin, cos, tan, cot, sec, csc, exp, log, sqrt, sinh,
    cosh, tanh, coth, asin, acos, atan, acot, atan2, asinh, acosh, atanh, Abs,
    erf, erfc, gamma, besselj, bessely, besseli, besselk, legendre, sign, floor,
    ceiling, binomial, airyai, airybi)
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.function import AppliedUndef, UndefinedFunction

from sympy_extras._typing import as_expr

from sympy_extras_benchmarks.cache import cache_directory

__all__ = ['ODEEntry', 'COLLECTIONS', 'FILES', 'fetch', 'load', 'parse_equation',
           'parse_expression', 'parse_file', 'tokenize', 'MaximaSyntaxError']

#: Maxima's git repository (SourceForge) and the directory of the tests
REPOSITORY = "https://git.code.sf.net/p/maxima/code"
SUBDIRECTORY = "share/contrib/diffequations/tests"
#: the raw files of the GitHub mirror and of SourceForge's browser, as fallbacks
MIRRORS = (
    "https://raw.githubusercontent.com/calyau/maxima/master/" + SUBDIRECTORY + "/%s.mac",
    "https://sourceforge.net/p/maxima/code/ci/master/tree/" + SUBDIRECTORY + "/%s.mac?format=raw",
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


class MaximaSyntaxError(ValueError):
    """The text is not a Maxima expression the parser understands."""


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


x = Symbol('x')
y = Function('y')
assert isinstance(y, UndefinedFunction)


def derivative_order(expr: Basic, f: Expr) -> int:
    """The order of the highest derivative of ``f`` in ``expr``."""
    orders = [sum(int(as_expr(n)) for _, n in d.variable_count)
              for d in expr.atoms(Derivative) if d.expr == f]
    return max(orders, default=0)


# ---------------------------------------------------------------------------
# tokenizer

#: a token: its kind (``number``, ``name``, ``op``) and text
Token = tuple[str, str]

_NUMBER = re.compile(r"\d+\.\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|\d+(?:[eE][+-]?\d+)?")
_NAME = re.compile(r"%?[A-Za-z_][A-Za-z_0-9]*")
_OPERATORS = ('**', ':=', '+', '-', '*', '/', '^', '=', '(', ')', ',', "'", '!', '[', ']', ':')


def tokenize(text: str) -> list[Token]:
    """The tokens of a Maxima expression.

    Examples
    ========

    >>> from sympy_extras_benchmarks.datasets.maxima_ode import tokenize
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


# ---------------------------------------------------------------------------
# translation of names

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
}


# ---------------------------------------------------------------------------
# parser

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
        self.function: UndefinedFunction = y if dependent.name == 'y' else _undefined(dependent.name)
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
        while self.accept('!'):
            result = as_expr(factorial(result))
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
            self.functions[name] = _undefined(name)
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


def _undefined(name: str) -> UndefinedFunction:
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

    >>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_expression
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

    >>> from sympy_extras_benchmarks.datasets.maxima_ode import parse_equation
    >>> parse_equation("(y+1)*'diff(y,x)=y+x")
    -x + (y(x) + 1)*Derivative(y(x), x) - y(x)
    """
    expr = parse_expression(text, 'y', 'x')
    if derivative_order(expr, y(x)) == 0:
        raise MaximaSyntaxError("not a differential equation in y(x): %r" % text)
    return expr


# ---------------------------------------------------------------------------
# the test files

_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_ENTRY = re.compile(r"pn_\(\s*(\d+)\s*\)\s*,\s*ans\s*:\s*contrib_ode\s*\(\s*eqn\s*:")
_METHOD = re.compile(r"\[\s*method\s*,\s*ode_check\s*\(.*?\]\s*;\s*\[\s*([A-Za-z_0-9]+)\s*,", re.S)


def _call_arguments(text: str, start: int) -> Optional[tuple[list[str], int]]:
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
        parsed = _call_arguments(text, match.end())
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
                {_undefined(dependent)(x): y(x)}))
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


def _clone(target: pathlib.Path) -> bool:
    """A sparse checkout of the tests directory of Maxima's repository."""
    if (target / SUBDIRECTORY).is_dir():
        return True
    try:
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                        REPOSITORY, str(target)], check=True, capture_output=True, timeout=900)
        subprocess.run(['git', '-C', str(target), 'sparse-checkout', 'set', SUBDIRECTORY],
                       check=True, capture_output=True, timeout=900)
    except (subprocess.SubprocessError, OSError):
        return False
    return (target / SUBDIRECTORY).is_dir()


def _download(name: str, target: pathlib.Path) -> Optional[str]:
    for pattern in MIRRORS:
        try:
            with urllib.request.urlopen(pattern % name, timeout=60) as response:
                text = response.read().decode('utf-8', errors='replace')
        except OSError:
            continue
        if 'contrib_ode' in text or 'ode' in text[:2000]:
            target.write_text(text)
            return text
    return None


def fetch(name: str) -> Optional[str]:
    """The text of the test file ``name`` (without extension): from the
    directory named by ``$SYMPY_EXTRAS_BENCHMARKS_MAXIMA_TESTS``, from the
    cache, from a sparse clone of Maxima's repository, or from the mirrors;
    ``None`` when none of them is reachable."""
    local = _local_directory()
    if local is not None and (local / (name + '.mac')).is_file():
        return (local / (name + '.mac')).read_text(errors='replace')
    cache = cache_directory() / 'maxima'
    cache.mkdir(parents=True, exist_ok=True)
    clone = cache / 'repository'
    path = clone / SUBDIRECTORY / (name + '.mac')
    if path.is_file():
        return path.read_text(errors='replace')
    copy = cache / (name + '.mac')
    if copy.is_file():
        return copy.read_text(errors='replace')
    if _clone(clone) and path.is_file():
        return path.read_text(errors='replace')
    return _download(name, copy)


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
