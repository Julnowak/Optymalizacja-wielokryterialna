# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTableView, QTableWidget, QTableWidgetItem, QWidget)

from plotwidget import plotwidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(250, 16777215))
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.robodist_weight_num = QSpinBox(self.groupBox)
        self.robodist_weight_num.setObjectName(u"robodist_weight_num")
        self.robodist_weight_num.setValue(1)

        self.gridLayout_4.addWidget(self.robodist_weight_num, 4, 4, 1, 1)

        self.stop_point_y = QSpinBox(self.groupBox)
        self.stop_point_y.setObjectName(u"stop_point_y")
        self.stop_point_y.setMaximum(1000000000)
        self.stop_point_y.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_y, 11, 4, 1, 1)

        self.terrain_y = QSpinBox(self.groupBox)
        self.terrain_y.setObjectName(u"terrain_y")
        self.terrain_y.setMinimum(1)
        self.terrain_y.setMaximum(1000000000)
        self.terrain_y.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_y, 10, 4, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 4, 2, 1, 2)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 8, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 7, 2, 1, 3)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 0, 2, 1, 2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 1, 2, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 13, 2, 1, 3)

        self.robot_dist_num = QSpinBox(self.groupBox)
        self.robot_dist_num.setObjectName(u"robot_dist_num")
        self.robot_dist_num.setMinimum(1)
        self.robot_dist_num.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.robot_dist_num, 1, 4, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 3, 2, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 2, 2, 1, 2)

        self.map_type = QComboBox(self.groupBox)
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.addItem("")
        self.map_type.setObjectName(u"map_type")

        self.gridLayout_4.addWidget(self.map_type, 8, 3, 1, 2)

        self.terrain_x = QSpinBox(self.groupBox)
        self.terrain_x.setObjectName(u"terrain_x")
        self.terrain_x.setMinimum(1)
        self.terrain_x.setMaximum(1000000000)
        self.terrain_x.setSingleStep(1)
        self.terrain_x.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_x, 10, 3, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 9, 2, 1, 1)

        self.vehicle_num = QSpinBox(self.groupBox)
        self.vehicle_num.setObjectName(u"vehicle_num")
        self.vehicle_num.setMinimum(1)
        self.vehicle_num.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.vehicle_num, 0, 4, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 10, 2, 1, 1)

        self.stop_point_x = QSpinBox(self.groupBox)
        self.stop_point_x.setObjectName(u"stop_point_x")
        self.stop_point_x.setMaximum(1000000000)
        self.stop_point_x.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_x, 11, 3, 1, 1)

        self.generate_map_btn = QPushButton(self.groupBox)
        self.generate_map_btn.setObjectName(u"generate_map_btn")

        self.gridLayout_4.addWidget(self.generate_map_btn, 15, 2, 1, 3)

        self.iteration_num = QSpinBox(self.groupBox)
        self.iteration_num.setObjectName(u"iteration_num")
        self.iteration_num.setMinimum(1)
        self.iteration_num.setMaximum(1000000000)
        self.iteration_num.setValue(50)

        self.gridLayout_4.addWidget(self.iteration_num, 2, 4, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 14, 2, 1, 1)

        self.terrain_weight_num = QSpinBox(self.groupBox)
        self.terrain_weight_num.setObjectName(u"terrain_weight_num")
        self.terrain_weight_num.setValue(1)

        self.gridLayout_4.addWidget(self.terrain_weight_num, 3, 4, 1, 1)

        self.noise_num = QDoubleSpinBox(self.groupBox)
        self.noise_num.setObjectName(u"noise_num")
        self.noise_num.setMaximum(100.000000000000000)
        self.noise_num.setSingleStep(0.010000000000000)
        self.noise_num.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.noise_num, 9, 3, 1, 2)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 11, 2, 1, 1)

        self.start_btn = QPushButton(self.groupBox)
        self.start_btn.setObjectName(u"start_btn")

        self.gridLayout_4.addWidget(self.start_btn, 16, 2, 1, 3)

        self.algorithm_type = QComboBox(self.groupBox)
        self.algorithm_type.addItem("")
        self.algorithm_type.addItem("")
        self.algorithm_type.addItem("")
        self.algorithm_type.setObjectName(u"algorithm_type")

        self.gridLayout_4.addWidget(self.algorithm_type, 14, 3, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 2, 1)

        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.map_plot = plotwidget(self.groupBox_2)
        self.map_plot.setObjectName(u"map_plot")
        self.map_plot.setMinimumSize(QSize(300, 0))
        self.map_plot.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_3.addWidget(self.map_plot, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 2, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.beg_points_table = QTableWidget(self.tab_3)
        self.beg_points_table.setObjectName(u"beg_points_table")
        self.beg_points_table.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_8.addWidget(self.beg_points_table, 1, 0, 1, 2)

        self.openFile_btn = QPushButton(self.tab_3)
        self.openFile_btn.setObjectName(u"openFile_btn")

        self.gridLayout_8.addWidget(self.openFile_btn, 2, 1, 1, 1)

        self.file_path = QLineEdit(self.tab_3)
        self.file_path.setObjectName(u"file_path")

        self.gridLayout_8.addWidget(self.file_path, 2, 0, 1, 1)

        self.info_lab = QLabel(self.tab_3)
        self.info_lab.setObjectName(u"info_lab")
        self.info_lab.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.info_lab, 3, 0, 1, 2)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(500, 0))
        self.gridLayout_6 = QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.result_plot = plotwidget(self.groupBox_3)
        self.result_plot.setObjectName(u"result_plot")
        self.result_plot.setMinimumSize(QSize(300, 0))
        self.result_plot.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_6.addWidget(self.result_plot, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_7 = QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_7.addWidget(self.label_11, 1, 0, 1, 1)

        self.best_resul_val = QLineEdit(self.groupBox_4)
        self.best_resul_val.setObjectName(u"best_resul_val")
        self.best_resul_val.setMaximumSize(QSize(200, 16777215))
        self.best_resul_val.setReadOnly(True)

        self.gridLayout_7.addWidget(self.best_resul_val, 1, 1, 1, 1)

        self.animation_btn = QPushButton(self.groupBox_4)
        self.animation_btn.setObjectName(u"animation_btn")

        self.gridLayout_7.addWidget(self.animation_btn, 2, 0, 1, 2)

        self.result_table = QTableView(self.groupBox_4)
        self.result_table.setObjectName(u"result_table")

        self.gridLayout_7.addWidget(self.result_table, 0, 0, 1, 2)


        self.gridLayout_5.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_9 = QGridLayout(self.tab_6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.cost_plot = plotwidget(self.tab_6)
        self.cost_plot.setObjectName(u"cost_plot")
        self.cost_plot.setMinimumSize(QSize(300, 0))
        self.cost_plot.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_9.addWidget(self.cost_plot, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parametry", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Waga dystansu robot\u00f3w:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Typ mapy:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Liczba pojazd\u00f3w:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Odleg\u0142o\u015b\u0107 robot\u00f3w:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Waga terenu:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Iteracje:", None))
        self.map_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Wzg\u00f3rza", None))
        self.map_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Linie", None))
        self.map_type.setItemText(2, QCoreApplication.translate("MainWindow", u"Skos", None))
        self.map_type.setItemText(3, QCoreApplication.translate("MainWindow", u"Z\u0119by", None))
        self.map_type.setItemText(4, QCoreApplication.translate("MainWindow", u"Kanion", None))
        self.map_type.setItemText(5, QCoreApplication.translate("MainWindow", u"\u0141uk", None))
        self.map_type.setItemText(6, QCoreApplication.translate("MainWindow", u"Labirynt", None))
        self.map_type.setItemText(7, QCoreApplication.translate("MainWindow", u"Szum", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Szum:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rozmiar:", None))
        self.generate_map_btn.setText(QCoreApplication.translate("MainWindow", u"Generuj map\u0119", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Algorytm:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Punkt stop:", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.algorithm_type.setItemText(0, QCoreApplication.translate("MainWindow", u"A-STAR", None))
        self.algorithm_type.setItemText(1, QCoreApplication.translate("MainWindow", u"CSO", None))
        self.algorithm_type.setItemText(2, QCoreApplication.translate("MainWindow", u"TSP GA", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Mapa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Menu", None))
        self.openFile_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj z pliku", None))
        self.file_path.setText("")
        self.info_lab.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Punkty pocz\u0105tkowe", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Wykres wynikowy", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Tabela rezultat\u00f3w", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Najlepszy wynik: ", None))
        self.animation_btn.setText(QCoreApplication.translate("MainWindow", u"Wy\u015bwietl animacj\u0119", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Rezultaty", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Koszt", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Tabele", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Testowanie", None))
    # retranslateUi

