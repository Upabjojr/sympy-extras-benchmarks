"""The Hugging Face Hub mirrors of the collections too large for ``data/``.

Four collections are not kept in the repository. Each is mirrored,
unchanged and in its source language, in a public dataset repository of
its own (built by ``scripts/huggingface_upload.py``):

========================  ================================================
:data:`SMTLIB_2025`       the ``QF_NRA`` and ``NRA`` archives of the SMT-LIB
                          2025 release
:data:`TARSKI_BROWN`      the Brown--Vale-Enriquez data of Tarski
:data:`Z3TEST_NL_LARGE`   the two large files of ``z3test``'s
                          ``regressions/nl``
:data:`TPTP`              the TPTP distribution, v9.3.1
========================  ================================================

Where the data comes from
=========================

A dataset reads ``data/``, a local copy or the cache before it touches the
network at all. When it must download, it has two places to download from,
and :func:`first` decides the order:

* by default, the **upstream server** first (Zenodo, GitHub, tptp.org),
  and the Hub mirror only when the upstream cannot be reached or gives
  something that fails its check;
* with the global option -- ``$SYMPY_EXTRAS_BENCHMARKS_HUGGINGFACE`` set to
  ``1``, or ``--huggingface`` on the command line of
  ``python -m sympy_extras_benchmarks`` -- the **Hub mirror** first, and the
  upstream as the fallback. The option is an environment variable so that
  the worker processes of a parallel run inherit it.

A file downloaded from the Hub is checked against the ``SHA256SUMS`` of
its repository before it is used. Only the public ``resolve`` URLs are
read: ``huggingface_hub`` is not needed.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
import urllib.request
from typing import Callable, Optional, TypeVar

__all__ = ['ENVIRONMENT_VARIABLE', 'NAMESPACE', 'SMTLIB_2025', 'TARSKI_BROWN', 'Z3TEST_NL_LARGE',
           'TPTP', 'REPOSITORIES', 'preferred', 'enable', 'url', 'download', 'first']

#: the environment variable of the global option
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_HUGGINGFACE'

#: the Hub user the mirrors are published under
NAMESPACE = 'Upabjojr'
#: the SMT-LIB 2025 ``QF_NRA.tar.zst`` and ``NRA.tar.zst``
SMTLIB_2025 = NAMESPACE + '/smtlib-2025-nra'
#: ``smtlib-r1.tar.zst``, ``smtlib-r2.tar.zst``, ``round1inputs``,
#: ``round2inputs`` and ``README`` of Tarski's ``tests/dataset-Brown-V-E-2019``
TARSKI_BROWN = NAMESPACE + '/tarski-brown-vale-enriquez-2019'
#: ``regressions/nl/fastmul-unfolded-l-native-nl-wrapped.smt2`` and
#: ``regressions/nl/helperlemma-l-native-nl-wrapped.smt2``
Z3TEST_NL_LARGE = NAMESPACE + '/z3test-nl-large'
#: ``TPTP-v9.3.1.tgz``, the distribution as tptp.org publishes it
TPTP = NAMESPACE + '/tptp-v9.3.1'
#: every mirror
REPOSITORIES: tuple[str, ...] = (SMTLIB_2025, TARSKI_BROWN, Z3TEST_NL_LARGE, TPTP)

_T = TypeVar('_T')


def preferred() -> bool:
    """Whether the global option asks for the Hub mirrors first.

    Examples
    ========

    >>> import os
    >>> from sympy_extras_benchmarks import huggingface
    >>> os.environ.pop(huggingface.ENVIRONMENT_VARIABLE, None) and None
    >>> huggingface.preferred()
    False
    >>> huggingface.enable()
    >>> huggingface.preferred()
    True
    >>> del os.environ[huggingface.ENVIRONMENT_VARIABLE]
    """
    return os.environ.get(ENVIRONMENT_VARIABLE, '').strip().lower() in ('1', 'true', 'yes', 'on')


def enable() -> None:
    """Turn the global option on, for this process and the ones it starts."""
    os.environ[ENVIRONMENT_VARIABLE] = '1'


def url(repository: str, filename: str) -> str:
    """The public download URL of ``filename`` in the dataset ``repository``.

    >>> from sympy_extras_benchmarks.huggingface import url, TPTP
    >>> url(TPTP, 'TPTP-v9.3.1.tgz')
    https://huggingface.co/datasets/Upabjojr/tptp-v9.3.1/resolve/main/TPTP-v9.3.1.tgz
    """
    return 'https://huggingface.co/datasets/%s/resolve/main/%s' % (repository, filename)


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def _checksums(repository: str) -> Optional[dict[str, str]]:
    try:
        with urllib.request.urlopen(url(repository, 'SHA256SUMS'), timeout=60) as response:
            text = response.read().decode('utf-8')
    except OSError:
        return None
    sums: dict[str, str] = {}
    for line in text.splitlines():
        digest, _, name = line.partition('  ')
        if name:
            sums[name] = digest
    return sums


def download(repository: str, filename: str, target: pathlib.Path) -> Optional[pathlib.Path]:
    """``filename`` of the Hub dataset ``repository``, saved as ``target``
    and checked against the repository's ``SHA256SUMS``; ``None`` when the
    Hub cannot be reached or the file does not match. A ``target`` already
    matching is not downloaded again."""
    sums = _checksums(repository)
    if sums is None or filename not in sums:
        return None
    expected = sums[filename]
    if target.is_file() and _sha256(target) == expected:
        return target
    partial = target.with_name(target.name + '.partial')
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url(repository, filename), timeout=3600) as response, \
                open(partial, 'wb') as sink:
            shutil.copyfileobj(response, sink, 1 << 20)
        if _sha256(partial) != expected:
            partial.unlink()
            return None
        partial.replace(target)
    except OSError:
        if partial.exists():
            partial.unlink()
        return None
    return target


def first(upstream: Callable[[], _T], hub: Callable[[], _T]) -> Optional[_T]:
    """The first of the two sources which gives something: the upstream
    and then the Hub, or the other way round under the global option.
    A source gives nothing when it returns ``None`` or an empty value.

    Examples
    ========

    >>> import os
    >>> from sympy_extras_benchmarks import huggingface
    >>> os.environ.pop(huggingface.ENVIRONMENT_VARIABLE, None) and None
    >>> huggingface.first(lambda: 'upstream', lambda: 'hub')
    upstream
    >>> huggingface.first(lambda: None, lambda: 'hub')
    hub
    >>> huggingface.enable()
    >>> huggingface.first(lambda: 'upstream', lambda: 'hub')
    hub
    >>> huggingface.first(lambda: [], lambda: [])
    >>> del os.environ[huggingface.ENVIRONMENT_VARIABLE]
    """
    for source in ((hub, upstream) if preferred() else (upstream, hub)):
        result = source()
        if result:
            return result
    return None
