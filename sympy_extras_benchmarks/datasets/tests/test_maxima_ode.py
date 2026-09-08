"""The Maxima parser on samples written here in the syntax of the test
files (no network, nothing copied from Maxima)."""
from __future__ import annotations

from sympy import (Symbol, Function, Derivative, E, pi, I, Rational, sin, cos,
    exp, log, sqrt, besselj, legendre, factorial, Abs, atan)
from sympy.testing.pytest import raises

from sympy_extras_benchmarks.datasets.maxima_ode import (tokenize, parse_expression,
    parse_equation, parse_file, derivative_order, MaximaSyntaxError, ODEEntry, x, y)

a, b, c, n = Symbol('a'), Symbol('b'), Symbol('c'), Symbol('n')
f = Function('f')


def test_tokenize() -> None:
    assert tokenize("a+2") == [('name', 'a'), ('op', '+'), ('number', '2')]
    assert tokenize("%e^-x") == [('name', '%e'), ('op', '^'), ('op', '-'), ('name', 'x')]
    assert tokenize("1.5e-3*x**2") == [('number', '1.5e-3'), ('op', '*'), ('name', 'x'),
                                       ('op', '**'), ('number', '2')]
    assert tokenize("'diff(y,x,2)")[0] == ('op', "'")
    raises(MaximaSyntaxError, lambda: tokenize("a $ b"))


def test_arithmetic_and_precedence() -> None:
    assert parse_expression("a+b*c") == a + b*c
    assert parse_expression("a-b-c") == a - b - c
    assert parse_expression("a/b/c") == a/b/c
    assert parse_expression("-x^2") == -x**2
    assert parse_expression("2^-x") == 2**(-x)
    assert parse_expression("a^b^c") == a**(b**c)
    assert parse_expression("(a+b)^2") == (a + b)**2
    assert parse_expression("x**3") == x**3
    assert parse_expression("n!") == factorial(n)
    assert parse_expression("1/2") == Rational(1, 2)
    assert parse_expression("0.25*x") == x/4
    assert parse_expression("+a") == a


def test_constants_and_functions() -> None:
    assert parse_expression("%e^x") == exp(x)
    assert parse_expression("%pi*%i") == pi*I
    assert parse_expression("%e") == E
    assert parse_expression("sin(x)+cos(x)") == sin(x) + cos(x)
    assert parse_expression("log(x)*sqrt(x)") == log(x)*sqrt(x)
    assert parse_expression("bessel_j(n,x)") == besselj(n, x)
    assert parse_expression("legendre_p(n,x)") == legendre(n, x)
    assert parse_expression("abs(x)") == Abs(x)
    assert parse_expression("arctan(x)") == atan(x)
    assert parse_expression("f(x)") == f(x)
    assert parse_expression("lambda*x") == Symbol('lambda')*x
    assert parse_expression("gamma") == Symbol('gamma')
    raises(MaximaSyntaxError, lambda: parse_expression("sin(x, y)"))
    raises(MaximaSyntaxError, lambda: parse_expression("%pi(x)"))


def test_dependent_variable_and_derivatives() -> None:
    assert parse_expression("y") == y(x)
    assert parse_expression("'diff(y,x)") == Derivative(y(x), x)
    assert parse_expression("'diff(y,x,2)") == Derivative(y(x), (x, 2))
    assert parse_expression("'diff(y,x,1)") == Derivative(y(x), x)
    assert parse_expression("diff(y,x)") == Derivative(y(x), x)
    assert parse_expression("'diff(y,x)^2") == Derivative(y(x), x)**2
    # the verb form of a known function is evaluated
    assert parse_expression("diff(x^3,x)") == 3*x**2
    # another pair of variables
    u, t = Function('u'), Symbol('t')
    assert parse_expression("'diff(u,t,2)+u", 'u', 't') == Derivative(u(t), (t, 2)) + u(t)
    raises(MaximaSyntaxError, lambda: parse_expression("'diff(y)"))
    raises(MaximaSyntaxError, lambda: parse_expression("'x"))


def test_equations() -> None:
    assert parse_expression("'diff(y,x)=a*y") == Derivative(y(x), x) - a*y(x)
    assert parse_equation("(y+1)*'diff(y,x)=y+x") == (y(x) + 1)*Derivative(y(x), x) - y(x) - x
    assert parse_equation("4*'diff(y,x)^2=9*x") == 4*Derivative(y(x), x)**2 - 9*x
    raises(MaximaSyntaxError, lambda: parse_equation("a*x+b"))
    raises(MaximaSyntaxError, lambda: parse_equation("'diff(y,x)+"))
    raises(MaximaSyntaxError, lambda: parse_equation("'diff(y,x) x"))
    raises(MaximaSyntaxError, lambda: parse_equation("ode[3]"))


def test_derivative_order() -> None:
    assert derivative_order(Derivative(y(x), (x, 3)) + Derivative(y(x), x), y(x)) == 3
    assert derivative_order(y(x) + x, y(x)) == 0
    assert derivative_order(Derivative(f(x), x), y(x)) == 0


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
