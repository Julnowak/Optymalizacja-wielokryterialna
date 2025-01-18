# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from algorytmy.CSO import algorithm, plot_graph
from algorytmy.terrain import terrain_generator
from ui_form import Ui_MainWindow
from PySide6.QtCore import QThread, Signal


class AlgorithmThread(QThread):
    progress = Signal(str)  # Signal to send progress or result back to the main thread

    def __init__(self, start, end, map_size, terrain, visibility_range):
        super().__init__()
        self.start = start
        self.end = end
        self.map_size = map_size
        self.terrain = terrain
        self.visibility_range = visibility_range

    def run(self):
        # Execute the algorithm in a separate thread
        best_path = algorithm(self.start, self.end, self.map_size, self.terrain, self.visibility_range)
        self.progress.emit(str(best_path))  # Emit the result back to the main thread


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flag = True
        self.thread = None

        self.ui.map_plot.hide()
        self.ui.result_plot.hide()
        self.ui.generate_map_btn.clicked.connect(self.visualize_map)
        self.ui.start_btn.clicked.connect(self.start)


    def start(self):
        start = [0, 0]
        end = [19, 19]
        map_size = [20, 20]

        best_path, minimum_loss_values = algorithm(start=[int(self.ui.start_point_x.value()), int(self.ui.start_point_y.value())],
                              end=[int(self.ui.stop_point_x.value()), int(self.ui.stop_point_y.value())],
                              map_size=[int(self.ui.terrain_x.value()), int(self.ui.terrain_y.value())],
                              terrain=self.terrain, visibility_range=10,
                              num_of_iterations=int(self.ui.iteration_num.value()))

        print(best_path)
        print(minimum_loss_values )

        print("100% completed!")

        # pso = MultiObjectivePSO(int(self.ui.particle_num.value()),
        #                         2, (0,100), int(self.ui.iteration_num.value()),
        #                         self.terrain,
        #                         (int(self.ui.start_point_x.value()), int(self.ui.start_point_y.value())),
        #                         (int(self.ui.stop_point_x.value()), int(self.ui.stop_point_y.value())))
        # pso.update()
        # print(pso.gbest_positions)

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
        self.terrain = terrain_generator(noise_num=float(self.ui.noise_num.value()),
                                    terrain_size=(int(self.ui.terrain_x.value()), int(self.ui.terrain_y.value())),
                                    terrain_type=map_terrain_type(self.ui.map_type.currentText()))


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
            edgecolor="black",  # Czerwony kolor obwódki
            s=150,  # Większy rozmiar obwódki
        )

        # Rysowanie środka punktu stop (mniejszy punkt, wypełniony)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.stop_point_x.value())],
            [int(self.ui.stop_point_y.value())],
            color="black",  # Czerwony kolor wypełnienia
            edgecolor="none",  # Brak obwódki dla środka
            s=50,  # Mniejszy rozmiar punktu
        )

        # Dodanie adnotacji "Stop" obok punktu
        self.ui.map_plot.canvas.axes.text(
            int(self.ui.stop_point_x.value()) + 3,  # Przesunięcie tekstu w poziomie
            int(self.ui.stop_point_y.value()) + 3,  # Przesunięcie tekstu w pionie
            "Stop",  # Tekst adnotacji
            color="white",  # Kolor tekstu
            fontsize=12  # Rozmiar czcionki
        )

        # Rysowanie obwódki dla punktu start (większy punkt, tylko kolor obwódki)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.start_point_x.value())],
            [int(self.ui.start_point_y.value())],
            color="none",  # Brak wypełnienia punktu
            edgecolor="black",  # Niebieski kolor obwódki
            s=150,  # Większy rozmiar obwódki
        )

        # Rysowanie środka punktu start (mniejszy punkt, wypełniony)
        self.ui.map_plot.canvas.axes.scatter(
            [int(self.ui.start_point_x.value())],
            [int(self.ui.start_point_y.value())],
            color="black",  # Niebieski kolor wypełnienia
            edgecolor="none",  # Brak obwódki dla środka
            s=50,  # Mniejszy rozmiar punktu
        )

        # Dodanie adnotacji "Start" obok punktu
        self.ui.map_plot.canvas.axes.text(
            int(self.ui.start_point_x.value()) + 3,  # Przesunięcie tekstu w poziomie
            int(self.ui.start_point_y.value()) + 3,  # Przesunięcie tekstu w pionie
            "Start",  # Tekst adnotacji
            color="white",  # Kolor tekstu
            fontsize=12  # Rozmiar czcionki
        )

        # Dodanie opisu osi i tytułu
        self.ui.map_plot.canvas.axes.set_xlabel(f"X")
        self.ui.map_plot.canvas.axes.set_ylabel(f"Y")
        self.ui.map_plot.canvas.axes.set_title("Mapa")

        # Odświeżenie wykresu
        self.ui.map_plot.canvas.draw()

    def hide_graph(self):
        self.ui.map_plot.canvas.axes.clear()
        self.ui.map_plot.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
