"""The Maxima parser on samples written here in Maxima's syntax (no network,
nothing copied from Maxima)."""
from __future__ import annotations

from sympy import (Symbol, Function, Derivative, E, pi, I, Rational, Integer, sin, cos,
    exp, log, sqrt, besselj, legendre, factorial, factorial2, jn, yn, uppergamma,
    Integral, Sum, Product, Abs, atan, Eq, Ne, oo)
from sympy.core.function import AppliedUndef
from sympy.testing.pytest import raises

from sympy_extras_benchmarks.parsers.maxima import (tokenize, parse_expression,
    parse_equation, derivative_order, MaximaSyntaxError, readable, relation,
    split_arguments, x, y)
from sympy_extras_benchmarks.parsers.maxima import (NO_FUNCTION as N, application,
    call_arguments, group, parse, statements, strip_comments)

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


def test_relations_of_every_kind() -> None:
    assert relation('a >= 2') == (a >= 2)
    assert relation('b - a < 1') == (b - a < 1)
    assert relation('a # b') == Ne(a, b)
    assert relation('equal(a, b)') == Eq(a, b)
    assert relation('notequal(a, 0)') == Ne(a, 0)


def test_not_a_relation() -> None:
    assert relation('a + b') is None
    # the comparison is inside a call, not at the top level
    assert relation('g(a > 0)') is None


def test_split_arguments_respects_brackets_and_strings() -> None:
    assert split_arguments('g(u, v), [1, 2], "p, q"') == ['g(u, v)', '[1, 2]', '"p, q"']


def test_readable_refuses_what_did_not_translate() -> None:
    assert readable(exp(x))
    assert not readable(Function('mystery')(x))


# ---------------------------------------------------------------------------
# numbers: the parser reads them exactly, never as floating point

def test_numbers_are_exact() -> None:
    assert parse_expression('1.5', N, N) == Rational(3, 2)
    assert parse_expression('.5', N, N) == Rational(1, 2)
    assert parse_expression('2.', N, N) == Integer(2)
    assert parse_expression('0.1+0.2', N, N) == Rational(3, 10)
    assert parse_expression('1/3', N, N) == Rational(1, 3)


def test_scientific_notation() -> None:
    assert parse_expression('1e3', N, N) == Integer(1000)
    assert parse_expression('1.5e-3', N, N) == Rational(3, 2000)
    assert parse_expression('1.0e10', N, N) == Integer(10**10)


def test_a_long_integer_keeps_every_digit() -> None:
    assert parse_expression('123456789012345678901', N, N) == Integer(123456789012345678901)


# ---------------------------------------------------------------------------
# precedence and associativity

def test_unary_minus_binds_looser_than_the_power() -> None:
    assert parse_expression('-x^2', N, N) == -x**2
    assert parse_expression('(-x)^2', N, N) == x**2


def test_the_power_is_right_associative() -> None:
    # 2^(3^2) = 512, non (2^3)^2 = 64
    assert parse_expression('2^3^2', N, N) == Integer(512)
    assert parse_expression('x^2^3', N, N) == x**8


def test_subtraction_and_division_are_left_associative() -> None:
    a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
    assert parse_expression('a-b-c', N, N) == a - b - c
    assert parse_expression('a/b/c', N, N) == a/(b*c)
    assert parse_expression('1-2-3', N, N) == Integer(-4)


def test_a_sign_after_an_operator() -> None:
    assert parse_expression('2*-3', N, N) == Integer(-6)
    assert parse_expression('2--3', N, N) == Integer(5)
    assert parse_expression('2^-1', N, N) == Rational(1, 2)
    assert parse_expression('-+x', N, N) == -x


# ---------------------------------------------------------------------------
# factorial and double factorial

def test_factorial_postfix_binds_tighter_than_the_sign() -> None:
    assert parse_expression('3!', N, N) == Integer(6)
    assert parse_expression('-2!', N, N) == Integer(-2)      # -(2!), non (-2)!


def test_double_factorial_is_not_two_factorials() -> None:
    # ``5!!`` is 15 in Maxima (5*3*1); reading it as ``(5!)!`` would give 120!
    assert parse_expression('5!!', N, N) == Integer(15)
    assert parse_expression('n!!', N, N) == factorial2(Symbol('n'))
    assert parse_expression('(2!)!', N, N) == Integer(2)


def test_factorial_as_a_call_is_the_sympy_function() -> None:
    assert parse_expression('factorial(5)', N, N) == Integer(120)
    assert parse_expression('factorial(n)', N, N) == factorial(Symbol('n'))
    assert not parse_expression('factorial(n)', N, N).atoms(AppliedUndef)


# ---------------------------------------------------------------------------
# the constructs with a bound variable stay unevaluated

def test_integrate_becomes_an_unevaluated_integral() -> None:
    xs = Symbol('x')
    assert parse_expression('integrate(f(x),x)', N, N) == Integral(Function('f')(xs), xs)
    assert parse_expression('integrate(x^2,x,0,1)', N, N) == Integral(xs**2, (xs, 0, 1))
    raises(MaximaSyntaxError, lambda: parse_expression('integrate(x)', N, N))


