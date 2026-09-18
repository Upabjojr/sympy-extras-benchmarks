"""The reader of Maxima's contrib_ode test files on samples written here in
their layout (no network, nothing copied from Maxima)."""
from __future__ import annotations

from sympy import Symbol, Function, Derivative

from sympy_extras_benchmarks.datasets.maxima_ode import parse_file, ODEEntry
from sympy_extras_benchmarks.parsers.maxima import x, y

a, b, c, n = Symbol('a'), Symbol('b'), Symbol('c'), Symbol('n')
f = Function('f')


SAMPLE = """
(load("contrib_ode"),0);
0$

/* a sample in the layout of Maxima's files; the equations are our own */
(pn_(n_):=print("Sample ODE 1.",n_),true);
true;

/* 1 */
(pn_(1),ans:contrib_ode(eqn:'diff(y,x)+a*y-b,y,x));
[y = b/a+%c*%e^-(a*x)];
[method,ode_check(eqn,ans[1])];
[linear,0];

/* 2 */
(pn_(2),ans:contrib_ode(eqn:'diff(y,x)^2+y*'diff(y,x)=x*(x+y),y,x),0);
[y = x^2/2+%c, y = %c*%e^-x-x+1];
[method,ode_check(eqn,ans[1])];
[factor,0];

/* 3: two equations under one number */
(pn_(3),ans:contrib_ode(eqn:'diff(y,x)=f(x),y,x));
[y = 'integrate(f(x),x)+%c];
[method,ode_check(eqn,ans[1])];
[linear,0];
(pn_(3),ans:contrib_ode(eqn:'diff(y,x)=g(x)*y,y,x));
false;

/* 4: a reference the parser cannot follow */
(pn_(4),ans:contrib_ode(eqn:ode[4],y,x));
false;

/* 5: an algebraic equation is not an ODE */
(pn_(5),ans:contrib_ode(eqn:y^2-x,y,x));
false;

/* 6 */
(pn_( 6 ),ans:contrib_ode(eqn:x^2*'diff(y,x,2)+x*'diff(y,x)+(x^2-n^2)*y,y,x));
[y = %k1*bessel_j(n,x)+%k2*bessel_y(n,x)];
[method,ode_check(eqn,ans[1])];
[bessel,0];
"""


def test_parse_file() -> None:
    entries, skipped = parse_file(SAMPLE, 'sample')
    assert [e.name for e in entries] == ['sample.1', 'sample.2', 'sample.3', 'sample.3b', 'sample.6']
    assert [e.number for e in entries] == [1, 2, 3, 3, 6]
    assert [e.order for e in entries] == [1, 1, 1, 1, 2]
    assert [e.method for e in entries] == ['linear', 'factor', 'linear', '', 'bessel']
    assert skipped == [('4', 'ode[4]'), ('5', 'y^2-x')]
    first = entries[0]
    assert isinstance(first, ODEEntry)
    assert first.equation == Derivative(y(x), x) + a*y(x) - b
    assert first.source == "'diff(y,x)+a*y-b"
    assert first.parameters == [a, b]
    assert first.arbitrary_functions == []
    assert first.function == y(x) and first.variable == x
    second = entries[1]
    assert second.equation == Derivative(y(x), x)**2 + y(x)*Derivative(y(x), x) - x*(x + y(x))
    assert entries[2].arbitrary_functions == [f]
    assert entries[3].arbitrary_functions == [Function('g')]
    bessel = entries[4]
    assert bessel.equation == x**2*Derivative(y(x), (x, 2)) + x*Derivative(y(x), x) + (x**2 - n**2)*y(x)
    assert bessel.parameters == [n]
    assert bessel.collection == 'sample'
    assert repr(bessel).startswith('ODEEntry(sample.6, ')


def test_parse_file_other_variables() -> None:
    text = "(pn_(1),ans:contrib_ode(eqn:'diff(u,t)=c*u,u,t));\n[u = %c*%e^(c*t)];\n"
    entries, skipped = parse_file(text, 't')
    assert skipped == []
    assert entries[0].equation == Derivative(y(x), x) - c*y(x)
