import numpy as np
import sympy as sp

from src.equation import Equation
from sys import __stdout__


def half_divide_method(equation: Equation):
    while True:
        print("Как будем вводить данные?")
        print("1. С клавиатуры")
        print("2. С файла")
        print("0. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            while True:
                try:
                    a = float(input("Введите границу отрезка a: "))
                    b = float(input("Введите границу отрезка b: "))
                    epsilon = float(input("Введите погрешность: "))
                    if a < b and a != b:
                        break
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
                except ValueError:
                    print("Ошибка: вводите только числа.")
        elif choice == "2":
            file_name = input("Введите имя файла: ").strip()
            try:
                with open(file_name, "r") as file:
                    a, b = map(float, file.readline().split())
                    if a < b and a != b:
                        return a, b
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
            except FileNotFoundError:
                print("Ошибка: файл не найден.")
            except ValueError:
                print("Ошибка: неверный формат данных в файле.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            return None
        else:
            print("Не понял")
            continue
        if not equation.single_root_exist(a, b):
            print("На данном отрезеке нет корня или их больше одного")
            continue
        break
    equation.draw(a, b)
    file = input("Введите файл для вывода (Нажмите ENTER для вывод в консоль): ")
    if file == '':
        file = __stdout__
    else:
        file = open(file, "w+")
    x_prev = (a + b) / 2
    counter = 0
    while True:
        counter += 1
        if (equation.function(x_prev) * equation.function(a) < 0):
            b = x_prev
        else:
            a = x_prev
        x = (a + b) / 2
        print(f"Номер итерации {counter}", file=file)
        print(f"Новые границы: {[a, b]}", file=file)
        print(f"Значение x_{counter} = {x}", file=file)
        print(f"Значение функции в точке x_{counter}: {equation.function(x)}", file=file)
        print(f"Погрешность: {abs(x - x_prev)}", file=file)
        if (abs(x - x_prev) < epsilon):
            break
        x_prev = x
    print(file=file)


def secant_method(equation: Equation):
    while True:
        print("Как будем вводить данные?")
        print("1. С клавиатуры")
        print("2. С файла")
        print("0. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            while True:
                try:
                    a = float(input("Введите границу отрезка a: "))
                    b = float(input("Введите границу отрезка b: "))
                    epsilon = float(input("Введите погрешность: "))
                    if a < b and a != b:
                        break
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
                except ValueError:
                    print("Ошибка: вводите только числа.")
        elif choice == "2":
            file_name = input("Введите имя файла: ").strip()
            try:
                with open(file_name, "r") as file:
                    a, b = map(float, file.readline().split())
                    if a < b and a != b:
                        return a, b
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
            except FileNotFoundError:
                print("Ошибка: файл не найден.")
            except ValueError:
                print("Ошибка: неверный формат данных в файле.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            return None
        else:
            print("Не понял")
            continue
        if not equation.single_root_exist(a, b):
            print("На данном отрезеке нет корня или их больше одного")
            continue
        break
    equation.draw(a, b)
    file = input("Введите файл для вывода (Нажмите ENTER для вывод в консоль): ")
    if file == '':
        file = __stdout__
    else:
        file = open(file, "w+")
    x_prev_prev = a
    x_prev = b
    counter = 0
    while True:
        counter += 1
        x = x_prev - (x_prev - x_prev_prev)*equation.function(x_prev)/(equation.function(x_prev) - equation.function(x_prev_prev))
        print(f"Номер итерации {counter}", file=file)
        print(f"Значение x_{counter} = {x}", file=file)
        print(f"Значение функции в точке x_{counter}: {equation.function(x)}", file=file)
        print(f"Погрешность: {abs(x - x_prev)}", file=file)
        if (abs(x - x_prev) < epsilon):
            break
        x_prev_prev = x_prev
        x_prev = x

    print(file=file)


def simple_iteration_method(equation: Equation):
    while True:
        print("Как будем вводить данные?")
        print("1. С клавиатуры")
        print("2. С файла")
        print("0. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            while True:
                try:
                    a = float(input("Введите границу отрезка a: "))
                    b = float(input("Введите границу отрезка b: "))
                    epsilon = float(input("Введите погрешность: "))
                    if a < b and a != b:
                        break
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
                except ValueError:
                    print("Ошибка: вводите только числа.")
        elif choice == "2":
            file_name = input("Введите имя файла: ").strip()
            try:
                with open(file_name, "r") as file:
                    a, b = map(float, file.readline().split())
                    if a < b and a != b:
                        return a, b
                    else:
                        print("Ошибка: a должно быть меньше b и они не должны быть равны.")
            except FileNotFoundError:
                print("Ошибка: файл не найден.")
            except ValueError:
                print("Ошибка: неверный формат данных в файле.")
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "0":
            return None
        else:
            print("Не понял")
            continue
        if not equation.single_root_exist(a, b):
            print("На данном отрезеке нет корня или их больше одного")
            continue
        break
    equation.draw(a, b)
    file = input("Введите файл для вывода (Нажмите ENTER для вывод в консоль): ")
    if file == '':
        file = __stdout__
    else:
        file = open(file, "w+")
    l = equation.find_lambda(a, b)
    phi = lambda x: x + l * equation.function(x)
    phi_derivative = lambda x: 1 + l * equation.derivative(x)
    for x in np.arange(a, b, 0.001):
        if abs(phi_derivative(x)) >= 1:
            print("Функция не сходится на данном отрезке", file=file)
            return None
    if equation.double_derivative(a) * equation.function(a) > 0:
        x_prev = a
    else:
        x_prev = b
    print(f"Начальное приближение x0 = {x_prev}", file=file)
    counter = 0
    while True:
        counter += 1
        x = phi(x_prev)
        print(f"Номер итерации {counter}", file=file)
        print(f"Значение x_{counter} = {x}", file=file)
        print(f"Значение функции в точке x_{counter}: {equation.function(x)}", file=file)
        print(f"Погрешность: {abs(x - x_prev)}", file=file)
        if (abs(x - x_prev) < epsilon):
            break
        x_prev = x

    print(file=file)