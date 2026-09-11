"""The test inputs of Tarski.

Tarski (C. W. Brown, https://github.com/chriswestbrown/tarski, ISC-style
licence in ``interpreter/LICENSE``) ships

* ``regression/geogebra``: the quantifier elimination problems GeoGebra
  Discovery sends to Tarski (``compare``: 132, ``proverrg``: 49), each an
  ``(epc [ ex ... [ ... ]])`` command in a ``.in`` file with the answer of
  Tarski in the ``.out`` file (empty when it gave none);
* ``tests/ISSAC2015DataSet`` and ``tests/ISSAC2017/suite1``: the 225
  random conjunctions of strict polynomial inequalities of the ISSAC 2015
  paper on open NuCADs (nine files of 25, the 2017 files repeating them),
  with no recorded answers;
* ``interpreter/examples``: the formulas of the examples, and the unit
  tests whose target is a statement about the formula (``normalize`` and
  ``qfr`` return an equivalent formula);
* ``tests/dataset-Brown-V-E-2019``: the conjunctions of C. W. Brown and F.
  Vale-Enriquez, *From simplification to a partial theory solver for
  non-linear real polynomial constraints* (2019): 19555 disjuncts of the
  DNF of Meti-Tarski problems of SMT-LIB (``smtlib-r1``) and 119395 cases
  of the simplified ones (``smtlib-r2``), as SMT-LIB files without a
  status. A disjunct of an unsatisfiable problem is unsatisfiable; its
  source is the Meti-Tarski file its name starts with.

The repository is cloned sparsely on first use (or read from
``$SYMPY_EXTRAS_BENCHMARKS_TARSKI``). Only the formulas and Tarski's
recorded answers are read; no code of Tarski is used.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.qepcad_syntax import Example

__all__ = ['REPOSITORY', 'ENVIRONMENT_VARIABLE', 'fetch', 'examples', 'brown_files', 'brown_source']

REPOSITORY = 'https://github.com/chriswestbrown/tarski'
_SPARSE = ['/tests/', '/regression/', '/interpreter/examples/', '/interpreter/LICENSE']
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_TARSKI'

#: the unit tests of the interpreter whose target is equivalent to the input
_EQUIVALENT_TARGETS = ('normalize', 'qfr')


def fetch() -> Optional[pathlib.Path]:
    """The root of the sparse clone, made on first use."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    clone = cache_directory() / 'tarski'
    if (clone / 'regression').is_dir():
        return clone
    try:
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse', REPOSITORY, str(clone)],
                       check=True, capture_output=True, timeout=1800)
        subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', '--no-cone', *_SPARSE],
                       check=True, capture_output=True, timeout=1800)
    except (OSError, subprocess.SubprocessError):
        return None
    return clone if (clone / 'regression').is_dir() else None


def _bracket(text: str, start: int) -> Optional[str]:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == '[':
            depth += 1
        elif text[index] == ']':
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    return None


def examples() -> list[Example]:
    """The GeoGebra, ISSAC and interpreter problems, in the order of the files."""
    root = fetch()
    if root is None:
        return []
    found: list[Example] = []
    for group in ('compare', 'proverrg'):
        for path in sorted((root / 'regression' / 'geogebra' / group).glob('*.in')):
            command = path.read_text().strip()
            match = re.fullmatch(r'\(\s*epc\s*(.*)\)', command, re.S)
            answer_path = path.with_suffix('.out')
            answer = answer_path.read_text().strip() if answer_path.exists() else ''
            found.append(Example('geogebra-' + group, path.stem, 'tarski',
                                 match.group(1) if match else command, expected=answer or None))
    first: dict[str, str] = {}
    for directory in (root / 'tests' / 'ISSAC2015DataSet', root / 'tests' / 'ISSAC2017' / 'suite1'):
        for path in sorted(directory.glob('in.*')):
            for name, formula in re.findall(r'\(def\s+(\w+)\s+(\[.*?\])\s*\)', path.read_text(), re.S):
                body = ' '.join(formula.split())
                example = Example('issac-' + directory.name, '%s:%s' % (path.name, name), 'tarski', formula,
                                  question='satisfiable', duplicate_of=first.get(body))
                first.setdefault(body, example.key)
                found.append(example)
    interpreter = root / 'interpreter' / 'examples'
    for path in sorted((interpreter / 'formulas').glob('*')):
        if path.suffix == '.smt2' or not path.is_file():
            continue
        text = path.read_text(errors='replace')
        for match in re.finditer(r'\(def\s+(\w+)\s*\[', text):
            formula = _bracket(text, match.end() - 1)
            if formula is not None:
                found.append(Example('tarski-formulas', '%s:%s' % (path.name, match.group(1)), 'tarski', formula))
    for path in sorted((interpreter / 'utests').glob('*')):
        text = path.read_text(errors='replace') if path.is_file() else ''
        match = re.search(r'\(def\s+expr\s+\((%s)\s*\[' % '|'.join(_EQUIVALENT_TARGETS), text)
        target = re.search(r'\(def\s+targ\s*\[', text)
        if match is None or target is None:
            continue
        formula = _bracket(text, match.end() - 1)
        claim = _bracket(text, target.end() - 1)
        if formula is not None and claim is not None:
            found.append(Example('tarski-utests', path.name, 'tarski', formula, expected=claim))
    return found


def brown_files(round_: int) -> list[pathlib.Path]:
    """The SMT-LIB files of round 1 or 2 of the Brown--Vale-Enriquez data."""
    root = fetch()
    if root is None:
        return []
    return sorted((root / 'tests' / 'dataset-Brown-V-E-2019' / ('smtlib-r%d' % round_)).glob('*.smt2'))


def brown_source(path: pathlib.Path) -> str:
    """The name of the Meti-Tarski file a problem of the data comes from.

    >>> import pathlib
    >>> from sympy_extras_benchmarks.datasets.tarski_tests import brown_source
    >>> brown_source(pathlib.Path('sqrt-1mcosq-7-chunk-0231.smt2-1-201.smt2'))
    sqrt-1mcosq-7-chunk-0231.smt2
    """
    return path.name.split('.smt2')[0] + '.smt2'
