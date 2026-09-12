"""A ``work`` function for the tests of :mod:`sympy_extras_benchmarks.runner`."""
from __future__ import annotations

import os
import pathlib
import time

from sympy_extras_benchmarks.runner import Result, Task


def work(task: Task) -> Result:
    """Square ``n``; sleep for ``sleep`` seconds; die when ``die`` is set."""
    if task.get('die'):
        os._exit(3)
    if task.get('signal'):
        # killed from outside the first time, fine when it comes back
        marker = pathlib.Path(str(task['signal']))
        if not marker.exists():
            marker.write_text('once')
            os.kill(os.getpid(), 15)
    sleep = task.get('sleep')
    if isinstance(sleep, (int, float)):
        time.sleep(sleep)
    if task.get('fail'):
        raise KeyError('broken')
    if task.get('exhaust'):
        raise MemoryError
    n = task['n']
    assert isinstance(n, int)
    return {'square': n*n}
