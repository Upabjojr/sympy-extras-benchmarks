"""``integrate`` on the indefinite integrals of Maxima's and FriCAS's test
suites, each result checked by differentiation.

Usage::

    python -m sympy_extras_benchmarks indefinite_integrals
        [--collections a,b] [--sample N] [--seed N] [--timeout S]
        [--extras] [--workers N] [--memory MB] [--output results.jsonl]

This driver measures SymPy's ``integrate(f, x)`` or, with ``--extras``,
the indefinite integrator of sympy-extras
(``sympy_extras.integrals.indefinite.indefinite_integral`` when the
package has it, else ``sympy_extras.integrals.antiderivative.antiderivative``,
the antiderivative behind its definite integrator: the Risch port, Trager's
algorithm, the radical table, SymPy as the last resort).

Each integral is computed with its parameters carrying what the source
assumes about them (as in :mod:`~sympy_extras_benchmarks.drivers.definite_integrals`),
in parallel worker processes (:mod:`~sympy_extras_benchmarks.runner`,
resumable from ``--output``). The result ``F`` is checked against the
integrand ``f``, never against the reference the source records (a third
opinion, which may differ by a constant or be wrong):

``correct``
    ``F' - f`` is ``0`` after ``cancel`` or ``simplify``, or vanishes at
    every random real point of the variable at which ``f`` is real and
    both sides evaluate (the parameters at random values satisfying the
    facts);
``nonreal``
    correct, but ``F`` carries ``I``, ``exp_polar`` or ``polar_lift`` and
    ``F(q) - F(p)`` has an imaginary part for two real points ``p < q``
    between which the integrand is real and its numerical integral
    converges (an imaginary part constant on each side of a singularity,
    ``log(x)`` across ``0``, is an integration constant and is not
    counted): a right derivative from a complex antiderivative, which a
    definite integral evaluated between real bounds gets wrong;
``WRONG``
    ``F' - f`` is not ``0`` at a real point where both sides evaluate
    (SymPy's answer is wrong). The driver exits 1;
``unevaluated``
    an ``Integral`` remains in the result;
``no answer``
    the time ran out or the integrator gave up;
``crash``
    the integrator raised;
``unchecked``
    a result that could neither be simplified to ``0`` nor evaluated at
    three real points (no sample satisfies the facts, or the integrand is
    nowhere real there).

With ``--wolfram COMMAND`` (see :mod:`~sympy_extras_benchmarks.oracles.wolfram`)
Mathematica is asked two things after the run: ``Integrate[f, x]`` for
every entry whose source records no antiderivative, kept as a reference
(``reference (mathematica)`` in the listing; a difference from it is a
difference, not a wrong result); and, for every ``unchecked`` result,
``N[F' - f]`` and ``N[f]`` at five real points: a nonzero difference at
three points where ``f`` is real makes the result ``WRONG (mathematica)``,
a zero one ``correct (mathematica)``; the ``WRONG`` results are put to the
same check, which confirms them or, when SymPy's own numerical evaluation
of the derivative was at fault, clears them. Its answers are kept in
``<output>.wolfram.json`` and not asked again.

The wrong and the nonreal results are listed at the end with the
integrand, the result and the reference of the source when it records
one. Use a separate ``--output`` for each configuration: a run resumes
from the results already in the file.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys

import mpmath
from typing import Callable, Optional

from sympy import And, I, Integral, Rational, Symbol, exp_polar, integrate, nan, oo, polar_lift, sympify, zoo
from sympy.core.sympify import SympifyError
from sympy.core.expr import Expr
from sympy.logic.boolalg import Boolean
from sympy.polys.polytools import cancel
from sympy.simplify.simplify import simplify
from sympy.utilities.lambdify import lambdify

from sympy_extras._timeout import TimeLimitExceeded, attempt, time_limit
from sympy_extras._typing import as_expr
from sympy_extras.integrals.conditions import sample_values

from sympy_extras_benchmarks.datasets import indefinite_integrals
from sympy_extras_benchmarks.datasets.indefinite_integrals import IndefiniteIntegral
from sympy_extras_benchmarks.drivers.definite_integrals import assumed_symbols, statements
from sympy_extras_benchmarks.datasets.integrals import DefiniteIntegral
from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, number, to_wolfram
from sympy_extras_benchmarks.runner import JSON, Result, Task, run

__all__ = ['Integrator', 'INTEGRATORS', 'check', 'verify', 'work', 'main']

#: an integrator: the integrand, the variable and the facts about the
#: parameters; ``None`` when it gives up
Integrator = Callable[[Expr, Symbol, list[Boolean]], Optional[Expr]]

#: the real points of the variable tried, in three ranges of size, and how
#: many must evaluate
POINTS = 12
NEEDED = 3
#: the relative agreement asked of the derivative at a point
TOLERANCE = 1e-6
#: the questions that go to Mathematica together
_WOLFRAM_BATCH = 20


def _sympy(integrand: Expr, variable: Symbol, facts: list[Boolean]) -> Optional[Expr]:
    return as_expr(integrate(integrand, variable))


def _extras(integrand: Expr, variable: Symbol, facts: list[Boolean]) -> Optional[Expr]:
    try:
        from sympy_extras.integrals.indefinite import indefinite_integral
    except ImportError:
        from sympy_extras.integrals.antiderivative import antiderivative
        return antiderivative(integrand, variable)
    return as_expr(indefinite_integral(integrand, variable, facts))


INTEGRATORS: dict[str, Integrator] = {'default': _sympy, 'extras': _extras}


def _as_definite(entry: IndefiniteIntegral) -> DefiniteIntegral:
    """The entry as a definite integral over ``(0, 1)``, the shape the
    helpers of the definite driver read the facts and properties from."""
    return DefiniteIntegral(entry.name, entry.integrand, entry.variable, 0, 1, entry.facts,
                            entry.properties)


def _number(value: Expr, digits: int = 20) -> Optional[complex]:
    """``value`` as a complex number when it is a finite one."""
    try:
        evaluated = value.evalf(digits)
        number = complex(evaluated)
    except (TypeError, ValueError, OverflowError, ZeroDivisionError):
        return None
    if number != number or abs(number) == float('inf') or evaluated.has(nan, zoo, oo, -oo):
        return None
    return number


def _real(number: complex) -> bool:
    # absolute, not relative: bessely(11, -3/7) is 2.6e13 + 2e-15*I, a
    # complex number whose imaginary part a relative test would wave through,
    # and an antiderivative right for x > 0 was then reported wrong there
    return abs(number.imag) <= 1e-18


def _agree(a: complex, b: complex) -> bool:
    return abs(a - b) <= TOLERANCE * (1 + abs(a) + abs(b))


def verify(integrand: Expr, variable: Symbol, result: Expr, parameters: list[Symbol],
           facts: list[Boolean], rng: random.Random, timeout: float) -> tuple[str, list[JSON]]:
    """``('correct' | 'nonreal' | 'WRONG' | 'unchecked', points)``: the
    derivative of ``result`` against ``integrand``, symbolically and then
    at random real points, see the module documentation."""
    difference = as_expr(result.diff(variable) - integrand)
    zero = attempt(lambda: as_expr(cancel(difference)), timeout / 4)
    complex_form = result.has(I, exp_polar, polar_lift)
    if zero is not None and zero == 0 and not complex_form:
        return 'correct', []
    if zero is None or zero != 0:
        simpler = attempt(lambda: as_expr(simplify(difference)), timeout / 4)
        if simpler is not None and simpler == 0 and not complex_form:
            return 'correct', []
    values: dict[Symbol, Expr] = {}
    if parameters:
        found = sample_values(parameters, facts, rng)
        if found is None:
            return 'unchecked', []
        values = found
    derivative = as_expr(result.diff(variable).xreplace(values))
    target = as_expr(integrand.xreplace(values))
    antiderivative = as_expr(result.xreplace(values))
    checked: list[JSON] = []
    verdicts: list[str] = []
    valid: list[tuple[Rational, complex]] = []
    for index in range(POINTS):
        width = (1, 5, 40)[index % 3]
        point = Rational(rng.randint(-97 * width, 97 * width), 97) + Rational(1, 101)
        expected = _number(as_expr(target.subs(variable, point)))
        if expected is None or not _real(expected):
            continue
        ours = _number(as_expr(derivative.subs(variable, point)))
        if ours is None:
            continue
        if not _agree(ours, expected):
            # a disagreement is confirmed at fifty digits: SymPy's evaluation
            # of a G-function near 0 loses the twenty (the bug: two Bessel
            # integrals, right at thirty digits, were reported wrong)
            precise_expected = _number(as_expr(target.subs(variable, point)), 50)
            precise_ours = _number(as_expr(derivative.subs(variable, point)), 50)
            if precise_expected is not None and precise_ours is not None:
                expected, ours = precise_expected, precise_ours
        checked.append({'point': str(point), 'integrand': expected.real, 'derivative': [ours.real, ours.imag]})
        verdicts.append('ok' if _agree(ours, expected) else 'WRONG')
        value = _number(as_expr(antiderivative.subs(variable, point)))
        if value is not None:
            valid.append((point, value))
    if 'WRONG' in verdicts:
        return 'WRONG', checked
    if len(verdicts) < NEEDED:
        return 'unchecked', checked
    if complex_form and _branch_jumps(target, variable, valid):
        return 'nonreal', checked
    return 'correct', checked


def _branch_jumps(integrand: Expr, variable: Symbol, points: list[tuple[Rational, complex]]) -> bool:
    """Whether ``F(q) - F(p)`` has an imaginary part for two points between
    which the integrand is real and its numerical integral converges."""
    try:
        function = lambdify(variable, integrand, 'mpmath')
    except (TypeError, ValueError, NameError, SyntaxError):
        return False
    ordered = sorted(points, key=lambda pair: pair[0])
    for (p, value_p), (q, value_q) in zip(ordered[:-1], ordered[1:]):
        try:
            integral, error = mpmath.quad(function, [float(p), float(q)], error=True)
        except (ValueError, TypeError, ZeroDivisionError, OverflowError, mpmath.libmp.NoConvergence):
            continue
        integral, error = mpmath.mpc(integral), abs(mpmath.mpf(error))
        if abs(integral.imag) > 1e-9 * (1 + abs(integral)) or error > 1e-6 * (1 + abs(integral)):
            continue                                        # not real, or not converged, between them
        difference = value_q - value_p
        if abs(difference.imag) > 1e-6 * (1 + abs(difference)):
            return True
    return False


def check(entry: IndefiniteIntegral, rng: random.Random, timeout: float,
          integrator: Integrator = _sympy) -> Result:
    """Compute ``entry`` with ``integrator`` and check the result."""
    definite = _as_definite(entry)
    replacement = assumed_symbols(definite)
    integrand = as_expr(entry.integrand.xreplace(replacement))
    facts = statements(definite, replacement)
    parameters = [replacement.get(p, p) for p in entry.parameters]
    result: Result = {}
    try:
        with time_limit(timeout):
            value = integrator(integrand, entry.variable, facts)
    except (TimeLimitExceeded, NotImplementedError, RecursionError):
        value = None                                # gave up, or the time ran out
    except Exception as error:                      # noqa: BLE001 - a crash is a verdict here
        result['verdict'] = 'crash'
        result['error'] = '%s: %s' % (type(error).__name__, str(error)[:200])
        return result
    result['result'] = None if value is None else str(value)[:2000]
    if value is None:
        result['verdict'] = 'no answer'
        return result
    if value.has(Integral):
        result['verdict'] = 'unevaluated'
        return result
    verdict, checked = verify(integrand, entry.variable, value, parameters, facts, rng, timeout)
    result['verdict'] = verdict
    result['checked'] = checked
    if entry.recorded is not None:
        result['reference'] = str(entry.recorded)[:500]
    return result


_LOADED: dict[str, IndefiniteIntegral] = {}


def _entry(name: str) -> Optional[IndefiniteIntegral]:
    if not _LOADED:
        _LOADED.update({e.name: e for e in indefinite_integrals.load()})
    return _LOADED.get(name)


def work(task: Task) -> Result:
    """Check one integral (the ``work`` function of the runner)."""
    name = str(task['name'])
    entry = _entry(name)
    if entry is None:
        return {'verdict': 'missing'}
    timeout = task['timeout']
    rng = random.Random('%s/%s' % (task['seed'], name))
    return check(entry, rng, float(timeout) if isinstance(timeout, (int, float)) else 20.0,
                 INTEGRATORS[str(task['integrator'])])


def _reference_query(entry: IndefiniteIntegral) -> str:
    """Mathematica's ``Integrate`` of the entry under its facts."""
    body = "Integrate[%s, %s]" % (to_wolfram(entry.integrand), to_wolfram(entry.variable))
    if entry.facts:
        body = "Assuming[%s, %s]" % (to_wolfram(And(*entry.facts)), body)
    return body


