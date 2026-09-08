from __future__ import annotations

from sympy import groebner, QQ, Poly

from sympy_extras.polys.ideals import Ideal

from sympy_extras_benchmarks.datasets.polynomial_systems import katsura, cyclic, SYSTEMS


def test_katsura() -> None:
    eqs, us = katsura(2)
    assert len(eqs) == 3 and len(us) == 3
    for m in (2, 3):
        eqs, us = katsura(m)
        G = groebner(eqs, *us, order='lex', domain=QQ)
        assert G.is_zero_dimensional
        # the last polynomial is univariate of degree 2**m (the systems are radical)
        assert Poly(G.exprs[-1], us[-1]).degree() == 2**m


def test_cyclic() -> None:
    eqs, xs = cyclic(3)
    assert len(eqs) == 3
    G = groebner(eqs, *xs, order='lex', domain=QQ)
    assert G.is_zero_dimensional
    # the six solutions are the permutations of the cube roots of unity
    assert Poly(G.exprs[-1], xs[-1]) == Poly(xs[-1]**3 - 1, xs[-1])
    assert Ideal(eqs, *xs).vector_space_dimension() == 6
    eqs, xs = cyclic(4)
    assert not groebner(eqs, *xs, order='grevlex', domain=QQ).is_zero_dimensional


def test_systems() -> None:
    names = [s.name for s in SYSTEMS]
    assert names[:2] == ['katsura-2', 'katsura-3']
    by = {s.name: s for s in SYSTEMS}
    assert by['katsura-4'].solutions == 16
    assert by['cyclic-4'].dimension == 1 and by['cyclic-4'].solutions is None
    assert by['cyclic-5'].solutions == 70
    assert by['cyclic-6'].solutions == 156
    assert by['cyclic-7'].solutions == 924
    assert repr(by['cyclic-5']) == 'PolynomialSystem(cyclic-5, 5 equations)'
