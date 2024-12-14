# This Python file uses the following encoding: utf-8
import os
import sys

import numpy as np
import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from RSM.RSM_new import rsm_discrete
from SP_CS.SP_CS_gui import sp_cs
from TOPSIS.FUZZY_TOPSIS import fuzzy_topsis
from UTA_BIS.UTA_DIS import UTA_DIS
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.critNum = 0

        self.ui.load_btn.clicked.connect(self.getFileName)
        self.ui.graph.hide()

        self.ui.start_btn.clicked.connect(self.startAlgo)

    def visualize(self, data, utilities, criterion1=0, criterion2=1, criterion3=2, title="Tytuł"):
        """
        Wizualizacja alternatyw w 3D w PySide6. Zakładamy co najmniej 3 kryteria.
        """

        self.ui.graph.canvas.axes.clear()
        self.ui.graph.show()
        try:
            if self.ui.graph.canvas.axes is not None:
                self.ui.graph.canvas.figure.delaxes(self.ui.graph.canvas.axes)
                self.ui.graph.canvas.figure.clf()

        except:
            pass

        if title == "FUZZY TOPSIS":
            middle_points = [[(l[1]) for l in alt] for alt in data]
            middle_points = np.array(middle_points)
            x = middle_points[:, 0]
            y = middle_points[:, 1]
            z = middle_points[:, 2]
        else:
            # Tworzenie danych do wizualizacji
            x = [d[criterion1] for d in data]
            y = [d[criterion2] for d in data]
            z = [d[criterion3] for d in data]

        self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111, projection='3d')
        # Tworzenie wykresu 3D

        scatter = self.ui.graph.canvas.axes.scatter(
            x, y, z,
            c=utilities,
            cmap='viridis',
            edgecolor='k',
            s=100
        )

        # Dodanie opisu osi i tytułu
        self.ui.graph.canvas.axes.set_xlabel(f"Kryterium {criterion1 + 1}")
        self.ui.graph.canvas.axes.set_ylabel(f"Kryterium {criterion2 + 1}")
        self.ui.graph.canvas.axes.set_zlabel(f"Kryterium {criterion3 + 1}")
        self.ui.graph.canvas.axes.set_title(title)

        # Dodanie paska kolorów
        self.ui.graph.canvas.figure.colorbar(scatter, ax=self.ui.graph.canvas.axes, label="S(u)")

        # Aktualizacja płótna (canvas)
        self.ui.graph.canvas.draw()

    def hide_graph(self):
        self.ui.graph.canvas.axes.clear()
        self.ui.graph.hide()

    def getFileName(self):
        try:
            response = QFileDialog.getOpenFileName(
                self, 'Select a data file', os.getcwd(), "Excel files (*.xlsx *.csv )"
            )
            # self.ui.info_lab.setText("Wczytano plik!")
            df = pd.read_excel(response[0], header=0, sheet_name="Arkusz1")
            self.critNum = df.shape[1]
            lc = list(df.columns.values)
            if self.critNum == 1:
                self.ui.alternatives_table.setRowCount(df.shape[0])
                self.ui.alternatives_table.setColumnCount(self.critNum)
                for i in range(df.shape[0]):
                    print(df["Nazwa alternatywy"][i])
                    self.ui.alternatives_table.setItem(i, 0, QTableWidgetItem(str(df["Nr alternatywy"][i])))
                    self.ui.alternatives_table.setItem(i, 1, QTableWidgetItem(df["Nazwa alternatywy"][i]))
                    for j in range(len(lc)):
                        if j == 0 or j == 1:
                            pass
                        else:
                            self.ui.alternatives_table.setItem(i, j, QTableWidgetItem(str(df[f"Kryterium {j - 1}"][i])))
            else:
                self.ui.alternatives_table.setRowCount(df.shape[0])
                self.ui.alternatives_table.setColumnCount(self.critNum)
                for i in range(df.shape[0]):
                    self.ui.alternatives_table.setItem(i, 0, QTableWidgetItem(str(df["Nr alternatywy"][i])))
                    self.ui.alternatives_table.setItem(i, 1, QTableWidgetItem(df["Nazwa alternatywy"][i]))
                    for j in range(len(lc)):
                        if j == 0 or j == 1:
                            pass
                        else:
                            self.ui.alternatives_table.setItem(i, j, QTableWidgetItem(str(df[f"Kryterium {j - 1}"][i])))

            self.ui.alternatives_table.setHorizontalHeaderLabels(lc)

            df2 = pd.read_excel(response[0], header=0, sheet_name="Arkusz2")
            lc2 = list(df2.columns.values)
            if df2.shape[1] == 1:
                self.ui.class_table.setRowCount(df2.shape[0])
                self.ui.class_table.setColumnCount(df2.shape[1])
                self.ui.class_table.setItem(0, 0, QTableWidgetItem(df2["Nr klasy"][0]))
                # self.ui.criteriaTable.setCellWidget(0, 1, comboBox)
            else:
                self.ui.class_table.setRowCount(df2.shape[0])
                self.ui.class_table.setColumnCount(df2.shape[1])
                for i in range(df2.shape[0]):
                    self.ui.class_table.setItem(i, 0, QTableWidgetItem(str(df2["Nr klasy"][i])))
                    for j in range(len(lc2)):
                        if j == 0:
                            pass
                        else:
                            self.ui.class_table.setItem(i, j, QTableWidgetItem(str(df2[str(lc2[j])][i])))

            self.ui.class_table.setHorizontalHeaderLabels(lc2)

            self.ui.alternatives_table.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)

            self.ui.alternatives_table.resizeColumnsToContents()

            self.ui.class_table.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)

            self.ui.class_table.resizeColumnsToContents()

            msg = QMessageBox()
            msg.setText("Poprawnie załadowano dane z arkusza.")
            msg.setWindowTitle("Sukces")
            msg.setIcon(QMessageBox.Information)
            button = msg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
        except:
            msg = QMessageBox()
            msg.setText("W trakcie ładowania arkusza wystąpił błąd!")
            msg.setWindowTitle("Błąd!")
            msg.setIcon(QMessageBox.Critical)
            button = msg.exec()
            if button == QMessageBox.Ok:
                print("OK!")

    def startAlgo(self):

        metryka = self.ui.metric_select.currentText()
        wariant = self.ui.variant_select.currentText()
        sample_num = int(self.ui.sample_num.text())
        bounds = (int(self.ui.lower_bound.text()), int(self.ui.upper_bound.text()))

        metrica = None
        variant = None
        if metryka == "Euklidesowa":
            metrica = "euclidean"
        elif metryka == "Czebyszewa":
            metrica = "chebyshev"

        if wariant == "Ciągły":
            variant = "continuous"
        elif wariant == "Dyskretny":
            variant = "discrete"


        if self.ui.criterium_select.currentText() == "FUZZY TOPSIS":
            A = []
            for i in range(self.ui.alternatives_table.rowCount()):
                A.append([])
                for j in range(2, self.ui.alternatives_table.columnCount()):
                    val = float(self.ui.alternatives_table.item(i, j).text())
                    A[i].append((val-1, val, val+1))

            # A = [
            #     [(1, 2, 3), (3, 4, 5), (2, 3, 4)],
            #     [(42, 43, 44), (41, 42, 43), (43, 44, 45)],
            #     [(83, 84, 85), (82, 83, 84), (81, 82, 83)],
            # ]

            title = "FUZZY TOPSIS"
            if self.ui.opti_type.currentText() == "Minimalizacja":
                criteria_discrete = [False] * len(A[0])
            else:
                criteria_discrete = [True] * len(A[0])

            weights_discrete = [(1, 1, 1),
                                (1, 1, 1),
                                (1, 1, 1)]

            ranking_discrete, details_discrete = fuzzy_topsis(A, criteria_discrete, weights_discrete,
                                                              variant=variant, metric=metrica, num_samples=sample_num, bounds=[bounds]*len(A))

            ranking = dict()
            for i in range(len(ranking_discrete)):
                ranking[ranking_discrete[i]+1] = details_discrete['closeness'][i]
            sorted_ranking = sorted(ranking.items(), key=lambda h: h[1], reverse=True)

            print("\nCałkowite użyteczności alternatyw:")
            print(sorted_ranking)

            num = 0
            for (k, v) in sorted_ranking:
                self.ui.ranking_table.setRowCount(len(sorted_ranking))
                self.ui.ranking_table.setColumnCount(2)

                self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(k)))
                self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(v)))
                num += 1

            self.ui.ranking_table.setHorizontalHeaderLabels(["Nr alternatywy", "Wynik"])

            self.ui.ranking_table.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)

            self.ui.ranking_table.resizeColumnsToContents()

            ranks = dict()

            for i in ranking_discrete:
                ranks[i] = details_discrete['closeness'][i]

            self.visualize(A, details_discrete['closeness'], title=title)

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

            if self.ui.opti_type.currentText() == "Minimalizacja":
                criteria = [False] * len(A_3d[0])
            else:
                criteria = [True] * len(A_3d[0])

            # Obliczanie punktów i ich odległości
            discrete_results_3d = rsm_discrete(
                reference_points=A_3d,
                decision_points=B_3d,
                min_max=criteria,
            )
            data, utilities = zip(*discrete_results_3d)
            data = list(data)
            utilities = list(utilities)

            title = "RSM"
            print("Punkty w wariancie dyskretnym (posortowane według odległości):")
            for point, score in discrete_results_3d:
                print(f"Point: {np.round(point, 4)}, Score: {score:.4f}")

        elif self.ui.criterium_select.currentText() == "SP CS":
            title = "SP CS"

            A = []
            for i in range(self.ui.alternatives_table.rowCount()):
                A.append([])
                for j in range(2, self.ui.alternatives_table.columnCount()):
                    A[i].append(float(self.ui.alternatives_table.item(i, j).text()))

            if self.ui.opti_type.currentText() == "Minimalizacja":
                minmax_example = [False] * len(A[0])
            else:
                minmax_example = [True] * len(A[0])

            ranking = sp_cs(A, minmax_example, metric=metrica, debug=False)
            sorted_ranking = sorted(ranking, key=lambda h: h[1], reverse=True)
            self.visualize(A, [s[1] for s in sorted_ranking], title=title)

        elif self.ui.criterium_select.currentText() == "UTA DIS":
            A = []
            for i in range(self.ui.alternatives_table.rowCount()):
                A.append([])
                for j in range(2, self.ui.alternatives_table.columnCount()):
                    A[i].append(float(self.ui.alternatives_table.item(i, j).text()))
            A = np.array(A)

            # A = np.array([
            #     [12, 12, 12],
            #     [7, 8, 7],
            #     [6, 7, 6],
            #     [5, 6, 5],
            #     [4, 5, 4],
            #     [3, 4, 3]
            # ])

            title = "UTA DIS"
            # Maksymalizacja dla 1. i 3. kryterium, minimalizacja dla 2.
            if self.ui.opti_type.currentText() == "Minimalizacja":
                minmax = [False] * len(A[0])
            else:
                minmax = [True] * len(A[0])

            # Wagi kryteriów
            weights = [0.4, 0.3, 0.3]

            # Progi definiujące kategorie
            thresholds = [0.3, 0.5, 0.7]

            # Klasyfikacja alternatyw do kategorii
            categories, total_utilities = UTA_DIS(A, minmax, weights, thresholds)

            ranking = dict()
            for num, x in enumerate(total_utilities):
                ranking[num + 1] = float(x)

            sorted_ranking = sorted(ranking.items(), key=lambda h: h[1], reverse=True)

            print("\nCałkowite użyteczności alternatyw:")
            print(total_utilities)
            print(sorted_ranking)

            print("\nPrzypisane kategorie:")
            print(categories)
            self.visualize(A, [s[1] for s in sorted_ranking], title=title)

        num = 0
        for (k, v) in sorted_ranking:
            self.ui.ranking_table.setRowCount(len(sorted_ranking))
            self.ui.ranking_table.setColumnCount(2)

            self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(k)))
            self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(v)))
            num += 1

        self.ui.ranking_table.setHorizontalHeaderLabels(["Nr alternatywy", "Wynik"])

        self.ui.ranking_table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.ui.ranking_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
