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
from RSM.RSM_new import rsm_discrete
from SP_CS.SP_CS import sp_cs_continuous
from TOPSIS.FUZZY_TOPSIS import fuzzy_topsis
from UTA_BIS.UTA_DIS import UTA_DIS
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.load_btn.clicked.connect(self.getFileName)
        self.ui.graph.show()

        self.ui.start_btn.clicked.connect(self.startAlgo)

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

    def startAlgo(self):
        if self.ui.criterium_select.currentText() == "FUZZY TOPSIS":
            alternatives_discrete = [
                [(1, 2, 3), (1, 2, 3), (1, 2, 3)],
                [(2, 3, 4), (2, 3, 4), (2, 3, 4)],
                [(3, 4, 5), (3, 4, 5), (3, 4, 5)],
                [(4, 5, 6), (4, 5, 6), (4, 5, 6)],
            ]

            criteria_discrete = ['benefit', 'benefit', 'benefit']
            weights_discrete = [(0.3, 0.6, 0.1), (0.2, 0.5, 0.3), (0.1, 0.8, 0.1), (0.5, 0.2, 0.3)]

            ranking_discrete, details_discrete = fuzzy_topsis(alternatives_discrete, criteria_discrete,
                                                              weights_discrete)

            print("\nDiscrete Case Ranking:", ranking_discrete)
            print("Details (Discrete):", details_discrete)

        elif self.ui.criterium_select.currentText() == "RSM":
            A_3d = [
                [2, 3, 4],
                [-1, 1, 2],
                [1, 3, 4],
                [1, 1, 2],
                [2, 2, 4],
                [0, 0, 0],
            ]  # Punkty odniesienia (3D)
            B_3d = [[3, 4, 5], [5, 1, 2], [1, 2, 3], [3, 3, 4]]  # Punkty dopuszczalne (3D)

            # Obliczanie punktów i ich odległości
            discrete_results_3d = rsm_discrete(
                reference_points=A_3d,
                decision_points=B_3d,
                min_max_criterial=["min", "min", "min"],
            )
            data, utilities = zip(*discrete_results_3d)
            data = list(data)
            utilities = list(utilities)

            print("Punkty w wariancie dyskretnym (posortowane według odległości):")
            for point, score in discrete_results_3d:
                print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

        elif self.ui.criterium_select.currentText() == "SP CS":
            print("\n=== Case 3: All Criteria Maximized ===")
            status_quo_continuous = [0, 0]
            aspiration_continuous = [1, 1]
            bounds = [(0, 1), (0, 1)]  # U⊂R²
            minmax_continuous_case1 = [True, True]  # Both criteria maximized

            # Determine dynamic status quo and aspiration for continuous variant
            # Assuming the continuous alternatives are generated within the bounds
            # For demonstration, we use fixed aspiration and status quo

            results_continuous_case1, alternatives_continuous_case1 = sp_cs_continuous(
                bounds,
                status_quo_continuous,
                aspiration_continuous,
                minmax_continuous_case1,
                metric='euclidean',
                num_samples=1000,
                num_t_samples=100,
                debug=False
            )

            print("\nTop 5 alternatives in continuous variant (sorted by S(u)):")
            for alt, Su, t_star in results_continuous_case1[:5]:
                print(f"Alternative: {np.round(alt, 4)}, S(u): {Su:.4f}, t*: {t_star:.4f}")

        elif self.ui.criterium_select.currentText() == "UTA DIS":
            A = np.array([
                [12, 0.01024, 24.0646],
                [1, 0.00026, 62.1609],
                [4, 0.02004, 24.1212],
                [1, -0.27064, 23.2374],
                [2, 0.00476, 0.0327],
                [1, 0.11461, 33.8748]
            ])

            # Maksymalizacja dla 1. i 3. kryterium, minimalizacja dla 2.
            minmax = [True, False, True]

            # Wagi kryteriów
            weights = [0.4, 0.3, 0.3]

            # Progi definiujące kategorie
            thresholds = [0.3, 0.5, 0.7]

            # Klasyfikacja alternatyw do kategorii
            categories, total_utilities = UTA_DIS(A, minmax, weights, thresholds)
            print("\nCałkowite użyteczności alternatyw:")
            print(total_utilities)
            print("\nPrzypisane kategorie:")
            print(categories)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
