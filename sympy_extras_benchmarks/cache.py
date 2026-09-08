"""Location of the downloaded data.

External collections are fetched on first use into a cache directory and
never committed (see ``AGENTS.md``): the directory is
``$SYMPY_EXTRAS_BENCHMARKS_CACHE`` when that variable is set, and
``.cache/`` at the root of the repository otherwise.
"""
from __future__ import annotations

import os
import pathlib

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
