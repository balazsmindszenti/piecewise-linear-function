import pytest

from pw_lin_func.piecewise_linear_function import PiecewiseLinearFunction


@pytest.mark.parametrize('point_list, error_type, error_message', [
    (3, TypeError,
     'The piecewise linear function must be instantiated with a '
     'list, but was instead instantiated with a'
     "<class 'int'>."),
    ([], ValueError, 'The list of tuples must not be an empty list.'),
    ([(1, 2), (1, 3)], ValueError,
     'The passed elements of the domain must be strictly '
     'monotone increasing for the piecewise linear function to '
     'be well-defined. This fails, because '
     '1 >= 1.'),
    ([(-3, 2.5), (-4.998, 3.43)], ValueError,
     'The passed elements of the domain must be strictly '
     'monotone increasing for the piecewise linear function to '
     'be well-defined. This fails, because '
     '-3 >= -4.998.')
])
def test_well_definedness_check(point_list: list,
                                error_type: type[ValueError] | type[TypeError],
                                error_message: str):
    with pytest.raises(expected_exception=error_type, match=error_message):
        PiecewiseLinearFunction(point_list=point_list)


@pytest.mark.parametrize('x, expected', [
    (1, 2.0), (2.5, 5.0), (4, 0.0),
    (-10, 2.0), (0.99, 2.0),
    (1.75, 3.5), (3, 3.333333),
    (4.01, 0.0), (100.5, 0.0), (100, 0.0)
])
def test_general_case(x: float | int, expected: float | int):
    f = PiecewiseLinearFunction(point_list=[(1, 2), (2.5, 5.0), (4, 0)])

    assert f(x) == pytest.approx(expected)


@pytest.mark.parametrize('x, expected', [
    (-43789, -3.14), (0, -3.14), (5.5, -3.14), (1234, -3.14)
])
def test_single_point(x: float | int, expected: float | int):
    f = PiecewiseLinearFunction(point_list=[(5.5, -3.14)])

    assert f(x) == pytest.approx(expected)


@pytest.mark.parametrize('x, expected', [
    (1, 2.0), (2.0, 2.0), (3.5, -0.25)
])
def test_horizontal_segment(x: float | int, expected: float | int):
    f = PiecewiseLinearFunction(point_list=[(0, 2), (2, 2), (4, -1)])

    assert f(x) == pytest.approx(expected)


@pytest.mark.parametrize('test_points', [
    [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4]
])
def test_addition(test_points: list):
    f = PiecewiseLinearFunction(point_list=[(0, 1), (2, 3)])
    g = PiecewiseLinearFunction(point_list=[(1, 0), (3, 2)])

    h = f + g

    for x in test_points:
        assert h(x) == pytest.approx(f(x) + g(x))


@pytest.mark.parametrize('test_points', [
    [-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3]
])
def test_subtraction(test_points: list):
    f = PiecewiseLinearFunction(point_list=[(-2, -5.5), (0, 0), (2, 5.5)])
    g = PiecewiseLinearFunction(point_list=[(-1, 2), (1, -2)])

    h = f - g

    for x in test_points:
        assert h(x) == pytest.approx(f(x) - g(x))


@pytest.mark.parametrize('c, test_points', [
    (2, [-1, 0, 1.25, 2.5, 5]),
    (-1.5, [-1.2, 0.2, 1.15, 123, -43]),
    (0, [-21421, 0, -5.3]),
    (0.0, [-2, 12, 3]),
    (1, [-1.3, -10, 32, 23.4, 0.2])
])
def test_scalar_multiplication(c: float | int, test_points: list):
    f = PiecewiseLinearFunction(point_list=[(0, 1.5), (2.5, -3)])

    g = c * f

    for x in test_points:
        assert g(x) == pytest.approx(c * f(x))
