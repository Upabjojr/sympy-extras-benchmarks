"""Arithmetic goals from the ``micromega`` test suite of the Rocq (Coq)
standard library, as SymPy formulas.

The dataset
===========

Rocq's ``micromega`` plugin provides ``lia``, ``nia``, ``lra``, ``nra``
and ``psatz`` — decision and Positivstellensatz procedures over ``Z``,
``Q`` and ``R``. Its test suite is a file per historical bug plus a few
collections of examples, each a ``Lemma`` or ``Goal`` the plugin is
expected to close.

It complements the mathlib4 tactic tests read by
:mod:`~sympy_extras_benchmarks.datasets.lean_tactics`: those are mostly
linear, while ``example.v``, ``example_nia.v`` and ``bound.v`` are
deliberately nonlinear — degree-37 powers, products of hypotheses,
Positivstellensatz certificates — which is the part of the input space
where a quantifier-elimination procedure is most likely to give up or to
answer wrongly.

Every statement carries a machine-checked proof, so its truth value is
known:

* ``Lemma l : forall x, P -> G.`` says ``resolve(ForAll(x, P -> G))`` is
  ``True``;
* a statement whose conclusion is ``False`` says the hypotheses are
  contradictory, so ``resolve(Exists(x, P))`` is ``False``.

Only the goals stated over ``Z``, ``Q`` or ``R`` are read. ``nat`` and
``N`` are refused because their subtraction is truncated, and the
machine-integer scopes (``sint63``, ``uint63``) because they wrap.

Source and licence
==================

The Rocq standard library is distributed under the **GNU Lesser General
Public License, version 2.1**. The repository is cloned sparsely on first
use into the cache directory; a local copy can be named by
``$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB``. Nothing of the files is stored
in this repository, and only the mathematical content is read: the
binders, the hypotheses and the conclusion. **The proofs are not used.**

The parser
==========

:func:`goals` reads the ``Lemma``/``Theorem``/``Example``/``Goal``
statements of a file, up to the ``.`` that ends each. The accepted
syntax is the one of
:mod:`~sympy_extras_benchmarks.datasets.prover_syntax`, and every
identifier must be a variable the binders declared, so a statement using
a function, a coercion or a section variable is refused rather than
guessed at.

Examples
========

>>> from sympy_extras_benchmarks.datasets.coq_micromega import goals
>>> text = '''
... Open Scope Z_scope.
... Lemma mul_pos : forall (x y : Z), x > 0 -> y > 0 -> x * y > 0.
... Proof. nia. Qed.
... Goal forall x : Z, x > 1 -> x < 0 -> False.
... Proof. lia. Qed.
... '''
>>> first, second = goals(text, 'demo')
>>> first
CoqGoal(demo:mul_pos, Z, valid)
>>> first.statement
ForAll((x, y), Implies((x > 0) & (y > 0), x*y > 0))
>>> second
CoqGoal(demo:2, Z, unsatisfiable)
>>> second.statement
Exists(x, (x > 1) & (x < 0))
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy import And, Implies, Symbol
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.prover_syntax import (
    IDENTIFIER, SyntaxRefused, balanced, proposition, split_top)

__all__ = ['CoqGoal', 'REPOSITORY', 'SUBTREES', 'fetch', 'load', 'goals']

REPOSITORY = "https://github.com/rocq-prover/stdlib"
#: the test files read
SUBTREES: tuple[str, ...] = ('test-suite/micromega',)
#: a local checkout of the standard library
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB'

#: the scopes a goal may be stated in, and the domain each means
SCOPES: dict[str, str] = {'Z': 'integers', 'Q': 'rationals', 'R': 'reals'}
#: the types whose values are the nonnegative part of a domain sympy-extras
#: has; subtraction on them is truncated, so a goal using it is refused
NONNEGATIVE_TYPES: dict[str, str] = {'nat': 'integers', 'N': 'integers'}

_STATEMENT = re.compile(r'^(?:Lemma|Theorem|Example|Goal)\b(.*?)\.\s*$', re.M | re.S)
_SCOPE = re.compile(r'Open Scope (\w+)_scope')
_NAMED = re.compile(r"^\s*([A-Za-z_][A-Za-z_0-9']*)\s*:(?!=)(.*)$", re.S)
#: how a proof ends; only the first two mean the statement was proved
_ENDS = re.compile(r'\b(Qed|Defined|Abort|Admitted)\s*\.')


class CoqGoal:
    """One statement of the micromega test suite.

    Attributes
    ==========

    name : str
        The file and the name (or the position) of the statement in it.
    scope : str
        ``'Z'``, ``'Q'`` or ``'R'``, the scope the file opened.
    domain : Set
        ``S.Integers`` for ``Z``, ``S.Reals`` for ``Q`` and ``R``. The
        rationals are decided over the reals, which is sound in the
        direction these goals are used: they hold in every ordered
        field.
    variables : list[Symbol]
        The variables the binders declared.
    hypotheses : list[Boolean]
        The premises, both the ones written as named binders and the ones
        written to the left of an arrow.
    goal : Boolean or None
        The conclusion, or ``None`` when it is ``False``.
    statement : Boolean
        What must hold: the universally quantified implication, or the
        existential closure of the hypotheses when the conclusion is
        ``False``.
    expected : bool
        What ``resolve`` must return for :attr:`statement`.
    """

    def __init__(self, name: str, scope: str, variables: list[Symbol],
                 hypotheses: list[Boolean], goal: Optional[Boolean]) -> None:
        self.name = name
        self.scope = scope
        self.variables = variables
        self.hypotheses = hypotheses
        self.goal = goal

    @property
    def domain(self) -> Set:
        return S.Integers if self.scope == 'Z' else S.Reals

    @property
    def expected(self) -> bool:
        return self.goal is not None

    @property
    def statement(self) -> Boolean:
        premise = as_boolean(And(*self.hypotheses)) if self.hypotheses else as_boolean(S.true)
        if self.goal is None:
            return as_boolean(Exists(self.variables, premise)) if self.variables else premise
        body = as_boolean(Implies(premise, self.goal)) if self.hypotheses else self.goal
        return as_boolean(ForAll(self.variables, body)) if self.variables else body

    def __repr__(self) -> str:
        return "CoqGoal(%s, %s, %s)" % (self.name, self.scope,
                                        'valid' if self.expected else 'unsatisfiable')


def _normalise(text: str) -> str:
    """Rocq's notation rewritten in the ASCII the shared grammar reads."""
    text = text.replace('/\\', ' and ').replace('\\/', ' or ')
    text = text.replace('<>', '!=').replace('~', ' not ')
    # ``(0 <= z)%Z`` says which scope to read the parenthesised term in;
    # the scope is already known from the file, so the marker is dropped
    text = re.sub(r'\)\s*%[A-Za-z_][A-Za-z_0-9]*', ')', text)
    return " ".join(text.split())


