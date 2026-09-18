"""The expression language of REDUCE, rewritten into Maxima's.

REDUCE writes ``df(y, x, 2)`` for a derivative, calls a function of one
argument without brackets (``sin x``), multiplies implicitly (``2x``,
``4df(y,x)``) and names ``e`` and ``pi`` without a sigil. :func:`to_maxima`
rewrites that syntax, and :func:`to_maxima_names` REDUCE's special
function names as well, so that the expression parser of
:mod:`~sympy_extras_benchmarks.parsers.maxima` reads the result.
:func:`strip_comments` removes the ``%`` line comments.

Nothing here reads a file or knows which collection a text comes from.
"""
from __future__ import annotations

import re

__all__ = ['to_maxima', 'to_maxima_names', 'strip_comments']

#: functions REDUCE writes without brackets, and that SymPy also knows
_BRACKETLESS = ('sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'exp', 'sqrt',
                'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh')


def to_maxima(text: str) -> str:
    """REDUCE's expression syntax rewritten in Maxima's.

    Examples
    ========

    >>> from sympy_extras_benchmarks.parsers.reduce import to_maxima
    >>> to_maxima('df(y,x,2)*(a*x+b)^2 + 4df(y,x)*(a*x+b)*a')
    'diff(y,x,2)*(a*x+b)^2 + 4*'diff(y,x)*(a*x+b)*a
    >>> to_maxima('-1/2*df(y,x) + y = sin x')
    -1/2*'diff(y,x) + y = sin(x)
    """
    body = text.replace('**', '^')
    # a bracketless call of one argument: ``sin x`` -> ``sin(x)``
    for name in _BRACKETLESS:
        body = re.sub(r'\b%s\s+([A-Za-z_][A-Za-z_0-9]*)' % name, r'%s(\1)' % name, body)
    # implicit multiplication: 2x, 4df(y,x), 2(x+1). The exponent of a
    # floating point number is not one: in ``1.5e-3`` the ``e`` belongs to the
    # number, and splitting it off would give ``1.5*e-3``.
    body = re.sub(r'(\d)\s*(?![eE][-+]?\d)(?=[A-Za-z_(])', r'\1*', body)
    # ``df`` is the derivative; Maxima writes the noun form
    body = re.sub(r'\bdf\s*\(', "'diff(", body)
    # Euler's number
    body = re.sub(r'(?<![A-Za-z_0-9])e\s*\^', '%e^', body)
    return body


def strip_comments(text: str) -> str:
    """``text`` without REDUCE's ``%`` line comments."""
    return re.sub(r'%[^\n]*', '', text)


#: REDUCE's names (lower case) and Maxima's; a name mapped to one Maxima
#: does not know is refused by the parser
_NAMES: dict[str, str] = {
    'besselj': 'bessel_j', 'bessely': 'bessel_y', 'besseli': 'bessel_i', 'besselk': 'bessel_k',
    'ei': 'expintegral_ei', 'si': 'expintegral_si', 'ci': 'expintegral_ci',
    'shi': 'expintegral_shi', 'chi': 'expintegral_chi', 'heaviside': 'unit_step',
    'fresnel_c': 'reduce_fresnel_c', 'fresnel_s': 'reduce_fresnel_s',
}


def to_maxima_names(text: str) -> str:
    """A REDUCE expression in Maxima's syntax and names.

    >>> to_maxima_names('x*BesselJ(0,x)*e^(-2x)/infinity + Si(pi*x)')
    x*bessel_j(0,x)*%e^(-2*x)/inf + expintegral_si(%pi*x)
    """
    body = to_maxima(text.lower())
    body = re.sub(r"(?<![\w%])infinity(?!\w)", 'inf', body)
    body = re.sub(r"(?<![\w%])pi(?!\w)", '%pi', body)
    body = re.sub(r"(?<![\w%])e(?![\w(])", '%e', body)
    for name, maxima in _NAMES.items():
        body = re.sub(r"(?<![\w%])" + re.escape(name) + r"\s*\(", maxima + '(', body)
    return body
