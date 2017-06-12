from random import randint
from math import ceil, floor

rand_list_1 = list(map(lambda x: randint(0, x + 1), range(100)))
rand_list_2 = [randint(0, x + 1) for x in range(100)]
floating_list = [float(str(rand_1_val) + "." + str(rand_2_val)) for rand_1_val, rand_2_val
                 in zip(rand_list_1, rand_list_2)]

array = [rand_list_1, rand_list_2, floating_list]

pos = 0

for item in zip(*array):
    pos += 1
    print("Position #{} and random value {}".format(pos, item))
