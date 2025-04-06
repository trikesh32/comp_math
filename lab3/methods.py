def left_rectangle_method(func, a, b, epsilon):
    def core(func, a, b, n):
        h = (b - a) / n
        summ = 0
        for i in range(n):
            summ += func(a + i * h)
        return summ * h

    n = 4
    prev = core(func, a, b, n)
    actual = core(func, a, b, n * 2)
    while abs(actual - prev)/(2**2 - 1) > epsilon:
        n *= 2
        prev = actual
        actual = core(func, a, b, n * 2)
    return "Метод левых прямоугольников", actual, n * 2


def right_rectangle_method(func, a, b, epsilon):
    def core(func, a, b, n):
        h = (b - a) / n
        summ = 0
        for i in range(1, n + 1):
            summ += func(a + i * h)
        return summ * h

    n = 4
    prev = core(func, a, b, n)
    actual = core(func, a, b, n * 2)
    while abs(actual - prev) / (2 ** 2 - 1) > epsilon:
        n *= 2
        prev = actual
        actual = core(func, a, b, n * 2)
    return "Метод правых прямоугольников", actual, n * 2


def mid_rectangle_method(func, a, b, epsilon):
    def core(func, a, b, n):
        h = (b - a) / n
        summ = 0
        for i in range(n):
            summ += func(a + h / 2 + i * h)
        return summ * h

    n = 4
    prev = core(func, a, b, n)
    actual = core(func, a, b, n * 2)
    while abs(actual - prev) / (2 ** 2 - 1) > epsilon:
        n *= 2
        prev = actual
        actual = core(func, a, b, n * 2)
    return "Метод средних прямоугольников", actual, n * 2


def trap_method(func, a, b, epsilon):
    def core(func, a, b, n):
        h = (b - a) / n
        summ = func(a) + func(b)
        for i in range(1, n):
            summ += 2 * func(a + i * h)
        return summ * h / 2

    n = 4
    prev = core(func, a, b, n)
    actual = core(func, a, b, n * 2)
    while abs(actual - prev) / (2 ** 2 - 1) > epsilon:
        n *= 2
        prev = actual
        actual = core(func, a, b, n * 2)
    return "Метод трапеций", actual, n * 2


def simpson_method(func, a, b, epsilon):
    def core(func, a, b, n):
        h = (b - a) / n
        summ = func(a) + func(b)
        for i in range(1, n):
            if i % 2 == 0:
                summ += 2 * func(a + i * h)
            else:
                summ += 4 * func(a + i * h)
        return summ * h / 3

    n = 4
    prev = core(func, a, b, n)
    actual = core(func, a, b, n * 2)
    while abs(actual - prev) / (2 ** 4 - 1) > epsilon:
        n *= 2
        prev = actual
        actual = core(func, a, b, n * 2)
    return "Метод Симпсона", actual, n * 2