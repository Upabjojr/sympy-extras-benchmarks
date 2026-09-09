"""Tests of the ``algsys`` regression parser on samples written here in
Maxima syntax (nothing is copied from Maxima)."""
from __future__ import annotations

from sympy import Symbol

from sympy_extras_benchmarks.datasets.polynomial_solving import PolynomialSystem, systems


def _one(text: str) -> PolynomialSystem:
    found = systems(text, 'sample')
    assert len(found) == 1
    return found[0]


def test_a_system_and_its_recorded_solutions() -> None:
    system = _one("algsys([x^2+y-1,y-2],[x,y]);\n[[x = 1,y = 2],[x = -1,y = 2]];\n")
    x, y = Symbol('x'), Symbol('y')
    assert system.name == 'sample:1'
    assert system.equations == [x**2 + y - 1, y - 2]
    assert system.variables == [x, y]
    assert system.recorded == 2
    assert system.parametric is False


def test_an_equation_written_with_an_equals_sign_becomes_an_expression() -> None:
    # Maxima allows both forms; ``lhs = rhs`` is read as ``lhs - rhs``
    system = _one("algsys([x^2 = 4, y = 1],[x,y]);\n[[x = 2,y = 1],[x = -2,y = 1]];\n")
    x, y = Symbol('x'), Symbol('y')
    assert system.equations == [x**2 - 4, y - 1]


def test_an_arbitrary_constant_marks_the_answer_parametric() -> None:
    # %r1 is Maxima's arbitrary parameter: the solution set is a family
    system = _one("algsys([x+10*y],[x,y]);\n[[x = %r1, y = -(%r1/10)]];\n")
    assert system.parametric is True


def test_a_call_without_a_recorded_answer_has_no_count() -> None:
    system = _one("algsys([x^2-1],[x]);\nsomething_else;\n")
    assert system.recorded is None


def test_nested_brackets_in_the_equations_are_read() -> None:
    system = _one("algsys([4*(x+y)+(x-y)*((x-2)^2+y^2-1)],[x,y]);\n[[x = 0,y = 0]];\n")
    x, y = Symbol('x'), Symbol('y')
    assert system.equations == [4*(x + y) + (x - y)*((x - 2)**2 + y**2 - 1)]


def test_several_calls_are_numbered_in_order() -> None:
    text = ("algsys([x-1],[x]);\n[[x = 1]];\n"
            "/* a comment */\n"
            "algsys([y-2],[y]);\n[[y = 2]];\n")
    first, second = systems(text, 'file')
    assert (first.name, second.name) == ('file:1', 'file:2')


def test_a_call_whose_arguments_are_not_two_lists_is_skipped() -> None:
    assert systems("algsys(x^2-1, x);\n[[x = 1]];\n", 'sample') == []


def test_a_call_with_an_unparsable_equation_is_skipped() -> None:
    assert systems("algsys([x^^^2],[x]);\n[[x = 1]];\n", 'sample') == []


def test_the_unknowns_must_be_plain_names() -> None:
    assert systems("algsys([x-1],[f(x)]);\n[[x = 1]];\n", 'sample') == []


def test_a_call_inside_a_comment_is_not_a_test() -> None:
    # the file disables an entry by commenting it out, often because the
    # recorded answer is known to be wrong
    text = ("/* FIXME: cannot match the form of the solution\n"
            "algsys([x^2-1],[x]);\n[[x = 1],[x = -1]];\n*/\n")
    assert systems(text, 'sample') == []


def test_nested_comments_are_stripped() -> None:
    text = ("/* outer /* inner */ still commented\n"
            "algsys([x^2-1],[x]);\n*/\n"
            "algsys([y-2],[y]);\n[[y = 2]];\n")
    system, = systems(text, 'sample')
    assert system.variables == [Symbol('y')]


def test_an_equation_given_by_name_is_resolved() -> None:
    # the file names a system before solving it
    text = ("eq1 : a*x + c*y;\neq2 : b*x - y;\n"
            "algsys([eq1,eq2],[x,y]);\n[[x = 0,y = 0]];\n")
    system, = systems(text, 'sample')
    x, y, a, b, c = (Symbol(n) for n in 'xyabc')
    assert system.equations == [a*x + c*y, b*x - y]


def test_a_name_that_cannot_be_resolved_is_skipped() -> None:
    # left as a bare symbol, the "system" would mention none of the
    # unknowns and putting it to a solver would mean nothing
    assert systems("algsys([undefined_name],[x,y]);\n[[x = 0,y = 0]];\n", 'sample') == []
