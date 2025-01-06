# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from algorytmy.Multi_PSO import MultiObjectivePSO
from ui_form import Ui_MainWindow
from algorytmy.terrain import terrain_generator


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.flag = True

        self.ui.map_plot.hide()
        self.ui.result_plot.hide()
        self.ui.generate_map_btn.clicked.connect(self.visualize_map)
        self.ui.start_btn.clicked.connect(self.start)

    def start(self):
        pso = MultiObjectivePSO(int(self.ui.particle_num.value()),
                                2, (0,100), int(self.ui.iteration_num.value()),
                                self.terrain,
                                (int(self.ui.start_point_x.value()), int(self.ui.start_point_y.value())),
                                (int(self.ui.stop_point_x.value()), int(self.ui.stop_point_y.value())))
        pso.update()
        print(pso.gbest_positions)

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
