"""Lean 4 statements of arithmetic goals, read into SymPy formulas.

:func:`example` reads the text of one ``example`` — its binders and its
conclusion — into a :class:`LeanGoal`: the variables with the domain their
type means, the hypotheses and the goal, over the arithmetic grammar of
:mod:`~sympy_extras_benchmarks.parsers.prover`. Every identifier must be a
variable the binders declared, so a goal using anything else is refused
rather than guessed at; a refusal is returned as a string saying why.

Only concrete types are read (:data:`TYPES`): ``ℚ``, ``ℤ`` and ``ℝ``, and
the nonnegative ``ℕ`` and ``ℝ≥0`` (:data:`NONNEGATIVE_TYPES`) as long as the
goal neither subtracts nor divides, since their truncated arithmetic would
mean something else. A goal stated for an arbitrary structure is read at
``ℝ`` when every class it carries is one ``ℝ`` is a model of
(:data:`REAL_CLASSES`).

Nothing here reads a file, knows which collection a text comes from, or
decides whether a test suite proves the goal.

Examples
========

>>> from sympy_extras_benchmarks.parsers.lean import example
>>> goal = example('(x y : ℚ) (h1 : x < y) (h2 : 0 < x) : 0 < y', 'demo:1')
>>> goal
LeanGoal(demo:1, rationals, valid)
>>> goal.statement
ForAll((x, y), Implies((0 < x) & (x < y), 0 < y))
>>> example('(n : ℕ) : n - 1 < n', 'demo:2')
truncated subtraction on a nonnegative type
"""
from __future__ import annotations

import re
from typing import Optional, Union

from sympy import And, Implies, Symbol
from sympy.core.singleton import S
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.parsers.prover import (
    IDENTIFIER, SyntaxRefused, bars_to_abs, proposition, split_top)

__all__ = ['LeanGoal', 'TYPES', 'NONNEGATIVE_TYPES', 'REAL_CLASSES', 'example']


#: the concrete types a goal may be stated at, and the domain each means
TYPES: dict[str, str] = {
    'Rat': 'rationals', 'ℚ': 'rationals',
    'Int': 'integers', 'ℤ': 'integers',
    'Real': 'reals', 'ℝ': 'reals',
}


#: the types whose values are the nonnegative part of a domain sympy-extras
#: has: every variable gets ``0 <= v`` and the goal must not subtract, since
#: subtraction there is truncated (``1 - 2 = 0``) and would mean something else
NONNEGATIVE_TYPES: dict[str, str] = {
    'Nat': 'integers', 'ℕ': 'integers',
    'NNReal': 'reals', 'ℝ≥0': 'reals', 'NNRat': 'reals', 'ℚ≥0': 'reals',
}


#: the type classes ℝ is a model of, so that a goal stated for an arbitrary
#: structure carrying only these is true of ℝ in particular
REAL_CLASSES = frozenset({
    'CommRing', 'Ring', 'CommMonoid', 'Monoid', 'AddCommMonoid', 'AddMonoid',
    'AddCommGroup', 'AddGroup', 'CommGroup', 'Group', 'Field', 'DivisionRing',
    'LinearOrder', 'PartialOrder', 'Preorder', 'Lattice', 'LinearOrderedField',
    'LinearOrderedRing', 'LinearOrderedCommRing', 'LinearOrderedSemiring',
    'OrderedRing', 'OrderedField', 'OrderedSemiring', 'OrderedAddCommGroup',
    'StrictOrderedRing', 'StrictOrderedSemiring', 'IsStrictOrderedRing',
    'IsOrderedRing', 'IsOrderedField', 'IsOrderedMonoid', 'IsOrderedAddMonoid',
    'Semiring', 'CommSemiring', 'Nontrivial', 'DecidableEq', 'Inhabited',
})


#: types named often enough that a refusal should say which it was
_OTHER_TYPES = frozenset({'ℝ≥0∞', 'ENNReal', 'EReal', 'Prop', 'Complex', 'ℂ',
                          'Ordinal', 'Cardinal'})


_INSTANCE = re.compile(r'\[\s*([A-Za-z_][A-Za-z_0-9.]*)')


_UNIVERSE = re.compile(r'\{\s*([A-Za-z_α-ωΑ-Ω][A-Za-z_0-9α-ωΑ-Ω\']*)\s*(?::\s*Type\*?[0-9 ]*)?\}')


