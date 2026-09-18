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
Public License, version 2.1**. The ``micromega`` test suite is kept under
it in ``data/rocq-stdlib/`` with the library's ``LICENSE`` beside it (see
``data/README.md``) and read from there, or from a local copy named by
``$SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB``; if neither is there the
repository is cloned sparsely into the cache. Only the mathematical
content is read: the binders, the hypotheses and the conclusion. **The
proofs are not used.**

The parser
==========

:func:`goals` finds the ``Lemma``/``Theorem``/``Example``/``Goal``
statements of a file whose proof was accepted (``Qed`` or ``Defined``, not
``Abort``) and reads each with
:func:`~sympy_extras_benchmarks.parsers.rocq.statement`
(:mod:`~sympy_extras_benchmarks.parsers.rocq`), in the scope the file opens.

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
from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.rocq import CoqGoal, scope_of, statement

__all__ = ['REPOSITORY', 'SUBTREES', 'fetch', 'load', 'goals']

REPOSITORY = "https://github.com/rocq-prover/stdlib"
#: the test files read
SUBTREES: tuple[str, ...] = ('test-suite/micromega',)
#: a local checkout of the standard library
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_ROCQ_STDLIB'


_STATEMENT = re.compile(r'^(?:Lemma|Theorem|Example|Goal)\b(.*?)\.\s*$', re.M | re.S)
#: how a proof ends; only the first two mean the statement was proved
_ENDS = re.compile(r'\b(Qed|Defined|Abort|Admitted)\s*\.')


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
        goal = statement(match.group(1), scope, name, position)
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
        root = bundled('rocq-stdlib')
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
