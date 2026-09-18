"""The SMT-LIB 2 language, read into SymPy formulas.

S-expressions
=============

:func:`tokenize` and :func:`parse` read the s-expressions of a file:
parentheses, atoms, quoted symbols ``|...|`` and strings; comments are
dropped.

Nonlinear real arithmetic
=========================

:func:`translate` turns the commands of a ``QF_NRA`` file into a
:class:`Problem`: the ``declare-fun`` / ``declare-const`` of real
variables, ``define-fun`` of constants, the ``assert`` commands (conjoined)
and the ``:status``. Terms use ``+ - * /`` and numerals, formulas ``and or
not => xor = distinct ite let`` and the relations ``< <= > >= =``; a
``let`` binds terms or formulas. ``ite`` on terms is translated with
``Piecewise``.

Integers and quantifiers
========================

:func:`translate_arithmetic` reads the arithmetic logics over the reals
*and the integers*, quantified or not (:data:`ARITHMETIC_LOGICS`), into an
:class:`ArithProblem`: it adds the integer sorts and operations (``div``,
``mod``, ``abs``, ``divisible``, ``to_real``, ``to_int``) and the
quantifiers, which become :class:`~sympy_extras.assumptions.ForAll` and
:class:`~sympy_extras.assumptions.Exists`.

Integer division and remainder follow the SMT-LIB definition (Boute's
Euclidean division: the remainder is always non-negative), which is
*not* SymPy's ``Mod`` for a negative divisor, so ``div`` and ``mod`` are
translated only when the divisor is a positive numeral; anything else
makes the file unusable and :func:`translate_arithmetic` returns ``None``.

Both translators return ``None`` for a file beyond what they read, rather
than an approximation of it. Nothing here reads a file from disk or knows
which collection a text comes from.

Examples
========

>>> from sympy_extras_benchmarks.parsers.smtlib import translate, translate_arithmetic
>>> text = '''
... (set-logic QF_NRA)
... (set-info :status unsat)
... (declare-fun x () Real)
... (assert (let ((?v (* x x))) (and (< ?v 0) (> x 1))))
... (check-sat)
... '''
>>> problem = translate(text, 'demo')
>>> problem
Problem(demo, unsat, 1 variables)
>>> problem.formula
(x > 1) & (x**2 < 0)
>>> text = '''
... (set-info :status sat)
... (set-logic NRA)
... (declare-fun a () Real)
... (assert (exists ((x Real)) (= (* x x) a)))
... (check-sat)
... '''
>>> problem = translate_arithmetic(text, 'quantified')
>>> problem
ArithProblem(quantified, NRA, sat, 0 integer, 1 real)
>>> problem.formula
Exists(x, Eq(x**2, a))
"""
from __future__ import annotations

from typing import Optional, Sequence, Union

from sympy import (Abs, And, Eq, Implies, Mod, Ne, Not, Or, Piecewise, Rational, Symbol, Xor,
                   false, true)
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean, ITE
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean, as_expr

__all__ = ['SExpr', 'SMTLibError', 'tokenize', 'parse', 'Problem', 'translate',
           'ARITHMETIC_LOGICS', 'ArithProblem', 'translate_arithmetic']


#: an s-expression: an atom or a list of s-expressions
SExpr = Union[str, list['SExpr']]


class SMTLibError(ValueError):
    """The file uses something beyond the ``QF_NRA`` formulas translated."""


