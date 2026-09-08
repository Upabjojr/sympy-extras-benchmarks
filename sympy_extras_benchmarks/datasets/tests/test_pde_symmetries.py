from __future__ import annotations

from sympy_extras_benchmarks.datasets.pde_symmetries import TABLE, PDEEntry, u, x, t


def test_table() -> None:
    assert len(TABLE) == 12
    names = [e.name for e in TABLE]
    assert len(set(names)) == 12
    for entry in TABLE:
        assert isinstance(entry, PDEEntry)
        assert entry.equation.has(u)
        assert entry.equation.free_symbols >= {x, t} or entry.equation.has(t)
        assert entry.degree in (2, 3)
        assert entry.expected > 0
        assert entry.reference
    assert TABLE[-1].basis != ()
    assert repr(TABLE[0]) == 'PDEEntry(heat u_t = u_xx, dimension 6)'
