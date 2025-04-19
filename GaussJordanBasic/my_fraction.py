import math

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        self.normalize()

    def normalize(self):
        """Приводит дробь к нормализованному виду."""
        if self.numerator == 0:
            self.denominator = 1
            return

        # Находим наибольший общий делитель (НОД)
        common_divisor = math.gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= common_divisor
        self.denominator //= common_divisor

        # Убедимся, что знаменатель всегда положительный
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def sign(self):
        """Возвращает знак дроби: '+' или '-'."""
        return "-" if self.numerator < 0 else "+"

    def neg_sign(self):
        """Возвращает знак дроби для отрицательных чисел: '-' или пустую строку."""
        return "-" if self.numerator < 0 else ""

    def __add__(self, other):
        """Сложение дробей."""
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self + Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        """Вычитание дробей."""
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self - Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        """Умножение дробей."""
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self * Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other):
        """Деление дробей."""
        if isinstance(other, Fraction):
            if other.numerator == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            new_numerator = self.numerator * other.denominator
            new_denominator = self.denominator * other.numerator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return self / Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for /")

    def __eq__(self, other):
        """Проверка равенства дробей."""
        if isinstance(other, Fraction):
            return self.numerator == other.numerator and self.denominator == other.denominator
        elif isinstance(other, int):
            return self.numerator == other and self.denominator == 1
        else:
            return False

    def __ne__(self, other):
        """Проверка неравенства дробей."""
        return not self.__eq__(other)

    def __str__(self):
        """Строковое представление дроби."""
        if self.denominator == 1:
            return f"{self.numerator}"
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        """Представление дроби для отладки."""
        return self.__str__()

    def __format__(self, format_spec):
        """Форматирование дроби."""
        return format(str(self), format_spec)