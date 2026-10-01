from __future__ import annotations


class PiecewiseLinearFunction:
    """
    A class that represents a piecewise linear function defined by a list of
    tuples, which contains real numbers.
    """
    def __init__(self, point_list: list[tuple[float | int, float | int]]):
        """
        Constructor.
        :param list[tuple[float | int, float | int]] point_list: the list of
               tuples that defines the piecewise linear function
        """
        self.point_list = point_list

        self.check_input_type()
        self.check_well_definedness()

    def check_input_type(self):
        """
        This method ensures that the received point list is actually a python
        list.
        :raise TypeError: if the point list is not a list
        """
        if not isinstance(self.point_list, list):
            raise TypeError(
                'The piecewise linear function must be instantiated with a '
                'list, but was instead instantiated with a'
                f'{type(self.point_list)}.'
            )

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
        The representation of the class. This is a string that includes the
        point list that defines the class, unless that would be too long to
        show, in which case the first five and last five elements are shown.
        :return str: the string including the point list that defines the class
        """
        if len(self.point_list) <= 10:
            printed_list = [
                (round(number=x, ndigits=4), round(number=y, ndigits=4))
                for x, y in self.point_list
            ]
            return f"PiecewiseLinearFunction(points={printed_list})"
        else:
            first_five = [
                (round(number=x, ndigits=4), round(number=y, ndigits=4))
                for x, y in self.point_list[:5]
            ]
            last_five = [
                (round(number=x, ndigits=4), round(number=y, ndigits=4))
                for x, y in self.point_list[-5:]
            ]
            first_five_str = ", ".join(str(point) for point in first_five)
            last_five_str = ", ".join(str(point) for point in last_five)
            return ("PiecewiseLinearFunction(points="
                    f"[{first_five_str}, ..., {last_five_str}])")

    def __call__(self, x: float | int) -> float | int:
        """
        We call the function with the x parameter, a real number.
        :param float | int x: the parameter we call the function on
        :return float | int: the value that the function maps to x
        """
        if x <= self.point_list[0][0]:
            return self.point_list[0][1]
        elif x >= self.point_list[-1][0]:
            return self.point_list[-1][1]
        elif len(self.point_list) == 2:
            return self.linear_func(i=0, x=x)
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

    def linear_func(self, i: int, x: float | int) -> float:
        """
        The linear function that goes through (x_i, x_{i+1}) and
        (y_i, y_{i+1}).
        :param int i: the index of the specific linear function we are using
        :param float | int x: the parameter we call the function on
        :return float: the value that the linear function maps to x
        """
        x_i = self.point_list[i][0]
        y_i = self.point_list[i][1]
        x_j = self.point_list[i + 1][0]
        y_j = self.point_list[i + 1][1]

        delta_y = y_j - y_i
        delta_x = x_j - x_i

        slope = delta_y / delta_x

        return slope * (x - x_i) + y_i

    def __add__(self,
                f: PiecewiseLinearFunction | float | int
                ) -> PiecewiseLinearFunction:
        """
        Returns the sum of two piecewise linear functions in the usual
        interpretation of function addition, where (f + g)(x) = f(x) + g(x), or
        the sum of a function and a real number (the translation of the
        function on the y-axis).
        :param PiecewiseLinearFunction | float | int f: the function or the
               real number on the right side of the operator
        :raise TypeError: if attempting addition by an unsupported type
        :return PiecewiseLinearFunction: the resulting function
        """
        if isinstance(f, PiecewiseLinearFunction):
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
        elif isinstance(f, (float, int)):
            new_point_list = [(x, y + f) for x, y in self.point_list]

            return PiecewiseLinearFunction(point_list=new_point_list)
        else:
            raise TypeError('Addition is only supported for real numbers and '
                            'other piecewise linear functions.')

    def __radd__(self,
                 f: PiecewiseLinearFunction | float | int
                 ) -> PiecewiseLinearFunction:
        """
        Returns the sum of two piecewise linear functions in the usual
        interpretation of function addition, where (g + f)(x) = g(x) + f(x), or
        the sum of a function and a real number (the translation of the
        function on the y-axis).
        :param PiecewiseLinearFunction | float | int f: the function or the
               real number on the left side of the operator
        :return PiecewiseLinearFunction: the resulting function
        """
        return self + f

    def __rmul__(self, c: float | int) -> PiecewiseLinearFunction:
        """
        Returns the product of the c real number and the piecewise linear
        function in the usual interpretation of scalar multiplication of
        functions, where (c * f)(x) = c * f(x).
        :param float | int c: the scalar on the left side of the operator
        :return PiecewiseLinearFunction: the product of c and the function
        """
        new_point_list = [(x, c * y) for x, y in self.point_list]

        return PiecewiseLinearFunction(point_list=new_point_list)

    def __mul__(self, c: float | int) -> PiecewiseLinearFunction:
        """
        Returns the product of the c real number and the piecewise linear
        function in the usual interpretation of scalar multiplication of
        functions, where (f * c)(x) = f(x) * c.
        :param float | int c: the scalar on the right side of the operator
        :return PiecewiseLinearFunction: the product of c and the function
        """
        return c * self

    def __sub__(self,
                f: PiecewiseLinearFunction | float | int
                ) -> PiecewiseLinearFunction:
        """
        Returns the difference of two piecewise linear functions in the usual
        interpretation of function subtraction,
        where (f - g)(x) = f(x) + (-1) * g(x), or the subtraction of a real
        number from the function (the translation of the function on the
        y-axis).
        :param PiecewiseLinearFunction | float | int f: the function or real
               number on the right side of the operator
        :return PiecewiseLinearFunction: the resulting function
        """
        return self + (-1) * f

    def __rsub__(self,
                 f: PiecewiseLinearFunction | float | int
                 ) -> PiecewiseLinearFunction:
        """
        Returns the difference of two piecewise linear functions in the usual
        interpretation of function subtraction,
        where (g - f)(x) = g(x) + (-1) * f(x), or the subtraction of a function
        from a real number (the translation on the y-axis of the reflection
        of the function on the x-axis).
        :param PiecewiseLinearFunction | float | int f: the function or real
               number on the right side of the operator
        :return PiecewiseLinearFunction: the resulting function
        """
        return f + (-1) * self
