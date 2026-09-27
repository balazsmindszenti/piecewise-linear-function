from __future__ import annotations


class PiecewiseLinearFunction:
    """
    A class that represents a piecewise linear function defined by a list of
    tuples, which contains real numbers or integers.
    """
    def __init__(self, point_list: list[tuple[float | int, float | int]]):
        """
        Constructor.
        :param list[tuple[float | int, float | int]] point_list: the list of
               tuples that defines the piecewise linear function
        """
        self.point_list = point_list

        self.check_well_definedness()

    def check_well_definedness(self):
        """
        This method ensures that the received list of tuples define a
        well-defined piecewise linear function.
        :raise ValueError: if the piecewise linear function is not well-defined
        """
        if not self.point_list:
            raise ValueError('The list of tuples must not be an empty list.')

        it = iter(self.point_list)
        previous = next(it)[0]
        for tup in it:
            current = tup[0]
            if previous >= current:
                raise ValueError(
                    'The passed elements of the domain must be strictly '
                    'monotone increasing for the piecewise linear function to '
                    'be well-defined. This fails, because '
                    f'{previous} >= {current}.'
                )
            previous = current

    def __repr__(self) -> str:
        """
        The representation of the class.
        :return str: the object
        """
        return f"PiecewiseLinearFunction(points={self.point_list})"

    def __call__(self, x: float) -> float:
        """
        We call the function with the x parameter, a real number.
        :param float x: the parameter we call the function on
        :return float: the value that the function maps to x
        """
        if x <= self.point_list[0][0]:
            return self.point_list[0][1]
        elif x >= self.point_list[-1][0]:
            return self.point_list[-1][1]
        else:
            low = 0
            high = len(self.point_list)
            while True:
                n = (low + high) // 2
                previous_point = self.point_list[n - 1][0]
                current_point = self.point_list[n][0]
                next_point = self.point_list[n + 1][0]
                if current_point <= x <= next_point:
                    return self.linear_func(i=n, x=x)
                elif previous_point <= x < current_point:
                    return self.linear_func(i=(n - 1), x=x)
                elif x > self.point_list[n + 1][0]:
                    low = n
                else:
                    high = n

    def linear_func(self, i: int, x: float) -> float:
        """
        The linear function that maps from [x_i, x_{i+1}] -> [y_i, y_{i+1}].
        :param int i: the index of the specific linear function we are using
        :param float x: the parameter we call the function on
        :return float: the value that the linear function maps to x
        """
        x_i = self.point_list[i][0]
        y_i = self.point_list[i][1]
        x_j = self.point_list[i + 1][0]
        y_j = self.point_list[i + 1][1]

        delta_y = y_j - y_i
        delta_x = x_j - x_i

        slope = delta_y / delta_x

        return round(slope * (x - x_i) + y_i, ndigits=6)

    def __add__(self, f: PiecewiseLinearFunction) -> PiecewiseLinearFunction:
        """
        Returns the sum of two piecewise linear functions in the usual
        interpretation of function addition, where (f + g)(x) = f(x) + g(x).
        :param PiecewiseLinearFunction f: the function on the right side of the
               operator
        :return PiecewiseLinearFunction: the sum of the two functions
        """
        x_values = []

        i = 0
        j = 0
        m = len(self.point_list)
        n = len(f.point_list)

        while i < m and j < n:
            a = self.point_list[i][0]
            b = f.point_list[j][0]
            if a == b:
                x_values.append(a)
                i += 1
                j += 1
            elif a < b:
                x_values.append(a)
                i += 1
            else:
                x_values.append(b)
                j += 1

        while i < m:
            x_values.append(self.point_list[i][0])
            i += 1
        while j < n:
            x_values.append(f.point_list[j][0])
            j += 1

        new_point_list = [(x, self(x) + f(x)) for x in x_values]

        return PiecewiseLinearFunction(point_list=new_point_list)

    def __rmul__(self, c: float) -> PiecewiseLinearFunction:
        """
        Returns the product of the c real number and the piecewise linear
        function in the usual interpretation of scalar multiplication of
        functions, where (c * f)(x) = c * f(x).
        :param float c: the scalar on the left side of the operator
        :return PiecewiseLinearFunction: the product of c and the function
        """
        new_point_list = [(x, c * y) for x, y in self.point_list]

        return PiecewiseLinearFunction(point_list=new_point_list)

    def __sub__(self, f: PiecewiseLinearFunction) -> PiecewiseLinearFunction:
        """
        Returns the difference of two piecewise linear functions in the usual
        interpretation of function subtraction,
        where (f - g)(x) = f(x) + (-1) * g(x).
        :param PiecewiseLinearFunction f: the function on the right side of the
               operator
        :return PiecewiseLinearFunction: the difference of the two functions
        """
        return self + (-1) * f
