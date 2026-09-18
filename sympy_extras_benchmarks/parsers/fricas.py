"""The input language of FriCAS, rewritten into Maxima's.

FriCAS writes ``**`` as well as ``^``, ``%plusInfinity`` and
``%minusInfinity``, ``I`` (in Maple's style) for the imaginary unit, and
its own names for some functions (``real``, ``legendreP``, ...).
:func:`to_maxima` rewrites those, so that the expression parser of
:mod:`~sympy_extras_benchmarks.parsers.maxima` reads the result. :func:`joined`
removes ``--`` comments and system commands and joins continuation lines,
and :func:`quoted` reads a string literal.

Nothing here reads a file or knows which collection a text comes from.
"""
from __future__ import annotations

import re
from typing import Optional

__all__ = ['to_maxima', 'joined', 'quoted']

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


def joined(text: str) -> str:
    """A FriCAS input without its ``--`` comments and system commands, the
    continuation lines (ending in ``_``) joined."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(('--', ')')):
            lines.append('')
            continue
        lines.append(re.sub(r"\s--.*$", '', line))
    return re.sub(r"_\s*\n", '', "\n".join(lines))


def quoted(argument: str) -> Optional[str]:
    """The text of a FriCAS string literal, or of adjacent literals over
    several lines joined; ``None`` for anything else.

    >>> from sympy_extras_benchmarks.parsers.fricas import quoted
    >>> quoted('"(x+1)*"   "exp(x)"'), quoted('f: String')
    ('(x+1)*exp(x)', None)
    """
    body = argument.strip()
    if '_"' in body or not re.fullmatch(r'(\s*"[^"]*"\s*)+', body):
        return None
    return ''.join(re.findall(r'"([^"]*)"', body))
