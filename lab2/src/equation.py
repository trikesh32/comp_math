from typing import Callable
import matplotlib.pyplot as plt
import numpy as np


class Equation:
    def __init__(self, text: str, function: Callable, derivative: Callable, double_derivative: Callable):
        self.text= text
        self.function = function
        self.derivative = derivative
        self.double_derivative = double_derivative

    def draw(self, left: float, right: float):
        x = np.linspace(left, right)
        func = np.vectorize(self.function)(x)
        plt.gca().set_aspect('auto', adjustable='box')
        plt.title = f"График функции"
        plt.grid(True, which="both")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axhline(y=0, color='blue', label="y = 0")
        plt.plot(x, func, 'red', label=self.text)
        plt.legend(loc='best')
        plt.show()

    def single_root_exist(self, left: float, right: float):
        x_values = np.arange(left, right, 0.001)
        for x in x_values:
            if self.derivative(x) * self.derivative(left) < 0:
                return False
        return self.function(left) * self.function(right) < 0


    def find_lambda(self, left: float, right: float):
        x_values = np.arange(left, right, 0.001)
        maximum = 0
        for x in x_values:
            if abs(self.derivative(x)) > maximum:
                maximum = abs(self.derivative(x))
        if self.derivative(left) > 0:
            return - 1/ maximum
        return 1/ maximum



