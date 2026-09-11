"""The questions ``wolfram_check`` puts to Mathematica, built offline."""
from __future__ import annotations

from sympy import Symbol, srepr

from sympy_extras_benchmarks.drivers.wolfram_check import instance_questions, questions
from sympy_extras_benchmarks.runner import Result

x = Symbol('x')


def _result(verdict: str) -> Result:
    return {'id': 'made-up/1', 'syntax': 'tarski', 'text': '[ ex y [ y^2 = x ] ]',
            'verdict': verdict, 'result_srepr': srepr(x >= 0)}


def test_equivalence_question() -> None:
    asked = questions(_result('eliminated'))
    assert len(asked) == 1 and asked[0].kind == 'equivalent' and asked[0].confirming is True
    assert asked[0].expression.startswith('Resolve[ForAll[{sympyx}, Equivalent[')


def test_no_question_for_a_confirmed_answer() -> None:
    assert questions(_result('ok')) == []


def test_instances() -> None:
    asked = instance_questions(_result('eliminated'), points=8)
    assert len(asked) == 8
    for question in asked:
        value = question.kind.split('=')[1]
        # the result x >= 0 at the point is what Mathematica must answer
        assert question.confirming == (not value.startswith('-') or value == '0')
        assert question.expression.startswith('Resolve[Exists[{sympyy}, ')
