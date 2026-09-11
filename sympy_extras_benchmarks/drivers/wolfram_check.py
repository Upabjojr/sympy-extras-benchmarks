"""Settle with Mathematica the answers of sympy-extras that no recorded
answer confirms, and the ones that contradict a recorded answer.

Usage::

    python -m sympy_extras_benchmarks wolfram_check --results results/X.jsonl
        --wolfram "ssh host 'cat > /tmp/o.wl && wolframscript -file /tmp/o.wl'"
        [--timeout S] [--limit N] [--output results/X.wolfram.jsonl]

It reads the results of ``smtlib_release`` or ``cad_examples`` and picks

* an ``unsat`` answer to a problem without a recorded status (``unknown``
  in SMT-LIB, a disjunct of a satisfiable problem in the Brown data, an
  ISSAC conjunction): ``Resolve[Exists[vars, F], Reals]`` must be
  ``False``. A ``sat`` answer is not checked: its model was verified by
  exact evaluation;
* a ``WRONG`` or ``DISAGREES`` verdict: the problem is decided again by
  Mathematica, which tells a mistake of sympy-extras from a mistake of the
  recorded answer (or of the parser);
* a closed problem decided without a recorded answer: ``Resolve[F]`` must
  give the same truth value;
* a quantifier-free result without a recorded answer (and every
  disagreeing one): ``Resolve[ForAll[free, A ==> (R <=> F)], Reals]``,
  with ``A`` the assumptions of the problem, must be ``True``.

One line per checked result goes to the output, with Mathematica's answer
and whether it confirms the one of sympy-extras (``null`` when Mathematica
did not decide). A run resumes from its output.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Optional

from sympy import Symbol, sympify, true, false
from sympy.core.basic import Basic
from sympy.logic.boolalg import Boolean, Equivalent, Implies

from sympy_extras.assumptions import Exists, ForAll
from sympy_extras._typing import as_boolean

from sympy_extras_benchmarks.datasets import smtlib, solver_regressions, tarski_tests
from sympy_extras_benchmarks.datasets.qepcad_syntax import QEPCADSyntaxError
from sympy_extras_benchmarks.datasets.smtlib_release import fetch as fetch_release
from sympy_extras_benchmarks.drivers.cad_examples import problem
from sympy_extras_benchmarks.oracles.wolfram import Wolfram, WolframError, to_wolfram
from sympy_extras_benchmarks.runner import Result, load_results

#: the verdicts of ``smtlib_release`` that are checked, per checked function
_SMT_KEYS = ('satisfiable', 'resolve', 'simplify', 'refine')


class Question:
    """A question put to Mathematica: the Wolfram Language expression, and
    the answer which confirms sympy-extras."""

    def __init__(self, identifier: str, kind: str, expression: str, confirming: bool) -> None:
        self.identifier = identifier
        self.kind = kind
        self.expression = expression
        self.confirming = confirming


def _smt_problem(identifier: str) -> Optional[tuple[Boolean, list[Symbol], str]]:
    """The formula, the variables and the recorded status of an SMT-LIB
    problem of a result of ``smtlib_release``."""
    if identifier.startswith('brown-r'):
        round_ = int(identifier[len('brown-r')])
        name = identifier.split('/', 1)[1]
        root = tarski_tests.fetch()
        if root is None:
            return None
        path = root / 'tests' / 'dataset-Brown-V-E-2019' / ('smtlib-r%d' % round_) / name
        logic = 'QF_NRA'
    else:
        logic = identifier.split('/', 1)[0]
        directory = fetch_release(logic)
        if directory is None:
            return None
        path = directory.parent / identifier
    text = path.read_text(errors='replace')
    if logic == 'QF_NRA':
        parsed = smtlib.translate(text, path.stem)
        if parsed is None:
            return None
        return parsed.formula, list(parsed.variables), parsed.status
    arith = solver_regressions.translate(text, path.stem)
    if arith is None:
        return None
    return arith.formula, list(arith.variables), arith.status


def instance_questions(result: Result, points: int = 6) -> list[Question]:
    """When the equivalence of a quantifier-free result with its problem is
    too hard for Mathematica, decide the problem at a few random rational
    values of the free variables instead: at each, Mathematica's truth
    value of the closed instance must be the value of the result there,
    which is evaluated exactly here. This cannot prove the equivalence, but
    one disagreement disproves it."""
    import random
    from sympy import Rational
    from sympy_extras_benchmarks.drivers.smtlib_release import evaluate
    formula, free, assumptions = problem(str(result['syntax']), str(result['text']))
    ours = sympify(str(result['result_srepr']))
    if not isinstance(ours, Boolean) or not free:
        return []
    rng = random.Random(str(result['id']))
    asked: list[Question] = []
    tries = 0
    while len(asked) < points and tries < 50*points:
        tries += 1
        point: dict[Basic, Basic] = {v: Rational(rng.randint(-12, 12), rng.randint(1, 4)) for v in free}
        if assumptions is not None and evaluate(assumptions, point) is not True:
            continue
        value = evaluate(ours, point)
        if value is None:
            continue
        instance = as_boolean(formula.xreplace(point))
        label = ','.join('%s=%s' % (k, v) for k, v in point.items())
        asked.append(Question(str(result['id']), 'instance ' + label, "Resolve[%s, Reals]" % to_wolfram(instance), value))
    return asked


def questions(result: Result) -> list[Question]:
    """What to ask Mathematica about one result."""
    identifier = str(result['id'])
    asked: list[Question] = []
    if 'syntax' in result:
        verdict = str(result.get('verdict', ''))
        needs = (verdict.startswith('decided') or verdict.startswith('eliminated') or 'DISAGREES' in verdict
                 or verdict.startswith('unsat') or 'WRONG' in verdict)
        if not needs:
            return asked
        try:
            formula, free, assumptions = problem(str(result['syntax']), str(result['text']))
        except QEPCADSyntaxError:
            return asked
        if verdict.startswith('unsat') or 'model does not' in verdict:
            closed = as_boolean(Exists(free, formula)) if free else formula
            asked.append(Question(identifier, 'satisfiable', "Resolve[%s, Reals]" % to_wolfram(closed),
                                  verdict.startswith('unsat') is False))
            if verdict.startswith('unsat'):
                asked[-1].confirming = False
            return asked
        ours = sympify(str(result['result_srepr']))
        if not isinstance(ours, Boolean):
            return asked
        if not free or ours in (true, false) and not free:
            asked.append(Question(identifier, 'decide', "Resolve[%s, Reals]" % to_wolfram(formula), ours is true))
            return asked
        claim: Boolean = as_boolean(Equivalent(ours, formula))
        if assumptions is not None:
            claim = as_boolean(Implies(assumptions, claim))
        asked.append(Question(identifier, 'equivalent', "Resolve[%s, Reals]" % to_wolfram(ForAll(free, claim)), True))
        return asked
    for key in _SMT_KEYS:
        verdict = str(result.get(key, ''))
        unknown = result.get('status') == 'unknown' or result.get('source_status') not in (None, 'unsat')
        if not ('WRONG' in verdict or (verdict.startswith('unsat') and unknown)):
            continue
        parsed = _smt_problem(identifier)
        if parsed is None:
            return asked
        formula, variables, _ = parsed
        closed = as_boolean(Exists(variables, formula)) if variables else formula
        # sympy-extras said "no solution" unless its verdict was a
        # (claimed) solution, or True/False from simplify/refine
        ours_sat = ('model' in verdict or 'sat for' in verdict or 'True for' in verdict) and 'unsat for' not in verdict
        asked.append(Question(identifier, 'satisfiable:' + key, "Resolve[%s, Reals]" % to_wolfram(closed), ours_sat))
        break
    return asked


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True)
    parser.add_argument('--wolfram', required=True)
    parser.add_argument('--timeout', type=float, default=120.0)
    parser.add_argument('--chunk', type=int, default=10)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--instances', action='store_true',
                        help='for the equivalences Mathematica left undecided, check random instances instead')
    parser.add_argument('--output', default='')
    args = parser.parse_args(argv)
    source = pathlib.Path(args.results)
    output = pathlib.Path(args.output or str(source).replace('.jsonl', '.wolfram.jsonl'))
    earlier = load_results(output)
    done = {str(r['id']) for r in earlier}
    pending: list[Question] = []
    if args.instances:
        undecided = {str(r['id']) for r in earlier if r.get('kind') == 'equivalent' and r.get('agrees') is None}
        undecided -= {str(r['id']) for r in earlier if str(r.get('kind', '')).startswith('instance')}
        for result in load_results(source):
            if str(result['id']) in undecided:
                try:
                    pending.extend(instance_questions(result))
                except (WolframError, ValueError, TypeError, SyntaxError, QEPCADSyntaxError) as error:
                    print("%s: no instances (%s)" % (result['id'], error))
        done = {str(r['id']) for r in load_results(source)}
    for result in load_results(source):
        if str(result['id']) in done:
            continue
        try:
            pending.extend(questions(result))
        except (WolframError, ValueError, TypeError, SyntaxError) as error:
            with open(output, 'a') as sink:
                sink.write(json.dumps({'id': result['id'], 'kind': 'not asked', 'error': str(error)[:300]}) + '\n')
    if args.limit:
        pending = pending[:args.limit]
    print("%d questions for Mathematica" % len(pending), flush=True)
    oracle = Wolfram(args.wolfram, args.timeout, chunk=args.chunk)
    disagreements = 0
    for start in range(0, len(pending), args.chunk):
        batch = pending[start:start + args.chunk]
        try:
            answers = oracle.evaluate([q.expression for q in batch])
        except WolframError as error:
            print("the oracle failed: %s" % error, flush=True)
            return 2
        with open(output, 'a') as sink:
            for question, answer in zip(batch, answers):
                decided = True if answer == 'True' else (False if answer == 'False' else None)
                agrees = None if decided is None else decided == question.confirming
                if agrees is False:
                    disagreements += 1
                sink.write(json.dumps({'id': question.identifier, 'kind': question.kind, 'wolfram': answer[:500],
                                       'agrees': agrees}) + '\n')
                print("%-70s %-22s %-10s agrees=%s" % (question.identifier[-70:], question.kind, answer[:10], agrees),
                      flush=True)
    print("\n%d answers of sympy-extras contradicted by Mathematica" % disagreements)
    return 1 if disagreements else 0


if __name__ == '__main__':
    sys.exit(main())
