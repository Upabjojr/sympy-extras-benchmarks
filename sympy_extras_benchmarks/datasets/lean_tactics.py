"""Arithmetic goals from the tactic tests of Lean's mathlib4, as SymPy
formulas.

The dataset
===========

`mathlib4 <https://github.com/leanprover-community/mathlib4>`_ keeps a
test file for each of its tactics. The ones for the arithmetic tactics —
``linarith``, ``nlinarith`` and ``positivity`` — are collections of
hand-written goals over the rationals, the integers and the reals which
those tactics are expected to close: awkward-on-purpose implications
between linear and polynomial inequalities, the cases that once needed a
fix.

They are read here as an oracle in both directions:

* a goal ``example (x : ℚ) (h : P) : G := by linarith`` says that
  ``P → G`` holds for every ``x``, so
  ``resolve(ForAll(x, Implies(P, G)))`` must be ``True``;
* a goal whose conclusion is ``False`` says that the hypotheses are
  contradictory, so ``resolve(Exists(x, P))`` must be ``False``.

Only the tests which are stated at a concrete type are usable: mathlib
proves most of its lemmas for an arbitrary ordered ring, and a goal about
``{α} [CommRing α] [LinearOrder α]`` names no domain sympy-extras could
decide over. ``ℕ`` is refused as well, because subtraction on it is
truncated and ``a - b`` would not mean what it says.

Source and licence
==================

mathlib4 is distributed under the **Apache License 2.0**. The test files
are kept under it in ``data/mathlib4/`` with mathlib's ``LICENSE`` beside
them (see ``data/README.md``) and read from there, or from a local copy
named by ``$SYMPY_EXTRAS_BENCHMARKS_MATHLIB``; if neither is there the
repository is cloned sparsely into the cache. Only the mathematical
content is read: the binders, the hypotheses and the goal. **Mathlib's
proofs are not used.**

The parser
==========

:func:`goals` finds the ``example`` blocks of a file whose goal the suite
proves — not the negative tests, nor the ones leaning on ``sorry`` or on a
local axiom — and reads each with
:func:`~sympy_extras_benchmarks.parsers.lean.example`
(:mod:`~sympy_extras_benchmarks.parsers.lean`), whose accepted syntax is
deliberately small and whose refusals :func:`refusals` lists.

Examples
========

>>> from sympy_extras_benchmarks.datasets.lean_tactics import goals
>>> text = '''
... example (x y : ℚ) (h1 : x < y) (h2 : 0 < x) : 0 < y := by linarith
... example (a : ℚ) (h : a < 0) (h2 : 0 < a) : False := by linarith
... '''
>>> first, second = goals(text, 'demo')
>>> first
LeanGoal(demo:1, rationals, valid)
>>> first.statement
ForAll((x, y), Implies((0 < x) & (x < y), 0 < y))
>>> second
LeanGoal(demo:2, rationals, unsatisfiable)
>>> second.statement
Exists(a, (0 < a) & (a < 0))
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.lean import LeanGoal, example
from sympy_extras_benchmarks.parsers.prover import IDENTIFIER

__all__ = ['REPOSITORY', 'SUBTREES', 'fetch', 'load', 'goals', 'refusals']

REPOSITORY = "https://github.com/leanprover-community/mathlib4"
#: the test files read (the arithmetic tactics)
SUBTREES: tuple[str, ...] = (
    # decision procedures for arithmetic
    'MathlibTest/Tactic/Linarith',
    'MathlibTest/Tactic/Positivity.lean',
    'MathlibTest/Tactic/Polyrith.lean',
    # equalities: polynomial identities, and identities under equational
    # hypotheses, which is the same question put to ``resolve``
    'MathlibTest/Tactic/LinearCombination.lean',
    'MathlibTest/Tactic/LinearCombinationPrime.lean',
    'MathlibTest/Tactic/Ring',
    # ground arithmetic: numerals, no variables
    'MathlibTest/Tactic/NormNum',
)
#: a local mathlib4 checkout
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_MATHLIB'


_EXAMPLE = re.compile(r'^example\b(.*?):=\s*by\b', re.S | re.M)
#: what marks an example as a negative test — one whose tactic is expected
#: to fail, so that the goal itself need not be true
_NEGATIVE = re.compile(r'#guard_msgs|/--\s*error|fail_if_success|sorry|admit\b')
#: a local axiom: an example whose proof leans on one proves nothing, and
#: these files declare false ones on purpose (``axiom bad (q : ℚ) : q = 0``)
_AXIOM = re.compile(r'^axiom\s+([A-Za-z_][A-Za-z_0-9\']*)', re.M)
#: where the proof of one example stops and the next declaration begins
_DECLARATION = re.compile(r'^(?:example|theorem|lemma|axiom|def|abbrev|instance|section|end|'
                          r'variable|open|namespace|/--|#guard|@\[)', re.M)


def _proved(text: str, match: 're.Match[str]', axioms: frozenset[str]) -> bool:
    """Whether an example's goal is actually a theorem.

    A mathlib test file also holds examples that are expected to *fail* —
    marked with ``#guard_msgs``, an ``/-- error: -/`` docstring or
    ``fail_if_success`` — examples whose proof assumes what it needs
    (``sorry``, and mathlib's own ``test_sorry``), and examples leaning on
    a false ``axiom`` the file declares to exercise a tactic. None of them
    says its goal is true, so none may be read as an oracle.
    """
    preamble = text[max(0, match.start() - 400):match.start()]
    if _NEGATIVE.search(preamble.rsplit('\n\n', 1)[-1]):
        return False
    following = _DECLARATION.search(text, match.end())
    proof = text[match.end():following.start() if following else len(text)]
    if _NEGATIVE.search(proof):
        return False
    return not any(IDENTIFIER.fullmatch(word) and word in axioms
                   for word in re.findall(r"[A-Za-z_][A-Za-z_0-9']*", proof))


def goals(text: str, name: str = '') -> list[LeanGoal]:
    """Every usable ``example`` of a Lean test file, in order."""
    axioms = frozenset(_AXIOM.findall(text))
    found: list[LeanGoal] = []
    for index, match in enumerate(_EXAMPLE.finditer(text), start=1):
        if not _proved(text, match, axioms):
            continue
        goal = example(match.group(1).strip(), '%s:%d' % (name, index))
        if isinstance(goal, LeanGoal):
            found.append(goal)
    return found


def refusals(text: str, name: str = '') -> list[tuple[str, str]]:
    """``(example, reason)`` for every block :func:`goals` does not read.

    A maintenance view of the dataset: it says what a test file holds that
    the parser has no translation for, which is how the accepted subset is
    grown without guessing.
    """
    axioms = frozenset(_AXIOM.findall(text))
    found: list[tuple[str, str]] = []
    for index, match in enumerate(_EXAMPLE.finditer(text), start=1):
        label = '%s:%d' % (name, index)
        if not _proved(text, match, axioms):
            found.append((label, 'a negative test: the goal need not be true'))
            continue
        goal = example(match.group(1).strip(), label)
        if isinstance(goal, str):
            found.append((label, goal))
    return found


def fetch() -> list[pathlib.Path]:
    """The mathlib4 test files: the ones under
    ``$SYMPY_EXTRAS_BENCHMARKS_MATHLIB``, or a sparse clone in the cache
    (made on first use). An empty list when it cannot be obtained."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    root = pathlib.Path(override) if override and pathlib.Path(override).is_dir() else None
    if root is None:
        root = bundled('mathlib4')
    if root is None:
        clone = cache_directory() / 'mathlib4'
        if not any((clone / s).exists() for s in SUBTREES):
            try:
                subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                                REPOSITORY, str(clone)], check=True, capture_output=True, timeout=1800)
                # sparse-checkout's cone mode takes directories only, so a
                # subtree naming a single file is asked for by its directory
                cones = sorted({s if s.endswith('/') or '.' not in s.rsplit('/', 1)[-1]
                                else s.rsplit('/', 1)[0] for s in SUBTREES})
                subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', *cones],
                               check=True, capture_output=True, timeout=1800)
            except (subprocess.SubprocessError, OSError):
                return []
        root = clone
    paths: list[pathlib.Path] = []
    for subtree in SUBTREES:
        target = root / subtree
        if target.is_dir():
            paths.extend(sorted(target.rglob('*.lean')))
        elif target.is_file():
            paths.append(target)
    return paths


def _label(path: pathlib.Path) -> str:
    """The name a file is known by: its directory and stem, because the
    suite has more than one ``Basic.lean``."""
    return '%s/%s' % (path.parent.name, path.stem)


def load() -> list[LeanGoal]:
    """Every usable goal of the fetched files."""
    found: list[LeanGoal] = []
    for path in fetch():
        try:
            text = path.read_text(errors='replace')
        except OSError:
            continue
        found.extend(goals(text, _label(path)))
    return found
