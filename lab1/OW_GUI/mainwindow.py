# This Python file uses the following encoding: utf-8
import os
import sys
import threading
import time

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog
from PySide6.QtCore import Qt

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
        self.hide_graph()

        self.ui.distribution_select.currentTextChanged.connect(self.change_dist_options)
        self.ui.lab1.setText("Średnia:")
        self.ui.lab2.setText("")
        self.ui.odch_num.hide()
        self.ui.odch_num.setDisabled(True)
        self.ui.mean_num.setValue(1)
        self.ui.benchmark_btn.setEnabled(False)
        self.ui.start_btn.setEnabled(False)
        self.flag = False

        self.ui.addVal_btn.clicked.connect(self.add_value)
        self.ui.benchmark_btn.clicked.connect(self.run_benchmark)
        self.thread = threading.Thread()
        self.event = threading.Event()
        self.ui.info_lab.setText("")
        self.counter_wyn = 0
        self.d_crit_nzd_proc = dict()
        self.d_crit_nzd = dict()
        self.ff = False

    def change_flag(self):
        self.flag = True
        self.event.set()

    def change_dist_options(self):
        self.ui.odch_num.show()
        if self.ui.distribution_select.currentText() == "Eksponencjalny":
            self.ui.lab1.setText("Średnia:")
            self.ui.lab2.setText("")
            self.ui.odch_num.hide()
            self.ui.odch_num.setDisabled(True)
            self.ui.mean_num.setValue(1)
            self.ui.mean_num.setMinimum(0)
        elif self.ui.distribution_select.currentText() == "Jednostajny":
            self.ui.lab1.setText("Limit dolny:")
            self.ui.lab2.setText("Limit górny:")
            self.ui.mean_num.setEnabled(True)
            self.ui.odch_num.setEnabled(True)
            self.ui.mean_num.setValue(0)
            self.ui.odch_num.setValue(2)
        elif self.ui.distribution_select.currentText() == "Gaussa":
            self.ui.lab1.setText("Średnia:")
            self.ui.lab2.setText("Odchylenie:")
            self.ui.mean_num.setEnabled(True)
            self.ui.odch_num.setEnabled(True)
            self.ui.mean_num.setValue(1)
            self.ui.odch_num.setValue(1)
            self.ui.odch_num.setMinimum(0)
        elif self.ui.distribution_select.currentText() == "Poissona":
            self.ui.odch_num.setDisabled(True)
            self.ui.lab2.setText("")
            self.ui.odch_num.hide()
            self.ui.mean_num.setValue(2)
            self.ui.mean_num.setMinimum(0)

    def run_algorithm(self):
        # Create a new thread and target the method that should be executed
        self.thread = threading.Thread(target=self.run_algorithm_thread)
        self.thread.start()

    def run_algorithm_thread(self):
        l = []
        algo = self.ui.algorithm_select.currentText()
        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.cellWidget(row, 1)
            text = it.currentText() if it is not None else ""
            l.append(text)

        points = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i, j).text()))

        niezdom, zdom, iter = [], [], 0
        start = time.perf_counter_ns()
        if algo == "Naiwny bez filtracji":
            niezdom, zdom, iter = Algorytm1.bez_filtracji(points, l, self.event)
            print("end")
        elif algo == "Naiwny z filtracją":
            niezdom, zdom, iter = Algorytm2.algorytm_z_filtracja(points, l, self.flag)
        elif algo == "Oparty o punkt idealny":
            niezdom, zdom, iter = Algorytm3.punkt_idealny(points, l, self.flag)

        self.flag = False
        self.event.clear()


        end = time.perf_counter_ns()
        print("time: " + str(end-start))
        self.update_graph(points, niezdom, zdom, iter, algo, end - start)
        self.save_sol(niezdom, zdom)

        if self.critNum in self.d_crit_nzd_proc.keys():
            self.d_crit_nzd_proc[self.critNum] += [len(niezdom)/len(points)*100]
        else:
            self.d_crit_nzd_proc[self.critNum] = [len(niezdom)/len(points)*100]

        if self.critNum in self.d_crit_nzd.keys():
            self.d_crit_nzd[self.critNum] += [len(niezdom)]
        else:
            self.d_crit_nzd[self.critNum] = [len(niezdom)]

        self.regr_do()

    def regr_do(self):
        # Tworzenie wykresu 1D (histogramu)
        self.ui.regresja.canvas.axes.clear()
        self.ui.regresja_2.canvas.axes.clear()


        X = []
        y = []

        for key, values in self.d_crit_nzd_proc.items():
            for value in values:
                X.append(key)
                y.append(value)

        # Calculate the mean of X and y
        X_mean = np.mean(X)
        y_mean = np.mean(y)

        # Calculate the slope (m) and intercept (b) of the regression line
        numerator = np.sum((X - X_mean) * (y - y_mean))
        denominator = np.sum((X - X_mean) ** 2)
        slope = numerator / denominator
        intercept = y_mean - (slope * X_mean)


        # Calculate predicted values
        y_pred = slope * np.array(X) + intercept

        self.ui.regresja.canvas.axes.plot(X, y_pred, color="b",linestyle='--')


        X = []
        y = []

        for key, values in self.d_crit_nzd.items():
            for value in values:
                X.append(key)
                y.append(value)

        # Calculate the mean of X and y
        X_mean = np.mean(X)
        y_mean = np.mean(y)

        # Calculate the slope (m) and intercept (b) of the regression line
        numerator = np.sum((X - X_mean) * (y - y_mean))
        denominator = np.sum((X - X_mean) ** 2)
        slope = numerator / denominator
        intercept = y_mean - (slope * X_mean)

        # Calculate predicted values
        y_pred = slope * np.array(X) + intercept

        residuals = y - y_pred
        se = np.sqrt(np.sum(residuals ** 2) / (len(X) - 2))

        # Calculate confidence intervals
        t_value = 2.262  # for 95% CI and n-2 degrees of freedom, use appropriate value based on t-distribution
        ci_upper = y_pred + t_value * se
        ci_lower = y_pred - t_value * se
        self.ui.regresja_2.canvas.axes.plot(X, y_pred, color="b",linestyle='--')
        self.ui.regresja_2.canvas.axes.fill_between(X, ci_lower, ci_upper, color='blue', alpha=0.1, label='95% Confidence Interval')


        for k,v in self.d_crit_nzd_proc.items():
            self.ui.regresja.canvas.axes.scatter([k]*len(v), v, c="k")

        for k, v in self.d_crit_nzd.items():
            self.ui.regresja_2.canvas.axes.scatter([k]*len(v), v, c="k")

        self.ui.regresja.canvas.axes.legend(["Regresja liniowa","Procent punktów niezdominowanych"])
        self.ui.regresja.canvas.axes.set_title('Wykres zależności ilości punktów niezdominowanych od ilości kryteriów')
        self.ui.regresja.canvas.axes.set_xlabel("Ilość kryteriów")
        self.ui.regresja.canvas.axes.set_ylabel("% punktów niezdominowanych")
        self.ui.regresja.canvas.axes.grid()
        self.ui.regresja.canvas.axes.figure.tight_layout()
        self.ui.regresja.canvas.draw()

        self.ui.regresja_2.canvas.axes.legend(["Regresja liniowa", "Obszar ufności" ,"Liczba punktów niezdominowanych"])
        self.ui.regresja_2.canvas.axes.set_title('Wykres zależności ilości punktów niezdominowanych od ilości kryteriów')
        self.ui.regresja_2.canvas.axes.set_xlabel("Ilość kryteriów")
        self.ui.regresja_2.canvas.axes.set_ylabel("Liczba punktów niezdominowanych")
        self.ui.regresja_2.canvas.axes.grid()
        self.ui.regresja_2.canvas.axes.figure.tight_layout()
        self.ui.regresja_2.canvas.draw()

    def run_benchmark(self):
        # Create a new thread and target the method that should be executed
        thread = threading.Thread(target=self.run_benchmark_thread)
        thread.start()

    def run_benchmark_thread(self):
        l = []
        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.cellWidget(row, 1)
            text = it.currentText() if it is not None else ""
            l.append(text)

        points = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i, j).text()))

        start_bf = time.perf_counter_ns()
        niezdom_bf, zdom_bf, iter_bf = Algorytm1.bez_filtracji(points, l, self.flag)
        end_bf = time.perf_counter_ns()
        time_bf = end_bf - start_bf

        start_zf = time.perf_counter_ns()
        niezdom_zf, zdom_zf, iter_zf = Algorytm2.algorytm_z_filtracja(points, l, self.flag)
        end_zf = time.perf_counter_ns()
        time_zf = end_zf - start_zf

        start_pi = time.perf_counter_ns()
        niezdom_pi, zdom_pi, iter_pi = Algorytm3.punkt_idealny(points, l, self.flag)
        end_pi = time.perf_counter_ns()
        time_pi = end_pi - start_pi

        self.ui.benchmark_table.setItem(0, 0, QTableWidgetItem(str(time_bf/1000)))
        self.ui.benchmark_table.setItem(1, 0, QTableWidgetItem(str(time_zf/1000)))
        self.ui.benchmark_table.setItem(2, 0, QTableWidgetItem(str(time_pi/1000)))

        self.ui.benchmark_table.setItem(0, 1, QTableWidgetItem(str(iter_bf)))
        self.ui.benchmark_table.setItem(1, 1, QTableWidgetItem(str(iter_zf)))
        self.ui.benchmark_table.setItem(2, 1, QTableWidgetItem(str(iter_pi)))

        for i in range(3):
            for j in range(2):
                self.ui.benchmark_table.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def sort(self):
        points = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i, j).text()))

        crit_sort = self.ui.criterium_num.value()
        dir = self.ui.criteriaTable.cellWidget(crit_sort-1, 1).currentText()
        if dir == "Min":
            new_p = sorted(points, key=lambda x: (x[crit_sort-1]))
        else:
            new_p = sorted(points, key=lambda x: (x[crit_sort - 1]), reverse=True)

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

        if self.ff:
            self.ui.valuesTable.insertColumn(self.ui.valuesTable.columnCount())
            lc = []
            for i in range(self.critNum):
                lc.append(f"Kryterium {i+1}")

            self.ui.valuesTable.setHorizontalHeaderLabels(lc)
            for x in range(-1, self.ui.valuesTable.rowCount()+1):
                print(x,self.critNum)
                self.ui.valuesTable.setItem(x, self.critNum-1, QTableWidgetItem(str(0)))

    def delete_criterium(self,):
        rows = self.ui.criteriaTable.selectionModel().selectedRows()
        for index in sorted(rows):
            self.ui.criteriaTable.removeRow(index.row())
            self.ui.valuesTable.removeColumn(index.row())
        self.critNum -= len(rows)
        self.ui.criterium_num.setMaximum(self.critNum)
        if self.critNum == 0:
            self.ui.criterium_num.setMaximum(0)

    def add_value(self,):
        self.ui.benchmark_btn.setEnabled(True)
        self.ui.start_btn.setEnabled(True)
        self.ui.valuesTable.insertRow(self.ui.valuesTable.rowCount())

    def delete_value(self,):
        rows = self.ui.valuesTable.selectionModel().selectedRows()
        for index in sorted(rows):
            self.ui.valuesTable.removeRow(index.row())

        cols = self.ui.valuesTable.selectionModel().selectedColumns()
        for index in sorted(cols):
            self.ui.valuesTable.removeColumn(index.column())
            self.ui.criteriaTable.removeRow(index.column())
        self.critNum -= len(cols)

    def save(self):
        points = []
        data = []

        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.item(row, 0)
            direction = self.ui.criteriaTable.cellWidget(row, 1)
            text = it.text() if it is not None else ""
            text += "_" + direction.currentText()
            data.append(text)

        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i,j).text()))
        df = pd.DataFrame(data=np.array(points))
        df.to_excel(f"../Punkty/punkty_{self.counter}.xlsx", index=False, header=False)
        self.counter += 1
        self.ui.info_lab.setText("Punkty zapisano!")

    def save_sol(self, nzd, zd):
        points = []
        data = []
        data_dir = []

        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.item(row, 0)
            direction = self.ui.criteriaTable.cellWidget(row, 1)
            text = it.text() if it is not None else ""
            data.append(text)
            data_dir.append(direction.currentText())

        dom = []
        for i in range(self.ui.valuesTable.rowCount()):
            points.append([])
            for j in range(self.ui.valuesTable.columnCount()):
                points[i].append(float(self.ui.valuesTable.item(i,j).text()))
        print(points)

        for r in points:
            if r in zd:
                dom.append("zdominowany")
            elif r in nzd:
                dom.append("niezdominowany")

        df1 = pd.DataFrame({0: data, 1: data_dir})

        df2 = pd.DataFrame(data=np.array(np.transpose(points)))

        df_combined = pd.concat([df1, df2], axis=1)
        df_combined.loc[len(df_combined)] = ["", ""] + dom
        df_combined.to_excel(f"../Wyniki/wynik_{self.counter_wyn}.xlsx", index=False,header=False)
        self.ui.info_lab.setText("Wynik zapisano!")

    def generate(self):
        self.ui.benchmark_btn.setEnabled(True)
        self.ui.start_btn.setEnabled(True)
        data = []
        d = []
        self.ff = True
        n = self.ui.point_num.value()

        if self.ui.distribution_select.currentText() == "Eksponencjalny":
            d = np.random.exponential(self.ui.mean_num.value(), n)
        elif self.ui.distribution_select.currentText() == "Jednostajny":
            d = np.random.uniform(self.ui.mean_num.value(), self.ui.odch_num.value(), n)
        elif self.ui.distribution_select.currentText() == "Gaussa":
            d = np.random.normal(self.ui.mean_num.value(), self.ui.odch_num.value(), n)
        elif self.ui.distribution_select.currentText() == "Poissona":
            d = np.random.poisson(self.ui.mean_num.value(), n)

        for row in range(self.ui.criteriaTable.rowCount()):
            it = self.ui.criteriaTable.item(row, 0)
            text = it.text() if it is not None else ""
            data.append(text)

        if len(data) == 1:
            self.ui.valuesTable.setColumnCount(len(data))
            self.ui.valuesTable.setRowCount(len(d))
            self.ui.valuesTable.setHorizontalHeaderLabels(data)
            for j in range(n):
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
        self.hide_graph()

    def update_graph(self, pts, nz, z, it, title, tim):
        new_pte = np.array(pts)
        new_z = np.array(z)
        new_nz = np.array(nz)

        self.ui.graph.canvas.axes.clear()
        self.ui.graph.show()
        try:
            if self.ui.graph.canvas.axes is not None:
                self.ui.graph.canvas.figure.delaxes(self.ui.graph.canvas.axes)
        except:
            pass

        if self.critNum == 1 or self.critNum == 2 or self.critNum == 3:
            # Ustalanie rodzaju wykresu na podstawie parametru `plot_type`
            if self.critNum == 1:
                self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111)
                # Tworzenie wykresu 1D (histogramu)
                self.ui.graph.canvas.axes.scatter(new_z, [0] * len(new_z), c="k", label="Zdominowane")
                self.ui.graph.canvas.axes.scatter(new_nz, [0] * len(new_nz), c="r", label="Niezdominowane")
            elif self.critNum == 2:
                self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111)
                # Domyślny wykres 2D
                x = new_pte[:, 0]
                y = new_pte[:, 1]
                try:
                    self.ui.graph.canvas.axes.scatter(new_z[:, 0], new_z[:, 1], c="k", label="Zdominowane")
                except:
                    pass
                try:
                    self.ui.graph.canvas.axes.scatter(new_nz[:, 0], new_nz[:, 1], c="r", label="Niezdominowane")
                except:
                    pass
                self.ui.graph.canvas.axes.set_ylabel("Kryterium 2")

            elif self.critNum == 3:

                # Tworzenie wykresu 3D
                x = new_pte[:, 0]
                y = new_pte[:, 1]
                z = new_pte[:, 2]
                self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111, projection='3d')
                self.ui.graph.canvas.axes.scatter(new_z[:, 0], new_z[:, 1], new_z[:, 2], c="k", label="Zdominowane")
                self.ui.graph.canvas.axes.scatter(new_nz[:, 0], new_nz[:, 1], new_nz[:, 2], c="r", label="Niezdominowane")
                self.ui.graph.canvas.axes.set_ylabel("Kryterium 2")
                self.ui.graph.canvas.axes.set_zlabel("Kryterium 3")  # Etykieta dla osi Z


            self.ui.graph.canvas.axes.legend()
            self.ui.graph.canvas.axes.set_title('Wykres')
            self.ui.graph.canvas.axes.set_xlabel("Kryterium 1")
            self.ui.graph.canvas.axes.set_title("Algorytm " + title.lower() + ", czas wykonania: " + str(tim/1000) + " ms , porównania: " + str(it))
            self.ui.graph.canvas.axes.figure.tight_layout()
            self.ui.graph.canvas.draw()

            self.ui.por_line.setText(str(it))
            self.ui.czas_line.setText(str(tim/1000))
            self.ui.nzd_line.setText(str(len(new_nz)/len(pts)*100))
            self.ui.wym_line.setText(str(len(pts[0])))
            print(len(pts[0]))
            if len(pts[0]) > 3:
                self.ui.plot_line.setText("Nie")
            else:
                self.ui.plot_line.setText("Tak")
        else:
            self.ui.graph.hide()
            self.ui.por_line.setText(str(it))
            self.ui.czas_line.setText(str(tim/1000))
            self.ui.nzd_line.setText(str(len(new_nz)/len(pts)*100))
            self.ui.wym_line.setText(str(len(pts[0])))
            if len(pts[0]) > 3:
                self.ui.plot_line.setText("Nie")
            else:
                self.ui.plot_line.setText("Tak")


    def hide_graph(self):
        self.ui.graph.canvas.axes.clear()
        self.ui.graph.hide()

    def getFileName(self):
        try:
            response = QFileDialog.getOpenFileName(
                self, 'Select a data file', os.getcwd(), "Excel files (*.xlsx *.csv )"
            )

            self.ui.info_lab.setText("Wczytano plik!")
            df = pd.read_excel(response[0], header=None)
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
            xi = 0
            yi = 0
            for i in df.values:
                for j in i:
                    self.ui.valuesTable.setItem(xi, yi, QTableWidgetItem(str(j)))
                    yi += 1
                yi = 0
                xi += 1
            self.ui.benchmark_btn.setEnabled(True)
            self.ui.start_btn.setEnabled(True)

        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
