import math
import methods

def f1(x):
    return 1/x

def f2(x):
    return x**2

def f3(x):
    return math.sin(x)

def f4(x):
    return -2 * x**3-5*x**2+7*x-13

def F1(x):
    return math.log(x)

def F2(x):
    return x ** 3 / 3

def F3(x):
    return -math.cos(x)

def F4(x):
    return -2 * x ** 4 / 4 - 5 * x **3 / 3 + 7 * x ** 2 / 2 - 13 * x

meth = [methods.left_rectangle_method, methods.mid_rectangle_method, methods.right_rectangle_method, methods.trap_method, methods.simpson_method]
funcs = [f1, f2, f3, f4]
Funcs = [F1, F2, F3, F4]

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
    Func = Funcs[choice - 1]
    a = float(input("Введи нижний предел интегрирования: "))
    b = float(input("Введи верхний предел интегрирования: "))
    try:
        func(a)
        func(b)
    except Exception as e:
        print("Функция неопределена на одном из концов интервалов")
        exit(0)
    eps = float(input("Введи погрешность: "))
    print()
    print(f"Точное значение интеграла: F(a)={Func(a)}, F(b)={Func(b)}, F(a)-F(b)={Func(b) - Func(a)}" )
    print()
    for m in meth:
        name, res, n = m(func, a, b, eps)
        print(name)
        print(f"Результат: {res}, количество отрезков: {n}")
        print()

