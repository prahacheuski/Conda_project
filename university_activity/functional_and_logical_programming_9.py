from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSlot
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi
import pandas as pd
import numpy as np
import sys

"""
lab #9 task#9
Написать программу вывода графиков функции (лабораторная работа №3) Y(x) и ее разложения в ряд S(x) для аргумента x, 
изменяющегося от a до b с шагом h (вводятся с клавиатуры) с использованием компоненты Сhart и графика функции Y(x) 
с использованием компоненты Image.
"""


class Lab9(QDialog):
    def __init__(self):
        super(Lab9, self).__init__()
        loadUi('lab9.ui', self)
        self.setWindowTitle('Lab9: Rahacheuski Pavel')
        self.pushButton.clicked.connect(self.on_push_button_clicked)

    @pyqtSlot()
    def on_push_button_clicked(self):
        a = self.lineEdit_2.text()
        b = self.lineEdit_3.text()
        h = self.lineEdit_4.text()
        n = self.lineEdit_5.text()
        df = do_the_work(a, b, h, n)

        fig, ax = plt.subplots()
        ax.grid(True)
        ax.plot(df['Y(x)'], '-', color='green', label='Y(x)')
        ax.plot(df['S(x, n)'], '--', color='blue', label='S(x, n)')
        ax.plot(df['|Y(x) - S(x, n)|'], '.-', color='red', label='|Y(x) - S(x, n)|')
        plt.legend(loc='best')
        plt.show()

    @staticmethod
    def parse_seq(input_str: str) -> list or str:
        """
        Perform string parsing, covert into nums and sort it.
        :return: list.
        """
        str_arr: list = input_str.split(' ')
        try:
            sorted_arr: list = sorted(str_arr, key=lambda x: int(x))
            res: list = [x for x in map(int, sorted_arr)]

        except Exception:
            res: str = "Incorrect input string. It should consist only of digits."

        return res


def do_the_work(a: str, b: str, h: str, n: str) -> pd.DataFrame:
    a = np.float(a)
    b = np.float(b)
    h = np.float(h)
    n = np.int(n)

    arr = []

    for x in np.arange(a, b, h):
        yx = np.float64(y(x))
        sxn = np.float64(s(x, n))
        ys = np.float64(np.abs((y(x) - s(x, n))))
        arr.append([yx, sxn, ys])

    df = pd.DataFrame(arr, columns=['Y(x)', 'S(x, n)', '|Y(x) - S(x, n)|'], dtype=np.float64, index=np.arange(a, b, h))
    df.index.name = 'x'

    return df


def s(x: np.float, step: np.int) -> float:
    grand_total = 0
    for k in range(1, step + 1):
        grand_total += np.power(-1, (k + 1)) * np.power(x, (2 * k + 1)) / 4 * np.power(k, 2) - 1
    return grand_total


def y(x: np.float) -> float:
    return (1 + np.power(x, 2)) / 2 * np.arctan(x) - x / 2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Lab9()
    widget.show()
    sys.exit(app.exec_())