def tokenize(text: str) -> list[str]:
    """The tokens of an SMT-LIB file: parentheses, atoms, quoted symbols
    ``|...|`` and strings ``"..."``; comments (``;``) are dropped.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.smtlib import tokenize
    >>> tokenize('(assert (< x 1)) ; a comment')
    ['(', 'assert', '(', '<', 'x', '1', ')', ')']
    """
    tokens: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif c == ';':
            while i < n and text[i] != '\n':
                i += 1
        elif c in '()':
            tokens.append(c)
            i += 1
        elif c == '|':
            j = text.find('|', i + 1)
            if j < 0:
                raise SMTLibError("unterminated quoted symbol")
            tokens.append(text[i:j + 1])
            i = j + 1
        elif c == '"':
            j = i + 1
            while j < n:
                if text[j] == '"':
                    if j + 1 < n and text[j + 1] == '"':
                        j += 2
                        continue
                    break
                j += 1
            if j >= n:
                raise SMTLibError("unterminated string")
            tokens.append(text[i:j + 1])
            i = j + 1
        else:
            j = i
            while j < n and not text[j].isspace() and text[j] not in '()':
                j += 1
            tokens.append(text[i:j])
            i = j
    return tokens


def parse(tokens: Sequence[str]) -> list[SExpr]:
    """The top level s-expressions of a token list.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.smtlib import parse, tokenize
    >>> parse(tokenize('(check-sat) (assert (and a (not b)))'))
    [['check-sat'], ['assert', ['and', 'a', ['not', 'b']]]]
    """
    stack: list[list[SExpr]] = [[]]
    for token in tokens:
        if token == '(':
            stack.append([])
        elif token == ')':
            if len(stack) == 1:
                raise SMTLibError("unbalanced parentheses")
            done = stack.pop()
            stack[-1].append(done)
        else:
            stack[-1].append(token)
    if len(stack) != 1:
        raise SMTLibError("unbalanced parentheses")
    return stack[0]


class Problem:
    """A parsed problem: its formula, variables and expected status.

    Attributes
    ==========

    name : str
        The file name without extension.
    formula : Boolean
        The conjunction of the assertions.
    variables : list[Symbol]
        The declared real variables, sorted by name.
    status : str
        ``'sat'``, ``'unsat'`` or ``'unknown'``.
    """

    def __init__(self, name: str, formula: Boolean, variables: list[Symbol], status: str) -> None:
        self.name = name
        self.formula = formula
        self.variables = variables
        self.status = status

    def __repr__(self) -> str:
        return "Problem(%s, %s, %d variables)" % (self.name, self.status, len(self.variables))


def _number(token: str) -> Optional[Rational]:
    """A numeral or decimal literal, ``None`` for anything else."""
    if not token or not (token[0].isdigit() or token[0] == '.'):
        return None
    try:
        return Rational(token)
    except (ValueError, TypeError):
        return None


