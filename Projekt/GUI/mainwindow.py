# This Python file uses the following encoding: utf-8
import os
import sys
import time

import numpy as np
import pandas as pd
from PIL import Image
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from algorytmy.ASTAR_multi import astar
from algorytmy.CSO import algorithm

from algorytmy.TSP3D_multi import run_multi_robot_tsp3d_path
from algorytmy.terrain import terrain_generator
from ui_form import Ui_MainWindow
from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flag = True
        self.thread = None
        self.all_costs = []
        self.all_best_vals = []
        self.paths = []

        self.ui.map_plot.hide()
        self.ui.cost_plot.hide()
        self.ui.result_plot.hide()
        self.ui.generate_map_btn.clicked.connect(self.visualize_map)
        self.ui.start_btn.clicked.connect(self.start)


        self.ui.animation_btn.clicked.connect(self.visualize_animation)
        self.ui.openFile_btn.clicked.connect(self.getFileName)
        self.ui.read_image_btn.clicked.connect(self.getImageName)

        self.ui.algorithm_type.currentIndexChanged.connect(self.change_prams)
        self.ui.generator_radio.clicked.connect(self.radioclick)
        self.ui.image_radio.clicked.connect(self.radioclick)

    def radioclick(self):
        if not self.ui.generator_radio.isChecked():
            self.ui.map_type.setEnabled(False)
            self.ui.noise_num.setEnabled(False)
            self.ui.terrain_y.setEnabled(False)
            self.ui.terrain_x.setEnabled(False)
        else:
            self.ui.map_type.setEnabled(True)
            self.ui.noise_num.setEnabled(True)
            self.ui.terrain_y.setEnabled(True)
            self.ui.terrain_x.setEnabled(True)

    def change_prams(self):
        if self.ui.algorithm_type.currentText() == "A-STAR":
            self.ui.stackedWidget.setCurrentIndex(0)
        elif self.ui.algorithm_type.currentText() == "CSO":
            self.ui.stackedWidget.setCurrentIndex(1)
        elif self.ui.algorithm_type.currentText() == "TSP GA":
            self.ui.stackedWidget.setCurrentIndex(2)

    def start(self):
        A = []
        for i in range(self.ui.beg_points_table.rowCount()):
            A.append([])
            for j in range(1, self.ui.beg_points_table.columnCount()):
                print(self.ui.beg_points_table.item(i, j).text())
                val = int(self.ui.beg_points_table.item(i, j).text())
                A[i].append(val)

        A_list = []
        for i in A:
            A_list.append((i[0], i[1]))

        start_positions = A_list
        self.starts = start_positions
        goal = (int(self.ui.stop_point_y.value()), int(self.ui.stop_point_x.value()))

        if self.ui.algorithm_type.currentText() == "A-STAR":
            # ASTAR
            occupied_positions = list()
            self.paths = []

            beg = time.time()
            self.all_costs = []
            self.all_best_vals = []
            for start in start_positions:

                path, min_val, costs, costs_f = astar(self.terrain, start, goal, occupied_positions, robot_distance=int(self.ui.robot_dist_num.value()) ,
                             terrain_weight=int(self.ui.terrain_weight_num.value()), robot_distance_weight=int(self.ui.robodist_weight_num.value()))
                self.all_costs.append(costs)
                self.all_best_vals.append(min_val)
                print(" -------------------- ")
                if path:
                    self.paths.append(path)
                    occupied_positions.append(path)  # Aktualizacja zajętych pozycji
                else:
                    print(f"Brak możliwej ścieżki dla robota z pozycji {start}")

            end = time.time()

            self.ui.ASTAR_time_line.setText(str(end-beg))

            max_len = max(len(p) for p in self.paths)

            # Ustawienie liczby wierszy i kolumn w tabeli
            self.ui.result_table.setRowCount(max_len)  # Liczba wierszy to liczba ścieżek
            self.ui.result_table.setColumnCount(len(self.paths))  # Liczba kolumn to maksymalna długość ścieżki

            # Wypełnienie tabeli danymi
            for i, p in enumerate(self.paths):
                for j, pi in enumerate(p):
                    self.ui.result_table.setItem(j, i, QTableWidgetItem(str(pi)))
            self.ui.result_table.setHorizontalHeaderLabels(self.labels)

            print("100% completed!")


            max_len = max(len(ac) for ac in self.all_costs)
            self.ui.cost_table.setRowCount(max_len)  # Liczba wierszy to liczba ścieżek
            self.ui.cost_table.setColumnCount(len(self.paths))  # Liczba kolumn to maksymalna długość ścieżki

            # Wypełnienie tabeli danymi
            for i, ac in enumerate(self.all_costs):
                for j, aci in enumerate(ac):
                    self.ui.cost_table.setItem(j, i, QTableWidgetItem(str(aci)))
            self.ui.cost_table.setHorizontalHeaderLabels(self.labels)

        elif self.ui.algorithm_type.currentText() == "CSO":

            occupied_positions = []
            paths = []

            beg = time.time()

            for start in A:
                result_path, _ = algorithm(
                    start=start,
                    end=[int(self.ui.stop_point_y.value()), int(self.ui.stop_point_x.value())],
                    map_size=(len(self.terrain), len(self.terrain[0])),
                    terrain=self.terrain,
                    visibility_range=10,
                    occupied_positions=[],
                    cockroaches_num = int(self.ui.vehicle_num.value())
                )
                print("poszło")
                self.paths.append(result_path)
                occupied_positions.append(result_path)

            end = time.time()
            self.ui.CSO_time_line.setText(str(end - beg))

            print("100% completed!")
        elif self.ui.algorithm_type.currentText() == "TSP GA":

            # Parametry GA
            pop_size = int(self.ui.generation_size_num.value())
            num_of_generations = int(self.ui.generation_num.value())
            elite_size = 5
            tournament_size = 3
            offspring_rate = float(self.ui.offspring_percent_num.value())
            mutation_rate = float(self.ui.mutation_percent_num.value())

            beg = time.time()
            # Uruchamiamy wielorobotowe planowanie
            self.paths = run_multi_robot_tsp3d_path(
                self.terrain,
                self.starts,
                [goal]*len(self.starts),
                pop_size=pop_size,
                num_of_generations=num_of_generations,
                elite_size=elite_size,
                tournament_size=tournament_size,
                offspring_rate=offspring_rate,
                mutation_rate=mutation_rate
            )

            end = time.time()
            self.ui.TSPGA_time_line.setText(str(end - beg))

            max_len = max(len(p) for p in self.paths)

            # Ustawienie liczby wierszy i kolumn w tabeli
            self.ui.result_table.setRowCount(max_len)  # Liczba wierszy to liczba ścieżek
            self.ui.result_table.setColumnCount(len(self.paths))  # Liczba kolumn to maksymalna długość ścieżki

            # Wypełnienie tabeli danymi
            for i, p in enumerate(self.paths):
                for j, pi in enumerate(p):
                    self.ui.result_table.setItem(j, i, QTableWidgetItem(str(pi)))
            self.ui.result_table.setHorizontalHeaderLabels(self.labels)

        ### Zobrazowanie wyników
        self.visualize_results()
        self.visualize_cost_plot()
        algo_time = end-beg
        print(algo_time)

    def visualize_map(self):
        """
        Wizualizacja alternatyw w 3D w PySide6. Zakładamy co najmniej 3 kryteria.
        """

        def map_terrain_type(map_type):
            ans = ""
            if map_type == "Wzgórza":
                ans = "hills"
            elif map_type == "Linie":
                ans = "lines"
            elif map_type == "Skos":
                ans = "slope"
            elif map_type == "Zęby":
                ans = "razors"
            elif map_type == "Kanion":
                ans = "canyon"
            elif map_type == "Łuk":
                ans = "bow"
            elif map_type == "Labirynt":
                ans = "maze"
            return ans

        self.ui.map_plot.canvas.axes.clear()
        self.ui.map_plot.show()

        # Generowanie terenu
        if self.ui.generator_radio.isChecked():
            self.terrain = terrain_generator(noise_num=float(self.ui.noise_num.value()),
                                        terrain_size=(int(self.ui.terrain_x.value()), int(self.ui.terrain_y.value())),
                                        terrain_type=map_terrain_type(self.ui.map_type.currentText()))

        else:
            image = Image.open(self.ui.image_path.text())
            grayscale_image = image.convert('L')  # 'L' oznacza obraz w skali szarości
            matrix = np.array(grayscale_image)

            # Przekonwertuj macierz NumPy na listę list
            matrix_list_of_lists = matrix.tolist()

            # # Wyświetl wynik (listę list)
            # for row in matrix_list_of_lists:
            #     print(row)
            self.terrain = matrix_list_of_lists



        # Wyświetlanie terenu za pomocą imshow
        terrain_image = self.ui.map_plot.canvas.axes.imshow(self.terrain, origin='upper', cmap="magma")

        # Dodanie colorbar (pasek kolorów) do mapy
        if self.flag:
            self.ui.map_plot.canvas.figure.colorbar(terrain_image, ax=self.ui.map_plot.canvas.axes, label="S(u)")
            self.flag = False

        # Rysowanie obwódki dla punktu stop (większy punkt, tylko kolor obwódki)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.stop_point_x.value())],
            [int(self.ui.stop_point_y.value())],
            color="none",  # Brak wypełnienia punktu
            edgecolor="red",  # Czerwony kolor obwódki
            marker = 'o',
            s=150,  # Większy rozmiar obwódki
        )

        # Rysowanie środka punktu stop (mniejszy punkt, wypełniony)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.stop_point_x.value())],
            [int(self.ui.stop_point_y.value())],
            color="black",  # Czerwony kolor wypełnienia
            edgecolor="none",  # Brak obwódki dla środka
            marker= "*",
            s=50,  # Mniejszy rozmiar punktu
        )

        A = []
        for i in range(self.ui.beg_points_table.rowCount()):
            A.append([])
            for j in range(1, self.ui.beg_points_table.columnCount()):
                print(self.ui.beg_points_table.item(i, j).text())
                val = int(self.ui.beg_points_table.item(i, j).text())
                A[i].append(val)

        for start in A:
            # Rysowanie obwódki dla punktu start (większy punkt, tylko kolor obwódki)
            self.ui.map_plot.canvas.axes.scatter(
                start[0],
                start[1],
                color="none",  # Brak wypełnienia punktu
                edgecolor="blue",  # Niebieski kolor obwódki
                s=150,  # Większy rozmiar obwódki
            )

            # Rysowanie środka punktu start (mniejszy punkt, wypełniony)
            self.ui.map_plot.canvas.axes.scatter(
                start[0],
                start[1],
                color="black",  # Niebieski kolor wypełnienia
                edgecolor="none",  # Brak obwódki dla środka
                s=50,  # Mniejszy rozmiar punktu
            )

        # Dodanie opisu osi i tytułu
        self.ui.map_plot.canvas.axes.set_xlabel(f"X")
        self.ui.map_plot.canvas.axes.set_ylabel(f"Y")
        self.ui.map_plot.canvas.axes.set_title("Mapa")

        # Odświeżenie wykresu
        self.ui.map_plot.canvas.draw()

    def getImageName(self):
        try:
            response = QFileDialog.getOpenFileName(
                self, 'Wybierz plik graficzny', os.getcwd()[:-3] + "dane", "(*.png *.PNG *.jpg *.jpeg )"
            )

            def func():
                self.ui.info_lab.setText("Wczytano obraz!")  # Display message
                timer.stop()  # Stop the timer after showing the message
                QTimer.singleShot(5000, clear_message)  # Wait 5 seconds before clearing the message

            def clear_message():
                self.ui.info_lab.setText("")  # Clear the message after 5 seconds

            print(response)
            self.ui.image_path.setText(response[0])  # Assuming response contains a file path

            # Create the timer
            timer = QTimer()
            timer.timeout.connect(func)  # Connect the timer's timeout signal to the func method
            timer.start(50)  # Set the interval for the timer (50 ms)

            msg = QMessageBox()
            msg.setText("Poprawnie załadowano obraz.")
            msg.setWindowTitle("Sukces")
            msg.setIcon(QMessageBox.Information)
            button = msg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
        except:
            msg = QMessageBox()
            msg.setText("W trakcie ładowania obrazu wystąpił błąd!")
            msg.setWindowTitle("Błąd!")
            msg.setIcon(QMessageBox.Critical)
            button = msg.exec()
            if button == QMessageBox.Ok:
                print("OK!")

    def getFileName(self):
        try:
            response = QFileDialog.getOpenFileName(
                self, 'Wybierz plik z danymi', os.getcwd()[:-3] + "dane", "Excel files (*.xlsx *.csv )"
            )

            def func():
                self.ui.info_lab.setText("Wczytano plik!")  # Display message
                timer.stop()  # Stop the timer after showing the message
                QTimer.singleShot(5000, clear_message)  # Wait 5 seconds before clearing the message

            def clear_message():
                self.ui.info_lab.setText("")  # Clear the message after 5 seconds

            print(response)
            self.ui.file_path.setText(response[0])  # Assuming response contains a file path

            # Create the timer
            timer = QTimer()
            timer.timeout.connect(func)  # Connect the timer's timeout signal to the func method
            timer.start(50)  # Set the interval for the timer (50 ms)

            df = pd.read_excel(response[0], header=0, )
            print(df)
            lc = list(df.columns.values)

            self.ui.beg_points_table.setRowCount(df.shape[0])
            self.ui.beg_points_table.setColumnCount(df.shape[1])
            self.labels = df["Nazwa robota"]
            for i in range(df.shape[0]):
                self.ui.beg_points_table.setItem(i, 0, QTableWidgetItem(str(df["Nazwa robota"][i])))
                self.ui.beg_points_table.setItem(i, 1, QTableWidgetItem(df["X"][i]))
                self.ui.beg_points_table.setItem(i, 2, QTableWidgetItem(df["Y"][i]))
                for j in range(df.shape[1]):
                    if j == 0:
                        pass
                    elif j == 1:
                        self.ui.beg_points_table.setItem(i, 1, QTableWidgetItem(str(df["X"][i])))
                    elif j == 2:
                        self.ui.beg_points_table.setItem(i, 2, QTableWidgetItem(str(df["Y"][i])))

            self.ui.beg_points_table.setHorizontalHeaderLabels(lc)

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

    def hide_graph(self):
        self.ui.map_plot.canvas.axes.clear()
        self.ui.map_plot.hide()

    def visualize_results(self):

        def map_terrain_type(map_type):
            ans = ""
            if map_type == "Wzgórza":
                ans = "hills"
            elif map_type == "Linie":
                ans = "lines"
            elif map_type == "Skos":
                ans = "slope"
            elif map_type == "Zęby":
                ans = "razors"
            elif map_type == "Kanion":
                ans = "canyon"
            elif map_type == "Łuk":
                ans = "bow"
            elif map_type == "Labirynt":
                ans = "maze"
            return ans

        self.ui.map_plot.canvas.axes.clear()
        self.ui.map_plot.show()

        # Wyświetlanie terenu za pomocą imshow
        terrain_image = self.ui.map_plot.canvas.axes.imshow(self.terrain, origin='upper', cmap="magma")

        # Dodanie colorbar (pasek kolorów) do mapy
        if self.flag:
            self.ui.map_plot.canvas.figure.colorbar(terrain_image, ax=self.ui.map_plot.canvas.axes, label="S(u)")
            self.flag = False


        # Rysowanie środka punktu stop (mniejszy punkt, wypełniony)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.stop_point_x.value())],
            [int(self.ui.stop_point_y.value())],
            color="black",  # Czerwony kolor wypełnienia
            edgecolor="none",  # Brak obwódki dla środka
            marker="*",
            s=50,  # Mniejszy rozmiar punktu
        )

        for start in self.starts:
            # Rysowanie środka punktu start (mniejszy punkt, wypełniony)
            self.ui.map_plot.canvas.axes.scatter(
                start[1],
                start[0],
                color="black",  # Niebieski kolor wypełnienia
                edgecolor="none",  # Brak obwódki dla środka
                marker = "o",
                s=50,  # Mniejszy rozmiar punktu
            )


        colors = ["red", "blue", "orange", "yellow", "magenta"]

        for i, path in enumerate(self.paths):
            for point in path:
                self.ui.map_plot.canvas.axes.scatter(
                    point[1], point[0],
                    facecolors=colors[i % len(colors)],
                    edgecolor="face",  # Brak obwódki dla środka
                    marker=".",
                    s=25,  # Mniejszy rozmiar punktu
                )

        # Dodanie opisu osi i tytułu
        self.ui.map_plot.canvas.axes.set_xlabel(f"X")
        self.ui.map_plot.canvas.axes.set_ylabel(f"Y")
        self.ui.map_plot.canvas.axes.set_title("Mapa")

        # Odświeżenie wykresu
        self.ui.map_plot.canvas.draw()

    def visualize_animation(self):
        def map_terrain_type(map_type):
            mapping = {
                "Wzgórza": "hills",
                "Linie": "lines",
                "Skos": "slope",
                "Zęby": "razors",
                "Kanion": "canyon",
                "Łuk": "bow",
                "Labirynt": "maze"
            }
            return mapping.get(map_type, "")

        self.ui.result_plot.canvas.axes.clear()
        self.ui.result_plot.show()

        # Wyświetlanie terenu za pomocą imshow
        terrain_image = self.ui.result_plot.canvas.axes.imshow(self.terrain, origin='upper', cmap="magma")

        # Dodanie colorbar (pasek kolorów) do mapy
        if self.flag:
            self.ui.result_plot.canvas.figure.colorbar(terrain_image, ax=self.ui.result_plot.canvas.axes, label="S(u)")
            self.flag = False

        # Rysowanie środka punktu stop (mniejszy punkt, wypełniony)
        self.ui.result_plot.canvas.axes.scatter(
            [int(self.ui.stop_point_x.value())],
            [int(self.ui.stop_point_y.value())],
            color="black",
            edgecolor="none",
            marker="*",
            s=50,
        )

        for start in self.starts:
            self.ui.result_plot.canvas.axes.scatter(
                start[1],
                start[0],
                color="black",
                edgecolor="none",
                marker="o",
                s=50,
            )

        colors = ["red", "blue", "orange", "yellow", "magenta"]

        self.current_step = 0  # Licznik do animacji

        def update_animation():
            nonlocal self
            if self.current_step < max(len(path) for path in self.paths):
                for i, path in enumerate(self.paths):
                    if self.current_step < len(path):
                        point = path[self.current_step]
                        self.ui.result_plot.canvas.axes.scatter(
                            point[1], point[0],
                            facecolors=colors[i % len(colors)],
                            edgecolor="face",
                            marker=".",
                            s=25,
                        )

                self.ui.result_plot.canvas.draw()
                self.current_step += 1
            else:
                timer.stop()  # Zatrzymanie animacji po wyświetleniu wszystkich punktów

        # Ustawienie timera dla animacji
        timer = QTimer()
        timer.timeout.connect(update_animation)
        timer.start(50)  # Czas aktualizacji w ms (100 ms = 10 FPS)

        # Dodanie opisu osi i tytułu
        self.ui.result_plot.canvas.axes.set_xlabel("X")
        self.ui.result_plot.canvas.axes.set_ylabel("Y")
        self.ui.result_plot.canvas.axes.set_title("Mapa")

        self.ui.result_plot.canvas.draw()

    def visualize_cost_plot(self):
        """
        Wizualizacja alternatyw w 3D w PySide6. Zakładamy co najmniej 3 kryteria.
        """

        self.ui.cost_plot.canvas.axes.clear()
        self.ui.cost_plot.show()

        # Rysowanie obwódki dla punktu stop (większy punkt, tylko kolor obwódki)

        num = 0
        for x in self.all_costs:
            self.ui.cost_plot.canvas.axes.plot(x, color= ["red", "blue", "orange", "yellow", "magenta"][num])
            num+=1

        # Dodanie opisu osi i tytułu
        self.ui.cost_plot.canvas.axes.set_xlabel(f"Przejście")
        self.ui.cost_plot.canvas.axes.set_ylabel(f"Wartość")
        self.ui.cost_plot.canvas.axes.set_title("Zmiany kosztu")
        self.ui.cost_plot.canvas.axes.legend(self.labels)

        # Odświeżenie wykresu
        self.ui.cost_plot.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
