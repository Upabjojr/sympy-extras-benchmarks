"""Maple's polynomial notation, read into SymPy.

The polynomials of a Maple list are written with ``^`` for powers and
``*`` for products, which SymPy's own parser reads once ``^`` is spelled
``**``. :func:`polynomial` does that, with the names of ``symbols`` (every
other name becomes a new symbol, added to ``symbols``).

Nothing here reads a file or knows which collection a text comes from.
"""
from __future__ import annotations

import re

from sympy import Symbol
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from sympy_extras._typing import as_expr

__all__ = ['polynomial']

def polynomial(text: str, symbols: dict[str, Symbol]) -> Expr:
    for name in re.findall(r'[A-Za-z_][A-Za-z0-9_]*', text):
        symbols.setdefault(name, Symbol(name))
    local: dict[str, object] = dict(symbols)
    return as_expr(parse_expr(text.replace('^', '**'), local_dict=local))
