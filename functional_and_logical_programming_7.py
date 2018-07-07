import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

"""
lab #7 task#9

Дана строка символов, состоящая из цифр, разделенных пробелами. 
Вывести на экран числа этой строки в порядке возрастания их значений.
"""


class Lab7(QDialog):
    def __init__(self):
        super(Lab7, self).__init__()
        loadUi('lab7.ui', self)
        self.setWindowTitle('Lab7: Rahacheuski Pavel')
        self.pushButton.clicked.connect(self.on_push_button_clicked)

    @pyqtSlot()
    def on_push_button_clicked(self):
        init_text = self.lineEdit.text()
        res = self.parse_seq(init_text)
        self.label_3.setText(str(res))

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Lab7()
    widget.show()
    sys.exit(app.exec_())