class _Translator:
    def __init__(self) -> None:
        self.symbols: dict[str, Symbol] = {}
        self.definitions: dict[str, Basic] = {}
        self.bindings: list[dict[str, Basic]] = []

    def lookup(self, name: str) -> Optional[Basic]:
        for scope in reversed(self.bindings):
            if name in scope:
                return scope[name]
        if name in self.definitions:
            return self.definitions[name]
        return self.symbols.get(name)

    def _bind(self, bindings: SExpr) -> None:
        """Push the scope of a ``let``; every value is a term or a formula."""
        if not isinstance(bindings, list):
            raise SMTLibError("bad let")
        scope: dict[str, Basic] = {}
        for binding in bindings:
            if not isinstance(binding, list) or len(binding) != 2 or not isinstance(binding[0], str):
                raise SMTLibError("bad let binding")
            scope[binding[0]] = self.value(binding[1])
        self.bindings.append(scope)

    def value(self, e: SExpr) -> Basic:
        """A term or a formula, whichever ``e`` is."""
        try:
            return self.term(e)
        except SMTLibError:
            return self.formula(e)

    def term(self, e: SExpr) -> Expr:
        if isinstance(e, str):
            number = _number(e)
            if number is not None:
                return number
            bound = self.lookup(e)
            if isinstance(bound, Expr):
                return bound
            raise SMTLibError("unknown term %s" % e)
        if not e or not isinstance(e[0], str):
            raise SMTLibError("bad term")
        head, args = e[0], e[1:]
        if head == '!':
            # ``(! t :named foo)``: an annotation does not change the term
            if not args:
                raise SMTLibError("bad annotation")
            return self.term(args[0])
        if head == '^':
            # a power with a literal integer exponent, as the nonlinear
            # benchmarks of cvc5 and Z3 write it
            if len(args) != 2 or not isinstance(args[1], str):
                raise SMTLibError("bad power")
            exponent = _number(args[1])
            if exponent is None or not exponent.is_Integer or exponent < 0:
                raise SMTLibError("power with a non-literal exponent")
            return as_expr(self.term(args[0])**exponent)
        if head == 'let':
            if len(args) != 2:
                raise SMTLibError("bad let")
            self._bind(args[0])
            try:
                return self.term(args[1])
            finally:
                self.bindings.pop()
        if head == '+':
            total: Expr = Rational(0)
            for a in args:
                total = as_expr(total + self.term(a))
            return total
        if head == '*':
            product: Expr = Rational(1)
            for a in args:
                product = as_expr(product*self.term(a))
            return product
        if head == '-':
            if len(args) == 1:
                return as_expr(-self.term(args[0]))
            difference = self.term(args[0])
            for a in args[1:]:
                difference = as_expr(difference - self.term(a))
            return difference
        if head == '/':
            quotient = self.term(args[0])
            for a in args[1:]:
                quotient = as_expr(quotient/self.term(a))
            return quotient
        if head == 'ite':
            if len(args) != 3:
                raise SMTLibError("bad ite")
            condition = self.formula(args[0])
            return as_expr(Piecewise((self.term(args[1]), condition), (self.term(args[2]), True)))
        raise SMTLibError("unknown operator %s" % head)

    def formula(self, e: SExpr) -> Boolean:
        if isinstance(e, str):
            if e == 'true':
                return true
            if e == 'false':
                return false
            bound = self.lookup(e)
            if isinstance(bound, Boolean):
                return bound
            raise SMTLibError("unknown formula %s" % e)
        if not e or not isinstance(e[0], str):
            raise SMTLibError("bad formula")
        head, args = e[0], e[1:]
        if head == '!':
            if not args:
                raise SMTLibError("bad annotation")
            return self.formula(args[0])
        if head == 'let':
            if len(args) != 2:
                raise SMTLibError("bad let")
            self._bind(args[0])
            try:
                return self.formula(args[1])
            finally:
                self.bindings.pop()
        if head == 'and':
            return as_boolean(And(*[self.formula(a) for a in args]))
        if head == 'or':
            return as_boolean(Or(*[self.formula(a) for a in args]))
        if head == 'xor':
            return as_boolean(Xor(*[self.formula(a) for a in args]))
        if head == 'not':
            if len(args) != 1:
                raise SMTLibError("bad not")
            return as_boolean(Not(self.formula(args[0])))
        if head == '=>':
            parts = [self.formula(a) for a in args]
            result = parts[-1]
            for p in reversed(parts[:-1]):
                result = as_boolean(Implies(p, result))
            return result
        if head == 'ite':
            if len(args) != 3:
                raise SMTLibError("bad ite")
            return as_boolean(ITE(self.formula(args[0]), self.formula(args[1]), self.formula(args[2])))
        if head in ('<=', '<', '>=', '>', '=', 'distinct'):
            if head == '=' and args and not _is_term(args[0], self):
                # equality of formulas
                parts = [self.formula(a) for a in args]
                return as_boolean(And(*[_equivalent(p, q) for p, q in zip(parts, parts[1:])]))
            terms = [self.term(a) for a in args]
            relations: list[Boolean] = []
            if head == 'distinct':
                for i, s in enumerate(terms):
                    for t in terms[i + 1:]:
                        relations.append(as_boolean(Ne(s, t)))
                return as_boolean(And(*relations))
            for s, t in zip(terms, terms[1:]):
                if head == '<=':
                    relations.append(as_boolean(s <= t))
                elif head == '<':
                    relations.append(as_boolean(s < t))
                elif head == '>=':
                    relations.append(as_boolean(s >= t))
                elif head == '>':
                    relations.append(as_boolean(s > t))
                else:
                    relations.append(as_boolean(Eq(s, t)))
            return as_boolean(And(*relations))
        raise SMTLibError("unknown connective %s" % head)