def _named(text: str, entry: IndefiniteIntegral) -> Optional[Expr]:
    """A result read back from its text, its symbols those of the entry."""
    try:
        parsed = sympify(text)
    except (SympifyError, SyntaxError, TypeError, ValueError):
        return None
    if not isinstance(parsed, Expr):
        return None
    names = {s.name: s for s in entry.integrand.free_symbols | {entry.variable} if isinstance(s, Symbol)}
    replacement = {s: names[s.name] for s in parsed.free_symbols if isinstance(s, Symbol) and s.name in names}
    return as_expr(parsed.xreplace(replacement))


def _settling_queries(entry: IndefiniteIntegral, result: Expr, rng: random.Random
                      ) -> Optional[list[tuple[str, str]]]:
    """``(N[f], N[F' - f])`` at five real points, in Wolfram Language."""
    values: dict[Symbol, Expr] = {}
    if entry.parameters:
        found = sample_values(entry.parameters, list(entry.facts), rng)
        if found is None:
            return None
        values = found
    difference = as_expr((result.diff(entry.variable) - entry.integrand).xreplace(values))
    target = as_expr(entry.integrand.xreplace(values))
    queries: list[tuple[str, str]] = []
    for index in range(5):
        width = (1, 5, 40, 1, 5)[index]
        point = Rational(rng.randint(-97 * width, 97 * width), 97) + Rational(1, 101)
        try:
            queries.append(("N[%s, 20]" % to_wolfram(target.subs(entry.variable, point)),
                            "N[%s, 20]" % to_wolfram(difference.subs(entry.variable, point))))
        except WolframError:
            return None
    return queries


