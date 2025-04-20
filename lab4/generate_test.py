import random
import math
f = lambda x: 12 * math.log(x) + 12.3323221
trash = 6
start_x = 1
end_x = 20
n = 12
filename = "log_test3.txt"



x = start_x
file = open(filename, "w+")
h = (end_x - start_x) / (n - 1)
while x <= end_x:
    y = f(x) - trash/2 + 3 * random.random()
    file.write(str(x) + " " + str(y) + "\n")
    x += h
file.close()

