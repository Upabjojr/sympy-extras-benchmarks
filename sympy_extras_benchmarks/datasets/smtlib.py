"""SMT-LIB 2 problems of the ``QF_NRA`` logic (quantifier-free nonlinear
real arithmetic) as SymPy formulas.

The dataset
===========

The Meti-Tarski family of the SMT-LIB benchmark library holds 7713 proof
obligations extracted from the MetiTarski theorem prover (Akbarpour and
Paulson, *MetiTarski: An automatic theorem prover for real-valued special
functions*, JAR 44, 2010): polynomial bounds of ``exp``, ``log``, ``sin``,
``atan``, ... in a few real variables, each with its recorded
``:status sat|unsat`` (they were submitted by Jovanovic and de Moura for
*Solving Non-Linear Arithmetic*, IJCAR 2012). The family is mirrored in
the ``dreal/benchmarks`` repository on GitHub, which is cloned sparsely on
first use into the cache directory; a local copy can be named by
``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB``. Nothing of the files is stored in this
repository.

The parser
==========

``tokenize`` and ``parse`` read s-expressions; ``translate`` turns the
commands of a file into a :class:`Problem`: the ``declare-fun`` /
``declare-const`` of real variables, ``define-fun`` of constants, the
``assert`` commands (conjoined) and the ``:status``. Terms use ``+ - * /``
and numerals, formulas ``and or not => xor = distinct ite let`` and the
relations ``< <= > >= =``; a ``let`` binds terms or formulas. ``ite`` on
terms is translated with ``Piecewise``, which the formulas of the family
do not need.

Examples
========

>>> from sympy_extras_benchmarks.datasets.smtlib import translate
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
"""
from __future__ import annotations

import os
import pathlib
import subprocess
from typing import Optional, Sequence, Union

from sympy import Rational, Symbol, Eq, Ne, And, Or, Not, Implies, Xor, Piecewise, true, false
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean, ITE

from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.cache import cache_directory

__all__ = ['Problem', 'REPOSITORY', 'SUBDIRECTORY', 'fetch', 'load', 'tokenize', 'parse',
           'translate', 'SMTLibError']

REPOSITORY = "https://github.com/dreal/benchmarks"
SUBDIRECTORY = "smt2/smt-lib/meti-tarski"
#: a local directory with the ``.smt2`` files
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_SMTLIB'

#: an s-expression: an atom or a list of s-expressions
SExpr = Union[str, list['SExpr']]


class SMTLibError(ValueError):
    """The file uses something beyond the ``QF_NRA`` formulas translated."""


def tokenize(text: str) -> list[str]:
    """The tokens of an SMT-LIB file: parentheses, atoms, quoted symbols
    ``|...|`` and strings ``"..."``; comments (``;``) are dropped.

    Examples
    ========

    >>> from sympy_extras_benchmarks.datasets.smtlib import tokenize
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

    >>> from sympy_extras_benchmarks.datasets.smtlib import parse, tokenize
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
            except (SMTLibError, ZeroDivisionError, TypeError):
                return None
        elif head == 'assert' and len(command) == 2:
            try:
                assertions.append(translator.formula(command[1]))
            except (SMTLibError, ZeroDivisionError, TypeError):
                return None
        elif head in ('declare-sort', 'define-sort', 'push', 'pop'):
            return None
    if not assertions:
        return None
    variables = sorted(translator.symbols.values(), key=lambda s: s.name)
    return Problem(name, as_boolean(And(*assertions)), variables, status)


def fetch() -> Optional[pathlib.Path]:
    """The directory of the Meti-Tarski files: the one named by
    ``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB``, or the sparse clone in the cache
    (made on first use); ``None`` when it cannot be obtained."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    clone = cache_directory() / 'dreal-benchmarks'
    target = clone / SUBDIRECTORY
    if target.is_dir() and any(target.iterdir()):
        return target
    try:
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                        REPOSITORY, str(clone)], check=True, capture_output=True, timeout=900)
        subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', SUBDIRECTORY],
                       check=True, capture_output=True, timeout=900)
    except (subprocess.SubprocessError, OSError):
        return None
    return target if target.is_dir() else None


def load(limit: int = 0) -> list[pathlib.Path]:
    """The paths of the problem files, sorted by name (``limit`` of them
    when it is positive); empty when they cannot be fetched."""
    directory = fetch()
    if directory is None:
        return []
    paths = sorted(directory.glob('*.smt2'))
    return paths[:limit] if limit else paths


def load_problems(limit: int = 0) -> list[Problem]:
    """The translated problems (files which cannot be translated are
    left out)."""
    problems: list[Problem] = []
    for path in load(limit):
        problem = translate(path.read_text(errors='replace'), path.stem)
        if problem is not None:
            problems.append(problem)
    return problems


if __name__ == '__main__':
    files = load()
    counts: dict[str, int] = {}
    sizes: dict[int, int] = {}
    for path in files:
        problem = translate(path.read_text(errors='replace'), path.stem)
        key = 'untranslated' if problem is None else problem.status
        counts[key] = counts.get(key, 0) + 1
        if problem is not None:
            sizes[len(problem.variables)] = sizes.get(len(problem.variables), 0) + 1
    print("files:", len(files), counts, "variables:", dict(sorted(sizes.items())))
