import math
import os
from sys import stdin, stdout

import numpy as np
import matplotlib.pyplot as plt


def linear_approximation(X, Y):
    sx = 0
    sxx = 0
    sy = 0
    sxy = 0
    for x, y in zip(X, Y):
        sx += x
        sxx += x * x
        sy += y
        sxy += x * y
    A = np.matrix([[len(X), sx], [sx, sxx]])
    B = np.matrix([[sy], [sxy]])
    res = np.linalg.solve(A, B)
    return res[0, 0], res[1, 0]


def square_approximation(X, Y):
    sx = 0
    sxx = 0
    sxxx = 0
    sxxxx = 0
    sy = 0
    sxy = 0
    sxxy = 0
    for x, y in zip(X, Y):
        sx += x
        sxx += x * x
        sxxx += x * x * x
        sxxxx += x * x * x * x
        sy += y
        sxy += x * y
        sxxy += x * x * y
    A = np.matrix([[len(X), sx, sxx], [sx, sxx, sxxx], [sxx, sxxx, sxxxx]])
    B = np.matrix([[sy], [sxy], [sxxy]])
    res = np.linalg.solve(A, B)
    return res[0, 0], res[1, 0], res[2, 0]


def cube_approximation(X, Y):
    sx = 0
    sxx = 0
    sxxx = 0
    sxxxx = 0
    sxxxxx = 0
    sxxxxxx = 0
    sy = 0
    sxy = 0
    sxxy = 0
    sxxxy = 0
    for x, y in zip(X, Y):
        sx += x
        sxx += x * x
        sxxx += x * x * x
        sxxxx += x * x * x * x
        sy += y
        sxy += x * y
        sxxy += x * x * y
        sxxxxx += x ** 5
        sxxxxxx += x ** 6
        sxxxy += x ** 3 * y
    A = np.matrix([
        [len(X), sx, sxx, sxxx],
        [sx, sxx, sxxx, sxxxx],
        [sxx, sxxx, sxxxx, sxxxxx],
        [sxxx, sxxxx, sxxxxx, sxxxxxx]
    ])
    B = np.matrix([[sy], [sxy], [sxxy], [sxxxy]])
    res = np.linalg.solve(A, B)
    return res[0, 0], res[1, 0], res[2, 0], res[3, 0]


def exponential_approximation(X, Y):
    new_y = []
    for y in Y:
        new_y.append(math.log(y))
    A, b = linear_approximation(X, new_y)
    return math.exp(A), b


def logarithmic_approximation(X, Y):
    new_x = []
    for x in X:
        new_x.append(math.log(x))
    return linear_approximation(new_x, Y)


def power_approximation(X, Y):
    new_y = []
    new_x = []
    for y in Y:
        new_y.append(math.log(y))
    for x in X:
        new_x.append(math.log(x))
    A, b = linear_approximation(new_x, new_y)
    return math.exp(A), b


def get_linear_approximation(X, Y):
    a, b =  linear_approximation(X, Y)
    return lambda x: a + b * x


def get_square_approximation(X, Y):
    a, b, c = square_approximation(X, Y)
    return lambda x: a + b * x + c * x ** 2


def get_cube_approximation(X, Y):
    a, b, c, d = cube_approximation(X, Y)
    return lambda x: a + b * x + c * x ** 2 + d * x ** 3


def get_exponential_approximation(X, Y):
    a, b = exponential_approximation(X, Y)
    return lambda x: a * np.exp(b * x)


def get_logarithmic_approximation(X, Y):
    a, b = logarithmic_approximation(X, Y)
    return lambda x: a * np.log(x) + b


def get_power_approximation(X, Y):
    a, b = power_approximation(X, Y)
    return lambda x: a * x ** b


def count_correlation(X, Y):
    mean_x = sum(X) / len(X)
    mean_y = sum(Y) / len(Y)
    numerator = sum([(X[i] - mean_x) * (Y[i]-mean_y) for i in range(len(X))])
    denominator = sum([(X[i] - mean_x)** 2 for i in range(len(X))]) * sum([(Y[i] - mean_y)** 2 for i in range(len(X))])
    r = numerator / math.sqrt(denominator)
    return r


def count_R2(Y, PHI):
    mean_phi = sum(PHI) / len(PHI)
    numerator = sum([(Y[i] - PHI[i])** 2 for i in range(len(Y))])
    denominator = sum([(Y[i] - mean_phi)** 2 for i in range(len(Y))])
    return 1 - numerator / denominator