def _equivalent(p: Boolean, q: Boolean) -> Boolean:
    from sympy import Equivalent
    return as_boolean(Equivalent(p, q))


def _is_term(e: SExpr, translator: _Translator) -> bool:
    """Whether ``e`` denotes a term (rather than a formula), decided by
    translating it."""
    try:
        translator.term(e)
    except SMTLibError:
        return False
    return True


def translate(text: str, name: str = '') -> Optional[Problem]:
    """The problem in an SMT-LIB file, or ``None`` when it uses something
    beyond ``QF_NRA`` formulas (non-real sorts, uninterpreted functions
    with arguments, quantifiers) or has no assertion."""
    try:
        commands = parse(tokenize(text))
    except SMTLibError:
        return None
    translator = _Translator()
    status = 'unknown'
    assertions: list[Boolean] = []
    for command in commands:
        if not isinstance(command, list) or not command:
            continue
        head = command[0]
        if head == 'set-info' and len(command) >= 3 and command[1] == ':status' and isinstance(command[2], str):
            status = command[2]
        elif head == 'declare-fun' and len(command) == 4 and isinstance(command[1], str):
            if command[2] != [] or command[3] != 'Real':
                return None
            translator.symbols[command[1]] = Symbol(command[1])
        elif head == 'declare-const' and len(command) == 3 and isinstance(command[1], str):
            if command[2] != 'Real':
                return None
            translator.symbols[command[1]] = Symbol(command[1])
        elif head == 'define-fun' and len(command) == 5 and isinstance(command[1], str):
            if command[2] != []:
                return None
            try:
                translator.definitions[command[1]] = translator.value(command[4])
            except (SMTLibError, ZeroDivisionError, TypeError, RecursionError):
                return None
        elif head == 'assert' and len(command) == 2:
            try:
                assertions.append(translator.formula(command[1]))
            except (SMTLibError, ZeroDivisionError, TypeError, RecursionError):
                return None
        elif head in ('declare-sort', 'define-sort', 'push', 'pop'):
            return None
    if not assertions:
        return None
    variables = sorted(translator.symbols.values(), key=lambda s: s.name)
    return Problem(name, as_boolean(And(*assertions)), variables, status)


# ---------------------------------------------------------------------------
# integers and quantifiers

#: the arithmetic logics whose files are read (``ALL`` is kept when the
#: file turns out to use nothing but arithmetic)
ARITHMETIC_LOGICS: frozenset[str] = frozenset({
    'QF_LIA', 'QF_NIA', 'LIA', 'NIA', 'QF_LRA', 'QF_NRA', 'LRA', 'NRA',
    'QF_LIRA', 'QF_NIRA', 'LIRA', 'NIRA', 'ALL', 'AUFLIA', 'AUFNIRA'})


