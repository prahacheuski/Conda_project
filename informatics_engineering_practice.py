from functools import reduce
from math import fabs
from random import randint

initial_array = (2, 4, 7, 13, 22)
print("initial array: {}".format(initial_array))

product_of_initial_array = reduce(lambda pre_arg, post_arg: pre_arg * post_arg, initial_array, 1)
print("the direct product of initial array: {}\n".format(product_of_initial_array))

# constants
m = randint(1, 11)
x = randint(2, 22)
e = randint(3, 33)
print("constants: m = {}, x = {}, e = {}".format(m, x, e))

counted_array = []
for l in range(1, 7):
    inner_func = round(((((m / fabs(x)) ** 0.5) - e ** - m) * l + m), 1)
    counted_array.insert(l - 1, inner_func)
print("formula for calculating array elements: ((((m /|x|)**0.5)-e**-m)*l+m), where l = 1..6")
print("counted array: {}".format(counted_array))

sum_array = round(reduce(lambda pre_arg, post_arg: pre_arg + post_arg, counted_array, 1), 1)
print("algebraic sum of counted array: {}\n".format(sum_array))


def prod(arr1: list) -> int or float:
    return min(arr1) * max(arr1)


array_1 = [x * x for x in range(1, 7)]
array_2 = [x * x for x in range(1, 9)]
print("array with len = 6: {}".format(array_1))
print("array with len = 8: {}".format(array_2))
print("product of min and max value in first array: {}".format(prod(array_1)))
print("product of min and max value in second array: {}".format(prod(array_2)))
