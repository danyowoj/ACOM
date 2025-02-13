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

// Класс для работы с простыми дробями
class Fraction
{
public:
    int numerator;   // Числитель
    int denominator; // Знаменатель

    // Метод для упрощения дроби (сокращение на НОД)
    void simplify()
    {
        int gcdValue = calculate_gcd(abs(numerator), abs(denominator)); // Используем std::gcd
        numerator /= gcdValue;
        denominator /= gcdValue;
        if (denominator < 0)
        {
            // Если знаменатель отрицательный, делаем его положительным
            numerator *= -1;
            denominator *= -1;
        }
    }

public:
    // Конструктор для создания дроби
    Fraction(int num = 0, int denom = 1) : numerator(num), denominator(denom)
    {
        // Упрощаем дробь при создании
        simplify();
    }

    // Перегрузка оператора сложения
    Fraction operator+(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator + other.numerator * denominator, denominator * other.denominator);
    }

    // Перегрузка оператора вычитания
    Fraction operator-(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator - other.numerator * denominator, denominator * other.denominator);
    }

    // Перегрузка оператора умножения
    Fraction operator*(const Fraction &other) const
    {
        return Fraction(numerator * other.numerator, denominator * other.denominator);
    }

    // Перегрузка оператора деления
    Fraction operator/(const Fraction &other) const
    {
        return Fraction(numerator * other.denominator, denominator * other.numerator);
    }

    // Перегрузка оператора сравнения (равенство)
    bool operator==(const Fraction &other) const
    {
        return numerator == other.numerator && denominator == other.denominator;
    }

    // Перегрузка оператора сравнения (неравенство)
    bool operator!=(const Fraction &other) const
    {
        return !(*this == other);
    }

    // Перегрузка унарного минуса
    Fraction operator-() const
    {
        return Fraction(-numerator, denominator);
    }

    // Перегрузка оператора вывода для печати дроби
    friend std::ostream &operator<<(std::ostream &os, const Fraction &f)
    {
        if (f.denominator == 1)
        {
            // Если знаменатель равен 1, выводим только числитель
            os << f.numerator;
        }
        else
        {
            // Иначе выводим дробь в формате a/b
            os << f.numerator << "/" << f.denominator;
        }
        return os;
    }

    // Перегрузка оператора ввода для чтения дроби
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

// Функция для вывода матрицы на экран
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

// Функция для выполнения метода Жордана-Гаусса
void gaussJordan(std::vector<std::vector<Fraction>> &matrix)
{
    int m = matrix.size();        // Количество строк
    int n = matrix[0].size() - 1; // Количество переменных (столбцов без учета столбца свободных членов)

    for (int col = 0, row = 0; col < n && row < m; ++col)
    {
        // Поиск строки с максимальным элементом в текущем столбце (выбор главного элемента)
        int pivot = row;
        for (int i = row + 1; i < m; ++i)
        {
            if (abs(matrix[i][col].numerator) > abs(matrix[pivot][col].numerator))
            {
                pivot = i;
            }
        }

        // Если главный элемент равен нулю, пропускаем этот столбец
        if (matrix[pivot][col] == Fraction(0))
        {
            continue;
        }

        // Меняем местами текущую строку и строку с главным элементом
        std::swap(matrix[row], matrix[pivot]);

        // Делим текущую строку на главный элемент, чтобы получить 1 на диагонали
        Fraction div = matrix[row][col];
        for (int j = 0; j <= n; ++j)
        {
            matrix[row][j] = matrix[row][j] / div;
        }

        // Обнуляем элементы в текущем столбце для всех остальных строк
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

        // Выводим промежуточную матрицу после каждого шага
        printMatrix(matrix);
        ++row; // Переходим к следующей строке
    }
}

// Функция для определения и вывода решения системы
void solveSystem(const std::vector<std::vector<Fraction>> &matrix)
{
    int m = matrix.size();        // Количество строк
    int n = matrix[0].size() - 1; // Количество переменных

    std::vector<Fraction> solution(n, Fraction(0)); // Вектор для хранения решения

    for (int i = 0; i < m; ++i)
    {
        int col = 0;
        // Пропускаем нулевые элементы в строке
        while (col < n && matrix[i][col] == Fraction(0))
        {
            ++col;
        }

        if (col == n)
        {
            // Если все коэффициенты нулевые, но свободный член не нулевой
            if (matrix[i][n] != Fraction(0))
            {
                std::cout << "Система не имеет решений." << std::endl;
                return;
            }
        }
        else if (col < n)
        {
            // Если есть ненулевой коэффициент
            solution[col] = matrix[i][n]; // Записываем значение переменной
        }
    }

    // Выводим решение системы
    std::cout << "Решение системы:" << std::endl;
    for (int i = 0; i < n; ++i)
    {
        std::cout << "x" << i + 1 << " = " << solution[i] << std::endl;
    }
}

// Основная функция программы
int main()
{
    std::ifstream input("C:/Users/latsu/GitHub_projects/ACOM/input.txt"); // Открываем файл для чтения
    int m, n;
    input >> m >> n; // Читаем количество строк и переменных

    // Создаем матрицу коэффициентов
    std::vector<std::vector<Fraction>> matrix(m, std::vector<Fraction>(n + 1));

    // Заполняем матрицу данными из файла
    for (int i = 0; i < m; ++i)
    {
        for (int j = 0; j <= n; ++j)
        {
            input >> matrix[i][j];
        }
    }

    // Выводим исходную матрицу
    std::cout << "Исходная матрица:" << std::endl;
    printMatrix(matrix);

    // Применяем метод Жордана-Гаусса
    gaussJordan(matrix);

    // Находим и выводим решение системы
    solveSystem(matrix);

    return 0;
}
