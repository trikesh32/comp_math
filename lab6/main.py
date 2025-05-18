import math
from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate

funcs = [
    ["y'= y/3 + 2x", lambda x, y: y / 3 + 2 * x,
     lambda x, x0, y0: ((y0 + 6 * x0 + 18) / math.exp(x0 / 3)) * math.exp(x / 3) - 6 * x - 18],
    ["y'= x + y", lambda x, y: x + y, lambda x, x0, y0: ((y0 + x0 + 1) / math.exp(x0)) * math.exp(x) - x - 1],
    ["y'= 2y + cos(x)", lambda x, y: 2 * y + math.cos(x),
     lambda x, x0, y0: ((y0 + 2 * math.cos(x0) / 5 - math.sin(x0) / 5) / (math.exp(2 * x0))) * math.exp(
         2 * x) + math.sin(x) / 5 - 2 * math.cos(x) / 5],
    ["y'= y + (1 + x)*y^2", lambda x, y: y + (1 + x) * y ** 2,
     lambda x, x0, y0: -math.exp(x) / (x * math.exp(x) - (x0 * math.exp(x0) * y0 + math.exp(x0)) / y0)]
]


def euler_method(func, x0, xn, y0, h):
    xs = [x0]
    ys = [y0]
    x = x0
    while x < xn and not math.isclose(x, xn):
        ys.append(ys[-1] + h * func(x, ys[-1]))
        x += h
        xs.append(x)
    return xs, ys


def modified_euler_method(func, x0, xn, y0, h):
    xs = [x0]
    ys = [y0]
    x = x0
    while x < xn and not math.isclose(x, xn):
        new_y = ys[-1] + h / 2 * (func(x, ys[-1]) + func(x + h, ys[-1] + h * func(x, ys[-1])))
        ys.append(new_y)
        x += h
        xs.append(x)
    return xs, ys


def milner_method(func, x0, xn, y0, h):
    xs = [x0]
    ys = [y0]
    for i in range(3):
        y_i = ys[-1]
        x_i = xs[-1]
        k1 = h * func(x_i, y_i)
        k2 = h * func(x_i + h / 2, y_i + k1 / 2)
        k3 = h * func(x_i + h / 2, y_i + k2 / 2)
        k4 = h * func(x_i + h, y_i + k3)
        new_y = y_i + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        ys.append(new_y)
        xs.append(x_i + h)
    while xs[-1] < xn and not math.isclose(xs[-1], xn):
        y_pred = ys[-4] + 4 * h / 3 * (2 * func(xs[-3], ys[-3]) - func(xs[-2], ys[-2]) + 2 * func(xs[-1], ys[-1]))
        y_corr = ys[-2] + h / 3 * (func(xs[-2], ys[-2]) + 4 * func(xs[-1], ys[-1]) + func(xs[-1] + h, y_pred))
        ys.append(y_corr)
        xs.append(xs[-1] + h)
    return xs, ys


def draw_plot(xs, ys, func, name, func_name):
    plt.clf()
    func_x = np.linspace(xs[0], xs[-1], 400)
    func_y = []
    for x in func_x:
        func_y.append(func(x, xs[0], ys[0]))
    plt.plot(func_x, func_y, 'r', label=func_name)
    plt.scatter(xs, ys, color='b')
    plt.title(name)
    plt.grid(True)
    plt.legend()
    plt.show()


methods = [
    ["Метод Эйлера", euler_method, 1, 2],
    ["Модифицированный метод Эйлера", modified_euler_method, 2, 2],
    ["Метод Милна", milner_method, None, 5]
]


def run(uravn, x0, xn, y0, normal_h, eps):
    func_name = uravn[0]
    func = uravn[1]
    original_func = uravn[2]
    for method in methods:
        method_name = method[0]
        method_func = method[1]
        method_accuracy = method[2]
        method_min_points = method[3]
        print(method_name)
        h = normal_h
        if (xn - x0) / h + 1 < method_min_points:
            print("Слишком большой шаг для такого отрезка")
            print("Минимальное число точек на отрезке для данного метода - ", method_min_points)
            h = (xn - x0) / (method_min_points - 1)
            print("Автоматически назначенный начальный шаг: ", h)
        if method_accuracy is not None:
            while True:
                xs_h, ys_h = method_func(func, x0, xn, y0, h)
                xs_h05, ys_h05 = method_func(func, x0, xn, y0, h / 2)
                inaccuracy = abs(ys_h[-1] - ys_h05[-1]) / (2 ** method_accuracy - 1)
                if inaccuracy < eps:
                    print("Достаточная точность получилась при шаге: ", h / 2)
                    print("Погрешность: ", inaccuracy)
                    print(tabulate(list(zip(xs_h05, ys_h05, [original_func(xs_h05[i], xs_h05[0], ys_h05[0]) for i in
                                                             range(len(xs_h05))])), headers=["x", "y", "y_true"]))
                    draw_plot(xs_h05, ys_h05, original_func, method_name, func_name)
                    break
                h /= 2
                if h < 1e-6:
                    print("Я отказываюсь дальше решать этот ужас")
                    break
        else:
            while True:
                xs_h, ys_h = method_func(func, x0, xn, y0, h)
                inaccuracy = max([abs(original_func(xs_h[i], xs_h[0], ys_h[0]) - ys_h[i]) for i in range(len(xs_h))])
                if inaccuracy < eps:
                    print("Достаточная точность получилась при шаге: ", h)
                    print("Погрешность: ", inaccuracy)
                    print(tabulate(
                        list(zip(xs_h, ys_h, [original_func(xs_h[i], xs_h[0], ys_h[0]) for i in range(len(xs_h))])),
                        headers=["x", "y", "y_true"]))
                    draw_plot(xs_h, ys_h, original_func, method_name, func_name)
                    break
                h /= 2
                if h < 1e-6:
                    print("Я отказываюсь дальше решать этот ужас")
                    break
        print("---------------------------------------------------------------------")


def main():
    for i in range(len(funcs)):
        print(i + 1, ". ", funcs[i][0])
    while True:
        try:
            uravn = funcs[int(input("Ваш выбор: ")) - 1]
            break
        except Exception:
            print("Невалидный выбор!")
    x0 = float(input("Введите нижнюю границу отрезка: "))
    xn = float(input("Введите верхнюю границу отрезка: "))
    y0 = float(input("Введите y0 = y(x0): "))
    h = float(input("Введите начальный шаг: "))
    eps = float(input("Введите точность: "))
    run(uravn, x0, xn, y0, h, eps)


if __name__ == "__main__":
    main()
