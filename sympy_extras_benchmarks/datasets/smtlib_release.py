"""Every problem of the SMT-LIB logics ``QF_NRA`` and ``NRA``.

SMT-LIB publishes its benchmarks in yearly releases on Zenodo, one
compressed archive per logic. This module reads the 2025 release of the
non-incremental benchmarks (Zenodo record 16740866,
doi:10.5281/zenodo.16740866, licence CC BY 4.0):

* ``QF_NRA`` -- 12154 quantifier-free problems of nonlinear real
  arithmetic in 16 families (Meti-Tarski 7006, hycomp 2752,
  LassoRanker 821, Sturm-MBO 405, Pine 245, Uncu 225, zankl 166, ...),
  of which 5257 are recorded ``sat``, 5536 ``unsat`` and 1361 ``unknown``;
* ``NRA`` -- 3819 quantified problems (KeYmaera 3813, and six more),
  3806 recorded ``unsat``, 5 ``sat`` and 8 ``unknown``.

The archives are downloaded on first use into the cache, checked against
the MD5 sums Zenodo publishes and unpacked with ``tar --zstd`` (the
``zstd`` program must be installed). A directory holding an unpacked
release (the one containing ``non-incremental/``) can be named with
``$SYMPY_EXTRAS_BENCHMARKS_SMTLIB_RELEASE`` instead. The files are
parsed by :mod:`~sympy_extras_benchmarks.datasets.smtlib` (``QF_NRA``) and
:mod:`~sympy_extras_benchmarks.datasets.solver_regressions`
(``NRA``, which has quantifiers); only the formulas and the ``:status``
are read.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
import subprocess
import urllib.request
from typing import Optional

from sympy_extras_benchmarks.cache import cache_directory

__all__ = ['RECORD', 'ARCHIVES', 'ENVIRONMENT_VARIABLE', 'fetch', 'load', 'family']

#: the Zenodo record of the release
RECORD = '16740866'

#: the archive of each logic, with its MD5 sum as published by Zenodo
ARCHIVES: dict[str, tuple[str, str]] = {
    'QF_NRA': ('QF_NRA.tar.zst', '85a04fcea6dd10fb4c505703cac46e2c'),
    'NRA': ('NRA.tar.zst', '07011f51333098ab9f77e09bf537f9ea'),
}

#: the environment variable naming an unpacked copy of the release
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_SMTLIB_RELEASE'


def _root() -> pathlib.Path:
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override:
        return pathlib.Path(override)
    return cache_directory() / 'smtlib-2025'


def _md5(path: pathlib.Path) -> str:
    digest = hashlib.md5()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def fetch(logic: str) -> Optional[pathlib.Path]:
    """The directory of the problems of ``logic`` (``'QF_NRA'`` or
    ``'NRA'``), downloaded and unpacked on first use; ``None`` when it
    cannot be obtained."""
    if logic not in ARCHIVES:
        raise ValueError("unknown logic %s" % logic)
    root = _root()
    target = root / 'non-incremental' / logic
    if target.is_dir() and any(target.iterdir()):
        return target
    name, checksum = ARCHIVES[logic]
    archive = root / name
    try:
        root.mkdir(parents=True, exist_ok=True)
        if not archive.exists() or _md5(archive) != checksum:
            url = 'https://zenodo.org/records/%s/files/%s?download=1' % (RECORD, name)
            with urllib.request.urlopen(url, timeout=600) as response, open(archive, 'wb') as sink:
                shutil.copyfileobj(response, sink)
        if _md5(archive) != checksum:
            return None
        subprocess.run(['tar', '--zstd', '-xf', str(archive), '-C', str(root)],
                       check=True, capture_output=True, timeout=3600)
    except (OSError, subprocess.SubprocessError):
        return None
    return target if target.is_dir() else None


def load(logic: str) -> list[pathlib.Path]:
    """The problem files of ``logic``, sorted by path; empty when they
    cannot be fetched."""
    directory = fetch(logic)
    if directory is None:
        return []
    return sorted(directory.rglob('*.smt2'))


def family(path: pathlib.Path, logic: str) -> str:
    """The family of a problem: the directory under the logic.

    >>> import pathlib
    >>> from sympy_extras_benchmarks.datasets.smtlib_release import family
    >>> family(pathlib.Path('/data/non-incremental/QF_NRA/kissing/sub/p.smt2'), 'QF_NRA')
    kissing
    """
    parts = path.parts
    index = len(parts) - 1 - parts[::-1].index(logic)
    return parts[index + 1]
