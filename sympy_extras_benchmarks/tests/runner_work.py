"""A ``work`` function for the tests of :mod:`sympy_extras_benchmarks.runner`."""
from __future__ import annotations

import os
import time

from sympy_extras_benchmarks.runner import Result, Task


def work(task: Task) -> Result:
    """Square ``n``; sleep for ``sleep`` seconds; die when ``die`` is set."""
    if task.get('die'):
        os._exit(3)
    sleep = task.get('sleep')
    if isinstance(sleep, (int, float)):
        time.sleep(sleep)
    if task.get('fail'):
        raise KeyError('broken')
    if task.get('opaque'):
        return {'square': object()}
    if task.get('exhaust'):
        raise MemoryError
    n = task['n']
    assert isinstance(n, int)
    return {'square': n*n}
