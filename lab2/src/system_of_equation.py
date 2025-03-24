from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import epsilon


class SystemOfEquation:
    def __init__(self, first_function: Callable, second_function: Callable, df_dx: Callable, df_dy: Callable, dg_dx: Callable, dg_dy: Callable, text1: str, text2: str):
        self.jacobian = lambda x, y: np.array([[df_dx(x, y), df_dy(x, y)], [dg_dx(x, y), dg_dy(x, y)]])
        self.first_function = first_function
        self.second_function = second_function
        self.text1 = text1
        self.text2 = text2

    def draw(self):
        x = np.linspace(-5, 5, 400)
        y = np.linspace(-5, 5, 400)
        X, Y = np.meshgrid(x, y)

        Z1 = np.array([self.first_function(x_, y_) for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)
        Z2 = np.array([self.second_function(x_, y_) for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.contour(X, Y, Z1, levels=[0], colors='r')
        plt.contour(X, Y, Z2, levels=[0], colors='b')
        plt.grid(True, which="both")
        line1 = plt.Line2D([0], [0], color='r', label=self.text1)
        line2 = plt.Line2D([0], [0], color='b', label=self.text2)

        plt.legend(handles=[line1, line2], loc='best')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def solve(self):
        self.draw()
        print("Введите погрешность (нажмите ENTER для погрешности по умолчанию 0.01): ")
        while True:
            inp = input()
            if inp == '':
                epsilon = 0.01
                break
            else:
                try:
                    epsilon = float(inp)
                    break
                except Exception:
                    print("Упс попробуйте еще пожалуйста")
                    continue

        print("Введите начальное приблежение через пробел: ")
        while True:
            try:
                x, y = map(float, input().split())
                break
            except Exception:
                print("Упс попробуйте еще пожалуйста")
                continue
        prev_x = x
        prev_y = y
        counter = 0
        while True:
            counter += 1
            F = np.array([self.first_function(prev_x, prev_y), self.second_function(prev_x, prev_y)])
            J = self.jacobian(prev_x, prev_y)
            J_inv = np.linalg.inv(J)
            delta = J_inv @ F
            x = prev_x - delta[0]
            y = prev_y - delta[1]
            print(f"Итерация {counter}")
            print("Вектор неизвестных: ", [x, y])
            print("Вектор погрешностей: ", [abs(prev_x - x), abs(prev_y - y)])
            if abs(prev_x - x) < epsilon and abs(prev_y - y) < epsilon:
                break
            prev_x = x
            prev_y = y
        print(f"Всего потрачено {counter} итераций")
        print(f"Проверим правильность решения при x={x}, y={y}")
        print(f"f(x, y)={self.first_function(x, y)}")
        print(f"g(x, y)={self.second_function(x, y)}")
        print("Выводы делайте сами")

