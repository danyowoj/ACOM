#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <sstream>

int calculate_gcd(int a, int b)
{
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

class Fraction
{
public:
    int numerator;
    int denominator;

    void simplify()
    {
        int gcdValue = calculate_gcd(abs(numerator), abs(denominator)); // Используем std::gcd
        numerator /= gcdValue;
        denominator /= gcdValue;
        if (denominator < 0)
        {
            numerator *= -1;
            denominator *= -1;
        }
    }

public:
    Fraction(int num = 0, int denom = 1) : numerator(num), denominator(denom)
    {
        simplify();
    }

    Fraction operator+(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator + other.numerator * denominator, denominator * other.denominator);
    }

    Fraction operator-(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator - other.numerator * denominator, denominator * other.denominator);
    }

    Fraction operator*(const Fraction &other) const
    {
        return Fraction(numerator * other.numerator, denominator * other.denominator);
    }

    Fraction operator/(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator, denominator * other.numerator);
    }

    bool operator==(const Fraction &other) const
    {
        return numerator == other.numerator && denominator == other.denominator;
    }

    bool operator!=(const Fraction &other) const
    {
        return !(*this == other);
    }

    Fraction operator-() const
    {
        return Fraction(-numerator, denominator);
    }

    friend std::ostream &operator<<(std::ostream &os, const Fraction &f)
    {
        if (f.denominator == 1)
        {
            os << f.numerator;
        }
        else
        {
            os << f.numerator << "/" << f.denominator;
        }
        return os;
    }

    friend std::istream &operator>>(std::istream &is, Fraction &f)
    {
        std::string input;
        is >> input; // Считываем входные данные как строку

        size_t slashPos = input.find('/'); // Ищем символ '/'
        if (slashPos == std::string::npos)
        {
            // Если '/' нет, значит это целое число
            f.numerator = std::stoi(input); // Преобразуем строку в целое число
            f.denominator = 1;              // Знаменатель равен 1
        }
        else
        {
            // Если '/' есть, значит это дробь
            f.numerator = std::stoi(input.substr(0, slashPos));    // Числитель
            f.denominator = std::stoi(input.substr(slashPos + 1)); // Знаменатель
        }

        f.simplify(); // Упрощаем дробь
        return is;
    }
};

void printMatrix(const std::vector<std::vector<Fraction>> &matrix)
{
    for (const auto &row : matrix)
    {
        for (const auto &elem : row)
        {
            std::cout << elem << "\t";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void gaussJordan(std::vector<std::vector<Fraction>> &matrix)
{
    int m = matrix.size();
    int n = matrix[0].size() - 1;

    for (int col = 0, row = 0; col < n && row < m; ++col)
    {
        int pivot = row;
        for (int i = row + 1; i < m; ++i)
        {
            if (abs(matrix[i][col].numerator) > abs(matrix[pivot][col].numerator))
            {
                pivot = i;
            }
        }

        if (matrix[pivot][col] == Fraction(0))
        {
            continue;
        }

        std::swap(matrix[row], matrix[pivot]);

        Fraction div = matrix[row][col];
        for (int j = 0; j <= n; ++j)
        {
            matrix[row][j] = matrix[row][j] / div;
        }

        for (int i = 0; i < m; ++i)
        {
            if (i != row)
            {
                Fraction mult = matrix[i][col];
                for (int j = 0; j <= n; ++j)
                {
                    matrix[i][j] = matrix[i][j] - mult * matrix[row][j];
                }
            }
        }

        printMatrix(matrix);
        ++row;
    }
}

void solveSystem(const std::vector<std::vector<Fraction>> &matrix)
{
    int m = matrix.size();
    int n = matrix[0].size() - 1;

    std::vector<Fraction> solution(n, Fraction(0));

    for (int i = 0; i < m; ++i)
    {
        int col = 0;
        while (col < n && matrix[i][col] == Fraction(0))
        {
            ++col;
        }

        if (col == n)
        {
            if (matrix[i][n] != Fraction(0))
            {
                std::cout << "Система не имеет решений." << std::endl;
                return;
            }
        }
        else if (col < n)
        {
            solution[col] = matrix[i][n];
        }
    }

    std::cout << "Решение системы:" << std::endl;
    for (int i = 0; i < n; ++i)
    {
        std::cout << "x" << i + 1 << " = " << solution[i] << std::endl;
    }
}

int main()
{
    std::ifstream input("C:/Users/latsu/GitHub_projects/input.txt");
    int m, n;
    input >> m >> n;

    std::vector<std::vector<Fraction>> matrix(m, std::vector<Fraction>(n + 1));

    for (int i = 0; i < m; ++i)
    {
        for (int j = 0; j <= n; ++j)
        {
            input >> matrix[i][j];
        }
    }

    std::cout << "Исходная матрица:" << std::endl;
    printMatrix(matrix);

    gaussJordan(matrix);
    solveSystem(matrix);

    return 0;
}