def _binders(text: str) -> Optional[list[tuple[str, str]]]:
    """The binders of a ``forall`` head, as ``(names, type)`` pairs.

    Rocq writes them parenthesised and typed, ``(x y : Z)``, unbracketed
    and typed, ``forall x y : Z,``, or bare, ``forall x y,``, where the
    type comes from the scope; a named hypothesis, ``(H : 0 <= x)``, is a
    binder too. Every character must
    belong to one of those forms, so that nothing is silently skipped:
    dropping a hypothesis would turn a valid goal into a false
    counterexample.
    """
    bare = split_top(text, ':')
    if bare is not None:
        # ``forall x y : Z,``: one declaration, written without brackets
        return [(bare[0].strip(), bare[1].strip())]
    found: list[tuple[str, str]] = []
    index, size = 0, len(text)
    while index < size:
        if text[index].isspace():
            index += 1
            continue
        if text[index] == '(':
            depth, end = 0, index
            while end < size:
                if text[end] == '(':
                    depth += 1
                elif text[end] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                end += 1
            if depth != 0:
                return None
            split = split_top(text[index + 1:end], ':')
            if split is None:
                return None
            found.append((split[0].strip(), split[1].strip()))
            index = end + 1
            continue
        match = IDENTIFIER.match(text, index)
        if match is None:
            return None
        found.append((match.group(0), ''))       # bare: the type is the scope
        index = match.end()
    return found


