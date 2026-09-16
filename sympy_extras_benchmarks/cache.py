"""Where the data of the collections is found.

Two directories hold it. The one returned by :func:`data_directory` is
``data/`` at the root of the repository: the collections which may be
redistributed are kept there in their own source language, with the
licence of each (see ``data/README.md``), and are read directly. The one
returned by :func:`cache_directory` is for what is not kept: the
collections which are too large or whose terms do not grant
redistribution are downloaded into it on first use and never committed.
The cache is ``$SYMPY_EXTRAS_BENCHMARKS_CACHE`` when that variable is
set, and ``.cache/`` at the root of the repository otherwise.
"""
from __future__ import annotations

import os
import pathlib
from typing import Optional

#: the environment variable overriding the location of the cache
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_CACHE'


def cache_directory() -> pathlib.Path:
    """The directory holding the downloaded data (created on demand).

    Examples
    ========

    >>> from sympy_extras_benchmarks.cache import cache_directory
    >>> print(cache_directory().name)
    .cache
    """
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override:
        path = pathlib.Path(override)
    else:
        path = pathlib.Path(__file__).resolve().parent.parent / '.cache'
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_directory() -> pathlib.Path:
    """The directory of the data kept in the repository.

    Examples
    ========

    >>> from sympy_extras_benchmarks.cache import data_directory
    >>> print(data_directory().name)
    data
    """
    return pathlib.Path(__file__).resolve().parent.parent / 'data'


def bundled(*parts: str) -> Optional[pathlib.Path]:
    """The path ``parts`` under :func:`data_directory` when it exists,
    ``None`` otherwise: what a dataset reads before reaching for the
    network.

    Examples
    ========

    >>> from sympy_extras_benchmarks.cache import bundled
    >>> print(bundled('maxima', 'repository', 'COPYING').name)
    COPYING
    >>> print(bundled('maxima', 'no-such-file'))
    None
    """
    path = data_directory().joinpath(*parts)
    return path if path.exists() else None
