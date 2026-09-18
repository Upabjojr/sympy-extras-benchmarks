"""The record of a problem of the CAD test collections.

The Bath example bank (:mod:`~sympy_extras_benchmarks.datasets.bath_cad`),
the tests of QEPCAD B (:mod:`~sympy_extras_benchmarks.datasets.qepcad_tests`)
and those of Tarski (:mod:`~sympy_extras_benchmarks.datasets.tarski_tests`)
are read to a list of :class:`Example`: the problem as the collection writes
it, in QEPCAD or Tarski syntax, the question it asks and the answer it
records. The text is parsed later, by
:mod:`~sympy_extras_benchmarks.parsers.qepcad`.
"""
from __future__ import annotations

from typing import Optional

__all__ = ['Example']


class Example:
    """A problem of a CAD test collection, written in QEPCAD or Tarski syntax.

    Attributes
    ==========

    collection : str
        The collection and set it comes from, e.g. ``'qepcad-application'``.
    name : str
        Its name in the collection.
    syntax : str
        ``'qepcad'`` when :attr:`text` is a QEPCAD input (read with
        :func:`parse_inputs`), ``'tarski'`` when it is a formula (read with
        :func:`parse_formula`).
    text : str
        The problem as written in the collection.
    question : str
        ``'resolve'``: eliminate the quantifiers (decide the formula when
        every variable is quantified); ``'satisfiable'``: whether the
        quantifier-free formula has a real solution.
    expected : str or None
        The answer the collection records, in Tarski syntax (a formula, or
        ``true``/``false``); ``None`` when it records none.
    duplicate_of : str or None
        The name of an earlier problem of the collections which is the same
        question, when there is one.
    """

    def __init__(self, collection: str, name: str, syntax: str, text: str, question: str = 'resolve',
                 expected: Optional[str] = None, duplicate_of: Optional[str] = None) -> None:
        self.collection = collection
        self.name = name
        self.syntax = syntax
        self.text = text
        self.question = question
        self.expected = expected
        self.duplicate_of = duplicate_of

    @property
    def key(self) -> str:
        return '%s/%s' % (self.collection, self.name)

    def __repr__(self) -> str:
        return "Example(%r, %r)" % (self.collection, self.name)
