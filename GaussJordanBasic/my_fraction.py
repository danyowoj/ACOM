import math

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        self.normalize()

    def normalize(self):
        if self.numerator == 0:
            self.denominator = 1
            return

        common_divisor = math.gcd(self.numerator, self.denominator)
        self.numerator //= common_divisor
        self.denominator //= common_divisor

        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def sign(self):
        return "-" if self.numerator < 0 else "+"

    def neg_sign(self):
        return "-" if self.numerator < 0 else ""

    def __add__(self, other):
        result = Fraction()
        result.numerator = self.numerator * other.denominator + other.numerator * self.denominator
        result.denominator = self.denominator * other.denominator
        result.normalize()
        return result

    def __sub__(self, other):
        result = Fraction()
        result.numerator = self.numerator * other.denominator - other.numerator * self.denominator
        result.denominator = self.denominator * other.denominator
        result.normalize()
        return result

    def __mul__(self, other):
        result = Fraction()
        result.numerator = self.numerator * other.numerator
        result.denominator = self.denominator * other.denominator
        result.normalize()
        return result

    def __truediv__(self, other):
        result = Fraction()
        result.numerator = self.numerator * other.denominator
        result.denominator = self.denominator * other.numerator
        result.normalize()
        return result

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.numerator == other.numerator and self.denominator == other.denominator
        elif isinstance(other, int):
            return self.numerator == other and self.denominator == 1
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"{self.numerator}" if self.denominator == 1 else f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return self.__str__()

    def __format__(self, format_spec):
        return format(str(self), format_spec)
