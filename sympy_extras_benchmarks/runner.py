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
import faulthandler
import importlib
import json
import os
import pathlib
import resource
import selectors
import signal
import subprocess
import sys
import time
import traceback
from types import FrameType, FunctionType
from typing import IO, Callable, Iterable, Optional, Union

__all__ = ['JSON', 'Task', 'Result', 'run', 'load_results']

JSON = Union[None, bool, int, float, str, list['JSON'], dict[str, 'JSON']]

#: the exit code of a worker which ran out of memory between tasks
MEMORY_EXIT = 75
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


def memory_stall() -> Optional[float]:
    """The seconds, since boot, during which every non-idle task of the
    machine was stalled waiting for memory (the ``full`` line of
    ``/proc/pressure/memory``); ``None`` where Linux does not report it.

    The difference over a task tells a worker killed because the machine
    was thrashing from one whose computation overran its time limit: a
    swapped-out process cannot run its alarm handler either.
    """
    try:
        text = pathlib.Path('/proc/pressure/memory').read_text()
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith('full'):
            for field in line.split():
                if field.startswith('total='):
                    return int(field[len('total='):])/1e6
    return None


def signal_state(pid: int) -> dict[str, JSON]:
    """What the kernel says about a process: which signals it blocks,
    ignores and catches, its state and its CPU time.

    A worker which does not answer SIGUSR1 and outruns its alarm may have
    the signals blocked (``SigBlk``), or may not be running at all. Reading
    this from ``/proc`` needs nothing of the worker itself.
    """
    state: dict[str, JSON] = {}
    try:
        for line in pathlib.Path('/proc/%d/status' % pid).read_text().splitlines():
            name, _, value = line.partition(':')
            if name in ('State', 'SigBlk', 'SigIgn', 'SigCgt', 'Threads', 'VmRSS'):
                state[name] = value.strip()
        fields = pathlib.Path('/proc/%d/stat' % pid).read_text().rsplit(') ', 1)[-1].split()
        ticks = os.sysconf('SC_CLK_TCK')
        state['cpu_seconds'] = round((int(fields[11]) + int(fields[12]))/ticks, 2)
    except (OSError, IndexError, ValueError):
        return state
    return state


class _Worker:
    """One worker process and the task it is running."""

    def __init__(self, module: str, memory: int, log: pathlib.Path) -> None:
        self.log = open(log, 'a')
        self.process = subprocess.Popen(
            [sys.executable, '-m', 'sympy_extras_benchmarks.runner', '--worker', module, '--memory', str(memory)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.log, text=True, bufsize=1)
        self.task: Optional[Task] = None
        self.started = 0.0
        self.stall_at_start: Optional[float] = None
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
        self.stall_at_start = memory_stall()
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
    #: the tasks already given a second chance after a worker was killed
    retried: set[str] = set()
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
                    retire(worker)
                    if code < 0 and str(task['id']) not in retried:
                        # something outside killed the worker (the out-of-memory
                        # killer of the machine, a stop signal): the problem is
                        # not at fault, so it goes back in the queue once
                        retried.add(str(task['id']))
                        pending.append(task)
                        feed(spawn())
                        continue
                    record({'id': task['id'], 'verdict': 'memory' if code == MEMORY_EXIT else 'died', 'exit': code,
                            'time': round(time.monotonic() - worker.started, 2)})
                    feed(spawn())
                    continue
                result: Result = json.loads(line)
                result['id'] = task['id']
                result.setdefault('time', round(time.monotonic() - worker.started, 2))
                record(result)
                worker.done += 1
                if (worker.done >= recycle or result.get('verdict') == 'memory') and pending:
                    retire(worker)
                    worker = spawn()
                feed(worker)
            now = time.monotonic()
            for worker in list(pool):
                task = worker.task
                if task is not None and now - worker.started > deadline:
                    if worker.process.poll() is None:
                        worker.process.send_signal(signal.SIGUSR1)
                        time.sleep(1.0)
                    killed: Result = {'id': task['id'], 'verdict': 'killed', 'time': round(now - worker.started, 2)}
                    killed['signals'] = signal_state(worker.process.pid)
                    stall = memory_stall()
                    if stall is not None and worker.stall_at_start is not None:
                        killed['memory_stall'] = round(stall - worker.stall_at_start, 2)
                    record(killed)
                    retire(worker)
                    feed(spawn())
        for worker in list(pool):
            retire(worker)
    return load_results(output)


def _report_state(signum: int, frame: Optional[FrameType]) -> None:
    """Write where the worker is and the state of its alarm timer to its log
    (the parent asks for it before killing a worker at the deadline)."""
    remaining, interval = signal.getitimer(signal.ITIMER_REAL)
    handler = signal.getsignal(signal.SIGALRM)
    name = handler.__qualname__ if isinstance(handler, FunctionType) else repr(handler)
    lines = ['STATE alarm timer: %.3f s left (interval %.3f); SIGALRM handler: %s' % (remaining, interval, name)]
    lines.extend('STATE ' + line.rstrip() for entry in traceback.format_stack(frame)[-40:]
                 for line in entry.splitlines())
    sys.stderr.write('\n'.join(lines) + '\n')
    sys.stderr.flush()


def _serve(module_name: str, memory: int) -> int:
    """The loop of a worker: one task per line in, one result per line out."""
    signal.signal(signal.SIGUSR1, _report_state)
    # the Python handler above only runs between bytecodes; a worker stuck
    # in one long C call (a huge integer operation) still dumps its stack
    # from faulthandler's C-level handler, which then chains to it
    faulthandler.register(signal.SIGUSR1, file=sys.stderr, all_threads=False, chain=True)
    if memory > 0:
        limit = memory*2**20
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    channel = os.fdopen(os.dup(1), 'w')
    os.dup2(2, 1)
    module = importlib.import_module(module_name)
    work: Callable[[Task], Result] = module.work
    from sympy.core.cache import clear_cache
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                return 0
            task: Task = json.loads(line)
        except MemoryError:
            return MEMORY_EXIT
        exhausted = False
        try:
            result = work(task)
            # what the check left behind is released before the next task
            clear_cache()
            answer = json.dumps(result, default=str)
        except MemoryError:
            # also when it is the bookkeeping after the check that runs out:
            # a worker near its cap is replaced by a fresh one
            answer = json.dumps({'id': task['id'], 'verdict': 'memory'})
            exhausted = True
        except Exception as error:
            # the worker must outlive whatever one problem does
            answer = json.dumps({'id': task['id'], 'verdict': 'crash',
                                 'error': '%s: %s' % (type(error).__name__, str(error)[:300]),
                                 'traceback': traceback.format_exc()[-3000:]})
        channel.write(answer + '\n')
        channel.flush()
        if exhausted:
            return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="worker process of sympy_extras_benchmarks.runner")
    parser.add_argument('--worker', required=True)
    parser.add_argument('--memory', type=int, default=0)
    args = parser.parse_args(argv)
    return _serve(args.worker, args.memory)


if __name__ == '__main__':
    sys.exit(main())
