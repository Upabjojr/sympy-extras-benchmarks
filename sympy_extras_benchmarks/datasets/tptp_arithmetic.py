"""The arithmetic (``ARI``) domain of the TPTP problem library, as SymPy
formulas.

The dataset
===========

`TPTP <https://tptp.org>`_ is the standard problem library for automated
theorem provers. Its ``ARI`` domain is arithmetic: several hundred
problems in TFF (typed first-order form) over ``$int``, ``$rat`` and
``$real``, each with a recorded ``Status`` — ``Theorem`` when the
conjecture follows from the axioms, ``CounterSatisfiable`` when it does
not. They range from ``$less(2,3)`` to quantified nonlinear statements,
and unlike the proof-assistant suites they were written to be hard for
provers rather than to exercise one tactic.

A problem is read as one closed formula: the axioms imply the conjecture,
with every free variable universally quantified. ``resolve`` must return
the truth value the ``Status`` records.

What is refused
===============

* problems declaring an **uninterpreted function or predicate**
  (``tff(f_type, type, f: $int > $int)``), which sympy-extras has no way
  to express;
* the ``cnf`` problems, whose clauses carry implicit variables;
* ``$quotient``, ``$floor``, ``$ceiling``, ``$to_int``, ``$is_int`` and
  the other conversions, whose TPTP semantics over ``$int`` are not the
  ones the same expression has over ℤ;
* problems mixing two arithmetic types, since the domain would be
  ambiguous;
* the ``$rat`` problems. sympy-extras has no rational domain, and
  deciding them over ℝ changes the question -- ``ARI536_4`` asks whether
  ``? [X: $rat] : $product(X,X) = 2``, which is false over ℚ and true
  over ℝ, and is recorded ``CounterSatisfiable`` for exactly that
  reason.

Source and licence
==================

The TPTP library is distributed by Geoff Sutcliffe under its own terms
(see ``https://tptp.org``); the problems are the work of their individual
authors, recorded in each file's header. Nothing is stored in this
repository: the ``ARI`` domain is extracted on first use from the official
distribution into the cache directory, or read from a local copy named by
``$SYMPY_EXTRAS_BENCHMARKS_TPTP``. Only the formulas and the recorded
``Status`` are read.

Examples
========

>>> from sympy_extras_benchmarks.datasets.tptp_arithmetic import problem
>>> text = '''
... % Status   : Theorem
... tff(easy,conjecture,
...     ! [X: $int,Y: $int] :
...       ( $less(0,Y) => $less(X,$sum(X,Y)) ) ).
... '''
>>> p = problem(text, 'demo')
>>> p
TPTPProblem(demo, integers, Theorem, expected True)
>>> p.formula
ForAll((X, Y), Implies(0 < Y, X < X + Y))
"""
from __future__ import annotations

import os
import pathlib
import re
import tarfile
import urllib.request
from typing import Optional

from sympy import Abs, And, Eq, Equivalent, Implies, Ne, Not, Or, Symbol, Xor
from sympy.core.expr import Expr
from sympy.core.numbers import Integer, Rational
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean, as_expr

from sympy_extras_benchmarks.cache import cache_directory

__all__ = ['TPTPProblem', 'TPTPError', 'DISTRIBUTION', 'TYPES', 'fetch', 'load', 'problem']

#: the official distribution; only ``Problems/ARI`` is extracted from it
DISTRIBUTION = "https://tptp.org/TPTP/Distribution/TPTP-v9.3.1.tgz"
#: a local copy of the library, or of its ``ARI`` directory
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_TPTP'

