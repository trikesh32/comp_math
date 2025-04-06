import math
import methods

def f1(x):
    return x

def f2(x):
    return x**2

def f3(x):
    return math.sin(x)

def f4(x):
    return -2 * x**3-5*x**2+7*x-13

meth = [methods.left_rectangle_method, methods.mid_rectangle_method, methods.right_rectangle_method, methods.trap_method, methods.simpson_method]
funcs = [f1, f2, f3, f4]

while True:
    print("""Выбирай функцию которую хочешь проинтегрировать
1. y = x
2. y = x^2
3. y = sin(x)
4. y = -2x^3 - 5x^2 + 7x - 13""")
    choice = int(input("Твой выбор: "))
    if choice not in [1, 2, 3, 4]:
        print("Мне не нравится твой выбор, делай заново")
        continue
    func = funcs[choice - 1]
    a = float(input("Введи нижний предел интегрирования: "))
    b = float(input("Введи верхний предел интегрирования: "))
    eps = float(input("Введи погрешность: "))
    for m in meth:
        name, res, n = m(func, a, b, eps)
        print(name)
        print(f"Результат: {res}, количество отрезков: {n}")
        print()

