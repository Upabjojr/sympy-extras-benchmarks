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
>>> from sympy import CRootOf
>>> print(to_wolfram(x > CRootOf(x**3 - x - 1, 0)))
(sympyx > Root[Function[{sympyx}, (-1 + sympyx^(3) + (-1*sympyx))], 1])
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

__all__ = ['WolframError', 'wolfram_name', 'to_wolfram', 'Wolfram']

#: the prefix which keeps SymPy names away from Mathematica's built-ins
PREFIX = 'sympy'


class WolframError(RuntimeError):
    """The oracle could not be reached, or answered something unusable."""


#: the elementary functions, spelled as Mathematica spells them. A
#: function absent here is refused rather than guessed at: a wrong
#: spelling would make the oracle answer a different question.
FUNCTIONS: dict[str, str] = {
    'log': 'Log', 'exp': 'Exp', 'sqrt': 'Sqrt',
    'sin': 'Sin', 'cos': 'Cos', 'tan': 'Tan', 'cot': 'Cot', 'sec': 'Sec', 'csc': 'Csc',
    'asin': 'ArcSin', 'acos': 'ArcCos', 'atan': 'ArcTan', 'acot': 'ArcCot',
    'sinh': 'Sinh', 'cosh': 'Cosh', 'tanh': 'Tanh', 'coth': 'Coth',
    'asinh': 'ArcSinh', 'acosh': 'ArcCosh', 'atanh': 'ArcTanh',
    'gamma': 'Gamma', 'loggamma': 'LogGamma', 'digamma': 'PolyGamma',
    'erf': 'Erf', 'erfc': 'Erfc', 'Ei': 'ExpIntegralEi', 'li': 'LogIntegral',
    'factorial': 'Factorial', 'binomial': 'Binomial', 'zeta': 'Zeta',
    'floor': 'Floor', 'ceiling': 'Ceiling', 'sign': 'Sign', 're': 'Re', 'im': 'Im',
    'arg': 'Arg', 'conjugate': 'Conjugate', 'Max': 'Max', 'Min': 'Min',
    'besselj': 'BesselJ', 'bessely': 'BesselY', 'besseli': 'BesselI', 'besselk': 'BesselK',
    'harmonic': 'HarmonicNumber', 'polygamma': 'PolyGamma', 'lowergamma': 'Gamma',
}


def wolfram_name(name: str) -> str:
    """The Wolfram Language symbol standing for a SymPy symbol.

    A Mathematica name is made of letters and digits only: ``_`` is a
    pattern (``x__1`` reads as the pattern ``x__`` times ``1``) and ``$``
    marks system names. Every other character is written as ``Z<code>Z``,
    and ``Z`` itself as ``ZZ``, which keeps distinct names distinct.

    >>> from sympy_extras_benchmarks.oracles.wolfram import wolfram_name
    >>> wolfram_name('x'), wolfram_name('ts2_0__1'), wolfram_name('Zeta$1')
    ('sympyx', 'sympyts2Z95Z0Z95ZZ95Z1', 'sympyZZetaZ36Z1')
    """
    encoded = []
    for character in name:
        if character == 'Z':
            encoded.append('ZZ')
        elif character.isascii() and character.isalnum():
            encoded.append(character)
        else:
            encoded.append('Z%dZ' % ord(character))
    return PREFIX + ''.join(encoded)


def _binary(node: Basic, operator: str) -> str:
    return "(" + (" %s " % operator).join(to_wolfram(a) for a in node.args) + ")"


def to_wolfram(node: Basic) -> str:
    """``node`` as Wolfram Language source.

    Only what the arithmetic benchmarks need is printed: rational
    numbers, the arithmetic operations, the relations, the propositional
    connectives, ``Mod``, ``Abs`` and the quantifiers of sympy-extras.
    Anything else raises :class:`WolframError`.
    """
    from sympy import (Abs, Add, And, Eq, Ge, Gt, Implies, Le, Lt, Mod, Mul, Ne, Not, Or, Pow,
                       Xor, atan2, nan, oo, pi, zoo)
    from sympy.core.numbers import Exp1, ImaginaryUnit, NegativeInfinity
    from sympy.logic.boolalg import BooleanFalse, BooleanTrue, Equivalent
    from sympy.core.function import AppliedUndef
    from sympy.polys.rootoftools import ComplexRootOf
    if node is oo:
        return "Infinity"
    if isinstance(node, NegativeInfinity):
        return "-Infinity"
    if node is zoo:
        return "ComplexInfinity"
    if node is nan:
        return "Indeterminate"
    if node is pi:
        return "Pi"
    if isinstance(node, Exp1):
        return "E"
    if isinstance(node, ImaginaryUnit):
        return "I"
    if isinstance(node, atan2):
        # Mathematica takes the arguments the other way round:
        # ArcTan[x, y] is the angle of (x, y), i.e. atan2(y, x)
        return "ArcTan[%s, %s]" % (to_wolfram(node.args[1]), to_wolfram(node.args[0]))
    name = FUNCTIONS.get(type(node).__name__)
    if name is not None and not isinstance(node, AppliedUndef):
        return "%s[%s]" % (name, ", ".join(to_wolfram(a) for a in node.args))
    if isinstance(node, ComplexRootOf):
        # SymPy numbers the real roots first, in increasing order, and so
        # does Mathematica's Root: the k-th real root is Root[f, k + 1]
        polynomial, index = node.args
        generators = sorted(polynomial.free_symbols, key=str)
        if not node.is_real or len(generators) != 1 or not isinstance(index, Integer):
            raise WolframError("cannot print the root %s" % (node,))
        return "Root[Function[{%s}, %s], %d]" % (to_wolfram(generators[0]), to_wolfram(polynomial), int(index) + 1)
    if isinstance(node, BooleanTrue):
        return "True"
    if isinstance(node, BooleanFalse):
        return "False"
    if isinstance(node, Symbol):
        return wolfram_name(node.name)
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
