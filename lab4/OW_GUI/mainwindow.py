# This Python file uses the following encoding: utf-8
import os
import sys

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.load_btn.clicked.connect(self.getFileName)
        self.ui.graph.show()

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
                self.ui.graph.canvas.axes.scatter(new_nz[:, 0], new_nz[:, 1], new_nz[:, 2], c="r",
                                                  label="Niezdominowane")
                self.ui.graph.canvas.axes.set_ylabel("Kryterium 2")
                self.ui.graph.canvas.axes.set_zlabel("Kryterium 3")  # Etykieta dla osi Z

            self.ui.graph.canvas.axes.legend()
            self.ui.graph.canvas.axes.set_title('Wykres')
            self.ui.graph.canvas.axes.set_xlabel("Kryterium 1")
            self.ui.graph.canvas.axes.set_title(
                "Algorytm " + title.lower() + ", czas wykonania: " + str(tim / 1000) + " ms , porównania: " + str(it))
            self.ui.graph.canvas.axes.figure.tight_layout()
            self.ui.graph.canvas.draw()

            self.ui.por_line.setText(str(it))
            self.ui.czas_line.setText(str(tim / 1000))
            self.ui.nzd_line.setText(str(len(new_nz) / len(pts) * 100))
            self.ui.wym_line.setText(str(len(pts[0])))
            print(len(pts[0]))
            if len(pts[0]) > 3:
                self.ui.plot_line.setText("Nie")
            else:
                self.ui.plot_line.setText("Tak")
        else:
            self.ui.graph.hide()
            self.ui.por_line.setText(str(it))
            self.ui.czas_line.setText(str(tim / 1000))
            self.ui.nzd_line.setText(str(len(new_nz) / len(pts) * 100))
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

            # self.ui.info_lab.setText("Wczytano plik!")
            df = pd.read_excel(response[0], header=None)
            # self.critNum = df.shape[1]
            #
            # lc = []
            # if self.critNum == 1:
            #     comboBox = QtWidgets.QComboBox()
            #     comboBox.addItem("Min")
            #     comboBox.addItem("Max")
            #     self.ui.criteriaTable.setRowCount(self.critNum)
            #     lc.append("Kryterium 1")
            #     self.ui.criteriaTable.setItem(0, 0, QTableWidgetItem(f"Kryterium {1}"))
            #     self.ui.criteriaTable.setCellWidget(0, 1, comboBox)
            # else:
            #     self.ui.criteriaTable.setRowCount(self.critNum)
            #     for i in range(self.critNum):
            #         comboBox = QtWidgets.QComboBox()
            #         comboBox.addItem("Min")
            #         comboBox.addItem("Max")
            #         lc.append(f"Kryterium {i + 1}")
            #         self.ui.criteriaTable.setItem(i, 0, QTableWidgetItem(f"Kryterium {i + 1}"))
            #         self.ui.criteriaTable.setCellWidget(i, 1, comboBox)
            #
            # self.ui.valuesTable.setRowCount(df.shape[0])
            # self.ui.valuesTable.setColumnCount(df.shape[1])
            # self.ui.valuesTable.setHorizontalHeaderLabels(lc)
            # xi = 0
            # yi = 0
            # for i in df.values:
            #     for j in i:
            #         self.ui.valuesTable.setItem(xi, yi, QTableWidgetItem(str(j)))
            #         yi += 1
            #     yi = 0
            #     xi += 1
            # self.ui.benchmark_btn.setEnabled(True)
            # self.ui.start_btn.setEnabled(True)

        except:
            pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
