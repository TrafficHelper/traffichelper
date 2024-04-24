from __future__ import annotations

import math

import numpy

from DS.Temporal.time import Time


class Recurrence:

    """
    A Recurrence represents any periodic continuous function
    In this case, it maps functions in the Cartesian Plane to a Fourier Series
    The Recurrence is used to interpolate partial data, as well as represent cyclicity
    - This manifests in Traffic Flows, Vehicle traversal times, etc.
    The details of a Fourier Series (and associated transform) may be found at:
    - https://en.wikipedia.org/wiki/Fourier_series
    - https://ncatlab.org/nlab/show/Fourier+transform
    """

    PRECISION = 5  # Standard number of terms for precision of a recurrence

    def __init__(self, period: float = Time.RECURRENCE, shift: float = 0, coefficients: [(float, float)] = []):  # This should be accessible only from the interpolate method
        """
        A Fourier Series is of the form fN(t) = k + E ai cos(2*pi*i/P * t) + bi sin (2*pi*i/p * t)
        :param period: "P" in the above expression, the repeating time for the series
        :param shift: "k" in the expression, the upward shift of the series
        :param coefficients: A pair of cos and sin coefficients, whose sum corresponds to the periodic part of the series
        """
        self.period = period
        self.shift = shift
        self._terms = coefficients
        self.precision = len(coefficients)

    @property
    def terms(self):
        return self._terms

    @terms.setter
    def terms(self, new:[(float, float)]):
        self._terms = new
        self.precision = len(new)

    # TODO FIX interpolate, coefficients, value, number, evaluate, NOT USED SO FAR
    @staticmethod
    def interpolate(datapoints:[(float, float)], period:float = Time.RECURRENCE):
        """
        Interpolates the given datapoints with a Recurrence/Fourier Series
        The precision is construed such that the datapoints uniquely determine the answer
        It is recommended for the data points to yield a non-negative Recurrence, avoiding pathological behaviour
        :param datapoints: The list of datapoints to interpolate
        :param period: The desired period of the Recurrence interpolate
        :return: The interpolating recurrence
        """

        assert len(datapoints)%2 == 1 # Must have odd number for interpolation of odd number of unknowns
        y = []
        matrix = []
        for elem in range(datapoints):
            y+=elem[1] # +fN(t)
            terms = [1] + Recurrence.coefficients(datapoints[i][1])
        kaibi = numpy.linalg.solve(matrix, y)
        k, kaibi = float(kaibi[0]), kaibi[1:]
        cfs = [(kaibi[i], kaibi[i + 1]) for i in range(0, 2*len(datapoints), 2)]
        return Recurrence(period, k, cfs)

    @staticmethod
    def coefficients(value: float, period: float = Time.RECURRENCE, precision: int = PRECISION, extrusive: bool = False):
        """
        Helper method to find the coefficients given the value to evaluate at, period, precision and whether to determine the area or simple value
        Returns the sine and cosine terms of each term of the fourier series.
        Use formula sin/cos (2pi*x/P) or cos/-sin(2pi*x/p)p/(2pi*x) depending on the integral or not
        :param value:
        :param period:
        :param precision:
        :param extrusive:
        :return:
        """
        # Helper method to find both sin and cos terms either as part of an integral (extrusive is True) or in evaluation (extrusive is False)
        values = []
        tau = (2 * math.pi) / period
        tin = 1 / tau
        for i in range(1, precision + 1):
            inside = tau * i * value
            outside = tin / i if extrusive else 1
            values += [outside * math.sin(inside), outside * math.cos(inside)]
        return values

    def value(self, start: Time, end: Time):
        # Returns the value of the time function if the start and end times are identical, returns the 2-measure (area) under the curve between start and end otherwise
        if start.based() and end.based():
            return self.number((end.absolute, start.absolute) if end.absolute < start.absolute else (start.absolute, end.absolute))
        else:
            assert start.period == end.period  # We can only compare times of same cyclic length
            return self.number((start.time, end.time + (end.period if end.time < start.time else 0)))  # If end before start, wrap around and reassess

    def number(self, interval: tuple[float, float]):
        # Assumes the second term is never smaller than the first
        a = interval[0]
        b = interval[1]
        return self.evaluate(a, False) if a == b else (self.evaluate(interval[1], True) - self.evaluate(interval[0], True))

    def evaluate(self, value: float, integral: bool = False):
        """
        Evaluates the recurrence at the given value
        Evaluates the integral of the recurrence at that value akin to between the position when the function is zero and that value if the integral boolean is false, or the simple evaluation otherwise
        :param value:
        :param integral:
        :return:
        """
        result = self.shift * (value if integral else 1)
        coefficients = Recurrence.coefficients(value, self.period, integral)
        for i in range(self.precision):
            amplitudes = [-self.terms[i][1], self.terms[i][0]] if integral else [self.terms[i][0], self.terms[i][1]]
            print(str(amplitudes) + ', '+str(coefficients))
            result += numpy.dot(amplitudes, coefficients[i])

        return result

    @staticmethod
    def coefficients(sections:[(float, float)], value:float, period:float, integral:bool = False):
        """
        Returns a list of partial coefficients conducive to the calculation of derivatives or integrals
        :param sections:
        :param value:
        :param period:
        :param integral:
        :return:
        """
        tau = math.pi*2/period*value
        terms = []
        for i in range(len(sections)):
            temp = tau*i
            terms.append(((1/temp if integral else 1)*math.cos(tau*i), (1/temp if integral else 1)*math.sin(tau*i)))
        return terms




    def range(self) -> (float, float):
        """
        Returns the potential range of this Recurrence
        The lowest is the negative value of all terms and the highest is the positive value
        Finding the absolute range of the recurrence is nontrivial and inefficient
        :return:
        """

        # Case that all terms are maximized or minimized
        s = 0
        for elem in self.terms:
            a, b = elem[0], elem[1]
            if a == 0 and b == 0:
                s += 0
            elif a == 0:
                s += b
            elif b == 0:
                s += a
            else:
                s += (a*a + b*b)**0.5 # Upper bound on possible size of that term
        return self.shift - s, self.shift + s

    def __eq__(self, other: Recurrence):
        if self.shift != other.shift or self.period != other.period:
            return False
        st = self.truncate(min(len(self.terms), len(other.terms)))
        ot = other.truncate(min(len(self.terms), len(other.terms)))
        return st.terms == ot.terms

    def __add__(self, other:Recurrence):
        return self.addsub(other, True)

    def __sub__(self, other:Recurrence):
        return self.addsub(other, False)

    def __str__(self):
        """
        Return the str representation of this Recurrence
        :return: The str representation of this Recurrence
        """
        return 'Recurrence[period = '+str(self.period)+', shift = '+str(self.shift)+', coefficients: '+str(self.terms)+']'

    def addsub(self, other, op: bool):
        length = max(self.precision, other.precision)
        alpha = self.truncate(length)
        beta = other.truncate(length)
        if alpha.period != beta.period:
            raise ValueError(" Cannot add fourier series with unequal periods ")
        associate = 1 if op else -1
        sums = [(alpha.terms[i][0] + associate*beta.terms[i][0], alpha.terms[i][1] + associate*beta.terms[i][1]) for i in range(length)]
        return Recurrence(alpha.period, alpha.shift + associate*beta.shift, sums)
        # # May not be of same length, but this is fine
        # sums = []
        # associate = 1 if op else -1
        # this = alpha.terms
        # alen = len(this)
        # oth = beta.terms
        # olen = len(oth)
        # intersection = min(alen, olen)
        # union = max(alen, olen)
        # for j in range(intersection):  # Work on all common terms
        #     sums += (this[j][0] + associate * oth[j][0], this[j][1] + associate * oth[j][1])
        # for k in range(intersection, union):  # Work on all extra terms
        #     sums += [e * associate for e in (this if alen > olen else oth)[k]]
        # return Recurrence(alpha.period, alpha.shift+associate*beta.shift, sums)

    def truncate(self, precision: int = PRECISION) -> Recurrence:
        """
        Will return a Truncated Recurrence to the given precision level
        It will cut off extra coefficient pairs of precision if the desired precision is lower than the current one
        It will append redundant zeroes to the coefficients if the precision is more
        :param precision: The precision to truncate to
        :return: The Recurrence truncated to the desired precision
        """

        assert precision >= 0
        n = self.precision
        if n < precision:
            t = self.terms
            for i in range(precision - n):
                t.append((0, 0))
        else:
            t = self.terms[:precision]
        return Recurrence(self.period, self.shift, t)

    def increase(self, shift: float):
        self.shift += shift

    def multiply(self, constant: float):
        return Recurrence(self.period, self.shift * constant, [(t[0] * constant, t[1] * constant) for t in self.terms])

