from PySide6.QtWidgets import *

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure


class plotwidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
