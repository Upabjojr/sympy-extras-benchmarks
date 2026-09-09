"""Arithmetic problems from the regression suites of the SMT solvers
cvc5 and Z3, as SymPy formulas.

The dataset
===========

Solvers keep the problems which once broke them, and those are exactly
the awkward cases: degenerate coefficients, empty and full solution
sets, deep quantifier alternations, divisibility constraints. The two
suites read here are

* the ``test/regress`` tree of `cvc5 <https://github.com/cvc5/cvc5>`_,
  whose files record the expected answer in a ``; EXPECT: sat`` header
  and often in ``(set-info :status ...)`` as well;
* the ``regressions`` tree of `z3test <https://github.com/Z3Prover/z3test>`_,
  which records it in ``(set-info :status ...)``.

Both are cloned sparsely on first use into the cache directory; a local
copy can be named by ``$SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS``.
Nothing of the files is stored in this repository, and only the
mathematical content is read: the formula, the sorts of the variables
and the recorded status.

The logics kept are the arithmetic ones, over the reals *and over the
integers*, quantified or not: ``QF_LIA``, ``QF_NIA``, ``LIA``, ``NIA``,
``QF_LRA``, ``QF_NRA``, ``LRA``, ``NRA`` and ``ALL`` when the file turns
out to use nothing else. The integer and quantified problems are what
this dataset adds to
:mod:`~sympy_extras_benchmarks.datasets.smtlib`, which reads the
quantifier-free real Meti-Tarski family.

The parser
==========

The s-expression reader of :mod:`~sympy_extras_benchmarks.datasets.smtlib`
is reused; this module adds the integer sorts and operations (``div``,
``mod``, ``abs``, ``divisible``, ``to_real``, ``to_int``) and the
quantifiers, which become
:class:`~sympy_extras.assumptions.ForAll` and
:class:`~sympy_extras.assumptions.Exists`.

Integer division and remainder follow the SMT-LIB definition (Boute's
Euclidean division: the remainder is always non-negative), which is
*not* SymPy's ``Mod`` for a negative divisor, so ``div`` and ``mod`` are
translated only when the divisor is a positive numeral; anything else
makes the file unusable and :func:`translate` returns ``None``.

Examples
========

>>> from sympy_extras_benchmarks.datasets.solver_regressions import translate
>>> text = '''
... ; EXPECT: unsat
... (set-logic QF_LIA)
... (declare-fun n () Int)
... (assert (and (> n 0) (< n 1)))
... (check-sat)
... '''
>>> problem = translate(text, 'demo')
>>> problem
ArithProblem(demo, QF_LIA, unsat, 1 integer, 0 real)
>>> problem.formula
(n > 0) & (n < 1)
>>> problem.domain
Integers

A quantified problem keeps the prefix:

>>> text = '''
... (set-info :status sat)
... (set-logic NRA)
... (declare-fun a () Real)
... (assert (exists ((x Real)) (= (* x x) a)))
... (check-sat)
... '''
>>> problem = translate(text, 'quantified')
>>> problem.formula
Exists(x, Eq(x**2, a))
>>> problem.quantified
True


Source and licence
==================

cvc5 is distributed under a **modified BSD** licence, ``z3test`` under the
**MIT** licence. Neither is redistributed here: the suites are cloned
sparsely on first use into the cache directory, and only the formulas and
the recorded ``sat``/``unsat`` answers are read.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional, Sequence

from sympy import Abs, And, Eq, Implies, Mod, Ne, Not, Or, Piecewise, Rational, Symbol, Xor, false, true
from sympy.core.basic import Basic
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean, ITE
from sympy.sets.sets import Set
from sympy.core.singleton import S

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.smtlib import SExpr, SMTLibError, parse, tokenize

__all__ = ['ArithProblem', 'SOURCES', 'ARITHMETIC_LOGICS', 'fetch', 'load', 'translate']

#: the repositories and the subtrees taken from them
SOURCES: dict[str, tuple[str, tuple[str, ...]]] = {
    'cvc5': ("https://github.com/cvc5/cvc5",
             ('test/regress/cli/regress0/nl', 'test/regress/cli/regress1/nl',
              'test/regress/cli/regress0/arith', 'test/regress/cli/regress1/arith',
              'test/regress/cli/regress0/quantifiers')),
    'z3': ("https://github.com/Z3Prover/z3test",
           ('regressions/smt2', 'regressions/qsat', 'regressions/nl', 'regressions/mcsat_smt2')),
}

#: the arithmetic logics whose files are read (``ALL`` is kept when the
#: file turns out to use nothing but arithmetic)
ARITHMETIC_LOGICS: frozenset[str] = frozenset({
    'QF_LIA', 'QF_NIA', 'LIA', 'NIA', 'QF_LRA', 'QF_NRA', 'LRA', 'NRA',
    'QF_LIRA', 'QF_NIRA', 'LIRA', 'NIRA', 'ALL', 'AUFLIA', 'AUFNIRA'})

#: a local directory holding the ``.smt2`` files
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS'

_EXPECT = re.compile(r'^\s*;\s*EXPECT:\s*(sat|unsat)\s*$', re.MULTILINE)


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


def _number(token: str) -> Optional[Rational]:
    """A numeral or decimal literal, ``None`` for anything else."""
    if not token or not (token[0].isdigit() or token[0] == '.'):
        return None
    try:
        return Rational(token)
    except (ValueError, TypeError):
        return None


def _positive_numeral(e: SExpr) -> Optional[int]:
    """``e`` as a positive integer literal, ``None`` otherwise."""
    if not isinstance(e, str):
        return None
    value = _number(e)
    if value is None or not value.is_Integer or value <= 0:
        return None
    return int(value)


class _Translator:
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


def _application(translator: _Translator, e: SExpr) -> Boolean:
    """A formula whose head is an indexed operator, e.g. ``divisible``."""
    if not isinstance(e, list) or not e:
        raise SMTLibError("bad application")
    return translator.indexed(e[0], e[1:])


def _recorded_status(text: str, commands: Sequence[SExpr]) -> str:
    """The expected answer: the ``:status`` of the file, or the cvc5
    ``; EXPECT:`` header."""
    for command in commands:
        if (isinstance(command, list) and len(command) >= 3 and command[0] == 'set-info'
                and command[1] == ':status' and isinstance(command[2], str)):
            if command[2] in ('sat', 'unsat'):
                return command[2]
    found = _EXPECT.findall(text)
    if len(set(found)) == 1:
        return found[0]
    return 'unknown'


def translate(text: str, name: str = '') -> Optional[ArithProblem]:
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
    translator = _Translator()
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
            except (SMTLibError, ZeroDivisionError, TypeError):
                return None
        elif head == 'assert' and len(command) == 2:
            try:
                assertions.append(_assertion(translator, command[1]))
            except (SMTLibError, ZeroDivisionError, TypeError, ValueError):
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
                        _recorded_status(text, commands), logic, quantified,
                        translator.bound_integers, translator.bound_reals)


def _assertion(translator: _Translator, e: SExpr) -> Boolean:
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


def fetch() -> list[pathlib.Path]:
    """The directories holding the ``.smt2`` files: the one named by
    ``$SYMPY_EXTRAS_BENCHMARKS_SOLVER_REGRESSIONS``, or the sparse clones
    in the cache (made on first use). Sources which cannot be obtained
    are skipped."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return [pathlib.Path(override)]
    directories: list[pathlib.Path] = []
    for key, (repository, subtrees) in SOURCES.items():
        clone = cache_directory() / ('solver-regressions-' + key)
        present = [clone / s for s in subtrees if (clone / s).is_dir()]
        if present:
            directories.extend(present)
            continue
        try:
            subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                            repository, str(clone)], check=True, capture_output=True, timeout=1800)
            subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', *subtrees],
                           check=True, capture_output=True, timeout=1800)
        except (subprocess.SubprocessError, OSError):
            continue
        directories.extend(clone / s for s in subtrees if (clone / s).is_dir())
    return directories


def load() -> list[pathlib.Path]:
    """Every ``.smt2`` file of the fetched directories, sorted."""
    paths: list[pathlib.Path] = []
    for directory in fetch():
        paths.extend(sorted(directory.rglob('*.smt2')))
    return sorted(set(paths))