class LeanGoal:
    """One ``example`` of a tactic test.

    Attributes
    ==========

    name : str
        The file and the position of the example in it.
    domain : Set
        ``S.Reals`` for a goal over the rationals or the reals,
        ``S.Integers`` for one over the integers. The rationals are
        decided over the reals, which is sound for these goals: they are
        the ones ``linarith`` closes, and its reasoning holds in every
        ordered field.
    variables : list[Symbol]
        The variables the binders declared.
    hypotheses : list[Boolean]
        The propositions among the binders.
    goal : Boolean or None
        The conclusion, or ``None`` when it is ``False``.
    statement : Boolean
        What must hold: the universally quantified implication, or the
        existential closure of the hypotheses when the conclusion is
        ``False``.
    expected : bool
        What ``resolve`` must return for :attr:`statement`: ``True`` for
        an implication, ``False`` for contradictory hypotheses.
    """

    def __init__(self, name: str, domain: Set, variables: list[Symbol],
                 hypotheses: list[Boolean], goal: Optional[Boolean]) -> None:
        self.name = name
        self.domain = domain
        self.variables = variables
        self.hypotheses = hypotheses
        self.goal = goal

    @property
    def expected(self) -> bool:
        return self.goal is not None

    @property
    def statement(self) -> Boolean:
        premise = as_boolean(And(*self.hypotheses)) if self.hypotheses else as_boolean(S.true)
        if self.goal is None:
            body: Boolean = premise
            return as_boolean(Exists(self.variables, body)) if self.variables else body
        implication = as_boolean(Implies(premise, self.goal)) if self.hypotheses else self.goal
        return as_boolean(ForAll(self.variables, implication)) if self.variables else implication

    def __repr__(self) -> str:
        kind = 'valid' if self.expected else 'unsatisfiable'
        domain = 'integers' if self.domain is S.Integers else (
            'rationals' if self._rationals else 'reals')
        return "LeanGoal(%s, %s, %s)" % (self.name, domain, kind)

    #: set by the parser, only so that the printed form says which it was
    _rationals: bool = False


def _normalise(text: str) -> str:
    """Lean's notation rewritten in the ASCII the parser reads."""
    for lean, ascii_ in (('≤', '<='), ('≥', '>='), ('≠', '!='),
                         ('∧', ' and '), ('∨', ' or '), ('¬', ' not '),
                         ('→', ' -> '), ('↔', ' <-> ')):
        text = text.replace(lean, ascii_)
    return text


def _drop_ascriptions(text: str) -> str:
    """``(3 : ℤ)`` is ``3``: a type ascription inside a proposition
    carries no arithmetic content.

    It is stripped from the propositions only, never from the binder
    list, where ``(x y : ℚ)`` is a declaration and not an ascription.
    """
    return re.sub(r'\(\s*([^():]+?)\s*:\s*(?:Rat|Int|Real|Nat|ℚ|ℤ|ℝ|ℕ)\s*\)', r'(\1)', text)


def _binders(text: str) -> Optional[list[tuple[str, str]]]:
    """The binder list read as ``(names, type)`` pairs.

    Every character of ``text`` must belong to a group of the form
    ``(names : type)`` or ``{names : type}`` — Lean's explicit and
    implicit binders, which declare the same thing. Anything else — an
    instance argument, an unbalanced expression — makes the whole
    example unreadable and returns ``None``. Refusing is the point: a
    binder quietly skipped would drop a hypothesis and turn a valid goal
    into a false counterexample.
    """
    found: list[tuple[str, str]] = []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            i += 1
            continue
        if text[i] not in '({':
            return None
        close = ')' if text[i] == '(' else '}'
        depth, j = 0, i
        while j < n:
            if text[j] == text[i]:
                depth += 1
            elif text[j] == close:
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if depth != 0:
            return None
        inner = text[i + 1:j]
        cut = split_top(inner, ':')
        if cut is None:
            return None
        found.append((cut[0].strip(), cut[1].strip()))
        i = j + 1
    return found


def _last_colon(text: str) -> int:
    """The position of the colon separating the binders from the goal."""
    depth = 0
    last = -1
    for i, c in enumerate(text):
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == ':' and depth == 0:
            last = i
    return last


def _type_variable(block: str) -> Optional[str]:
    """The name of the structure a polymorphic goal is stated over, when
    every class it carries is one ℝ is a model of.

    A goal proved for an arbitrary linearly ordered field holds of ℝ in
    particular, so it can be read at ℝ; a goal carrying a class ℝ does not
    satisfy — or one this list has not vouched for — is refused instead.
    """
    classes = _INSTANCE.findall(block)
    if not classes or any(c.split('.')[0] not in REAL_CLASSES for c in classes):
        return None
    names = set(_UNIVERSE.findall(block))
    carriers = {m.split()[-1] for m in re.findall(r'\[\s*[A-Za-z_][A-Za-z_0-9.]*\s+([^\]]+)\]', block)}
    carriers = {c.strip() for c in carriers if IDENTIFIER.fullmatch(c.strip())}
    candidates = names & carriers if names & carriers else carriers
    if len(candidates) != 1:
        return None
    return candidates.pop()


