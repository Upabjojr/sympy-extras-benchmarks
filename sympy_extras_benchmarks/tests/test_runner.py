"""The parallel runner: results, resumption, crashes, dead and stuck workers."""
from __future__ import annotations

import pathlib

from sympy_extras_benchmarks.runner import Task, load_results, run

MODULE = 'sympy_extras_benchmarks.tests.runner_work'


def test_run_and_resume(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    tasks: list[Task] = [{'id': 'n%d' % n, 'n': n} for n in range(6)]
    results = run(tasks[:4], MODULE, output, workers=2, deadline=60, memory=0)
    assert sorted((r['id'], r['square']) for r in results) == [('n0', 0), ('n1', 1), ('n2', 4), ('n3', 9)]
    seen: list[str] = []
    results = run(tasks, MODULE, output, workers=2, deadline=60, memory=0,
                  report=lambda r: seen.append(str(r['id'])))
    assert sorted(seen) == ['n4', 'n5']
    assert len(load_results(output)) == 6


def test_failures(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    tasks: list[Task] = [{'id': 'crash', 'n': 1, 'fail': True}, {'id': 'dead', 'n': 1, 'die': True},
                         {'id': 'stuck', 'n': 1, 'sleep': 30}, {'id': 'fine', 'n': 3}]
    results = {str(r['id']): r for r in run(tasks, MODULE, output, workers=2, deadline=3, memory=0)}
    assert results['crash']['verdict'] == 'crash' and 'KeyError' in str(results['crash']['error'])
    assert results['dead']['verdict'] == 'died' and results['dead']['exit'] == 3
    assert results['stuck']['verdict'] == 'killed'
    assert results['fine']['square'] == 9


def test_truncated_line(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    output.write_text('{"id": "a", "v": 1}\n{"id": "b", "v"')
    assert [r['id'] for r in load_results(output)] == ['a']
