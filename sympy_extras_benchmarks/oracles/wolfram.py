"""Wolfram Mathematica as an independent oracle.

A driver can hand a formula to Mathematica's ``Resolve`` to decide it
over the reals or the integers, and compare the verdict with the one
sympy-extras produced. Mathematica is not a dependency of this
repository: the command which evaluates Wolfram Language code is given
on the command line (``--wolfram``), which is also how a remote
installation is reached, so nothing here assumes a local licence.

The command must read Wolfram Language code on its standard input and
print what the code prints on its standard output. ``wolframscript``
wants a file rather than a stream, so the usual shape saves the input
first (which also works over ssh)::

    python -m sympy_extras_benchmarks solver_regressions --wolfram \\
        "sh -c 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"
    python -m sympy_extras_benchmarks solver_regressions --wolfram \\
        "ssh mathematica-host 'cat > /tmp/oracle.wl && wolframscript -file /tmp/oracle.wl'"

:func:`to_wolfram` prints a SymPy formula in Wolfram Language. Variables
are renamed (``x`` becomes ``sympyx``) so that they cannot collide with
Mathematica's built-in symbols, which are capitalised but include ``C``,
``D``, ``E``, ``I``, ``K``, ``N`` and ``O``.

Examples
========

>>> from sympy import Eq, Symbol
>>> from sympy_extras_benchmarks.oracles.wolfram import to_wolfram
>>> x, y = Symbol('x'), Symbol('y')
>>> print(to_wolfram((x**2 > 2) & Eq(x*y, 1)))
(((sympyx*sympyy) == 1) && (sympyx^(2) > 2))
>>> from sympy_extras.assumptions import Exists
>>> print(to_wolfram(Exists(x, x**2 < y)))
Exists[{sympyx}, (sympyx^(2) < sympyy)]
"""
from __future__ import annotations

import subprocess
from typing import Optional, Sequence

from sympy.core.basic import Basic
from sympy.core.numbers import Integer, Rational
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import Boolean
from sympy.sets.sets import Set
from sympy.core.singleton import S

from sympy_extras.assumptions import ForAll, Quantifier

__all__ = ['WolframError', 'to_wolfram', 'Wolfram']

#: the prefix which keeps SymPy names away from Mathematica's built-ins
PREFIX = 'sympy'


class WolframError(RuntimeError):
    """The oracle could not be reached, or answered something unusable."""


def _binary(node: Basic, operator: str) -> str:
    return "(" + (" %s " % operator).join(to_wolfram(a) for a in node.args) + ")"


def to_wolfram(node: Basic) -> str:
    """``node`` as Wolfram Language source.

    Only what the arithmetic benchmarks need is printed: rational
    numbers, the arithmetic operations, the relations, the propositional
    connectives, ``Mod``, ``Abs`` and the quantifiers of sympy-extras.
    Anything else raises :class:`WolframError`.
    """
    from sympy import (Abs, Add, And, Eq, Ge, Gt, Implies, Le, Lt, Mod, Mul, Ne, Not, Or, Pow, Xor)
    from sympy.logic.boolalg import BooleanFalse, BooleanTrue, Equivalent
    if isinstance(node, BooleanTrue):
        return "True"
    if isinstance(node, BooleanFalse):
        return "False"
    if isinstance(node, Symbol):
        return PREFIX + node.name
    if isinstance(node, Integer):
        return str(int(node))
    if isinstance(node, Rational):
        return "(%d/%d)" % (node.p, node.q)
    if isinstance(node, Quantifier):
        head = "ForAll" if isinstance(node, ForAll) else "Exists"
        variables = ", ".join(to_wolfram(v) for v in node.variables)
        return "%s[{%s}, %s]" % (head, variables, to_wolfram(node.formula))
    if isinstance(node, Add):
        return "(" + " + ".join(to_wolfram(a) for a in node.args) + ")"
    if isinstance(node, Mul):
        return "(" + "*".join(to_wolfram(a) for a in node.args) + ")"
    if isinstance(node, Pow):
        return "%s^(%s)" % (to_wolfram(node.base), to_wolfram(node.exp))
    if isinstance(node, Abs):
        return "Abs[%s]" % to_wolfram(node.args[0])
    if isinstance(node, Mod):
        return "Mod[%s, %s]" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, And):
        return _binary(node, "&&")
    if isinstance(node, Or):
        return _binary(node, "||")
    if isinstance(node, Xor):
        return "Xor[" + ", ".join(to_wolfram(a) for a in node.args) + "]"
    if isinstance(node, Not):
        return "(!%s)" % to_wolfram(node.args[0])
    if isinstance(node, Implies):
        return "Implies[%s, %s]" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Equivalent):
        return "Equivalent[" + ", ".join(to_wolfram(a) for a in node.args) + "]"
    if isinstance(node, Eq):
        return "(%s == %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Ne):
        return "(%s != %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Lt):
        return "(%s < %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Le):
        return "(%s <= %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Gt):
        return "(%s > %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    if isinstance(node, Ge):
        return "(%s >= %s)" % (to_wolfram(node.args[0]), to_wolfram(node.args[1]))
    raise WolframError("cannot print %s (%s)" % (node, type(node).__name__))


