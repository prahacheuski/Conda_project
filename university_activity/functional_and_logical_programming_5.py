import numpy as np

"""
lab #5 task #9
Написать программу по обработке одномерных массивов. Размеры массивов вводить с клавиатуры. В консольном приложении 
предусмотреть возможность ввода данных как с клавиатуры, так и с использованием функции random().
При создании оконного приложения скалярный (простой) результат выводить в виде компоненты Label, а массивы вводить и 
выводить с помощью компонент StringGrid.
В одномерном массиве, состоящем из n вводимых с клавиатуры целых элементов, вычислить:
Сумму элементов массива, расположенных после последнего элемента, равного нулю.
"""


def do_the_work() -> int:
    arr = np.array([])
    while True:
        i = input('\nMenu:\n1. Insert integer array manually\n2. Generate integer array via random function\n'
                  '3. Calculate array sum after last zero\n4. Exit\nSelect the desired item: ')
        if i == '1':
            py_arr = []
            n = input('Insert number of elements: ')
            for x in range(0, int(n)):
                py_arr.append(int(input('Add {} element: '.format(x + 1))))
            arr = np.array(py_arr)
            print('Result array: {}'.format(arr))
        elif i == '2':
            arr = np.array([])
            arr = np.random.random_integers(0, 99, np.random.random_integers(1, 99, 1))
            print('Generated array: {}'.format(arr))
        elif i == '3':
            x = np.where(arr == 0)[0]
            if np.alen(x) == 0:
                print('No zeros in array: {}'.format(arr))
            elif np.alen(x) == 1:
                print('For this array : {}\nSum after zero = {}'.format(arr, np.sum(arr[x[0]:])))
            elif np.alen(x) > 1:
                print('For this array : {}\nSum after last zero = {}'.format(arr, np.sum(arr[np.max(x):])))
        elif i == '4':
            return 0


if __name__ == '__main__':
    do_the_work()
