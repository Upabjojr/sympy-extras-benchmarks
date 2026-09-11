"""Run a benchmark over many problems in parallel worker processes.

A driver describes each problem as a *task*, a JSON object with an
``id``, and names a module whose ``work(task) -> result`` function checks
one problem. :func:`run` hands the tasks to long-lived worker processes,
each running ``work`` in its main thread (the time limits of
:mod:`sympy_extras._timeout` rely on ``SIGALRM``, which only the main
thread receives) under a cap on its address space. The parent

* kills a worker which overruns the hard deadline of a task -- a
  computation stuck where the alarm cannot interrupt it -- and records the
  task as ``killed``;
* records a task whose worker died (a crash in C code, the address space
  cap enforced by the kernel) as ``died``;
* restarts the worker in both cases, and every ``recycle`` tasks anyway so
  that the caches of SymPy do not grow without bound;
* appends every result to a JSON Lines file as it arrives, so that an
  interrupted run resumes where it stopped (the tasks whose ``id`` is
  already in the file are skipped).

A worker reports its answers on a private copy of its standard output;
whatever the computation itself prints goes to the worker's log instead.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import pathlib
import resource
import selectors
import subprocess
import sys
import time
import traceback
from typing import IO, Callable, Iterable, Optional, Union

__all__ = ['JSON', 'Task', 'Result', 'run', 'load_results']

JSON = Union[None, bool, int, float, str, list['JSON'], dict[str, 'JSON']]
Task = dict[str, JSON]
Result = dict[str, JSON]


def load_results(output: pathlib.Path) -> list[Result]:
    """The results already written to ``output`` (a truncated last line,
    left by an interrupted run, is ignored)."""
    results: list[Result] = []
    if not output.exists():
        return results
    for line in output.read_text().splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and 'id' in value:
            results.append(value)
    return results


class _Worker:
    """One worker process and the task it is running."""

    def __init__(self, module: str, memory: int, log: pathlib.Path) -> None:
        self.log = open(log, 'a')
        self.process = subprocess.Popen(
            [sys.executable, '-m', 'sympy_extras_benchmarks.runner', '--worker', module, '--memory', str(memory)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log, text=True, bufsize=1)
        self.task: Optional[Task] = None
        self.started = 0.0
        self.done = 0

    @property
    def stdout(self) -> IO[str]:
        stream = self.process.stdout
        assert stream is not None
        return stream

    def send(self, task: Task) -> None:
        stream = self.process.stdin
        assert stream is not None
        self.task = task
        self.started = time.monotonic()
        stream.write(json.dumps(task) + '\n')
        stream.flush()

    def stop(self) -> None:
        if self.process.poll() is None:
            self.process.kill()
        self.process.wait()
        self.log.close()


def run(tasks: Iterable[Task], module: str, output: pathlib.Path, workers: int = 4,
        deadline: float = 300.0, memory: int = 2048, recycle: int = 100,
        report: Optional[Callable[[Result], None]] = None) -> list[Result]:
    """Run ``module.work`` on every task not yet in ``output``.

    ``deadline`` is the hard limit in seconds on one task (the time limits
    inside ``work`` should be well below it), ``memory`` the cap in
    megabytes on the address space of a worker. ``report`` is called with
    every new result. Returns all the results in ``output``, old and new.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.stat().st_size and not output.read_bytes().endswith(b'\n'):
        # a run killed while writing left half a line: end it, so that the
        # next result starts a line of its own instead of being glued to it
        with open(output, 'a') as sink:
            sink.write('\n')
    done = {str(r['id']) for r in load_results(output)}
    pending = [t for t in tasks if str(t['id']) not in done]
    pending.reverse()
    logs = output.with_suffix('.workers.log')
    selector = selectors.DefaultSelector()
    pool: list[_Worker] = []

    def spawn() -> _Worker:
        worker = _Worker(module, memory, logs)
        selector.register(worker.stdout, selectors.EVENT_READ, worker)
        pool.append(worker)
        return worker

    def retire(worker: _Worker) -> None:
        selector.unregister(worker.stdout)
        pool.remove(worker)
        worker.stop()

    with open(output, 'a') as sink:
        def record(result: Result) -> None:
            sink.write(json.dumps(result) + '\n')
            sink.flush()
            if report is not None:
                report(result)

        def feed(worker: _Worker) -> None:
            if pending:
                worker.send(pending.pop())
            else:
                worker.task = None

        for _ in range(min(workers, len(pending))):
            feed(spawn())
        while any(w.task is not None for w in pool):
            for key, _ in selector.select(timeout=1.0):
                worker = key.data
                assert isinstance(worker, _Worker)
                task = worker.task
                line = worker.stdout.readline()
                if task is None:
                    continue
                if not line:
                    code = worker.process.wait()
                    record({'id': task['id'], 'verdict': 'died', 'exit': code,
                            'time': round(time.monotonic() - worker.started, 2)})
                    retire(worker)
                    feed(spawn())
                    continue
                result: Result = json.loads(line)
                result['id'] = task['id']
                result.setdefault('time', round(time.monotonic() - worker.started, 2))
                record(result)
                worker.done += 1
                if worker.done >= recycle and pending:
                    retire(worker)
                    worker = spawn()
                feed(worker)
            now = time.monotonic()
            for worker in list(pool):
                task = worker.task
                if task is not None and now - worker.started > deadline:
                    record({'id': task['id'], 'verdict': 'killed', 'time': round(now - worker.started, 2)})
                    retire(worker)
                    feed(spawn())
        for worker in list(pool):
            retire(worker)
    return load_results(output)


def _serve(module_name: str, memory: int) -> int:
    """The loop of a worker: one task per line in, one result per line out."""
    if memory > 0:
        limit = memory*2**20
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    channel = os.fdopen(os.dup(1), 'w')
    os.dup2(2, 1)
    module = importlib.import_module(module_name)
    work: Callable[[Task], Result] = module.work
    from sympy.core.cache import clear_cache
    for line in sys.stdin:
        task: Task = json.loads(line)
        try:
            result = work(task)
        except MemoryError:
            result = {'verdict': 'memory'}
        except Exception as error:
            # the worker must outlive whatever one problem does
            result = {'verdict': 'crash', 'error': '%s: %s' % (type(error).__name__, str(error)[:300]),
                      'traceback': traceback.format_exc()[-3000:]}
        result['id'] = task['id']
        channel.write(json.dumps(result) + '\n')
        channel.flush()
        clear_cache()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="worker process of sympy_extras_benchmarks.runner")
    parser.add_argument('--worker', required=True)
    parser.add_argument('--memory', type=int, default=0)
    args = parser.parse_args(argv)
    return _serve(args.worker, args.memory)


if __name__ == '__main__':
    sys.exit(main())
