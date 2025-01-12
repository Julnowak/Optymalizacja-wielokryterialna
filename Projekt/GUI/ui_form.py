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
    QGroupBox, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QWidget)

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
        self.terrain_x = QSpinBox(self.groupBox)
        self.terrain_x.setObjectName(u"terrain_x")
        self.terrain_x.setMinimum(1)
        self.terrain_x.setMaximum(1000000000)
        self.terrain_x.setSingleStep(1)
        self.terrain_x.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_x, 8, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 9, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 8, 0, 1, 1)

        self.vehicle_num = QSpinBox(self.groupBox)
        self.vehicle_num.setObjectName(u"vehicle_num")
        self.vehicle_num.setMinimum(1)
        self.vehicle_num.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.vehicle_num, 0, 2, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 10, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 12, 0, 1, 3)

        self.particle_num = QSpinBox(self.groupBox)
        self.particle_num.setObjectName(u"particle_num")
        self.particle_num.setMinimum(1)
        self.particle_num.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.particle_num, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 5, 0, 1, 3)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 2)

        self.terrain_y = QSpinBox(self.groupBox)
        self.terrain_y.setObjectName(u"terrain_y")
        self.terrain_y.setMinimum(1)
        self.terrain_y.setMaximum(1000000000)
        self.terrain_y.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_y, 8, 2, 1, 1)

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

        self.gridLayout_4.addWidget(self.map_type, 6, 1, 1, 2)

        self.start_point_y = QSpinBox(self.groupBox)
        self.start_point_y.setObjectName(u"start_point_y")
        self.start_point_y.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.start_point_y, 9, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 2, 0, 1, 2)

        self.stop_point_y = QSpinBox(self.groupBox)
        self.stop_point_y.setObjectName(u"stop_point_y")
        self.stop_point_y.setMaximum(1000000000)
        self.stop_point_y.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_y, 10, 2, 1, 1)

        self.metric_type = QComboBox(self.groupBox)
        self.metric_type.addItem("")
        self.metric_type.addItem("")
        self.metric_type.setObjectName(u"metric_type")

        self.gridLayout_4.addWidget(self.metric_type, 3, 1, 1, 2)

        self.noise_num = QDoubleSpinBox(self.groupBox)
        self.noise_num.setObjectName(u"noise_num")
        self.noise_num.setMaximum(100.000000000000000)
        self.noise_num.setSingleStep(0.010000000000000)
        self.noise_num.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.noise_num, 7, 1, 1, 2)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 3, 0, 1, 1)

        self.stop_point_x = QSpinBox(self.groupBox)
        self.stop_point_x.setObjectName(u"stop_point_x")
        self.stop_point_x.setMaximum(1000000000)
        self.stop_point_x.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_x, 10, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 7, 0, 1, 1)

        self.start_btn = QPushButton(self.groupBox)
        self.start_btn.setObjectName(u"start_btn")

        self.gridLayout_4.addWidget(self.start_btn, 14, 0, 1, 3)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 6, 0, 1, 1)

        self.start_point_x = QSpinBox(self.groupBox)
        self.start_point_x.setObjectName(u"start_point_x")
        self.start_point_x.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.start_point_x, 9, 1, 1, 1)

        self.iteration_num = QSpinBox(self.groupBox)
        self.iteration_num.setObjectName(u"iteration_num")
        self.iteration_num.setMinimum(1)
        self.iteration_num.setMaximum(1000000000)
        self.iteration_num.setValue(50)

        self.gridLayout_4.addWidget(self.iteration_num, 2, 2, 1, 1)

        self.generate_map_btn = QPushButton(self.groupBox)
        self.generate_map_btn.setObjectName(u"generate_map_btn")

        self.gridLayout_4.addWidget(self.generate_map_btn, 13, 0, 1, 3)


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
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
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

        self.gridLayout_5.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

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

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parametry", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Punkt start:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rozmiar:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Punkt stop:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Liczba pojazd\u00f3w:", None))
        self.map_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Wzg\u00f3rza", None))
        self.map_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Linie", None))
        self.map_type.setItemText(2, QCoreApplication.translate("MainWindow", u"Skos", None))
        self.map_type.setItemText(3, QCoreApplication.translate("MainWindow", u"Z\u0119by", None))
        self.map_type.setItemText(4, QCoreApplication.translate("MainWindow", u"Kanion", None))
        self.map_type.setItemText(5, QCoreApplication.translate("MainWindow", u"\u0141uk", None))
        self.map_type.setItemText(6, QCoreApplication.translate("MainWindow", u"Labirynt", None))
        self.map_type.setItemText(7, QCoreApplication.translate("MainWindow", u"Szum", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Liczba cz\u0105stek:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Iteracje", None))
        self.metric_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Euklidesowa", None))
        self.metric_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Czebyszewa", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Metryka:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Szum:", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Typ mapy:", None))
        self.generate_map_btn.setText(QCoreApplication.translate("MainWindow", u"Generuj map\u0119", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Mapa", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Menu", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Wykres wynikowy", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Tabela rezultat\u00f3w", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Rezultaty", None))
    # retranslateUi

