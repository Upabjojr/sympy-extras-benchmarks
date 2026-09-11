"""The test inputs of QEPCAD B.

QEPCAD B (H. Hong, C. W. Brown, https://github.com/chriswestbrown/qepcad,
ISC-style licence in ``qesource/LICENSE``) ships regression tests and the
worked examples of its web pages:

* ``regressiontests/applicationTestSet``: seven problems from applications,
  with the answers of QEPCAD in ``applicationTestSet.out`` (one line for
  each ``sol E`` and ``sol T`` command; the ``sol T`` one, a Tarski
  formula, is the answer read here);
* ``regressiontests/largeSetTestSet``: 1000 problems ``(E y)[p(x, y) = 0]``
  with a random dense ``p`` of total degree 6, and no answers;
  ``CAD2DlargeSetTestSet`` holds the same 1000 formulas for the 2D-CAD
  command, and is read as a duplicate;
* ``public_html/B/examples``: the inputs of the worked examples, two of them
  session transcripts with QEPCAD's answer.

The repository is cloned sparsely on first use (or read from
``$SYMPY_EXTRAS_BENCHMARKS_QEPCAD``). Only the inputs and QEPCAD's recorded
answers are read; no code of QEPCAD is used.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.qepcad_syntax import Example, blocks

__all__ = ['REPOSITORY', 'ENVIRONMENT_VARIABLE', 'fetch', 'examples']

REPOSITORY = 'https://github.com/chriswestbrown/qepcad'
_SPARSE = ['/regressiontests/', '/public_html/B/examples/', '/qesource/LICENSE']
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_QEPCAD'


def fetch() -> Optional[pathlib.Path]:
    """The root of the sparse clone, made on first use."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    clone = cache_directory() / 'qepcad'
    if (clone / 'regressiontests').is_dir():
        return clone
    try:
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse', REPOSITORY, str(clone)],
                       check=True, capture_output=True, timeout=900)
        subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', '--no-cone', *_SPARSE],
                       check=True, capture_output=True, timeout=900)
    except (OSError, subprocess.SubprocessError):
        return None
    return clone if (clone / 'regressiontests').is_dir() else None


def _answers_after(commands: str, lines: list[str]) -> Optional[str]:
    """Consume the answer lines of the ``sol`` commands of one problem and
    return the one of ``sol T``."""
    answer: Optional[str] = None
    for kind in re.findall(r'^\s*sol\s+([A-Za-z])', commands, re.M):
        line = lines.pop(0) if lines else None
        if kind == 'T' and line is not None:
            answer = line.strip()
    return answer


def _transcript_answer(text: str) -> Optional[str]:
    """The formula QEPCAD printed after the ``sol T`` command of a session."""
    place = text.rfind('\nsol T')
    if place < 0:
        return None
    match = re.search(r'An equivalent quantifier-free formula:\s*\n\s*\n(.*?)\n\s*\n', text[place:], re.S)
    return ' '.join(match.group(1).split()) if match else None


def examples() -> list[Example]:
    """The problems, in the order of the files."""
    root = fetch()
    if root is None:
        return []
    found: list[Example] = []
    tests = root / 'regressiontests'
    lines = [l for l in (tests / 'applicationTestSet.out').read_text().splitlines() if l.strip()]
    for index, (match, commands) in enumerate(blocks((tests / 'applicationTestSet').read_text()), 1):
        found.append(Example('qepcad-application', '%d' % index, 'qepcad', match.group(0),
                             expected=_answers_after(commands, lines)))
    first: dict[str, str] = {}
    for name in ('largeSetTestSet', 'CAD2DlargeSetTestSet'):
        collection = 'qepcad-' + name.replace('TestSet', '')
        for index, (match, _) in enumerate(blocks((tests / name).read_text()), 1):
            example = Example(collection, '%04d' % index, 'qepcad', match.group(0))
            example.duplicate_of = first.get(match.group(0))
            first.setdefault(match.group(0), example.key)
            found.append(example)
    examples_directory = root / 'public_html' / 'B' / 'examples'
    for path in sorted(examples_directory.rglob('*')):
        if not path.is_file() or not (path.suffix == '.qe' or path.name.startswith('In.')):
            continue
        text = path.read_text(errors='replace')
        for index, (match, _) in enumerate(blocks(text), 1):
            name = '%s/%s' % (path.parent.name, path.name) + ('' if index == 1 else '#%d' % index)
            found.append(Example('qepcad-examples', name, 'qepcad', match.group(0),
                                 expected=_transcript_answer(text)))
    return found
