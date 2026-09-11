"""Definite integrals from FriCAS's ``mapleok.input``, as SymPy expressions.

The dataset
===========

Among the input files of FriCAS's test suite, ``mapleok.input`` is a
collection of about 250 definite integrals: logarithms and inverse
hyperbolic functions of rational and algebraic arguments, absolute values,
real and imaginary parts, orthogonal polynomials, many over infinite
ranges and many along complex paths (``z = -%i..%i``). Each is written
``label := integrate(f, z = a..b)``, sometimes with ``"noPole"``, the
user's assurance that no pole lies on the path, which does not change the
value.

What is read, and what is not
=============================

The integrand, the variable and the two endpoints, under the label of the
statement. The comments (``--``), which hold FriCAS's answers and notes on
them, are not read. Some entries write Maple's imaginary unit ``I`` and are
then repeated with FriCAS's ``%i``: ``I`` is read as the imaginary unit and
a repeated integral is kept once.

An integral between complex endpoints is taken along the straight segment
joining them, which is what an oracle computing it numerically integrates
(:mod:`~sympy_extras_benchmarks.oracles.quadrature`).

Source and licence
==================

FriCAS is distributed under the **modified (3-clause) BSD licence**
(``LICENSE.txt`` in the repository). Nothing of it is stored in this
repository: ``src/input`` is cloned sparsely on first use into the cache
directory, or read from ``$SYMPY_EXTRAS_BENCHMARKS_FRICAS`` (a checkout of
FriCAS, or a directory holding the file). FriCAS's code and answers are not
used.

Examples
========

>>> from sympy_extras_benchmarks.datasets.fricas_integrals import integrals
>>> text = ('-- an answer\\n'
...         't1 := integrate(acoth(w)/(w^2+1), w = 0..%plusInfinity, "noPole")\\n'
...         't2 := integrate(real(w)*w, w = -I..2)\\n'
...         't3 := integrate(real(w)*w, w = -%i..2)\\n')
>>> first, second = integrals(text, 'demo')
>>> first
DefiniteIntegral(demo:t1, w from 0 to oo, recorded None)
>>> second.integrand, second.lower
(w*re(w), -I)
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Optional

from sympy import Symbol

from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.integrals import (
    DefiniteIntegral, group, parse, split_arguments)

__all__ = ['REPOSITORY', 'SUBTREE', 'FILES', 'integrals', 'to_maxima', 'fetch', 'load']

REPOSITORY = "https://github.com/fricas/fricas"
SUBTREE = 'src/input'
FILES: tuple[str, ...] = ('mapleok.input',)
#: a checkout of FriCAS, or a directory holding the input files
ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_FRICAS'

_STATEMENT = re.compile(r"^\s*([A-Za-z_]\w*)\s*:=\s*integrate\s*\(", re.M)
#: FriCAS's names and Maxima's
_NAMES: dict[str, str] = {
    'real': 'realpart', 'imag': 'imagpart', 'legendreP': 'legendre_p',
    'hermiteH': 'hermite', 'laguerreL': 'laguerre',
}


def to_maxima(text: str) -> str:
    """A FriCAS expression in Maxima's syntax and names.

    >>> to_maxima('imag(z)*%pi + legendreP(2, z)**2 - I')
    imagpart(z)*%pi + legendre_p(2, z)^2 - %i
    """
    body = text.replace('**', '^')
    body = body.replace('%plusInfinity', 'inf').replace('%minusInfinity', 'minf')
    body = re.sub(r"(?<![\w%])I(?!\w)", '%i', body)
    for name, maxima in _NAMES.items():
        body = re.sub(r"(?<![\w%])" + re.escape(name) + r"\s*\(", maxima + '(', body)
    return body


def _uncomment(text: str) -> str:
    """``text`` without ``--`` comments and system commands, continuation
    lines (ending in ``_``) joined."""
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(('--', ')')):
            lines.append('')
            continue
        lines.append(re.sub(r"\s--.*$", '', line))
    return re.sub(r"_\n", '', "\n".join(lines))


def integrals(text: str, name: str = '') -> list[DefiniteIntegral]:
    """Every definite integral of a FriCAS input file that can be read,
    each integral once."""
    body = _uncomment(text)
    found: list[DefiniteIntegral] = []
    seen: set[tuple[object, ...]] = set()
    labels: dict[str, int] = {}
    for match in _STATEMENT.finditer(body):
        closed = group(body, match.end() - 1)
        if closed is None:
            continue
        arguments = split_arguments(closed[0])
        if len(arguments) not in (2, 3) or '=' not in arguments[1]:
            continue
        if len(arguments) == 3 and arguments[2] != '"noPole"':
            continue
        variable_text, _, bounds = arguments[1].partition('=')
        lower_text, dots, upper_text = bounds.partition('..')
        if not dots:
            continue
        integrand = parse(to_maxima(arguments[0]))
        variable = parse(variable_text)
        lower, upper = parse(to_maxima(lower_text)), parse(to_maxima(upper_text))
        if (integrand is None or lower is None or upper is None
                or not isinstance(variable, Symbol)):
            continue
        entry = DefiniteIntegral('', integrand, variable, lower, upper)
        if entry.key() in seen:
            continue
        seen.add(entry.key())
        label = match.group(1)
        labels[label] = labels.get(label, 0) + 1
        suffix = '.%d' % labels[label] if labels[label] > 1 else ''
        entry.name = '%s:%s%s' % (name, label, suffix)
        found.append(entry)
    return found


def _directory() -> Optional[pathlib.Path]:
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        root = pathlib.Path(override)
        return root / SUBTREE if (root / SUBTREE).is_dir() else root
    clone = cache_directory() / 'fricas'
    if not (clone / SUBTREE).is_dir():
        try:
            subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                            REPOSITORY, str(clone)], check=True, capture_output=True, timeout=1800)
            subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', SUBTREE],
                           check=True, capture_output=True, timeout=1800)
        except (subprocess.SubprocessError, OSError):
            return None
    return clone / SUBTREE if (clone / SUBTREE).is_dir() else None


def fetch() -> list[tuple[str, str]]:
    """``(collection, text)`` for every file that could be got."""
    directory = _directory()
    if directory is None:
        return []
    return [(f.split('.')[0], (directory / f).read_text(errors='replace'))
            for f in FILES if (directory / f).is_file()]


def load() -> list[DefiniteIntegral]:
    """Every readable definite integral of the files."""
    found: list[DefiniteIntegral] = []
    for name, text in fetch():
        found.extend(integrals(text, name))
    return found