def _second_opinions(results: list[Result], entries: dict[str, IndefiniteIntegral], oracle: Wolfram,
                     cache: pathlib.Path, seed: int) -> tuple[dict[str, str], dict[str, str]]:
    """``(references, verdicts)``: Mathematica's antiderivative for the
    entries without a recorded one, and its verdict (``'correct'``,
    ``'WRONG'`` or ``'undecided'``) on the ``unchecked`` results; answers
    already in ``cache`` are not asked again."""
    known: dict[str, dict[str, str]] = {'reference': {}, 'settled': {}}
    if cache.exists():
        loaded = json.loads(cache.read_text())
        if isinstance(loaded, dict):
            for key in known:
                part = loaded.get(key)
                if isinstance(part, dict):
                    known[key] = {str(k): str(v) for k, v in part.items()}
    wanted = [name for name, entry in entries.items()
              if entry.recorded is None and name not in known['reference']]
    queries: list[str] = []
    asked: list[str] = []
    for name in wanted:
        try:
            queries.append(_reference_query(entries[name]))
        except WolframError:
            continue
        asked.append(name)
    if queries:
        print("\nasking Mathematica for %d reference antiderivatives..." % len(queries), flush=True)
    for start in range(0, len(queries), _WOLFRAM_BATCH):
        try:
            answers = oracle.evaluate(queries[start:start + _WOLFRAM_BATCH])
        except WolframError as error:
            print("the oracle failed: %s" % error)
            break
        for name, answer in zip(asked[start:start + _WOLFRAM_BATCH], answers):
            known['reference'][name] = answer
        cache.write_text(json.dumps(known, indent=1))
        print("  %d of %d references" % (min(start + _WOLFRAM_BATCH, len(queries)), len(queries)), flush=True)
    pending: list[tuple[str, list[tuple[str, str]]]] = []
    for result in results:
        name = str(result['id'])
        if result.get('verdict') not in ('unchecked', 'WRONG') or name in known['settled'] or name not in entries:
            continue
        parsed = _named(str(result.get('result')), entries[name])
        if parsed is None:
            continue
        queries_ = _settling_queries(entries[name], parsed, random.Random('%s/%s/wolfram' % (seed, name)))
        if queries_:
            pending.append((name, queries_))
    if pending:
        print("asking Mathematica to settle %d unchecked results..." % len(pending), flush=True)
    for start in range(0, len(pending), _WOLFRAM_BATCH // 5 or 1):
        batch = pending[start:start + (_WOLFRAM_BATCH // 5 or 1)]
        flat = [q for _, pairs in batch for pair in pairs for q in pair]
        try:
            answers = oracle.evaluate(flat)
        except WolframError as error:
            print("the oracle failed: %s" % error)
            break
        position = 0
        for name, pairs in batch:
            zeros = nonzeros = 0
            for _ in pairs:
                value, difference = number(answers[position]), number(answers[position + 1])
                position += 2
                if value is None or difference is None or abs(value.imag) > 1e-9 * (1 + abs(value)):
                    continue
                if abs(difference) <= 1e-6 * (1 + abs(value)):
                    zeros += 1
                else:
                    nonzeros += 1
            known['settled'][name] = ('WRONG' if nonzeros >= NEEDED else
                                      'correct' if zeros >= NEEDED and not nonzeros else 'undecided')
        cache.write_text(json.dumps(known, indent=1))
    return known['reference'], known['settled']


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--collections', default=','.join(indefinite_integrals.COLLECTIONS))
    parser.add_argument('--sample', type=int, default=0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--timeout', type=float, default=20.0)
    parser.add_argument('--extras', action='store_true')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--memory', type=int, default=2048)
    parser.add_argument('--output', default='results/indefinite_integrals.jsonl')
    parser.add_argument('--wolfram', default='')
    args = parser.parse_args(argv)
    collections = args.collections.split(',')
    for collection in collections:
        if collection not in indefinite_integrals.COLLECTIONS:
            print("unknown collection %r; one of: %s" % (collection, ', '.join(indefinite_integrals.COLLECTIONS)))
            return 2
    entries = indefinite_integrals.load(collections)
    kept = indefinite_integrals.licence_files()
    print("%d integrals; licences %s; %s" % (
        len(entries), ', '.join(sorted(set(indefinite_integrals.LICENCES[c] for c in collections))),
        ', '.join(str(p) for p in kept) if kept else 'no licence file in the local copy'), flush=True)
    if not entries:
        print("no integral could be fetched")
        return 1
    tasks: list[Task] = [{'id': e.name, 'name': e.name, 'timeout': args.timeout, 'seed': args.seed,
                          'integrator': 'extras' if args.extras else 'default'} for e in entries]
    if args.sample:
        random.Random(args.seed).shuffle(tasks)
        tasks = tasks[:args.sample]
    by_name = {e.name: e for e in entries}

    def report(result: Result) -> None:
        line = "%-28s %-12s %6ss" % (str(result['id'])[:28], result.get('verdict'), result.get('time'))
        if result.get('verdict') in ('WRONG', 'nonreal', 'crash'):
            line += '  %s' % str(result.get('result') or result.get('error'))[:70]
        print(line, flush=True)

    output = pathlib.Path(args.output)
    ids = {str(t['id']) for t in tasks}
    results = [r for r in run(tasks, 'sympy_extras_benchmarks.drivers.indefinite_integrals',
                              output, workers=args.workers, deadline=3*args.timeout + 60,
                              memory=args.memory, report=report)
               if str(r['id']) in ids]
    references: dict[str, str] = {}
    settled: dict[str, str] = {}
    if args.wolfram:
        # the entries of this run only (a sample asks about its sample)
        chosen = {name: by_name[name] for name in ids if name in by_name}
        references, settled = _second_opinions(results, chosen, Wolfram(args.wolfram, 60.0, _WOLFRAM_BATCH),
                                               output.with_suffix('.wolfram.json'), args.seed)
    counts: dict[str, dict[str, int]] = {}
    findings: list[Result] = []
    for result in results:
        name = str(result['id'])
        verdict = str(result.get('verdict'))
        if verdict in ('unchecked', 'WRONG') and settled.get(name) in ('correct', 'WRONG'):
            # an unchecked result settled, or a WRONG one confirmed or cleared
            # by Mathematica's evaluation of the same derivative check
            verdict = '%s (mathematica)' % settled[name]
            result['verdict'] = verdict
        for key in (name.split(':')[0], 'total'):
            row = counts.setdefault(key, {})
            row[verdict] = row.get(verdict, 0) + 1
        if verdict in ('WRONG', 'nonreal', 'WRONG (mathematica)'):
            findings.append(result)
    print()
    for key, row in counts.items():
        print("%-16s %s" % (key, dict(sorted(row.items()))))
    if findings:
        print("\nwrong and nonreal results:")
        for result in sorted(findings, key=lambda r: str(r['id'])):
            entry = by_name.get(str(result['id']))
            print("  %s  %s" % (result['id'], result['verdict']))
            if entry is not None:
                print("      integrand  %s" % entry.integrand)
                print("      result     %s" % str(result.get('result'))[:300])
                if entry.recorded is not None:
                    print("      reference  %s" % str(entry.recorded)[:300])
                elif references.get(str(result['id'])):
                    print("      reference (mathematica)  %s" % references[str(result['id'])][:300])
    total = counts.get('total', {})
    return 1 if total.get('WRONG') or total.get('WRONG (mathematica)') else 0


if __name__ == '__main__':
    sys.exit(main())
