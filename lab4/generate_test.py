import random
import math
f = lambda x: 2.45 * math.exp(1.543 * x)
trash = 0
start_x = 1
end_x =5
n = 10
filename = "exp_test2.txt"



x = start_x
file = open(filename, "w+")
h = (end_x - start_x) / (n - 1)
while x <= end_x:
    y = f(x) - trash/2 + trash * random.random()
    file.write(str(x) + " " + str(y) + "\n")
    x += h
file.close()

