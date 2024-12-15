# This Python file uses the following encoding: utf-8
import os
import sys
import random

import numpy as np
import pandas as pd
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from matplotlib import cm
from matplotlib.colors import Normalize

from RSM.RSM_new import rsm_discrete, rsm_continuous
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

    def visualize_discrete(self, data, utilities, title="Tytuł"):
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
            x = [d[0] for d in data]
            y = [d[1] for d in data]
            z = [d[2] for d in data]

        self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111, projection='3d')
        # Tworzenie wykresu 3D

        min_val = min(utilities)
        max_val = max(utilities)

        # Scale the values
        # scaled_values = [(v - min_val) / (max_val - min_val) for v in utilities]
        # print(scaled_values)
        scatter = self.ui.graph.canvas.axes.scatter(
            x, y, z,
            c=utilities,
            cmap='viridis',
            edgecolor='k',
            s=100
        )

        # Dodanie opisu osi i tytułu
        self.ui.graph.canvas.axes.set_xlabel(f"Kryterium {1}")
        self.ui.graph.canvas.axes.set_ylabel(f"Kryterium {2}")
        self.ui.graph.canvas.axes.set_zlabel(f"Kryterium {3}")
        self.ui.graph.canvas.axes.set_title(title)

        # Dodanie paska kolorów
        self.ui.graph.canvas.figure.colorbar(scatter, ax=self.ui.graph.canvas.axes, label="S(u)")

        # Aktualizacja płótna (canvas)
        self.ui.graph.canvas.draw()

    def visualize(self, data, utilities, title="Tytuł"):
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

            # Sort alternatives by closeness coefficients in descending order
            sorted_indices = np.argsort(list(utilities.values()))[::-1]

            # Normalize closeness values to use the full color scale
            norm = Normalize(vmin=min(utilities.values()), vmax=max(utilities.values()))
            cmap = cm.viridis  # Using the reversed viridis color map

            # Generate colors based on the normalized closeness values
            colors = [cmap(norm(utilities[sorted_indices[i]])) for i in range(len(sorted_indices))]
        else:
            # Tworzenie danych do wizualizacji
            middle_points = data
            sorted_indices = np.argsort(list(utilities.values()))[::-1]

            # Normalize closeness values to use the full color scale
            norm = Normalize(vmin=min(utilities.values()), vmax=max(utilities.values()))
            cmap = cm.viridis  # Using the reversed viridis color map

            # Generate colors based on the normalized closeness values
            colors = [cmap(norm(utilities[sorted_indices[i]])) for i in range(len(sorted_indices))]

        self.ui.graph.canvas.axes = self.ui.graph.canvas.figure.add_subplot(111, projection='3d')
        # Tworzenie wykresu 3D
        print(sorted_indices)
        for rank, idx in enumerate(sorted_indices):
            point = middle_points[idx]
            self.ui.graph.canvas.axes.scatter(
                point[0], point[1], point[2],
                color=colors[rank],
                label=f"Alternative {idx + 1} (Rank: {rank + 1})"
            )

        # Dodanie opisu osi i tytułu
        self.ui.graph.canvas.axes.set_xlabel(f"Kryterium {1}")
        self.ui.graph.canvas.axes.set_ylabel(f"Kryterium {2}")
        self.ui.graph.canvas.axes.set_zlabel(f"Kryterium {3}")
        self.ui.graph.canvas.axes.set_title(title)


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
            title = "FUZZY TOPSIS"

            A = []
            for i in range(self.ui.alternatives_table.rowCount()):
                A.append([])
                for j in range(2, self.ui.alternatives_table.columnCount()):
                    val = float(self.ui.alternatives_table.item(i, j).text())
                    A[i].append((val-1, val, val+1))
            weights_discrete = [(1, 1, 1)]* len(A[0])

            if variant == "continuous":
                if self.ui.opti_type.currentText() == "Minimalizacja":
                    criteria_discrete = [False] * len(A[0])
                else:
                    criteria_discrete = [True] * len(A[0])

                ranking_discrete, details_discrete = fuzzy_topsis(A, criteria_discrete, weights_discrete,
                                                                  variant=variant, metric=metrica, num_samples=sample_num, bounds=[bounds]*len(A[0]))
            else:
                if self.ui.opti_type.currentText() == "Minimalizacja":
                    criteria_discrete = [False] * len(A[0])
                else:
                    criteria_discrete = [True] * len(A[0])
                ranking_discrete, details_discrete = fuzzy_topsis(A, criteria_discrete, weights_discrete,
                                                                  variant=variant, metric=metrica, num_samples=sample_num, bounds=[bounds]*len(A[0]))

            ranking = dict()
            for i in range(len(ranking_discrete)):
                ranking[ranking_discrete[i]] = details_discrete['closeness'][i]
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

            if variant == "continuous":
                for i in ranking_discrete:
                    ranks[i] = details_discrete['closeness'][i]

                alternatives_continuous = [
                    [(1, 3, 5), (2, 4, 6), (3, 5, 7), (1, 2, 3)],
                    [(22, 24, 26), (21, 23, 25), (22, 24, 26), (22, 23, 24)],
                    [(43, 45, 47), (43, 45, 47), (41, 43, 45), (42, 44, 46)],
                    [(71, 72, 73), (72, 73, 74), (73, 75, 77), (73, 75, 77)],
                ]

                criteria = [False] * len(A[0])
                weights_continuous = [(1.0, 1.0, 1.0)] * len(A[0])

                ranking_continuous, details_discrete = fuzzy_topsis(A, criteria_discrete,
                                                                      weights_continuous, variant="continuous",
                                                                      num_samples=sample_num,
                                                                      bounds=[bounds]*len(A[0]))
                ranks = dict()
                for i in ranking_continuous:
                    ranks[i] = details_discrete['closeness'][i]

                self.visualize(details_discrete["samples"], ranks, title=title)

            elif variant == "discrete":
                self.visualize_discrete(A, details_discrete['closeness'], title=title)

        elif self.ui.criterium_select.currentText() == "RSM":

            title = "RSM"

            if variant == "continuous":
                if self.ui.opti_type.currentText() == "Minimalizacja":
                    criteria = [False] * 4
                else:
                    criteria = [True] * 4

                bounds_continuous_4d = [bounds]*4

                lower_bound = max(0, bounds[0] - 2)
                upper_bound = min(10, bounds[1] + 2)

                A_4d_cont = [
                    [random.randint(lower_bound, upper_bound) for _ in range(4)] for _ in range(5)
                ]  # Punkty odniesienia (4D)

                results = rsm_continuous(
                    num_samples=sample_num,
                    bounds=bounds_continuous_4d,
                    reference_points=np.array(A_4d_cont),
                    min_max=criteria
                )

            elif variant == "discrete":

                A = []
                for i in range(self.ui.alternatives_table.rowCount()):
                    A.append([])
                    for j in range(2, self.ui.alternatives_table.columnCount()):
                        A[i].append(float(self.ui.alternatives_table.item(i, j).text()))

                lower_bound = 0
                upper_bound = 10
                B = [
                    [random.randint(lower_bound, upper_bound) for _ in range(len(A[0]))] for _ in range(5)
                ]

                if self.ui.opti_type.currentText() == "Minimalizacja":
                    criteria = [False] * len(A[0])
                else:
                    criteria = [True] * len(A[0])

                results = rsm_discrete(
                    reference_points=np.array(B),
                    decision_points=np.array(A),
                    min_max=criteria,
                )

            d = dict()
            for idx, v in enumerate(results):
                d[idx] = v[1]
            self.visualize([v[0] for v in results], d, title=title)
            print(results)

            num = 0
            if variant == "continuous":
                for idx, (point, score, cls) in enumerate(results):
                    self.ui.ranking_table.setRowCount(len(results))
                    self.ui.ranking_table.setColumnCount(4)

                    self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(idx +1)))
                    self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(score)))
                    self.ui.ranking_table.setItem(num, 2, QTableWidgetItem(str(point)))
                    self.ui.ranking_table.setItem(num, 3, QTableWidgetItem(str(cls)))
                    num += 1

                self.ui.ranking_table.setHorizontalHeaderLabels(
                    ["Pozycja w rankingu", "Wynik", "Punkt", "Klasa"])

            elif variant == "discrete":
                for idx, (point, score, cls) in enumerate(results):
                    self.ui.ranking_table.setRowCount(len(results))
                    self.ui.ranking_table.setColumnCount(5)

                    self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(idx + 1)))
                    self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(A.index(point) + 1)))
                    self.ui.ranking_table.setItem(num, 2, QTableWidgetItem(str(score)))
                    self.ui.ranking_table.setItem(num, 3, QTableWidgetItem(str(point)))
                    self.ui.ranking_table.setItem(num, 4, QTableWidgetItem(str(cls)))
                    num += 1

                self.ui.ranking_table.setHorizontalHeaderLabels(["Pozycja w rankingu", "Nr alternatywy", "Wynik", "Punkt", "Klasa"])

            self.ui.ranking_table.setSizeAdjustPolicy(
                QtWidgets.QAbstractScrollArea.AdjustToContents)

            self.ui.ranking_table.resizeColumnsToContents()

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
            print(ranking)
            sorted_ranking = sorted(ranking, key=lambda h: h[1], reverse=True)
            self.visualize_discrete(A, [s[1] for s in sorted_ranking], title=title)

            num = 0
            for (k, v) in sorted_ranking:
                self.ui.ranking_table.setRowCount(len(sorted_ranking))
                self.ui.ranking_table.setColumnCount(2)

                self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(k+1)))
                self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(v)))
                num += 1

        elif self.ui.criterium_select.currentText() == "UTA DIS":

            title = "UTA DIS"

            A = []
            for i in range(self.ui.alternatives_table.rowCount()):
                A.append([])
                for j in range(2, self.ui.alternatives_table.columnCount()):
                    A[i].append(float(self.ui.alternatives_table.item(i, j).text()))
            A = np.array(A)


            # Maksymalizacja dla 1. i 3. kryterium, minimalizacja dla 2.
            if self.ui.opti_type.currentText() == "Minimalizacja":
                minmax = [False] * len(A[0])
            else:
                minmax = [True] * len(A[0])

            # Wagi kryteriów
            weights = [1.0] * len(A[0])

            # Progi definiujące kategorie
            thresholds = [0.3, 0.5, 0.7]

            # Klasyfikacja alternatyw do kategorii
            if variant == "discrete":
                categories, total_utilities, _ = UTA_DIS(A, minmax, weights, thresholds, continuous=False)
                ranking = dict()
                for num, x in enumerate(total_utilities):
                    ranking[num] = float(x)

                sorted_ranking = sorted(ranking.items(), key=lambda h: h[1], reverse=True)

                print("\nCałkowite użyteczności alternatyw:")
                print(total_utilities)
                print(sorted_ranking)

                self.visualize(A, ranking, title=title)
            else:
                weights = [1.0] * 4
                if self.ui.opti_type.currentText() == "Minimalizacja":
                    minmax = [False] * 4
                else:
                    minmax = [True] * 4
                thresholds = [0.3, 0.5, 0.7, 1.0]
                categories, total_utilities, A = UTA_DIS(A, minmax, weights, thresholds, continuous=True, bounds=[bounds]*4, num_samples=sample_num)
                ranking = dict()
                for num, x in enumerate(total_utilities):
                    ranking[num] = float(x)

                sorted_ranking = sorted(ranking.items(), key=lambda h: h[1], reverse=True)

                print("\nCałkowite użyteczności alternatyw:")
                print(total_utilities)
                print(sorted_ranking)
                self.visualize(A, ranking, title=title)

            num = 0
            for (k, v) in sorted_ranking:
                self.ui.ranking_table.setRowCount(len(sorted_ranking))
                self.ui.ranking_table.setColumnCount(2)

                self.ui.ranking_table.setItem(num, 0, QTableWidgetItem(str(k)))
                self.ui.ranking_table.setItem(num, 1, QTableWidgetItem(str(v)))
                num += 1

        if self.ui.criterium_select.currentText() != "RSM":
            self.ui.ranking_table.setHorizontalHeaderLabels(["Nr alternatywy", "Wynik"])

        self.ui.ranking_table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.ui.ranking_table.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
