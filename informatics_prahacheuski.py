# _*_ coding:utf-8 _*_
"""
Matrix range: 6 <= m = n >= 18
Variable R is random float in range from 45 to 50
Variable x(value) is (value plus random float in range from 1 to 5) multiply with random float in range from 1 to 5
Variable y(value) is (value minus random float in range from 1 to 5) multiply with random float in range from 1 to 5
Used 1 num after comma
"""
from math import sin, cos
from random import randint, uniform
from copy import deepcopy

# Constants
R = uniform(45, 50)
m = n = randint(6, 18)

# Nums after comma
nums_after_comma = 1

# Matrix a
a = []

# Amount of all positive elements
q = 0

# Amount of all negative elements
z = 0

# The sum of all positive elements
P = 0

# Product of all negative elements
S = 1


# Global precondition
def variable_range(value: int or float) -> bool:
    if value in range(6, 19):
        return True
    else:
        return False


# Variable x
def x(value: int or float) -> int or float:
    return (value + uniform(1, 5)) * uniform(1, 5)


# Variable y
def y(value: int or float) -> int or float:
    return (value - uniform(1, 5)) * uniform(1, 5)


# Main variable
def gamma(value: int or float) -> int or float:
    return (R * x(value)) / (value + cos(R)) + sin(y(value))


# Crossroad
def crossroad(i, j: int or float) -> int or float:
    # condition if gamma <
    if gamma(i) < (4 + ((x(i) / R) * y(i))):
        return (sin(x(j)) / (R * j)) + R
    # condition if gamma =
    elif gamma(i) == (4 + ((x(i) / R) * y(i))):
        return (cos(gamma(i)) / (i * R)) - 2.9
    # condition if gamma >
    elif gamma(i) > (4 + ((x(i) / R) * y(i))):
        return y(i) * x(i)


# Return len of number
def return_len(value: int or float) -> int:
    _int = str(value)
    _len = len(_int)
    return _len + nums_after_comma


# Return maximum len from array
def max_len(array: list) -> int:
    return max(return_len(column) for row in array for column in row)


# Main condition
if variable_range(m):
    for row in range(m):
        a.append([])
        for column in range(n):
            value = crossroad(row + 1, column + 1)
            if value is not None:
                new_value = round(value, nums_after_comma)
                if new_value > 0:
                    q += 1
                    P += new_value
                elif new_value < 0:
                    z += 1
                    S *= new_value
            else:
                new_value = 0
            a[row].append(new_value)


# Count P_1, P_m, S_1, S_n -> return a list with results in this order
def counter(array: list) -> list:
    # The sum of elements in row #1
    P_1 = 0

    # The sum of elements in last row
    P_m = 0

    # The sum of elements in column #1
    S_1 = 0

    # The sum of elements in last column
    S_n = 0

    number_of_row = 0

    for row in array:

        number_of_element = 0

        for element in row:
            if number_of_row == 0:
                P_1 += element
            elif number_of_row == (m - 1):
                P_m += element
            if number_of_element == 0:
                S_1 += element
            elif number_of_element == (n - 1):
                S_n += element
            number_of_element += 1
        number_of_row += 1
    return [P_1, P_m, S_1, S_n]


# Create an instance of matrix a in counter
counter_a = counter(a)

# Matrix g
g = deepcopy(a)


# Replaces all nonzero elements of the main diagonal by their sum
def replace_main_diagonal(array: list) -> list:
    matrix = array
    sum_of_main_diagonal = 0
    for element in range(m):
        sum_of_main_diagonal += matrix[element][element]
    for element in range(m):
        if matrix[element][element] is not 0:
            matrix[element][element] = round(sum_of_main_diagonal, nums_after_comma)
    return matrix


# Create an instance of replaced main diagonal in matrix g
replaced_g = replace_main_diagonal(g)

# Create an instance of matrix g in counter
counter_g = counter(replaced_g)


# Replace all positive elements by the relation S_1 / S_n and all negative elements with P_m
def replace_positive_elements(array: list) -> list:
    matrix = array
    the_relation_1 = round(counter_g[2] / counter_g[3], nums_after_comma)
    the_relation_2 = round(counter_g[1], nums_after_comma)
    row_number = 0
    for row in matrix:
        element_number = 0
        for element, value in enumerate(row):
            if row_number != element_number:
                if value > 0:
                    row[element] = the_relation_1
                elif value < 0:
                    row[element] = the_relation_2
            element_number += 1
        row_number += 1
    return matrix


# Create an instance of final matrix g
matrix_g = replace_positive_elements(replaced_g)


# --------------- printing module -------------------
def printer(array: list, matrix_name: str):
    print("\nMatrix {}({}, {}) \n".format(matrix_name, m, n))
    for item in array:
        w = '\t'.join(['%' + str(max_len(array)) + 's'] * len(item))
        print(w % tuple(item))


if __name__ == '__main__':
    printer(a, "a")
    print("\nAmount of all positive elements: {}".format(q))
    print("\nThe sum of all positive elements: {}".format(round(P, nums_after_comma)))
    print("\nAmount of all negative elements: {}".format(z))
    print("\nProduct of all negative elements: {}".format(round(S, nums_after_comma)))
    print("\nThe sum of elements in row #1: {}".format(round(counter_a[0], nums_after_comma)))
    print("\nThe sum of elements in the last row: {}".format(round(counter_a[1], nums_after_comma)))
    print("\nThe sum of elements in column #1: {}".format(round(counter_a[2], nums_after_comma)))
    print("\nThe sum of elements in the last column: {}".format(round(counter_a[3], nums_after_comma)))
    printer(matrix_g, "g")
