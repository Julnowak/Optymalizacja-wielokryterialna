# This Python file uses the following encoding: utf-8
import os
import sys
import time

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from Algorithms import Algorytm1, Algorytm2, Algorytm3
import numpy as np
import pandas as pd


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.criteriaTable.setRowCount(1)
        self.ui.criteriaTable.setColumnCount(2)
        self.ui.criteriaTable.setHorizontalHeaderLabels(["Nazwa", "Kierunek"])

        self.critNum = 1
        self.r = None
        comboBox = QtWidgets.QComboBox()
        comboBox.addItem("Min")
        comboBox.addItem("Max")

        self.ui.criteriaTable.setItem(0, 0, QTableWidgetItem("Kryterium 1"))
        self.ui.criteriaTable.setCellWidget(0, 1, comboBox)

        self.ui.deleteCrit_btn.clicked.connect(self.delete_criterium)
        self.ui.addCrit_btn.clicked.connect(self.add_criterium)

        self.ui.generation_btn.clicked.connect(self.generate)

        self.ui.load_btn.clicked.connect(self.getFileName)
        self.ui.start_btn.clicked.connect(self.run_algorithm)
        self.ui.sort_btn.clicked.connect(self.sort)

        self.ui.deleteVal_btn.clicked.connect(self.delete_value)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.criterium_num.setMaximum(1)
        self.counter = 1

    def run_algorithm(self):
        l = []
        algo = self.ui.algorithm_select.currentText()
        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.cellWidget(row, 1)
            text = it.currentText() if it is not None else ""
            l.append(text)
        print(l)

        points = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i,j).text()))
                print(self.ui.valuesTable.item(i,j).text())

        # print(points)

        niezdom, zdom, iter = [], [], 0
        start = time.perf_counter_ns()
        if algo == "Naiwny bez filtracji":
            niezdom, zdom, iter = Algorytm1.bez_filtracji(points,l)
        elif algo == "Naiwny z filtracją":
            niezdom, zdom, iter = Algorytm2.algorytm_z_filtracja(points,l)
        elif algo == "Oparty o punkt idealny":
            niezdom, zdom, iter = Algorytm3.punkt_idealny(points,l)
        end = time.perf_counter_ns()
        print("Czas", end-start)
        print(niezdom, zdom, iter)
        self.update_graph(points, niezdom, zdom, iter)

    def sort(self):
        points = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i, j).text()))

        crit_sort = self.ui.criterium_num.value()
        new_p = sorted(points, key=lambda x: (x[crit_sort-1]))

        xi = 0
        yi = 0
        for x in new_p:
            for y in x:
                self.ui.valuesTable.setItem(xi,yi,QTableWidgetItem(str(y)))
                yi += 1
            yi = 0
            xi += 1

    def add_criterium(self):
        self.ui.criterium_num.setMinimum(1)
        comboBox = QtWidgets.QComboBox()
        comboBox.addItem("Min")
        comboBox.addItem("Max")

        self.ui.criteriaTable.setRowCount(self.critNum+1)
        self.ui.criteriaTable.setItem(self.critNum, 0, QTableWidgetItem(f"Kryterium {self.critNum+1}"))
        self.ui.criteriaTable.setCellWidget(self.critNum, 1, comboBox)
        self.critNum += 1
        self.ui.criterium_num.setMaximum(self.critNum)

    def delete_criterium(self,):
        rows = self.ui.criteriaTable.selectionModel().selectedRows()
        print(rows)
        for index in sorted(rows):
            self.ui.criteriaTable.removeRow(index.row())
        self.critNum -= len(rows)
        self.ui.criterium_num.setMaximum(self.critNum)
        if self.critNum == 0:
            self.ui.criterium_num.setMaximum(0)

    def add_value(self,):
        pass

    def delete_value(self,):
        rows = self.ui.valuesTable.selectionModel().selectedRows()
        print(rows)
        for index in sorted(rows):
            self.ui.valuesTable.removeRow(index.row())

        cols = self.ui.valuesTable.selectionModel().selectedColumns()
        print(cols)
        for index in sorted(cols):
            self.ui.valuesTable.removeColumn(index.column())
            self.ui.criteriaTable.removeRow(index.column())
        self.critNum -= len(cols)

    def save(self):
        points = []
        data = []

        print(os.getcwd())
        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.item(row, 0)
            direction = self.ui.criteriaTable.cellWidget(row, 1)
            print(direction)
            text = it.text() if it is not None else ""
            text += "_" + direction
            data.append(text)

        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i,j).text()))
        df = pd.DataFrame(columns=data, data=np.array(points))
        df.to_excel(f"../Wyniki/punkty_{self.counter}.xlsx")
        self.counter += 1

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
            for i in range(len(data)):
                if self.ui.distribution_select.currentText() == "Eksponencjalny":
                    d = np.random.exponential(1, n)
                elif self.ui.distribution_select.currentText() == "Jednostajny":
                    d = np.random.uniform(0, 2, n)
                elif self.ui.distribution_select.currentText() == "Gaussa":
                    d = np.random.normal(1, 1, n)
                elif self.ui.distribution_select.currentText() == "Poissona":
                    d = np.random.poisson(2, n)
                for j in range(n):
                    self.ui.valuesTable.setItem(j, i, QTableWidgetItem(str(d[j])))

        self.ui.valuesTable.resizeColumnsToContents()

    def update_graph(self, pts, nz, z, it):
        new_pte = np.array(pts)
        new_z = np.array(z)
        new_nz = np.array(nz)
        print(new_pte)
        x = new_pte[:, 0]
        y = new_pte[:, 1]
        self.ui.graph.canvas.axes.clear()
        self.ui.graph.show()

        self.ui.graph.canvas.axes.scatter(x, y, c="b", label="ddddddddd")
        self.ui.graph.canvas.axes.scatter(new_z[:, 0], new_z[:, 1], c="k", label="Zdominowane")
        self.ui.graph.canvas.axes.scatter(new_nz[:, 0], new_nz[:, 1], c="r", label="Niezdominowane")
        self.ui.graph.canvas.axes.legend()
        self.ui.graph.canvas.axes.set_title('t')
        self.ui.graph.canvas.axes.set_xlabel("Kryterium 1")
        self.ui.graph.canvas.axes.set_ylabel("Kryterium 2")
        self.ui.graph.canvas.axes.figure.tight_layout()
        self.ui.graph.canvas.draw()

    def hide_graph(self):
        self.ui.graph.canvas.axes.clear()
        self.ui.graph.hide()

    def getFileName(self):
        try:
            response = QFileDialog.getOpenFileName(
                self, 'Select a data file', os.getcwd(), "Excel files (*.xlsx *.csv )"
            )
            print(response)

            df = pd.read_excel(response[0])

            xi = 0
            yi = 0

            self.critNum = df.shape[1]

            lc = []
            if self.critNum == 1:
                comboBox = QtWidgets.QComboBox()
                comboBox.addItem("Min")
                comboBox.addItem("Max")
                self.ui.criteriaTable.setRowCount(self.critNum)
                lc.append("Kryterium 1")
                self.ui.criteriaTable.setItem(0, 0, QTableWidgetItem(f"Kryterium {1}"))
                self.ui.criteriaTable.setCellWidget(0, 1, comboBox)
            else:
                self.ui.criteriaTable.setRowCount(self.critNum)
                for i in range(self.critNum):
                    comboBox = QtWidgets.QComboBox()
                    comboBox.addItem("Min")
                    comboBox.addItem("Max")
                    lc.append(f"Kryterium {i + 1}")
                    self.ui.criteriaTable.setItem(i, 0, QTableWidgetItem(f"Kryterium {i + 1}"))
                    self.ui.criteriaTable.setCellWidget(i, 1, comboBox)

            self.ui.valuesTable.setRowCount(df.shape[0])
            self.ui.valuesTable.setColumnCount(df.shape[1])
            self.ui.valuesTable.setHorizontalHeaderLabels(lc)
            for i in df.values:
                for j in i:
                    self.ui.valuesTable.setItem(xi, yi, QTableWidgetItem(str(j)))
                    yi += 1
                yi = 0
                xi += 1
        except:
            pass
        # if str(response[0]):
        #     # self.ui.file_name.setText(str(response[0]))
        #     # self.fileName = self.ui.file_name.text()
        #     if self.fileName != '':
        #         pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