class ArithProblem:
    """One problem: its formula, the sorts of its variables and the
    recorded answer.

    Attributes
    ==========

    name : str
        The file name without extension.
    formula : Boolean
        The conjunction of the assertions, quantifiers included.
    integers, reals : list[Symbol]
        The free variables of each sort, sorted by name.
    status : str
        ``'sat'``, ``'unsat'`` or ``'unknown'``.
    logic : str
        The ``set-logic`` of the file (``''`` when it has none).
    quantified : bool
        Whether the formula carries a quantifier.
    bound_integers, bound_reals : list[Symbol]
        The variables a quantifier bound, of each sort. They are not free
        variables of the problem, but they decide its
        :attr:`domain` when every variable is bound.
    """

    def __init__(self, name: str, formula: Boolean, integers: list[Symbol], reals: list[Symbol],
                 status: str, logic: str, quantified: bool,
                 bound_integers: Optional[list[Symbol]] = None,
                 bound_reals: Optional[list[Symbol]] = None) -> None:
        self.name = name
        self.formula = formula
        self.integers = integers
        self.reals = reals
        self.status = status
        self.logic = logic
        self.quantified = quantified
        self.bound_integers = list(bound_integers or [])
        self.bound_reals = list(bound_reals or [])

    @property
    def variables(self) -> list[Symbol]:
        """The free variables, integers first."""
        return self.integers + self.reals

    @property
    def domain(self) -> Set:
        """``S.Integers`` when every variable is an integer, ``S.Reals``
        otherwise (a problem mixing the sorts is not produced).

        The quantifier-bound variables count: a closed formula has no
        free variable at all, and its domain is the one its binders
        range over.
        """
        integers = self.integers + self.bound_integers
        reals = self.reals + self.bound_reals
        return S.Integers if integers and not reals else S.Reals

    def __repr__(self) -> str:
        return "ArithProblem(%s, %s, %s, %d integer, %d real)" % (
            self.name, self.logic, self.status, len(self.integers), len(self.reals))


def _positive_numeral(e: SExpr) -> Optional[int]:
    """``e`` as a positive integer literal, ``None`` otherwise."""
    if not isinstance(e, str):
        return None
    value = _number(e)
    if value is None or not value.is_Integer or value <= 0:
        return None
    return int(value)