def print_r_result(R):
    if R >= 0.95:
        print("Высокая аппроксимация")
    elif R >= 0.75:
        print("Удовлетворительная аппроксимация")
    elif R >= 0.5:
        print("Слабая аппроксимация")
    else:
        print("Вообще мимо по аппроксимации")


def count_sigma(PHI, Y):
    return math.sqrt(sum([(PHI[i]-Y[i]) ** 2 for i in range(len(PHI))])/len(PHI))

functions = [
    (linear_approximation, get_linear_approximation, "линейная", "{} + ({})x"),
    (square_approximation, get_square_approximation, "квадратичная", "{} + ({})x + ({})x^2"),
    (cube_approximation, get_cube_approximation, "кубическая", "{} + ({})x + ({})x^2 + ({})x^3"),
    (exponential_approximation, get_exponential_approximation, "показательная", "{}e^({})x"),
    (power_approximation, get_power_approximation, "степенная", "{}x^{}"),
    (logarithmic_approximation, get_logarithmic_approximation, "логарифмическая", "{}ln(x) + ({})")
]
def run(X, Y, file):
    lowest_x, highest_x = min(X), max(X)
    lowest_sigma = math.inf
    best_func = []
    plt.scatter(X, Y, label="Вводные точки")
    for get_coeffs, get_function, name, sample in functions:
        try:

            coeffs = get_coeffs(X, Y)
            func = get_function(X, Y)
            phi = [func(X[i]) for i in range(len(X))]
            eps = [phi[i] - Y[i] for i in range(len(X))]
            sigma = count_sigma(phi, Y)
            R = count_R2(phi, Y)
            print(name + ": phi(x)=" +sample.format(*coeffs), file=file)
            for i in range(len(X)):
                print(f"{X[i]:.3f}", end="\t", file=file)
            print("x", file=file)
            for i in range(len(Y)):
                print(f"{Y[i]:.3f}", end="\t", file=file)
            print("y", file=file)
            for i in range(len(phi)):
                print(f"{phi[i]:.3f}", end="\t", file=file)
            print("phi(x)", file=file)
            for i in range(len(eps)):
                print(f"{eps[i]:.3f}", end="\t", file=file)
            print("eps", file=file)
            if name == "линейная":
                cor = count_correlation(X, Y)
                print(f"Корреляция: {cor:.3f}", file=file)
            print(f"Детерминация: {R:.3f}", file=file)
            print_r_result(R)
            if lowest_sigma > sigma:
                lowest_sigma = sigma
                best_func = []
                best_func.append(name)
            elif lowest_sigma == sigma:
                best_func.append(name)
            print(f"Среднеквадратичное отклонение: {sigma:.3f}", file=file)
            x = np.linspace(lowest_x, highest_x, 400)
            y = np.ravel(func(x))
            plt.plot(x, y, label=name)
            print("-" * 30, file=file)
        except Exception as e:
            print(f"Ошибка приближения \"{name}\": {e}\n", file=file)
    print(f"Лучшии функция: {best_func}", file=file)
    print(f"Ее среднеквадратичное отклонение: {lowest_sigma}", file=file)

    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        try:
            X = []
            Y = []
            inp_filename = input("Введите файл для считывания (ENTER для ручного ввода): ")
            if inp_filename == "":
                print("Режим ручного ввода активирован.")
                file = stdin
            else:
                if not os.path.isfile(inp_filename):
                    raise FileNotFoundError(f"Файл {inp_filename} не найден.")
                file = open(inp_filename, "r")
            for line in file:
                if line.strip() == "":
                    continue
                numbers = line.strip().split()
                if len(numbers) != 2:
                    raise ValueError(
                        f"Строка '{line.strip()}' содержит нечётное количество чисел. Каждая строка должна содержать пару чисел (x, y).")
                X.append(float(numbers[0]))
                Y.append(float(numbers[1]))
            out_filename = input("Введите файл для вывода (ENTER для вывода в консоль): ")
            if out_filename == "":
                out = stdout
            else:
                out = open(out_filename, "w+")
            run(X, Y, out)
            file.close()
            out.close()
            break
        except FileNotFoundError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Ошибка: {e}. Попробуйте снова.")


if __name__ == "__main__":
    main()
