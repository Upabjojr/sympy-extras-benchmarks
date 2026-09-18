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
the truth value the ``Status`` records. The files are read by
:func:`~sympy_extras_benchmarks.parsers.tptp.problem`, which also says what
is refused (:mod:`~sympy_extras_benchmarks.parsers.tptp`); this module finds
them.

Source and licence
==================

The TPTP is copyrighted by Geoff Sutcliffe and Christian Suttner, and is
not under an open licence; the problems are the work of their individual
authors, recorded in each file's header. Its terms (``Documents/ReadMe`` of
the distribution) permit verbatim redistribution of the TPTP and of parts of
it, clearly attributed to the TPTP, and require permission for a modified
version. Under that permission the ``ARI`` domain is kept verbatim in
``data/tptp/``, with the ReadMe and the attribution in ``data/tptp/NOTICE``
(see ``data/README.md``), and read from there, or from a local copy named by
``$SYMPY_EXTRAS_BENCHMARKS_TPTP``. Without either it is extracted from the
official distribution into the cache; the whole distribution is also
preserved verbatim on the Hugging Face Hub as `Upabjojr/tptp-v9.3.1
<https://huggingface.co/datasets/Upabjojr/tptp-v9.3.1>`_. Only the formulas
and the recorded ``Status`` are read.

"""
from __future__ import annotations

import os
import pathlib
import tarfile
import urllib.request
from typing import BinaryIO, Callable

from sympy_extras_benchmarks import huggingface
from sympy_extras_benchmarks.cache import bundled, cache_directory
from sympy_extras_benchmarks.parsers.tptp import TPTPProblem, problem

__all__ = ['DISTRIBUTION', 'fetch', 'load']

#: the official distribution; only ``Problems/ARI`` is extracted from it
DISTRIBUTION = "https://tptp.org/TPTP/Distribution/TPTP-v9.3.1.tgz"
#: a local copy of the library, or of its ``ARI`` directory
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_TPTP'


def fetch() -> list[pathlib.Path]:
    """The ``ARI`` problem files: from ``$SYMPY_EXTRAS_BENCHMARKS_TPTP``,
    from ``data/tptp/``, or extracted from the distribution into the cache
    on first use. The
    distribution is read from a copy of it in the cache, from tptp.org, or
    from its Hugging Face mirror when tptp.org cannot be reached or under
    the global option of :mod:`~sympy_extras_benchmarks.huggingface`."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    roots = [pathlib.Path(override)] if override else []
    kept = bundled('tptp')
    if kept is not None:
        roots.append(kept)
    roots.append(cache_directory() / 'tptp')
    for root in roots:
        if root.is_dir():
            found = sorted(p for p in root.rglob('ARI*.p'))
            if found:
                return found
    target = cache_directory() / 'tptp'
    target.mkdir(parents=True, exist_ok=True)
    local = target / DISTRIBUTION.rsplit('/', 1)[1]

    def extract(stream: Callable[[], BinaryIO]) -> list[pathlib.Path]:
        try:
            with stream() as source, tarfile.open(fileobj=source, mode='r|gz') as archive:
                for member in archive:
                    if '/Problems/ARI/' in member.name and member.name.endswith('.p'):
                        archive.extract(member, target, filter='data')
        except (OSError, tarfile.TarError, ValueError):
            return []
        return sorted(target.rglob('ARI*.p'))

    def tptp_org() -> list[pathlib.Path]:
        return extract(lambda: urllib.request.urlopen(DISTRIBUTION, timeout=3600))

    def hub() -> list[pathlib.Path]:
        if huggingface.download(huggingface.TPTP, local.name, local) is None:
            return []
        return extract(lambda: open(local, 'rb'))

    if local.is_file():
        found = extract(lambda: open(local, 'rb'))
        if found:
            return found
    return huggingface.first(tptp_org, hub) or []


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
