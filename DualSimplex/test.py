#!/usr/bin/env python3
"""
Реализация решения задачи линейного программирования двойственным симплекс-методом.
Код написан в одном файле и содержит подробные комментарии.
"""

import math
import sys


# =========================
# Класс Fraction для работы с простыми дробями
# (взято из файла my_fraction.py с незначительными изменениями)
# =========================

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

        common_divisor = math.gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= common_divisor
        self.denominator //= common_divisor
        # Знаменатель всегда положительный
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def __add__(self, other):
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self + Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self - Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Fraction):
            new_numerator = self.numerator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, int):
            return self * Fraction(other, 1)
        else:
            raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other):
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
        if isinstance(other, Fraction):
            return self.numerator == other.numerator and self.denominator == other.denominator
        elif isinstance(other, int):
            return self.numerator == other and self.denominator == 1
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Fraction):
            return self.numerator * other.denominator < other.numerator * self.denominator
        elif isinstance(other, int):
            return self.numerator < other * self.denominator
        else:
            raise TypeError("Unsupported operand type for <")

    def __gt__(self, other):
        if isinstance(other, Fraction):
            return self.numerator * other.denominator > other.numerator * self.denominator
        elif isinstance(other, int):
            return self.numerator > other * self.denominator
        else:
            raise TypeError("Unsupported operand type for >")

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __abs__(self):
        return Fraction(abs(self.numerator), abs(self.denominator))

    def __str__(self):
        if self.denominator == 1:
            return f"{self.numerator}"
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return self.__str__()

    def __float__(self):
        return self.numerator / self.denominator


# =========================
# Функции для работы с симплекс-таблицей
# =========================

def read_tableau(filename):
    """
    Читает матрицу из файла.
    Файл должен содержать строки, где числа разделены пробелами.
    Первая строка – целевая функция, остальные – ограничения.
    Каждое число преобразуется в Fraction.
    """
    tableau = []
    try:
        with open(filename, "r") as f:
            for line in f:
                # Игнорируем пустые строки
                if line.strip() == "":
                    continue
                # Разбиваем строку по пробелам и преобразуем в Fraction
                numbers = line.split()
                row = [Fraction(int(num)) for num in numbers]
                tableau.append(row)
    except Exception as e:
        print("Ошибка чтения файла:", e)
        sys.exit(1)
    return tableau


def print_tableau(tableau):
    """
    Выводит симплекс-таблицу в удобном для чтения виде.
    """
    for row in tableau:
        print("\t".join(str(x) for x in row))
    print()


def pivot(tableau, basic_indices, pivot_row, pivot_col):
    """
    Выполняет операцию поворота (pivot) в симплекс-таблице.

    1. Делим опорную строку на опорный элемент, чтобы он стал равен 1.
    2. Для всех остальных строк вычитаем нужную кратную опорной строке, чтобы в столбце pivot_col получился 0.
    3. Обновляем список базисных переменных: для строки pivot_row базис становится переменная с индексом pivot_col.
    """
    m = len(tableau)  # число строк
    n = len(tableau[0])  # число столбцов
    pivot_element = tableau[pivot_row][pivot_col]
    # Делим всю опорную строку на pivot_element
    tableau[pivot_row] = [elem / pivot_element for elem in tableau[pivot_row]]

    # Для всех других строк обнуляем элемент в столбце pivot_col
    for i in range(m):
        if i == pivot_row:
            continue
        factor = tableau[i][pivot_col]
        tableau[i] = [tableau[i][j] - factor * tableau[pivot_row][j] for j in range(n)]
    # Обновляем базис: в строке pivot_row теперь базисная переменная имеет индекс pivot_col
    basic_indices[pivot_row - 1] = pivot_col  # строки ограничений начинаются с 1
    # Возвращаем обновлённую таблицу и список базисных переменных
    return tableau, basic_indices


def dual_simplex(tableau, basic_indices):
    """
    Реализация двойственного симплекс-метода.

    Параметры:
      tableau – список списков, представляющий симплекс-таблицу.
                Первая строка – строка целевой функции, остальные – ограничения.
      basic_indices – список индексов базисных переменных для каждой строки ограничения.

    Алгоритм:
      Пока существует строка ограничения (i > 0) с отрицательным правым членом:
        1. Выбираем строку r с самым отрицательным правым членом.
        2. Для каждого столбца j, такого что a[r][j] < 0, вычисляем ratio = c[j] / (-a[r][j]),
           где c[j] – коэффициент из строки целевой функции.
        3. Если ни для одного j найти подходящий не удалось, задача не имеет допустимых решений.
        4. Иначе, выбираем столбец с минимальным ratio и выполняем операцию pivot.
      По завершении алгоритма – оптимальное решение.
    """
    m = len(tableau) - 1  # число ограничений
    n = len(tableau[0]) - 1  # число переменных
    iteration = 0

    while True:
        iteration += 1
        # Ищем строку с b < 0 среди ограничений (строки с индексами 1..m)
        r = -1
        min_b = Fraction(0)
        for i in range(1, m + 1):
            b_i = tableau[i][-1]
            if b_i < 0 and (r == -1 or b_i < min_b):
                r = i
                min_b = b_i
        # Если нет строки с отрицательным правым членом — решение прямодопустимо
        if r == -1:
            break

        # Выбираем входящий столбец
        pivot_col = -1
        min_ratio = None
        # Перебираем все столбцы (0..n-1)
        for j in range(n):
            # Рассматриваем только те j, для которых коэффициент в строке r отрицателен
            if tableau[r][j] < 0:
                # Относительное изменение в целевой функции:
                # ratio = c[j] / (-a[r][j])
                ratio = tableau[0][j] / (Fraction(0) - tableau[r][j])
                if pivot_col == -1 or ratio < min_ratio:
                    min_ratio = ratio
                    pivot_col = j

        # Если ни для одного столбца не найдено a[r][j] < 0, то задача не имеет допустимых решений
        if pivot_col == -1:
            print("Задача не имеет допустимых решений (двойственная неразрешимость).")
            sys.exit(0)

        # Вывод отладочной информации по итерации
        # print(f"Iteration {iteration}: pivot on row {r}, column {pivot_col}")
        pivot(tableau, basic_indices, r, pivot_col)
        # Можно выводить таблицу после каждого поворота для отладки:
        # print_tableau(tableau)

    return tableau, basic_indices