def example(block: str, name: str) -> Union[LeanGoal, str]:
    """One ``example`` block, or the reason it is out of scope.

    Every refusal names itself, so that a caller can report what a
    file holds that the parser does not read yet.
    """
    #: a goal over an arbitrary structure is read at ℝ when ℝ is a model of it
    parameter = _type_variable(block)
    if '[' in block and parameter is None:
        return 'instance argument outside the classes ℝ is a model of'
    if parameter is not None:
        # the classes are discharged by reading the goal at ℝ, and the
        # carrier's own binder says nothing once its name is ℝ's
        block = re.sub(r'\[[^\[\]]*\]', ' ', block)
        block = re.sub(r'\{\s*%s\s*(?::\s*Type\*?[0-9 ]*)?\}' % re.escape(parameter), ' ', block)
    block = bars_to_abs(_normalise(block))
    cut = _last_colon(block)
    if cut < 0:
        return 'no conclusion'
    binders, conclusion = block[:cut], block[cut + 1:].strip()
    variables: dict[str, Symbol] = {}
    propositions: list[str] = []
    kinds: set[str] = set()
    nonnegative: list[Symbol] = []
    #: the goal is stated at ℕ or ℝ≥0, or (a ground goal) names no type at
    #: all, which in Lean means ℕ: its subtraction and division truncate
    truncated = False
    declarations = _binders(binders) if binders.strip() else []
    if declarations is None:
        return 'unreadable binder list'
    for names, sort in declarations:
        if parameter is not None and sort == parameter:
            sort = 'Real'
        target = TYPES.get(sort) or NONNEGATIVE_TYPES.get(sort)
        if target is not None:
            if not all(IDENTIFIER.fullmatch(n) for n in names.split()):
                return 'unreadable variable name'
            kinds.add(target)
            for n in names.split():
                symbol = Symbol(n, integer=True) if target == 'integers' else Symbol(n)
                variables[n] = symbol
                if sort in NONNEGATIVE_TYPES:
                    nonnegative.append(symbol)
        elif sort in _OTHER_TYPES:
            return 'type %s' % sort
        elif sort.split()[0] in _OTHER_TYPES if sort.split() else False:
            return 'type %s' % sort
        else:
            propositions.append(sort)
    if len(kinds) > 1:
        return 'more than one domain: %s' % ', '.join(sorted(kinds))
    ground = not variables
    if not kinds and not ground:
        return 'no concretely typed variable'
    if kinds:
        kind: Optional[str] = kinds.pop()
    else:
        kind = _ground_kind(conclusion)
        truncated = kind is None or _ground_nonnegative(conclusion)
        if kind is None:
            # a numeral with no ascription is ℕ in Lean, and ℕ agrees with ℤ
            # on every formula that neither subtracts nor divides; the guard
            # below refuses the ones that do
            kind, truncated = 'integers', True
    if kind is None:
        return 'a ground goal naming no domain'
    domain: Set = S.Integers if kind == 'integers' else S.Reals
    # the truncation guards read the source, not the parsed formula: SymPy
    # evaluates ``5 - 20 = 0`` to False before anything can look at it, and
    # on ℕ that statement is true, so the evidence has to be caught earlier
    if nonnegative or truncated:
        reason = _truncated(propositions + [conclusion], kind == 'integers')
        if reason is not None:
            return reason + (', and the goal names no domain' if truncated else '')
    try:
        integers = kind == 'integers'
        hypotheses = [proposition(_drop_ascriptions(p), variables, integers)
                      for p in propositions]
        goal = (None if conclusion in ('False', 'false')
                else proposition(_drop_ascriptions(conclusion), variables, integers))
    except SyntaxRefused as refused:
        return str(refused)
    for symbol in nonnegative:
        hypotheses.insert(0, as_boolean(S.Zero <= symbol))
    result = LeanGoal(name, domain, sorted(variables.values(), key=lambda s: s.name),
                      hypotheses, goal)
    result._rationals = kind == 'rationals'
    return result


def _ground_nonnegative(conclusion: str) -> bool:
    """Whether a goal with no variables is stated at ℕ or ℝ≥0, whose
    subtraction is truncated."""
    return any(re.search(r':\s*%s\s*\)' % re.escape(sort), conclusion)
               for sort in NONNEGATIVE_TYPES)


def _ground_kind(conclusion: str) -> Optional[str]:
    """The domain a goal with no variables is stated over, when a type
    ascription says so; ``None`` when nothing does."""
    for sort, kind in list(TYPES.items()) + list(NONNEGATIVE_TYPES.items()):
        if re.search(r':\s*%s\s*\)' % re.escape(sort), conclusion):
            return kind
    return None


def _truncated(sources: list[str], integers: bool) -> Optional[str]:
    """Why a goal on a nonnegative type does not mean over ℝ or ℤ what it
    means in Lean, or ``None`` when it does.

    On ℕ and ℝ≥0 subtraction is truncated — ``5 - 20 = 0`` is a theorem —
    and on ℕ division is integer division, so ``5 / 2 = 2`` is one too.
    Both are read from the source text: by the time the formula is parsed
    SymPy has evaluated the arithmetic and the difference is invisible.
    """
    for source in sources:
        body = _drop_ascriptions(source)
        if '-' in body:
            return 'truncated subtraction on a nonnegative type'
        if integers and '/' in body:
            return 'integer division on a nonnegative type'
    return None