#: the arithmetic types, and the domain each means. ``$rat`` is **not**
#: here: sympy-extras has no rational domain, and deciding a ``$rat``
#: problem over ℝ changes the question. ARI536_4 is the standing example
#: -- "Rational: Square root of two does not exist", ``? [X: $rat] :
#: $product(X,X) = 2`` -- which is false over ℚ and true over ℝ.
TYPES: dict[str, str] = {'$int': 'integers', '$real': 'reals'}
#: named so that a ``$rat`` problem is recognised and refused rather than
#: silently read as though it were about the reals
REFUSED_TYPES = frozenset({'$rat'})
#: what the recorded status says ``resolve`` must return
STATUS: dict[str, bool] = {'Theorem': True, 'Unsatisfiable': True,
                           'CounterSatisfiable': False, 'Satisfiable': False}
#: arity-2 arithmetic functions
_BINARY = {'$sum': 'add', '$difference': 'sub', '$product': 'mul'}
#: the relations, as TPTP writes them
_RELATIONS = {'$less': 'lt', '$lesseq': 'le', '$greater': 'gt', '$greatereq': 'ge'}
#: anything here means the problem is outside the fragment
_REFUSED = frozenset({'$quotient', '$quotient_e', '$quotient_t', '$quotient_f',
                      '$remainder_e', '$remainder_t', '$remainder_f',
                      '$floor', '$ceiling', '$truncate', '$round',
                      '$is_int', '$is_rat', '$to_int', '$to_real', '$to_rat'})

_STATUS_LINE = re.compile(r'^%\s*Status\s*:\s*(\w+)', re.M)
_TOKEN = re.compile(r"""
      \s+ | %[^\n]* |                       # space and comments
      (?P<num>-?\d+/\d+|-?\d+\.\d+|-?\d+) |  # rationals, decimals, integers
      (?P<word>\$?[A-Za-z_][A-Za-z_0-9]*) |
      (?P<op><=>|<~>|~\||~&|=>|!=|[()\[\],:.!?&|~=])
    """, re.X)


class TPTPError(ValueError):
    """The problem is outside the fragment this module reads."""


class TPTPProblem:
    """One TPTP ``ARI`` problem.

    Attributes
    ==========

    name : str
        The problem's file name.
    status : str
        The ``Status`` recorded in the header.
    domain : Set
        ``S.Integers`` for ``$int``, ``S.Reals`` for ``$rat`` and
        ``$real``.
    formula : Boolean
        One closed formula: the axioms imply the conjecture.
    expected : bool
        What ``resolve`` must return for :attr:`formula`.
    """

    def __init__(self, name: str, status: str, domain: Set, formula: Boolean) -> None:
        self.name = name
        self.status = status
        self.domain = domain
        self.formula = formula

    @property
    def expected(self) -> bool:
        return STATUS[self.status]

    @property
    def statement(self) -> Boolean:
        """The closed formula, under the name the drivers expect."""
        return self.formula

    @property
    def variables(self) -> list[Symbol]:
        """Every variable of the problem, bound ones included: the formula
        is closed, so the free ones would always be none."""
        return sorted(self.formula.atoms(Symbol), key=lambda s: str(s))

    def __repr__(self) -> str:
        return "TPTPProblem(%s, %s, %s, expected %s)" % (
            self.name, 'integers' if self.domain is S.Integers else 'reals',
            self.status, self.expected)


def _tokens(text: str) -> list[str]:
    out: list[str] = []
    position = 0
    while position < len(text):
        match = _TOKEN.match(text, position)
        if match is None:
            raise TPTPError("cannot tokenise at %r" % text[position:position + 20])
        position = match.end()
        for group in ('num', 'word', 'op'):
            if match.group(group) is not None:
                out.append(match.group(group))
                break
    return out


