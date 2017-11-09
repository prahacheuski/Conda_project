import pandas as pd
import numpy as np

"""
lab #6 task#9
Написать программу по обработке динамических массивов. Размеры массивов вводить с клавиатуры. При создании оконного 
приложения скалярный (простой) результат выводить в виде компоненты Label, а массивы вводить и выводить с помощью 
компонент StringGrid, в которых 0-й столбец и 0-ю строку использовать для отображения индексов массивов.
В матрице размером N´M упорядочить строки по возрастанию их наибольших элементов.
"""


def do_the_work() -> int:
    df = None
    while True:
        z = input('\nMenu:\n1. Insert integer array manually\n2. Sort the lines in order increment of its elements\n'
                  '3. Print array\n4. Exit\nSelect the desired item: ')
        if z == '1':
            try:
                py_arr = []
                i = input('Insert number of rows: ')
                j = input('Insert number of columns: ')
                for _i in range(0, int(i)):
                    i_arr = []
                    for _j in range(0, int(j)):
                        i_arr.append(int(input('Insert: a({},{}) = '.format(_i + 1, _j + 1))))
                    py_arr.append(i_arr)
                df = pd.DataFrame(py_arr, columns=np.arange(1, int(j) + 1, 1), index=np.arange(1, int(i) + 1, 1))
                df.index.name = 'i\j'
            except Exception:
                print('\nException was stashed, try again!!!')
                continue
        elif z == '2':
            if df is not None:
                np_df = df.as_matrix()
                py_np_df = list(np_df)
                print(py_np_df)
                ind = 1
                while ind < len(py_np_df):
                    for i in range(len(py_np_df) - ind):
                        if np.max(py_np_df[i]) > np.max(py_np_df[i + 1]):
                            py_np_df[i], py_np_df[i + 1] = py_np_df[i + 1], py_np_df[i]
                    ind += 1
                df = pd.DataFrame(py_np_df, columns=np.arange(1, int(len(py_np_df[0])) + 1, 1),
                                  index=np.arange(1, int(len(py_np_df)) + 1, 1))
                df.index.name = 'i\j'

        elif z == '3':
            print('Array:\n{}'.format(df))
        elif z == '4':
            return 0


if __name__ == '__main__':
    do_the_work()
