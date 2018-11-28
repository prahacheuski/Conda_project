from PyQt5.QtWidgets import QApplication, QDialog
from collections import namedtuple
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel
import PyQt5.QtCore as QtCore
from PyQt5.uic import loadUi
import pandas as pd
import numpy as np
import sys

"""
lab #8 task#9
Написать программу обработки файла типа запись, содержащую следующие пункты меню: «Создание», «Просмотр», «Коррекция» 
(добавление новых данных или редактирование старых), «Решение индивидуального задания».

Каждая запись должна содержать следующую информацию о студентах:
– фамилия и инициалы;
– год рождения;
– номер группы;
– оценки за семестр: по физике, математике, информатике, химии;
– средний балл.

Организовать ввод исходных данных, средний балл рассчитать по введенным оценкам.
Содержимое всего файла и результаты решения индивидуального задания записать в текстовый файл.

Вычислить общий средний балл всех студентов и распечатать список студентов интересующей вас группы, 
имеющих средний балл выше общего среднего балла.
"""

StudAvg = namedtuple('StudAvg', ['df', 'grand_avg'])
path = 'students.csv'


class Lab8(QDialog):
    def __init__(self):
        super(Lab8, self).__init__()
        loadUi('lab8.ui', self)
        self.setWindowTitle('Lab8: Rahacheuski Pavel')
        self.stud_avg: StudAvg = None
        self.df: pd.DataFrame = None
        self.mod_df: pd.DataFrame = None
        self.pushButton.clicked.connect(self.load)
        self.pushButton_2.clicked.connect(self.add)
        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_4.clicked.connect(self.cnt)

    @pyqtSlot()
    def on_push_button_clicked(self):
        init_text = self.lineEdit.text()
        res = self.parse_seq(init_text)
        self.label_3.setText(str(res))

    @staticmethod
    def avg(df: pd.DataFrame) -> StudAvg:
        df: pd.DataFrame = df.copy(deep=True)
        df['avg'] = df.apply(lambda tup: np.average([tup[3], tup[4], tup[5], tup[6]]), axis=1, raw=True)
        grand_avg = np.average(df['avg'].reshape(-1))

        return StudAvg(df, grand_avg)

    def cnt(self):
        init_df = self.df.loc[self.df.group == int(self.lineEdit_9.text())]
        self.mod_df: pd.DataFrame = init_df.copy()
        self.mod_df['avg'] = self.mod_df.apply(lambda tup: np.average([tup[3], tup[4], tup[5], tup[6]]), axis=1,
                                               raw=True)
        res = self.avg(init_df)
        self.label_11.setText(str(res.grand_avg))
        self.show_tab()

    def load(self):
        self.df = pd.DataFrame.from_csv(self.lineEdit.text(), sep='\t', index_col=None)
        self.update_mod_df()
        self.show_tab()

    def update_mod_df(self):
        self.mod_df: pd.DataFrame = self.df.copy()
        self.mod_df['avg'] = self.mod_df.apply(lambda tup: np.average([tup[3], tup[4], tup[5], tup[6]]), axis=1,
                                               raw=True)

    def save(self):
        self.df.to_csv(self.lineEdit.text(), sep='\t', index=False)

    def show_tab(self):
        model = PandasModel(self.mod_df)
        self.tableView.clearSpans()
        self.tableView.setModel(model)

    def add(self):

        data: dict = {'name': [self.lineEdit_2.text()],
                      'year': [np.int64(int(self.lineEdit_3.text()))],
                      'group': [np.int64(int(self.lineEdit_4.text()))],
                      'physics': [np.int64(int(self.lineEdit_5.text()))],
                      'math': [np.int64(int(self.lineEdit_6.text()))],
                      'informatics': [np.int64(int(self.lineEdit_7.text()))],
                      'chemistry': [np.int64(int(self.lineEdit_8.text()))]}

        temp_df = pd.DataFrame(data=data, columns=['name', 'year', 'group', 'physics', 'math', 'informatics',
                                                   'chemistry'])

        if self.df is None:
            self.df = temp_df

        else:

            self.df = self.df.append(temp_df, ignore_index=True)

        self.update_mod_df()
        self.show_tab()


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Lab8()
    widget.show()
    sys.exit(app.exec_())