class _Parser:
    """A recursive descent parser for the TFF arithmetic fragment."""

    def __init__(self, tokens: list[str], integers: bool) -> None:
        self.tokens = tokens
        self.position = 0
        self.integers = integers
        self.bound: dict[str, Symbol] = {}

    def peek(self) -> Optional[str]:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, expected: Optional[str] = None) -> str:
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise TPTPError("expected %r, found %r" % (expected, token))
        self.position += 1
        return token

    def formula(self) -> Boolean:
        left = self.unary()
        token = self.peek()
        if token in ('&', '|', '=>', '<=>', '<~>'):
            self.take()
            right = self.formula()
            if token == '&':
                return as_boolean(And(left, right))
            if token == '|':
                return as_boolean(Or(left, right))
            if token == '=>':
                return as_boolean(Implies(left, right))
            if token == '<=>':
                return as_boolean(Equivalent(left, right))
            return as_boolean(Xor(left, right))
        return left

    def unary(self) -> Boolean:
        token = self.peek()
        if token == '~':
            self.take()
            return as_boolean(Not(self.unary()))
        if token in ('!', '?'):
            self.take()
            self.take('[')
            names: list[str] = []
            while True:
                name = self.take()
                self.take(':')
                kind = self.take()
                if kind not in TYPES:
                    raise TPTPError("binder type %s" % kind)
                if (TYPES[kind] == 'integers') != self.integers:
                    raise TPTPError("a second domain: %s" % kind)
                names.append(name)
                if self.peek() == ',':
                    self.take()
                    continue
                break
            self.take(']')
            self.take(':')
            shadowed = {n: self.bound[n] for n in names if n in self.bound}
            variables = []
            for name in names:
                symbol = Symbol(name, integer=True) if self.integers else Symbol(name)
                self.bound[name] = symbol
                variables.append(symbol)
            body = self.unary()
            for name in names:
                del self.bound[name]
            self.bound.update(shadowed)
            head = ForAll if token == '!' else Exists
            return as_boolean(head(variables, body))
        if token == '(':
            self.take('(')
            inner = self.formula()
            self.take(')')
            return inner
        return self.atom()

    def atom(self) -> Boolean:
        token = self.peek()
        if token in _RELATIONS:
            kind = _RELATIONS[self.take()]
            self.take('(')
            left = self.term()
            self.take(',')
            right = self.term()
            self.take(')')
            if kind == 'lt':
                return as_boolean(left < right)
            if kind == 'le':
                return as_boolean(left <= right)
            if kind == 'gt':
                return as_boolean(left > right)
            return as_boolean(left >= right)
        if token in ('$true', '$false'):
            return as_boolean(S.true if self.take() == '$true' else S.false)
        left = self.term()
        relation = self.peek()
        if relation in ('=', '!='):
            self.take()
            right = self.term()
            return as_boolean(Eq(left, right) if relation == '=' else Ne(left, right))
        raise TPTPError("not a proposition at %r" % token)

    def term(self) -> Expr:
        token = self.peek()
        if token is None:
            raise TPTPError("unexpected end of formula")
        if token in _REFUSED:
            raise TPTPError("uses %s" % token)
        if token in _BINARY:
            kind = _BINARY[self.take()]
            self.take('(')
            left = self.term()
            self.take(',')
            right = self.term()
            self.take(')')
            return as_expr(left + right if kind == 'add'
                           else left - right if kind == 'sub' else left*right)
        if token in ('$uminus', '$abs'):
            head = self.take()
            self.take('(')
            inner = self.term()
            self.take(')')
            return as_expr(-inner if head == '$uminus' else Abs(inner))
        if re.fullmatch(r'-?\d+', token):
            return as_expr(Integer(int(self.take())))
        if re.fullmatch(r'-?\d+/\d+', token):
            a, b = self.take().split('/')
            return as_expr(Rational(int(a), int(b)))
        if re.fullmatch(r'-?\d+\.\d+', token):
            return as_expr(Rational(self.take()))
        if token.startswith('$'):
            raise TPTPError("unsupported function %s" % token)
        name = self.take()
        if self.peek() == '(':
            raise TPTPError("uninterpreted function %s" % name)
        if name in self.bound:
            return as_expr(self.bound[name])
        raise TPTPError("free name %s" % name)


