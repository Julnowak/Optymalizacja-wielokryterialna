# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from Algorithms import Algorytm1, Algorytm2, Algorytm3
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.criteriaTable.setRowCount(1)
        self.ui.criteriaTable.setColumnCount(2)
        self.ui.criteriaTable.setHorizontalHeaderLabels(["Nazwa", "Kierunek"])

        self.critNum = 0
        self.r = None
        comboBox = QtWidgets.QComboBox()
        comboBox.addItem("Min")
        comboBox.addItem("Max")

        self.ui.criteriaTable.setItem(self.critNum, 0, QTableWidgetItem("Kryterium 1"))
        self.ui.criteriaTable.setCellWidget(self.critNum, 1, comboBox)
        self.ui.criteriaTable.cellClicked.connect(self.getClickedCell)

        self.ui.deleteCrit_btn.clicked.connect(self.delete_criterium)
        self.ui.addCrit_btn.clicked.connect(self.add_criterium)

        self.ui.generation_btn.clicked.connect(self.generate)

    def run_algorithm(self):
        algo = self.ui.algorithm_select.currentText()

        if algo == "Naiwny bez filtracji":
            wynik = Algorytm1.bez_filtracji()
        elif algo == "Naiwny z filtracją":
            wynik = Algorytm2.algorytm_z_filtracja()
        elif algo == "Oparty o punkt idealny":
            wynik = Algorytm3.punkt_idealny()

    def add_criterium(self):
        self.critNum += 1

        comboBox = QtWidgets.QComboBox()
        comboBox.addItem("Min")
        comboBox.addItem("Max")

        self.ui.criteriaTable.setRowCount(self.critNum+1)
        self.ui.criteriaTable.setItem(self.critNum, 0, QTableWidgetItem(f"Kryterium {self.critNum+1}"))
        self.ui.criteriaTable.setCellWidget(self.critNum, 1, comboBox)



    def delete_criterium(self,):
        if self.r is not None:
            self.ui.criteriaTable.removeRow(self.r)
            self.critNum -= 1
            self.r = None

    def getClickedCell(self, row, column):
        self.r = row

    def add_value(self,):
        pass

    def delete_value(self,):
        pass

    def generate(self):
        data = []
        d = []
        n = self.ui.point_num.value()
        if self.ui.distribution_select.currentText() == "Eksponencjalny":
            d = np.random.exponential(1, n)
        elif self.ui.distribution_select.currentText() == "Jednostajny":
            d = np.random.uniform(0, 2, n)
        elif self.ui.distribution_select.currentText() == "Gaussa":
            d = np.random.normal(1, 1, n)
        elif self.ui.distribution_select.currentText() == "Poissona":
            d = np.random.poisson(2, n)

        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.item(row, 0)
            text = it.text() if it is not None else ""
            data.append(text)
        print(data)
        print(d)
        if len(data) == 1:
            self.ui.valuesTable.setColumnCount(len(data))
            self.ui.valuesTable.setRowCount(len(d))
            self.ui.valuesTable.setHorizontalHeaderLabels(data)
            for j in range(n):
                print(d[j])
                self.ui.valuesTable.setItem(j, 0, QTableWidgetItem(str(d[j])))
        else:
            self.ui.valuesTable.setRowCount(len(d))
            self.ui.valuesTable.setColumnCount(len(data))
            self.ui.valuesTable.setHorizontalHeaderLabels(data)
            for i in range(self.critNum):
                for j in range(n):
                    self.ui.valuesTable.setItem(j, i, QTableWidgetItem(str(d[j])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
