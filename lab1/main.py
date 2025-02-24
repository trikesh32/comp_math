from sys import stdin

import numpy as np
from exceptions import *

def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print("{:.3f}".format(col), end='\t')
        print()

def read_matrix_from_keyboard():
    matrix = []
    n = int(input("Количество уравнений (не более 20): "))
    if n > 20:
        raise TooBigDimensionException
    print("""Введите уравнения по типу этого:
a11 a12 ... a1N b1
 .   .   .   .  .
aN1 aN2 ... aNN bN""")
    for i in range(n):
        matrix.append(list(map(float, input().split())))
        if len(matrix[-1]) != n + 1:
            raise BadMatrixEnteredException
    return matrix


def read_matrix_from_file(path):
    matrix = []
    file = open(path, "r")
    n = int(file.readline())
    if n > 20:
        raise TooBigDimensionException
    for i in range(n):
        matrix.append(list(map(float, file.readline().split())))
        if len(matrix[-1]) != n + 1:
            raise BadMatrixEnteredException
    return matrix


def change_lines(matrix, i, j):
    for k in range(len(matrix[0])):
        tmp = matrix[i][k]
        matrix[i][k] = matrix[j][k]
        matrix[j][k] = tmp
    return matrix


def find_line_with_max_element(matrix, i):
    maximum = abs(matrix[i][i])
    res = i
    for j in range(i, len(matrix)):
        if abs(matrix[j][i]) > maximum:
            maximum = matrix[j][i]
            res = j
    print("Максимальный элемент: ", maximum)
    if maximum == 0:
        return -1
    return res


def kill_elements_under(matrix, i):
    for j in range(i + 1, len(matrix)):
        multiplier = matrix[j][i] / matrix[i][i]
        for k in range(i, len(matrix[0])):
            matrix[j][k] -= multiplier * matrix[i][k]
    return matrix


def make_triangle_matrix(matrix):
    k = 0
    for i in range(len(matrix) - 1):
        print(f"Итерация: {i+1}")
        maximum_index = find_line_with_max_element(matrix, i)
        if maximum_index == -1:
            print("Наибольший модуль 0 => на главной диагонали 0 => определитель 0 => нет решений")
            return -1
        print(f"Номер строки с наибольшим модулем: ", maximum_index)
        if maximum_index != i:
            matrix = change_lines(matrix, maximum_index, i)
            print("Меняем местами строки")
            print_matrix(matrix)
            k+=1
        print("Вычтем строки: ")
        matrix = kill_elements_under(matrix, i)
        print_matrix(matrix)
    print("Количество перестановок: ", k)
    return k


def count_determinant(matrix, k):
    res = 1
    for i in range(len(matrix)):
        res *= matrix[i][i]
    return ((-1) ** k) * res


def find_roots(matrix):
    results = []
    for i in range(len(matrix) - 1, -1, -1):
        root = matrix[i][-1]
        for k, j in enumerate(range(i + 1, len(matrix))):
            root -= matrix[i][j] * results[k]
        results.insert(0, root / matrix[i][i])
    return results


def find_problem_vector(matrix, x):
    result = []
    for i in range(len(matrix)):
        temp = 0
        for j in range(len(matrix)):
            temp += matrix[i][j] * x[j]
        result.append(temp - matrix[i][-1])
    return result


def library_solve(matrix):
    A = []
    B = []
    for i in range(len(matrix)):
        B.append(matrix[i][-1])
        A.append([])
        for j in range(len(matrix)):
            A[i].append(matrix[i][j])
    A = np.array(A)
    B = np.array(B)
    det_A = np.linalg.det(A)
    print("Определитель: ", det_A)
    if det_A != 0:
        solution = np.linalg.solve(A, B)
        print(solution)
        print("Вектор неувязки:")
        print(np.dot(A, solution) - B)
    else:
        print("Решений нет, либо бесконечно много")


def main():
    while True:
        print("0. Для выхода с программы")
        print("1. Считать матрицу с клавиатуры")
        print("2. Считать матрицу с файла")
        option = input("Ваш выбор: ")
        try:
            if option == "0":
                break
            elif option == "1":
                matrix = read_matrix_from_keyboard()
                print_matrix(matrix)
            elif option == "2":
                path = input("Введите путь до файла с матрицей: ")
                matrix = read_matrix_from_file(path)
                print_matrix(matrix)
            else:
                print("Понятия не имею что это значит...")
                continue
            original_matrix = [row[:] for row in matrix]
            k = make_triangle_matrix(matrix)
            if k == -1:
                continue
            determinant = count_determinant(matrix, k)
            print(f"Определитель: {determinant}")
            if determinant == 0:
                print("Значит решений нет или их бесконечно много")
                return 0
            print("Найденное решение:")
            x = find_roots(matrix)
            print_matrix([x])
            print("Вектор неувязки:")
            print("\t".join(map(str, find_problem_vector(original_matrix, x))))
            print("----------------")
            print("Найдем решение с помощью библиотеки Numpy")
            library_solve(original_matrix)

        except TooBigDimensionException:
            print("Слишком большая размерность")
        except BadMatrixEnteredException:
            print("Проверьте корректность матрицы")
        except ValueError:
            print("Вводите чиселки, пожалуйста...")
        except EOFError:
            print("Недостаточно введенных данных")
        except FileNotFoundError:
            print("Не смог найти такой файл((")


if __name__ == "__main__":
    main()