def extract_solution(tableau, basic_indices, total_vars):
    """
    Из симплекс-таблицы извлекается оптимальное решение.

    total_vars – общее число переменных (без учёта свободного члена)

    Для переменных, входящих в базис, значение равно правому члену соответствующего ограничения.
    Для остальных переменных значение 0.
    """
    solution = [Fraction(0) for _ in range(total_vars)]
    # Ограничения находятся в строках с 1 по m
    for i, basic_var in enumerate(basic_indices):
        # Если базисный индекс меньше общего числа переменных, присваиваем значение
        if basic_var < total_vars:
            solution[basic_var] = tableau[i + 1][-1]
    # Оптимальное значение целевой функции находится в первом столбце свободного члена
    optimum = tableau[0][-1]
    return solution, optimum


def find_alternative_solution(tableau, basic_indices, total_vars):
    """
    Пытаемся найти альтернативное оптимальное решение.

    Если в оптимальном решении существует не-базисный столбец с нулевым коэффициентом в строке целевой функции,
    то можно получить другое оптимальное решение, изменив базис.

    В этой реализации, если найден такой столбец, производится попытка сделать поворот,
    а затем извлекается новое решение.
    Если поворот сделать невозможно, возвращается None.
    """
    m = len(tableau) - 1
    n = total_vars
    # Ищем не-базисный столбец j (то есть j не входит в basic_indices)
    # для которого коэффициент в строке целевой функции равен 0.
    for j in range(n):
        if j in basic_indices:
            continue
        if tableau[0][j] == Fraction(0):
            # Найдем строку, в которой можно осуществить поворот,
            # чтобы j стал базисной, при условии что коэффициент положительный (чтобы не нарушить оптимальность).
            candidate_row = -1
            for i in range(1, m + 1):
                # Для альтернативного решения часто ищут положительный коэффициент,
                # т.к. изменение базиса при коэффициенте 0 может сохранить оптимальность.
                if tableau[i][j] != Fraction(0):
                    candidate_row = i
                    break
            if candidate_row != -1:
                # Делаем поворот
                tableau_copy = [row[:] for row in tableau]  # делаем копию таблицы
                basic_copy = basic_indices.copy()
                try:
                    pivot(tableau_copy, basic_copy, candidate_row, j)
                    # После поворота проверим, сохранена ли оптимальность.
                    # Если правые части всех ограничений >= 0, решение допустимо.
                    feasible = all(tableau_copy[i][-1] >= Fraction(0) for i in range(1, m + 1))
                    if feasible:
                        return tableau_copy, basic_copy
                except Exception:
                    continue
    return None


def main():
    # Проверяем аргументы командной строки
    if len(sys.argv) < 2:
        print("Использование: python dual_simplex.py input.txt")
        sys.exit(1)

    filename = sys.argv[1]
    tableau = read_tableau(filename)
    print("Исходная симплекс-таблица:")
    print_tableau(tableau)

    # Определяем размеры таблицы
    total_rows = len(tableau)
    total_cols = len(tableau[0])
    total_vars = total_cols - 1  # число переменных (без свободного члена)
    m = total_rows - 1  # число ограничений

    # Предполагаем, что базис задаётся последними m столбцами
    # Например, если переменных 4 и m = 2, то базис = [2, 3]
    basic_indices = list(range(total_vars - m, total_vars))
    print("Начальный базис (индексы переменных):", basic_indices)

    # Применяем двойственный симплекс-метод.
    # Он итеративно улучшает решение, пока все правые части ограничений не будут неотрицательными.
    tableau, basic_indices = dual_simplex(tableau, basic_indices)
    print("Оптимизированная симплекс-таблица:")
    print_tableau(tableau)

    # Извлекаем оптимальное решение
    solution, optimum = extract_solution(tableau, basic_indices, total_vars)
    print("Оптимальное решение:")
    for i, val in enumerate(solution):
        print(f"x{i + 1} = {val}")
    print("Оптимальное значение целевой функции:", optimum)

    # Проверяем наличие альтернативных (оптимальных) решений.
    alt = find_alternative_solution(tableau, basic_indices, total_vars)
    if alt is not None:
        tableau2, basic_indices2 = alt
        solution2, _ = extract_solution(tableau2, basic_indices2, total_vars)
        print("\nНайдено альтернативное оптимальное решение:")
        for i, val in enumerate(solution2):
            print(f"x{i + 1} = {val}")
    else:
        print("\nАльтернативных оптимальных решений не найдено или их невозможно извлечь в данном варианте.")


if __name__ == "__main__":
    main()