class _ArithmeticTranslator:
    """Terms and formulas of one file, with the scopes of ``let`` and of
    the quantifiers."""

    def __init__(self) -> None:
        self.integers: dict[str, Symbol] = {}
        self.reals: dict[str, Symbol] = {}
        self.definitions: dict[str, Basic] = {}
        self.bindings: list[dict[str, Basic]] = []
        #: the sorts of every variable a quantifier bound, anywhere
        self.bound_integers: list[Symbol] = []
        self.bound_reals: list[Symbol] = []
        #: the names already taken, so that a quantifier cannot capture
        self.taken: set[str] = set()

    def lookup(self, name: str) -> Optional[Basic]:
        for scope in reversed(self.bindings):
            if name in scope:
                return scope[name]
        if name in self.definitions:
            return self.definitions[name]
        if name in self.integers:
            return self.integers[name]
        return self.reals.get(name)

    def declare(self, name: str, sort: SExpr) -> bool:
        """Record a variable of an arithmetic sort; ``False`` for any
        other sort."""
        if sort == 'Int':
            self.integers[name] = Symbol(name, integer=True)
            self.taken.add(name)
            return True
        if sort == 'Real':
            self.reals[name] = Symbol(name)
            self.taken.add(name)
            return True
        return False

    def _bind_let(self, bindings: SExpr) -> None:
        if not isinstance(bindings, list):
            raise SMTLibError("bad let")
        scope: dict[str, Basic] = {}
        for binding in bindings:
            if not isinstance(binding, list) or len(binding) != 2 or not isinstance(binding[0], str):
                raise SMTLibError("bad let binding")
            scope[binding[0]] = self.value(binding[1])
            self.taken.add(binding[0])
        self.bindings.append(scope)

    def _bind_quantifier(self, declarations: SExpr) -> list[Symbol]:
        """Push the scope of a quantifier and return its variables."""
        if not isinstance(declarations, list) or not declarations:
            raise SMTLibError("bad quantifier")
        scope: dict[str, Basic] = {}
        variables: list[Symbol] = []
        for declaration in declarations:
            if not isinstance(declaration, list) or len(declaration) != 2 or not isinstance(declaration[0], str):
                raise SMTLibError("bad quantifier binding")
            name = self._fresh(declaration[0])
            if declaration[1] == 'Int':
                variable = Symbol(name, integer=True)
                self.bound_integers.append(variable)
            elif declaration[1] == 'Real':
                variable = Symbol(name)
                self.bound_reals.append(variable)
            else:
                raise SMTLibError("quantifier over %s" % (declaration[1],))
            self.taken.add(name)
            scope[declaration[0]] = variable
            variables.append(variable)
        self.bindings.append(scope)
        return variables

    def _fresh(self, name: str) -> str:
        """``name`` itself when nothing else uses it, and a renaming
        otherwise.

        SymPy symbols are identified by their name, so a binder which
        shadows a declared variable, a ``let`` or an enclosing quantifier
        would capture the occurrences of the outer one.
        """
        if name not in self.taken:
            return name
        index = 1
        while '%s__%d' % (name, index) in self.taken:
            index += 1
        return '%s__%d' % (name, index)

    def value(self, e: SExpr) -> Basic:
        """A term or a formula, whichever ``e`` is."""
        try:
            return self.term(e)
        except SMTLibError:
            return self.formula(e)

    def term(self, e: SExpr) -> Expr:
        if isinstance(e, str):
            number = _number(e)
            if number is not None:
                return number
            bound = self.lookup(e)
            if isinstance(bound, Expr):
                return bound
            raise SMTLibError("unknown term %s" % e)
        if not e or not isinstance(e[0], str):
            raise SMTLibError("bad term")
        head, args = e[0], e[1:]
        if head == '!':
            # ``(! t :named foo)``: an annotation does not change the term
            if not args:
                raise SMTLibError("bad annotation")
            return self.term(args[0])
        if head == '^':
            # a power with a literal integer exponent, as the nonlinear
            # benchmarks of cvc5 and Z3 write it
            if len(args) != 2 or not isinstance(args[1], str):
                raise SMTLibError("bad power")
            exponent = _number(args[1])
            if exponent is None or not exponent.is_Integer or exponent < 0:
                raise SMTLibError("power with a non-literal exponent")
            return as_expr(self.term(args[0])**exponent)
        if head == 'let':
            if len(args) != 2:
                raise SMTLibError("bad let")
            self._bind_let(args[0])
            try:
                return self.term(args[1])
            finally:
                self.bindings.pop()
        if head == '+':
            total: Expr = Rational(0)
            for a in args:
                total = as_expr(total + self.term(a))
            return total
        if head == '*':
            product: Expr = Rational(1)
            for a in args:
                product = as_expr(product*self.term(a))
            return product
        if head == '-':
            if len(args) == 1:
                return as_expr(-self.term(args[0]))
            difference = self.term(args[0])
            for a in args[1:]:
                difference = as_expr(difference - self.term(a))
            return difference
        if head == '/':
            quotient = self.term(args[0])
            for a in args[1:]:
                divisor = self.term(a)
                if divisor.is_zero:
                    raise SMTLibError("division by zero")
                quotient = as_expr(quotient/divisor)
            return quotient
        if head in ('div', 'mod'):
            # only a positive numeral divisor, where SMT-LIB's Euclidean
            # division agrees with SymPy's floor division and ``Mod``
            if len(args) != 2:
                raise SMTLibError("bad %s" % head)
            divisor_value = _positive_numeral(args[1])
            if divisor_value is None:
                raise SMTLibError("%s by a non-numeral" % head)
            dividend = self.term(args[0])
            if head == 'mod':
                return as_expr(Mod(dividend, divisor_value))
            return as_expr((dividend - Mod(dividend, divisor_value))/divisor_value)
        if head == 'abs':
            if len(args) != 1:
                raise SMTLibError("bad abs")
            return as_expr(Abs(self.term(args[0])))
        if head in ('to_real', 'to_int'):
            if len(args) != 1:
                raise SMTLibError("bad %s" % head)
            if head == 'to_int':
                raise SMTLibError("to_int is not translated")
            return self.term(args[0])
        if head == 'ite':
            if len(args) != 3:
                raise SMTLibError("bad ite")
            condition = self.formula(args[0])
            return as_expr(Piecewise((self.term(args[1]), condition), (self.term(args[2]), True)))
        raise SMTLibError("unknown operator %s" % head)

    def formula(self, e: SExpr) -> Boolean:
        if isinstance(e, str):
            if e == 'true':
                return true
            if e == 'false':
                return false
            bound = self.lookup(e)
            if isinstance(bound, Boolean):
                return bound
            raise SMTLibError("unknown formula %s" % e)
        if not e or not isinstance(e[0], str):
            raise SMTLibError("bad formula")
        head, args = e[0], e[1:]
        if head == '!':
            if not args:
                raise SMTLibError("bad annotation")
            return self.formula(args[0])
        if head == 'let':
            if len(args) != 2:
                raise SMTLibError("bad let")
            self._bind_let(args[0])
            try:
                return self.formula(args[1])
            finally:
                self.bindings.pop()
        if head in ('forall', 'exists'):
            if len(args) != 2:
                raise SMTLibError("bad quantifier")
            variables = self._bind_quantifier(args[0])
            try:
                body = self.formula(args[1])
            finally:
                self.bindings.pop()
            quantifier = ForAll if head == 'forall' else Exists
            return as_boolean(quantifier(variables, body))
        if head == 'and':
            return as_boolean(And(*[self.formula(a) for a in args]))
        if head == 'or':
            return as_boolean(Or(*[self.formula(a) for a in args]))
        if head == 'xor':
            return as_boolean(Xor(*[self.formula(a) for a in args]))
        if head == 'not':
            if len(args) != 1:
                raise SMTLibError("bad not")
            return as_boolean(Not(self.formula(args[0])))
        if head == '=>':
            parts = [self.formula(a) for a in args]
            result = parts[-1]
            for p in reversed(parts[:-1]):
                result = as_boolean(Implies(p, result))
            return result
        if head == 'ite':
            if len(args) != 3:
                raise SMTLibError("bad ite")
            return as_boolean(ITE(self.formula(args[0]), self.formula(args[1]), self.formula(args[2])))
        if head == '_' and len(args) == 2 and args[0] == 'divisible':
            raise SMTLibError("bare divisible")
        if isinstance(head, str) and head in ('<=', '<', '>=', '>', '=', 'distinct'):
            return self._relation(head, args)
        raise SMTLibError("unknown connective %s" % head)

    def indexed(self, e: SExpr, args: Sequence[SExpr]) -> Boolean:
        """``((_ divisible k) t)``: ``k`` divides ``t``."""
        if (not isinstance(e, list) or len(e) != 3 or e[0] != '_' or e[1] != 'divisible'
                or len(args) != 1):
            raise SMTLibError("unknown indexed operator")
        divisor = _positive_numeral(e[2])
        if divisor is None:
            raise SMTLibError("divisible by a non-numeral")
        return as_boolean(Eq(Mod(self.term(args[0]), divisor), 0))

    def _relation(self, head: str, args: Sequence[SExpr]) -> Boolean:
        if head == '=' and args and not self._is_term(args[0]):
            parts = [self.formula(a) for a in args]
            from sympy import Equivalent
            return as_boolean(And(*[as_boolean(Equivalent(p, q)) for p, q in zip(parts, parts[1:])]))
        terms = [self.term(a) for a in args]
        relations: list[Boolean] = []
        if head == 'distinct':
            for i, s in enumerate(terms):
                for t in terms[i + 1:]:
                    relations.append(as_boolean(Ne(s, t)))
            return as_boolean(And(*relations))
        for s, t in zip(terms, terms[1:]):
            if head == '<=':
                relations.append(as_boolean(s <= t))
            elif head == '<':
                relations.append(as_boolean(s < t))
            elif head == '>=':
                relations.append(as_boolean(s >= t))
            elif head == '>':
                relations.append(as_boolean(s > t))
            else:
                relations.append(as_boolean(Eq(s, t)))
        return as_boolean(And(*relations))

    def _is_term(self, e: SExpr) -> bool:
        try:
            self.term(e)
        except SMTLibError:
            return False
        return True