def test_sum_and_product_keep_their_index() -> None:
    k, n_ = Symbol('k'), Symbol('n')
    assert parse_expression('sum(k,k,1,n)', N, N) == Sum(k, (k, 1, n_))
    assert parse_expression('product(k,k,1,n)', N, N) == Product(k, (k, 1, n_))


# ---------------------------------------------------------------------------
# Maxima's names and their SymPy counterparts

def test_special_functions_map_to_sympy() -> None:
    xs, n_ = Symbol('x'), Symbol('n')
    assert parse_expression('bessel_j(0,x)', N, N) == besselj(0, xs)
    assert parse_expression('spherical_bessel_j(1,x)', N, N) == jn(1, xs)
    assert parse_expression('spherical_bessel_y(1,x)', N, N) == yn(1, xs)
    assert parse_expression('legendre_p(2,x)', N, N) == legendre(2, xs)
    assert parse_expression('gamma_incomplete(n,x)', N, N) == uppergamma(n_, xs)


def test_constants() -> None:
    assert parse_expression('%e^x', N, N) == exp(x)
    assert parse_expression('%i*x', N, N) == I*x
    assert parse_expression('%pi', N, N) == pi
    assert parse_expression('inf', N, N) == oo
    assert parse_expression('minf', N, N) == -oo


def test_an_unknown_applied_name_becomes_an_undefined_function() -> None:
    e = parse_expression('baz(0,x)', N, N)
    assert e.atoms(AppliedUndef)
    assert str(e) == 'baz(0, x)'


def test_a_name_python_could_not_parse() -> None:
    assert parse_expression('lambda*y', N, N) == Symbol('lambda')*Symbol('y')


# ---------------------------------------------------------------------------
# derivatives

def test_the_noun_form_stays_a_derivative_and_the_verb_form_evaluates() -> None:
    assert parse_expression("'diff(y,x)") == Derivative(y(x), x)
    assert parse_expression("'diff(y,x,2)") == Derivative(y(x), (x, 2))
    assert parse_expression("'diff(y,x,1,t,2)") == Derivative(y(x), x, (Symbol('t'), 2))
    assert parse_expression("'diff(y,x,0)") == y(x)
    assert parse_expression('diff(sin(x),x)', N, N) == cos(Symbol('x'))


def test_a_quoted_name_must_be_a_call() -> None:
    raises(MaximaSyntaxError, lambda: parse_expression("'x", N, N))


# ---------------------------------------------------------------------------
# equations, and what is refused

def test_an_equation_becomes_lhs_minus_rhs() -> None:
    assert parse_expression('2*x+1 = 0', N, N) == 2*Symbol('x') + 1
    raises(MaximaSyntaxError, lambda: parse_expression('x = y = z', N, N))


def test_malformed_input_is_refused() -> None:
    for text in ('x +', '(x', 'x)', 'f(', ',x', 'x @ y', '', '   ', 'x::y', 'x:=y'):
        raises(MaximaSyntaxError, lambda: parse_expression(text, N, N))


def test_parse_equation_wants_a_differential_equation() -> None:
    raises(MaximaSyntaxError, lambda: parse_equation('x^2 - 1'))
    assert parse_equation("'diff(y,x) = y") == Derivative(y(x), x) - y(x)


# ---------------------------------------------------------------------------
# reading the source text: comments, statements, groups, argument lists

def test_comments_are_blanked_and_nest() -> None:
    text = 'a: 1 /* one /* nested */ still inside */ b: 2'
    blanked = strip_comments(text)
    assert len(blanked) == len(text)          # the positions do not move
    assert 'nested' not in blanked and 'inside' not in blanked
    assert blanked.startswith('a: 1') and blanked.rstrip().endswith('b: 2')


def test_an_unterminated_comment_hides_the_rest() -> None:
    assert strip_comments('a: 1 /* never closed').strip() == 'a: 1'


def test_statements_split_on_semicolon_and_dollar() -> None:
    assert statements('a: 1$ /* not ; here */ f(x; y); "s;t";') == ['a: 1', 'f(x; y)', '"s;t"']
    assert statements('') == []


def test_group_reads_a_bracketed_span() -> None:
    assert group('f(a, (b), c) resto', 1) == ('a, (b), c', 12)
    assert group('f(a, "b)", c)', 1) == ('a, "b)", c', 13)
    assert group('f(a', 1) is None


def test_split_arguments_at_the_top_level_commas() -> None:
    assert split_arguments('f(x, y), [a, b], "c, d"') == ['f(x, y)', '[a, b]', '"c, d"']
    assert split_arguments('') == []


def test_call_arguments_stops_at_the_closing_bracket() -> None:
    text = "contrib_ode(eqn:'diff(y,x),y,x));"
    read = call_arguments(text, len('contrib_ode('))
    assert read is not None
    args, end = read
    assert args == ["eqn:'diff(y,x)", 'y', 'x']
    assert text[end - 1] == ')'
    assert call_arguments('f(a, b', 2) is None


def test_application_reads_one_call_and_nothing_else() -> None:
    assert application('assume(a > 0, b # 0)') == ('assume', ['a > 0', 'b # 0'])
    assert application('assume(a) + 1') is None
    assert application('a + b') is None


def test_parse_refuses_what_did_not_translate() -> None:
    assert parse('2*x') == 2*Symbol('x')
    assert parse('integrate(f(x),x)') is None     # an integral is not a value
    assert parse('x +') is None
