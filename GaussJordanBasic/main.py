import copy
import itertools
import math
import sys
from my_fraction import Fraction

class EquationSolver:
    def __init__(self, filename=""):
        if not filename:
            print("Error: Please provide a filename.")
            sys.exit(-1)

        try:
            with open(filename, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(-1)

        self.matrix = [
            [Fraction(int(x), 1) for x in line.split()]
            for line in lines
        ]

    def solve(self):
        self.display_matrix()

        for pivot_row in range(len(self.matrix)):
            if self.matrix[pivot_row][pivot_row] == Fraction(0, 1):
                continue

            for row in range(len(self.matrix)):
                for col in range(pivot_row + 1, len(self.matrix[row])):
                    if row != pivot_row:
                        self.matrix[row][col] -= (
                            self.matrix[pivot_row][col] * self.matrix[row][pivot_row]
                        ) / self.matrix[pivot_row][pivot_row]

            for col in range(len(self.matrix[pivot_row])):
                if col != pivot_row:
                    self.matrix[pivot_row][col] /= self.matrix[pivot_row][pivot_row]

            self.matrix[pivot_row][pivot_row] = Fraction(1, 1)

            for row in range(len(self.matrix)):
                if row != pivot_row:
                    self.matrix[row][pivot_row] = Fraction(0, 1)

            print()
            self.display_matrix()

        if not self.has_solutions():
            print("\nNo solution exists.")
            return

        if self.display_solution() > len(self.matrix[0][:-1]):
            self.display_general_solution()

        variables = len(self.matrix[0][:-1])
        rank = len(self.matrix)
        combinations = math.factorial(variables) // (
            math.factorial(rank) * math.factorial(variables - rank)
        )

        print(f"\nAll possible variable combinations ({combinations}):")
        indices = ''.join(str(x) for x in range(variables))
        combinations_list = [
            [int(x) for x in combo]
            for combo in itertools.combinations(indices, rank)
        ]

        for combo in combinations_list:
            print(''.join(f"x{x+1}" for x in combo))

        if len(combinations_list) > combinations:
            raise RuntimeError("Combination count mismatch.")

        print()

        for combo in combinations_list:
            matrix_copy = copy.deepcopy(self.matrix)
            print(''.join(f"x{x+1}" for x in combo))

            if any(all(row[x] == row[0] for x in combo) for row in matrix_copy):
                print("Solution: ∅\n")
                continue

            recalculate = True
            free_vars = [0] * len(matrix_copy)
            for col in combo:
                for row in range(len(matrix_copy)):
                    free_vars[row] |= (1 if matrix_copy[row][col] == 1 else 0)

            print()
            self.display_matrix(matrix_copy)

            while recalculate:
                pivot = 0
                for col in combo:
                    recalculate = False
                    for row in range(len(matrix_copy)):
                        if matrix_copy[row][col] not in (0, 1):
                            recalculate = True
                            try:
                                pivot = free_vars.index(0)
                            except ValueError:
                                break
                            break
                    if recalculate:
                        if pivot >= len(matrix_copy):
                            pivot = 0
                        for row in range(len(matrix_copy)):
                            for c in range(col + 1, len(matrix_copy[row])):
                                if row != pivot:
                                    matrix_copy[row][c] -= (
                                        matrix_copy[pivot][c] * matrix_copy[row][col]
                                    ) / matrix_copy[pivot][col]

                        for c in range(len(matrix_copy[pivot])):
                            if c != col:
                                matrix_copy[pivot][c] /= matrix_copy[pivot][col]

                        matrix_copy[pivot][col] = Fraction(1, 1)

                        for row in range(len(matrix_copy)):
                            if row != pivot:
                                matrix_copy[row][col] = Fraction(0, 1)

                        free_vars[pivot] = 1

                        print()
                        self.display_matrix(matrix_copy)

            solution = "("
            for col in range(len(matrix_copy[0][:-1])):
                if col in combo:
                    for row in range(len(matrix_copy)):
                        if matrix_copy[row][col] == 1:
                            solution += str(matrix_copy[row][-1]) + ";"
                else:
                    solution += "0;"
            solution = solution[:-1] + ")"

            print(f"Solution: {solution}\n")

    def is_unit(self, fraction):
        return abs(fraction.numerator) == 1 and abs(fraction.denominator) == 1

    def has_solutions(self):
        i = 0
        while i < len(self.matrix):
            max_val = max(self.matrix[i][:-1], key=lambda x: x.numerator)
            min_val = min(self.matrix[i][:-1], key=lambda x: x.numerator)

            if max_val.numerator == 0 and min_val.numerator == 0:
                if self.matrix[i][-1] == 0:
                    del self.matrix[i]
                    i -= 1
                    print()
                    self.display_matrix()
                else:
                    return False
            i += 1
        return True

    def display_matrix(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        max_len = [max(len(str(row[col])) for row in matrix) for col in range(len(matrix[0]))]
        max_width = max(max_len)

        for row in matrix:
            for item in row:
                print(f"{item:>{max_width + 2}}", end="")
            print()

    def display_solution(self):
        print("\nSolution:")
        total_vars = 0
        for row in self.matrix:
            vars_in_row = 0
            for col in range(len(row) - 1):
                if row[col].numerator:
                    print(f"{' + ' if vars_in_row else ''}", end="")
                    print(
                        f"{row[col].neg_sign() if self.is_unit(row[col]) else row[col]}x{col + 1}",
                        end=""
                    )
                    vars_in_row += 1
            print(f" = {row[-1]}")
            total_vars += vars_in_row
        return total_vars

    def display_general_solution(self):
        matrix_copy = copy.deepcopy(self.matrix)
        print("\nGeneral Solution:")
        pivot_indices = {}
        for i, row in enumerate(matrix_copy):
            vars_in_row = 0
            pivot_indices[i] = 0
            for j in range(len(row) - 1):
                if row[j].numerator:
                    if self.is_unit(row[j]):
                        pivot_indices[i] = j
                    vars_in_row += 1

            if vars_in_row > 1:
                vars_in_row = 0
                print(
                    f"{row[pivot_indices[i]].neg_sign()}x{pivot_indices[i] + 1} = ", end=""
                )
                for j in range(len(row) - 1):
                    if row[j].numerator and j != pivot_indices[i]:
                        row[j] *= Fraction(-1, 1)
                        print(f"{' + ' if vars_in_row else ''}", end="")
                        print(
                            f"{row[j].neg_sign() if self.is_unit(row[j]) else row[j]}x{j + 1}",
                            end=""
                        )
                        vars_in_row += 1
                if row[-1].numerator != 0:
                    print(f" + {row[-1]}")
                else:
                    print()
            else:
                print(
                    f"{row[j].neg_sign()}x{pivot_indices[i] + 1} = {row[-1]}"
                )

        free_vars = ", ".join(
            f"x{j + 1}" for j in range(len(matrix_copy[0]) - 1)
            if j not in pivot_indices.values()
        )
        if free_vars:
            print(f"{free_vars} - free variables")

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else input("Enter filename: ")
    solver = EquationSolver(filename)
    solver.solve()

if __name__ == "__main__":
    main()