def _one(body: str, scope: str, name: str, position: int) -> Optional[CoqGoal]:
    """One statement, or ``None`` when it is out of scope."""
    body = _normalise(body)
    if '{' in body or '[' in body or '%' in body:
        return None                              # an implicit argument or a scope change
    match = _NAMED.match(body)
    if match is not None and not match.group(2).lstrip().startswith('='):
        name, body = '%s:%s' % (name, match.group(1)), match.group(2).strip()
    else:
        name = '%s:%d' % (name, position)
    variables: dict[str, Symbol] = {}
    premises: list[str] = []
    nonnegative: list[Symbol] = []
    while body.startswith('forall'):
        rest = body[len('forall'):]
        split = split_top(rest, ',')
        if split is None:
            return None
        head, body = split[0], split[1].strip()
        declarations = _binders(head)
        if declarations is None:
            return None
        for names, kind in declarations:
            kind = kind or scope
            if kind == scope or kind in NONNEGATIVE_TYPES:
                if kind in NONNEGATIVE_TYPES and NONNEGATIVE_TYPES[kind] != SCOPES[scope]:
                    return None                  # ℕ inside an R or Q statement
                for identifier in names.split():
                    if IDENTIFIER.fullmatch(identifier) is None:
                        return None
                    variables[identifier] = (Symbol(identifier, integer=True) if scope == 'Z'
                                             else Symbol(identifier))
                    if kind in NONNEGATIVE_TYPES:
                        nonnegative.append(variables[identifier])
            elif kind in SCOPES:
                return None                      # a second domain in the same statement
            else:
                premises.append(kind)            # a named hypothesis
    if not variables or not balanced(body):
        return None
    # the premises written with arrows, which bind looser than everything
    conclusion = body
    while True:
        split = split_top(conclusion, '->')
        if split is None:
            break
        premises.append(split[0])
        conclusion = split[1].strip()
    integers = scope == 'Z'
    # the truncation guard reads the source: SymPy evaluates ``5 - 20 = 0``
    # to False before anything can see that ℕ makes it a theorem
    if nonnegative and any('-' in p for p in premises + [conclusion]):
        return None
    try:
        hypotheses = [proposition(p, variables, integers) for p in premises]
        goal = (None if conclusion.strip() == 'False'
                else proposition(conclusion, variables, integers))
    except SyntaxRefused:
        return None
    for symbol in nonnegative:
        hypotheses.insert(0, as_boolean(S.Zero <= symbol))
    return CoqGoal(name, scope, sorted(variables.values(), key=lambda s: s.name),
                   hypotheses, goal)


def scope_of(text: str) -> Optional[str]:
    """The scope the file last opened, or ``None`` when it opens none of
    the three arithmetic ones."""
    scopes = [s for s in _SCOPE.findall(text) if s in SCOPES]
    if scopes:
        return scopes[-1]
    return 'Z' if 'ZArith' in text and 'Open Scope' not in text else None


def goals(text: str, name: str = '') -> list[CoqGoal]:
    """Every usable statement of a Rocq test file, in order."""
    scope = scope_of(text)
    if scope is None:
        return []
    found: list[CoqGoal] = []
    for position, match in enumerate(_STATEMENT.finditer(text), start=1):
        # a statement is an oracle only if its proof was accepted: these
        # files also hold goals left ``Abort``ed, to record that the
        # tactic gives up on them, and those say nothing about the truth
        end = _ENDS.search(text, match.end())
        if end is None or end.group(1) not in ('Qed', 'Defined'):
            continue
        goal = _one(match.group(1), scope, name, position)
        if goal is not None:
            found.append(goal)
    return found


def fetch() -> list[pathlib.Path]:
    """The micromega test files: the ones under
    ``$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB``, or a sparse clone in the
    cache (made on first use). An empty list when it cannot be
    obtained."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    root = pathlib.Path(override) if override and pathlib.Path(override).is_dir() else None
    if root is None:
        clone = cache_directory() / 'rocq-stdlib'
        if not any((clone / subtree).exists() for subtree in SUBTREES):
            try:
                subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                                REPOSITORY, str(clone)],
                               check=True, capture_output=True, timeout=1800)
                subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', *SUBTREES],
                               check=True, capture_output=True, timeout=1800)
            except (subprocess.SubprocessError, OSError):
                return []
        root = clone
    paths: list[pathlib.Path] = []
    for subtree in SUBTREES:
        target = root / subtree
        if target.is_dir():
            paths.extend(sorted(target.rglob('*.v')))
        elif target.is_file():
            paths.append(target)
    return paths


def load() -> list[CoqGoal]:
    """Every usable goal of the fetched files."""
    found: list[CoqGoal] = []
    for path in fetch():
        try:
            text = path.read_text(errors='replace')
        except OSError:
            continue
        found.extend(goals(text, path.stem))
    return found
