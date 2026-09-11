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


def test_resume_after_a_half_written_line(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    output.write_text('{"id": "n0", "square": 0}\n{"id": "n1", "squ')
    results = run([{'id': 'n%d' % n, 'n': n} for n in range(3)], MODULE, output, workers=1, deadline=60, memory=0)
    assert sorted(str(r['id']) for r in results) == ['n0', 'n1', 'n2']


def test_memory(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    tasks: list[Task] = [{'id': 'exhaust', 'n': 1, 'exhaust': True}, {'id': 'after', 'n': 4}]
    results = {str(r['id']): r for r in run(tasks, MODULE, output, workers=1, deadline=60, memory=0)}
    # the worker which ran out of memory reports it and is replaced
    assert results['exhaust']['verdict'] == 'memory'
    assert results['after']['square'] == 16


def test_state_of_a_killed_worker(tmp_path: pathlib.Path) -> None:
    output = tmp_path / 'results.jsonl'
    run([{'id': 'stuck', 'n': 1, 'sleep': 30}], MODULE, output, workers=1, deadline=2, memory=0)
    log = output.with_suffix('.workers.log').read_text()
    assert 'STATE alarm timer:' in log
    assert 'runner_work.py' in log
    # the C-level dump of faulthandler as well
    assert 'Current thread' in log or 'Stack (most recent call first)' in log
