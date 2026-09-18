"""Rocq (Coq) statements of arithmetic goals, read into SymPy formulas.

:func:`statement` reads the text of one ``Lemma``/``Theorem``/``Example``/
``Goal`` — its ``forall`` binders, its premises and its conclusion — into a
:class:`CoqGoal`, over the arithmetic grammar of
:mod:`~sympy_extras_benchmarks.parsers.prover`; :func:`scope_of` finds the
scope (``Z``, ``Q`` or ``R``) a file opens. Every identifier must be a
variable the binders declared, so a statement using a function, a coercion
or a section variable is refused (``None``) rather than guessed at. ``nat``
and ``N`` are read only as long as the goal does not subtract, since their
subtraction is truncated.

Nothing here reads a file, knows which collection a text comes from, or
decides whether a test suite proves the goal.

Examples
========

>>> from sympy_extras_benchmarks.parsers.rocq import statement
>>> goal = statement('mul_pos : forall (x y : Z), x > 0 -> y > 0 -> x * y > 0', 'Z', 'demo', 1)
>>> goal
CoqGoal(demo:mul_pos, Z, valid)
>>> goal.statement
ForAll((x, y), Implies((x > 0) & (y > 0), x*y > 0))
"""
from __future__ import annotations

import re
from typing import Optional

from sympy import And, Implies, Symbol
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.parsers.prover import (
    IDENTIFIER, SyntaxRefused, balanced, proposition, split_top)

__all__ = ['CoqGoal', 'SCOPES', 'NONNEGATIVE_TYPES', 'statement', 'scope_of']


#: the scopes a goal may be stated in, and the domain each means
SCOPES: dict[str, str] = {'Z': 'integers', 'Q': 'rationals', 'R': 'reals'}


#: the types whose values are the nonnegative part of a domain sympy-extras
#: has; subtraction on them is truncated, so a goal using it is refused
NONNEGATIVE_TYPES: dict[str, str] = {'nat': 'integers', 'N': 'integers'}


_SCOPE = re.compile(r'Open Scope (\w+)_scope')


_NAMED = re.compile(r"^\s*([A-Za-z_][A-Za-z_0-9']*)\s*:(?!=)(.*)$", re.S)


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


def statement(body: str, scope: str, name: str, position: int) -> Optional[CoqGoal]:
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