class Wolfram:
    """Mathematica behind a shell command reading code on its input.

    ``command`` is split with :func:`shlex.split`; ``timeout`` bounds one
    batch. :meth:`evaluate` returns one string per expression, in order.
    """

    def __init__(self, command: str, timeout: float = 120.0, chunk: int = 8) -> None:
        import shlex
        self.command = shlex.split(command)
        self.timeout = timeout
        #: how many expressions go into one invocation
        self.chunk = max(1, chunk)
        #: printed around each answer so that the batch can be split up
        self.delimiter = '<<<sympy-extras-benchmarks>>>'

    def evaluate(self, expressions: Sequence[str]) -> list[str]:
        """The value of each expression, as ``InputForm`` text.

        The expressions are sent in batches of :attr:`chunk`, so that one
        batch dying takes only its own answers with it. An expression
        which does not finish within the time limit gives ``'$Aborted'``;
        one which fails gives ``'$Failed'``; one whose batch produced no
        answer at all gives ``'$Aborted'`` as well.
        """
        answers: list[str] = []
        for start in range(0, len(expressions), self.chunk):
            answers.extend(self._batch(expressions[start:start + self.chunk]))
        return answers

    def _batch(self, expressions: Sequence[str]) -> list[str]:
        if not expressions:
            return []
        lines = ['$HistoryLength = 0;']
        for expression in expressions:
            escaped = expression.replace('\\', '\\\\').replace('"', '\\"')
            lines.append('Print["%s"];' % self.delimiter)
            lines.append('Print[ToString[InputForm[TimeConstrained['
                         'Quiet[Check[ToExpression["%s"], "$Failed"]], %d, "$Aborted"]]]];'
                         % (escaped, int(self.timeout)))
        lines.append('Print["%s"];' % self.delimiter)
        try:
            finished = subprocess.run(self.command, input="\n".join(lines), capture_output=True,
                                      text=True, timeout=self.timeout*len(expressions) + 120)
        except (subprocess.SubprocessError, OSError) as error:
            raise WolframError("the command %r failed: %s" % (" ".join(self.command), error))
        parts = finished.stdout.split(self.delimiter)
        values = [p.strip() for p in parts[1:1 + len(expressions)]]
        # a batch cut short (the kernel gave up, the connection dropped)
        # loses only its own tail, which is reported as aborted
        return values + ['$Aborted']*(len(expressions) - len(values))

    def resolve(self, formulas: Sequence[Boolean], domains: Sequence[Set]) -> list[Optional[bool]]:
        """The truth value of each closed formula, decided by ``Resolve``.

        ``None`` when Mathematica did not decide it. The formulas must be
        closed — a quantifier for every variable — which is what the
        quantified benchmarks state; ``Resolve`` reads every variable as
        an element of the region, so the domain is passed as the region.
        """
        expressions = ["Resolve[%s, %s]" % (to_wolfram(formula),
                                            "Integers" if domain is S.Integers else "Reals")
                       for formula, domain in zip(formulas, domains)]
        return self._truth(self.evaluate(expressions))

    @staticmethod
    def _truth(values: Sequence[str]) -> list[Optional[bool]]:
        answers: list[Optional[bool]] = []
        for value in values:
            answers.append(True if value == 'True' else (False if value == 'False' else None))
        return answers

    def satisfiable(self, formulas: Sequence[Boolean], domains: Sequence[Set]) -> list[Optional[bool]]:
        """Whether each formula has a solution, decided by ``Resolve``.

        ``None`` when Mathematica did not decide it. The free variables
        are existentially quantified, so the answer is a truth value.
        """
        expressions: list[str] = []
        for formula, domain in zip(formulas, domains):
            free = sorted((s for s in formula.free_symbols if isinstance(s, Symbol)), key=lambda s: s.name)
            region = "Integers" if domain is S.Integers else "Reals"
            body = to_wolfram(formula)
            if free:
                variables = ", ".join(to_wolfram(v) for v in free)
                if domain is S.Integers:
                    body = "Exists[{%s}, Element[{%s}, Integers] && (%s)]" % (variables, variables, body)
                else:
                    body = "Exists[{%s}, %s]" % (variables, body)
            expressions.append("Resolve[%s, %s]" % (body, region))
        return self._truth(self.evaluate(expressions))