def _application(translator: _ArithmeticTranslator, e: SExpr) -> Boolean:
    """A formula whose head is an indexed operator, e.g. ``divisible``."""
    if not isinstance(e, list) or not e:
        raise SMTLibError("bad application")
    return translator.indexed(e[0], e[1:])


def _recorded_status(commands: Sequence[SExpr]) -> str:
    """The expected answer the ``:status`` of the file records, ``'unknown'``
    when it records neither ``sat`` nor ``unsat``."""
    for command in commands:
        if (isinstance(command, list) and len(command) >= 3 and command[0] == 'set-info'
                and command[1] == ':status' and isinstance(command[2], str)):
            if command[2] in ('sat', 'unsat'):
                return command[2]
    return 'unknown'


def translate_arithmetic(text: str, name: str = '') -> Optional[ArithProblem]:
    """The problem in an SMT-LIB file, or ``None`` when it is not an
    arithmetic problem this module reads: a non-arithmetic logic, a sort
    other than ``Int`` or ``Real``, an uninterpreted function with
    arguments, an operation left untranslated, a mixture of the sorts, or
    no assertion.
    """
    try:
        commands = parse(tokenize(text))
    except SMTLibError:
        return None
    translator = _ArithmeticTranslator()
    logic = ''
    assertions: list[Boolean] = []
    for command in commands:
        if not isinstance(command, list) or not command:
            continue
        head = command[0]
        if head == 'set-logic' and len(command) == 2 and isinstance(command[1], str):
            logic = command[1]
            if logic not in ARITHMETIC_LOGICS:
                return None
        elif head in ('declare-fun', 'declare-const'):
            if head == 'declare-fun' and len(command) == 4 and isinstance(command[1], str):
                if command[2] != []:
                    return None
                if not translator.declare(command[1], command[3]):
                    return None
            elif head == 'declare-const' and len(command) == 3 and isinstance(command[1], str):
                if not translator.declare(command[1], command[2]):
                    return None
            else:
                return None
        elif head == 'define-fun' and len(command) == 5 and isinstance(command[1], str):
            if command[2] != []:
                return None
            try:
                translator.definitions[command[1]] = translator.value(command[4])
            except (SMTLibError, ZeroDivisionError, TypeError, RecursionError):
                return None
        elif head == 'assert' and len(command) == 2:
            try:
                assertions.append(_assertion(translator, command[1]))
            except (SMTLibError, ZeroDivisionError, TypeError, ValueError, RecursionError):
                return None
        elif head in ('declare-sort', 'define-sort', 'declare-datatype', 'declare-datatypes',
                      'push', 'pop', 'define-fun-rec', 'declare-fun-rec'):
            return None
    if not assertions:
        return None
    if (translator.integers or translator.bound_integers) and (translator.reals or translator.bound_reals):
        return None
    formula = as_boolean(And(*assertions))
    quantified = any(isinstance(a, (ForAll, Exists)) for a in _subformulas(formula))
    integers = sorted(translator.integers.values(), key=lambda s: s.name)
    reals = sorted(translator.reals.values(), key=lambda s: s.name)
    return ArithProblem(name, formula, integers, reals,
                        _recorded_status(commands), logic, quantified,
                        translator.bound_integers, translator.bound_reals)


def _assertion(translator: _ArithmeticTranslator, e: SExpr) -> Boolean:
    """One ``assert`` argument, allowing an indexed head such as
    ``((_ divisible 3) x)``."""
    if isinstance(e, list) and e and isinstance(e[0], list):
        return _application(translator, e)
    return translator.formula(e)


def _subformulas(formula: Boolean) -> list[Basic]:
    """``formula`` and everything inside it (quantifiers are not
    ``Boolean`` arguments of their parents in every case, so the walk is
    explicit)."""
    seen: list[Basic] = []
    stack: list[Basic] = [formula]
    while stack:
        node = stack.pop()
        seen.append(node)
        stack.extend(node.args)
    return seen
