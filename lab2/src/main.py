from math import sin, cos
from equation import Equation
from system_of_equation import SystemOfEquation
from methods import *

systems = {
    1: SystemOfEquation(lambda x, y: sin(y) + 2 * x - 2, lambda x, y: y + cos(x - 1) - 0.7, lambda x, y: 2, lambda x, y: cos(y), lambda x, y: -sin(x-1), lambda x, y: 1, "sin(y) + 2x = 2", "y + cos(x - 1) = 0.7"),
    2: SystemOfEquation(lambda x, y: x + sin(y) + 0.4, lambda x, y: 2 * y - cos(x + 1),  lambda x, y: 1, lambda x, y: cos(y), lambda x, y: sin(x + 1), lambda x, y: 2, "x + sin(y) = -0.4", "2y - cos(x + 1) = 0")
}
equations = {
    1: Equation("x^3 + 4.81x^2 - 17.37x + 5.38", lambda x: x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38,
                lambda x: 3 * x ** 2 + 9.62 * x - 17.37, lambda x, y: 6 * x + 9.62),
    2: Equation("4.45x^3 + 7.81x^2 - 9.62x - 8.17", lambda x: 4.45 * x ** 3 + 7.81 * x ** 2 - 9.62 * x - 8.17,
                lambda x: 4.45 * 3 * x ** 2 + 7.81 * 2 * x - 9.62, lambda x: 4.45 * 6 * x + 7.81 * 2),
    3: Equation("sin(x) - x + 1", lambda x: sin(x) - x + 1,
                lambda x: cos(x) - 1, lambda x: -sin(x))
}


while True:
    print("""Что вы хотите сделать?
1. Решить нелинейное уравнение
2. Решить систему нелинейных уравнений методом Ньютона.
0. Выйти""")
    choice = input("Ваш выбор: ")
    if choice == "0":
        break
    elif choice == "1":
        print("Выберите уравнение которое вы хотите решить:")
        print(f"1. {equations[1].text}")
        print(f"2. {equations[2].text}")
        print(f"3. {equations[3].text}")
        print("0. Назад")
        choice = input("Ваш выбор: ")
        if choice == "0":
            continue
        elif choice == "1" or choice == "2" or choice == "3":
            equation = equations[int(choice)]
        else:
            continue
        print("Выберите способ решения:")
        print(f"1. Метод половинного деления")
        print(f"2. Метод секущих")
        print(f"3. Метод простой итерации")
        print("0. Назад")
        choice = input("Ваш выбор: ")
        if choice == "0":
            continue
        elif choice == "1":
            half_divide_method(equation)
        elif choice == "2":
            secant_method(equation)
        elif choice == "3":
            simple_iteration_method(equation)

    elif choice == "2":
        print("Выберите систему которую вы хотите решить:")
        print(f"1. ({systems[1].text1}, {systems[1].text2})")
        print(f"2. ({systems[2].text1}, {systems[2].text2})")
        print("0. Назад")
        choice = input("Ваш выбор: ")
        if choice == "1":
            systems[1].solve()
        elif choice == "2":
            systems[2].solve()
        else:
            continue