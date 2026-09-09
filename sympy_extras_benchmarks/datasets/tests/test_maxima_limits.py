"""Tests of the Maxima limit parser on samples written here in Maxima
syntax (nothing is copied from Maxima)."""
from __future__ import annotations

from sympy import Symbol, oo, sin, zoo

from sympy_extras_benchmarks.datasets.maxima_limits import MaximaLimit, limits


def _one(text: str) -> MaximaLimit:
    found = limits(text, 'sample')
    assert len(found) == 1
    return found[0]


def test_a_limit_and_its_recorded_value() -> None:
    entry = _one("limit(7^n/8^n,n,inf);\n0$\n")
    n = Symbol('n')
    assert entry.name == 'sample:1'
    assert entry.expression == 7**n/8**n
    assert entry.variable == n
    assert entry.point == oo
    assert entry.direction == '+-'
    assert entry.recorded == 0


def test_maximas_infinities_are_translated() -> None:
    assert _one("limit(x,x,minf);\nminf$\n").point == -oo
    assert _one("limit(1/x,x,0);\ninfinity$\n").recorded == zoo


def test_a_one_sided_limit() -> None:
    assert _one("limit(1/x,x,0,plus);\ninf$\n").direction == '+'
    assert _one("limit(1/x,x,0,minus);\nminf$\n").direction == '-'


def test_und_and_ind_are_not_read_as_values() -> None:
    # Maxima's "undefined" and "indeterminate but bounded" have no single
    # SymPy counterpart
    assert _one("limit(sin(1/x),x,0);\nind$\n").recorded is None
    assert _one("limit(x,x,0);\nund$\n").recorded is None


def test_a_limit_under_an_assumption_is_refused() -> None:
    # the context would change the answer
    text = "assume(a>0);\n[a>0]$\nlimit(a*x,x,inf);\ninf$\n"
    assert limits(text, 'sample') == []


def test_an_assumption_that_was_forgotten_no_longer_blocks() -> None:
    text = "assume(a>0);\n[a>0]$\nforget(a>0);\n[a>0]$\nlimit(x,x,inf);\ninf$\n"
    assert len(limits(text, 'sample')) == 1


def test_kill_clears_the_context() -> None:
    text = "assume(a>0);\n[a>0]$\nkill(all);\ndone$\nlimit(x,x,inf);\ninf$\n"
    assert len(limits(text, 'sample')) == 1


def test_a_commented_out_call_is_skipped() -> None:
    assert limits("/* limit(x,x,inf);\ninf$ */\n", 'sample') == []


def test_a_call_without_a_variable_is_skipped() -> None:
    assert limits("limit(zeroa*inf);\nund$\n", 'sample') == []


def test_several_calls_are_numbered_in_order() -> None:
    text = "limit(x,x,inf);\ninf$\nlimit(sin(x)/x,x,0);\n1$\n"
    first, second = limits(text, 'file')
    assert (first.name, second.name) == ('file:1', 'file:2')
    assert second.expression == sin(Symbol('x'))/Symbol('x')