def _annotations(text: str) -> list[tuple[str, str, str]]:
    """``(name, role, body)`` for every ``tff(...)`` of the file."""
    found: list[tuple[str, str, str]] = []
    for match in re.finditer(r'\b(tff|thf|cnf|fof)\s*\(', text):
        if match.group(1) != 'tff':
            raise TPTPError("the %s language" % match.group(1))
        depth, index = 0, match.end() - 1
        while index < len(text):
            if text[index] == '(':
                depth += 1
            elif text[index] == ')':
                depth -= 1
                if depth == 0:
                    break
            index += 1
        else:
            raise TPTPError("unterminated annotation")
        inner = text[match.end():index]
        parts = inner.split(',', 2)
        if len(parts) != 3:
            raise TPTPError("malformed annotation")
        found.append((parts[0].strip(), parts[1].strip(), parts[2]))
    return found


def problem(text: str, name: str = '') -> Optional[TPTPProblem]:
    """One TPTP problem, or ``None`` when it is outside the fragment."""
    status = _STATUS_LINE.search(text)
    if status is None or status.group(1) not in STATUS:
        return None
    body = re.sub(r'^%[^\n]*', '', text, flags=re.M)
    try:
        annotations = _annotations(body)
    except TPTPError:
        return None
    if not annotations:
        return None
    if any(re.search(r'\%s\b' % t, body) for t in REFUSED_TYPES):
        return None                         # see REFUSED_TYPES
    kinds = {t for t in TYPES if re.search(r'\%s\b' % t, body)}
    domains = {TYPES[k] for k in kinds}
    if len(domains) != 1:
        return None
    integers = domains.pop() == 'integers'
    axioms: list[Boolean] = []
    conjecture: Optional[Boolean] = None
    for _, role, source in annotations:
        if role == 'type':
            return None                     # an uninterpreted symbol
        try:
            parser = _Parser(_tokens(source), integers)
            parsed = parser.formula()
            if parser.peek() is not None:
                return None
        except (TPTPError, TypeError, ValueError):
            return None
        if role == 'conjecture':
            if conjecture is not None:
                return None
            conjecture = parsed
        elif role in ('axiom', 'hypothesis', 'definition', 'lemma'):
            axioms.append(parsed)
        else:
            return None
    if conjecture is None:
        return None
    formula = as_boolean(Implies(And(*axioms), conjecture)) if axioms else conjecture
    # the parser refuses unbound names, so this is a safety net rather
    # than the usual path: a TFF formula is closed already
    free = sorted((s for s in formula.free_symbols if isinstance(s, Symbol)),
                  key=lambda s: s.name)
    if free:
        formula = as_boolean(ForAll(free, formula))
    return TPTPProblem(name, status.group(1),
                       S.Integers if integers else S.Reals, formula)


def fetch() -> list[pathlib.Path]:
    """The ``ARI`` problem files: from ``$SYMPY_EXTRAS_BENCHMARKS_TPTP``,
    or extracted from the distribution into the cache on first use."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    roots = [pathlib.Path(override)] if override else []
    roots.append(cache_directory() / 'tptp')
    for root in roots:
        if root.is_dir():
            found = sorted(p for p in root.rglob('ARI*.p'))
            if found:
                return found
    target = cache_directory() / 'tptp'
    target.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(DISTRIBUTION, timeout=3600) as response:
            with tarfile.open(fileobj=response, mode='r|gz') as archive:
                for member in archive:
                    if '/Problems/ARI/' in member.name and member.name.endswith('.p'):
                        archive.extract(member, target, filter='data')
    except (OSError, tarfile.TarError, ValueError):
        return []
    return sorted(target.rglob('ARI*.p'))


def load() -> list[TPTPProblem]:
    """Every readable problem of the ``ARI`` domain."""
    found: list[TPTPProblem] = []
    for path in fetch():
        try:
            text = path.read_text(errors='replace')
        except OSError:
            continue
        parsed = problem(text, path.stem)
        if parsed is not None:
            found.append(parsed)
    return found
