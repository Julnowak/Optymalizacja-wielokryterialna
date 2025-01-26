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
    QMainWindow, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

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

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(300, 16777215))
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.terrain_x = QSpinBox(self.groupBox)
        self.terrain_x.setObjectName(u"terrain_x")
        self.terrain_x.setMinimum(1)
        self.terrain_x.setMaximum(1000000000)
        self.terrain_x.setSingleStep(1)
        self.terrain_x.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_x, 7, 4, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 7, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 11, 2, 1, 1)

        self.stop_point_x = QSpinBox(self.groupBox)
        self.stop_point_x.setObjectName(u"stop_point_x")
        self.stop_point_x.setMaximum(1000000000)
        self.stop_point_x.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_x, 10, 4, 1, 1)

        self.terrain_y = QSpinBox(self.groupBox)
        self.terrain_y.setObjectName(u"terrain_y")
        self.terrain_y.setMinimum(1)
        self.terrain_y.setMaximum(1000000000)
        self.terrain_y.setValue(100)

        self.gridLayout_4.addWidget(self.terrain_y, 7, 5, 1, 1)

        self.stackedWidget = QStackedWidget(self.groupBox)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 180))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_16 = QGridLayout(self.page)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.groupBox_8 = QGroupBox(self.page)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_15 = QGridLayout(self.groupBox_8)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_4 = QLabel(self.groupBox_8)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_15.addWidget(self.label_4, 0, 0, 1, 1)

        self.robot_dist_num = QSpinBox(self.groupBox_8)
        self.robot_dist_num.setObjectName(u"robot_dist_num")
        self.robot_dist_num.setMaximumSize(QSize(50, 16777215))
        self.robot_dist_num.setMinimum(1)
        self.robot_dist_num.setMaximum(1000000000)
        self.robot_dist_num.setValue(2)

        self.gridLayout_15.addWidget(self.robot_dist_num, 0, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_8)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_15.addWidget(self.label_8, 1, 0, 1, 1)

        self.terrain_weight_num = QSpinBox(self.groupBox_8)
        self.terrain_weight_num.setObjectName(u"terrain_weight_num")
        self.terrain_weight_num.setValue(1)

        self.gridLayout_15.addWidget(self.terrain_weight_num, 1, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_8)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_15.addWidget(self.label_10, 2, 0, 1, 1)

        self.robodist_weight_num = QSpinBox(self.groupBox_8)
        self.robodist_weight_num.setObjectName(u"robodist_weight_num")
        self.robodist_weight_num.setValue(1)

        self.gridLayout_15.addWidget(self.robodist_weight_num, 2, 1, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_14 = QGridLayout(self.page_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.groupBox_9 = QGroupBox(self.page_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_17 = QGridLayout(self.groupBox_9)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.label = QLabel(self.groupBox_9)
        self.label.setObjectName(u"label")

        self.gridLayout_17.addWidget(self.label, 2, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_9)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_17.addWidget(self.label_2, 0, 0, 1, 1)

        self.vehicle_num = QSpinBox(self.groupBox_9)
        self.vehicle_num.setObjectName(u"vehicle_num")
        self.vehicle_num.setMinimum(1)
        self.vehicle_num.setMaximum(1000000000)
        self.vehicle_num.setValue(20)

        self.gridLayout_17.addWidget(self.vehicle_num, 0, 1, 1, 1)

        self.iteration_num = QSpinBox(self.groupBox_9)
        self.iteration_num.setObjectName(u"iteration_num")
        self.iteration_num.setMinimum(1)
        self.iteration_num.setMaximum(1000000000)
        self.iteration_num.setValue(50)

        self.gridLayout_17.addWidget(self.iteration_num, 2, 1, 1, 1)

        self.spinBox = QSpinBox(self.groupBox_9)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setValue(10)

        self.gridLayout_17.addWidget(self.spinBox, 1, 1, 1, 1)

        self.label_18 = QLabel(self.groupBox_9)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_17.addWidget(self.label_18, 1, 0, 1, 1)


        self.gridLayout_14.addWidget(self.groupBox_9, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_18 = QGridLayout(self.page_3)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.groupBox_10 = QGroupBox(self.page_3)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_19 = QGridLayout(self.groupBox_10)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.offspring_percent_num = QDoubleSpinBox(self.groupBox_10)
        self.offspring_percent_num.setObjectName(u"offspring_percent_num")
        self.offspring_percent_num.setMaximum(1.000000000000000)
        self.offspring_percent_num.setSingleStep(0.010000000000000)
        self.offspring_percent_num.setValue(0.500000000000000)

        self.gridLayout_19.addWidget(self.offspring_percent_num, 2, 1, 1, 1)

        self.label_17 = QLabel(self.groupBox_10)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_19.addWidget(self.label_17, 3, 0, 1, 1)

        self.mutation_percent_num = QDoubleSpinBox(self.groupBox_10)
        self.mutation_percent_num.setObjectName(u"mutation_percent_num")
        self.mutation_percent_num.setMaximum(1.000000000000000)
        self.mutation_percent_num.setValue(0.200000000000000)

        self.gridLayout_19.addWidget(self.mutation_percent_num, 3, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_10)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(110, 0))

        self.gridLayout_19.addWidget(self.label_14, 0, 0, 1, 1)

        self.generation_num = QSpinBox(self.groupBox_10)
        self.generation_num.setObjectName(u"generation_num")
        self.generation_num.setMinimum(1)
        self.generation_num.setMaximum(1000000000)
        self.generation_num.setValue(50)

        self.gridLayout_19.addWidget(self.generation_num, 1, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_10)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_19.addWidget(self.label_16, 2, 0, 1, 1)

        self.generation_size_num = QSpinBox(self.groupBox_10)
        self.generation_size_num.setObjectName(u"generation_size_num")
        self.generation_size_num.setMinimum(1)
        self.generation_size_num.setMaximum(1000000000)
        self.generation_size_num.setValue(1000)

        self.gridLayout_19.addWidget(self.generation_size_num, 0, 1, 1, 1)

        self.label_15 = QLabel(self.groupBox_10)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_19.addWidget(self.label_15, 1, 0, 1, 1)

        self.label_19 = QLabel(self.groupBox_10)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_19.addWidget(self.label_19, 4, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox_10)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_19.addWidget(self.label_20, 5, 0, 1, 1)

        self.ranking_num = QSpinBox(self.groupBox_10)
        self.ranking_num.setObjectName(u"ranking_num")
        self.ranking_num.setMinimum(1)
        self.ranking_num.setMaximum(1000000000)
        self.ranking_num.setValue(5)

        self.gridLayout_19.addWidget(self.ranking_num, 4, 1, 1, 1)

        self.elite_num = QSpinBox(self.groupBox_10)
        self.elite_num.setObjectName(u"elite_num")
        self.elite_num.setMinimum(1)
        self.elite_num.setValue(5)

        self.gridLayout_19.addWidget(self.elite_num, 5, 1, 1, 1)


        self.gridLayout_18.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_3)

        self.gridLayout_4.addWidget(self.stackedWidget, 1, 2, 2, 4)

        self.image_radio = QRadioButton(self.groupBox)
        self.image_radio.setObjectName(u"image_radio")
        self.image_radio.setMinimumSize(QSize(100, 0))
        self.image_radio.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_4.addWidget(self.image_radio, 4, 4, 1, 2)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 5, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 6, 2, 1, 1)

        self.generate_map_btn = QPushButton(self.groupBox)
        self.generate_map_btn.setObjectName(u"generate_map_btn")

        self.gridLayout_4.addWidget(self.generate_map_btn, 12, 2, 1, 4)

        self.stop_point_y = QSpinBox(self.groupBox)
        self.stop_point_y.setObjectName(u"stop_point_y")
        self.stop_point_y.setMaximum(1000000000)
        self.stop_point_y.setValue(50)

        self.gridLayout_4.addWidget(self.stop_point_y, 10, 5, 1, 1)

        self.algorithm_type = QComboBox(self.groupBox)
        self.algorithm_type.addItem("")
        self.algorithm_type.addItem("")
        self.algorithm_type.addItem("")
        self.algorithm_type.setObjectName(u"algorithm_type")

        self.gridLayout_4.addWidget(self.algorithm_type, 11, 4, 1, 2)

        self.generator_radio = QRadioButton(self.groupBox)
        self.generator_radio.setObjectName(u"generator_radio")
        self.generator_radio.setMinimumSize(QSize(100, 0))
        self.generator_radio.setChecked(True)

        self.gridLayout_4.addWidget(self.generator_radio, 4, 2, 1, 2)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 10, 2, 1, 1)

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

        self.gridLayout_4.addWidget(self.map_type, 5, 4, 1, 2)

        self.start_btn = QPushButton(self.groupBox)
        self.start_btn.setObjectName(u"start_btn")

        self.gridLayout_4.addWidget(self.start_btn, 13, 2, 1, 4)

        self.noise_num = QDoubleSpinBox(self.groupBox)
        self.noise_num.setObjectName(u"noise_num")
        self.noise_num.setMaximum(100.000000000000000)
        self.noise_num.setSingleStep(0.010000000000000)
        self.noise_num.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.noise_num, 6, 4, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 2, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.image_path = QLineEdit(self.tab_3)
        self.image_path.setObjectName(u"image_path")
        self.image_path.setReadOnly(True)

        self.gridLayout_8.addWidget(self.image_path, 2, 0, 1, 1)

        self.beg_points_table = QTableWidget(self.tab_3)
        self.beg_points_table.setObjectName(u"beg_points_table")
        self.beg_points_table.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_8.addWidget(self.beg_points_table, 1, 0, 1, 5)

        self.openFile_btn = QPushButton(self.tab_3)
        self.openFile_btn.setObjectName(u"openFile_btn")

        self.gridLayout_8.addWidget(self.openFile_btn, 2, 4, 1, 1)

        self.info_lab = QLabel(self.tab_3)
        self.info_lab.setObjectName(u"info_lab")
        self.info_lab.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.info_lab, 4, 3, 1, 2)

        self.read_image_btn = QPushButton(self.tab_3)
        self.read_image_btn.setObjectName(u"read_image_btn")

        self.gridLayout_8.addWidget(self.read_image_btn, 2, 1, 1, 1)

        self.file_path = QLineEdit(self.tab_3)
        self.file_path.setObjectName(u"file_path")
        self.file_path.setReadOnly(True)

        self.gridLayout_8.addWidget(self.file_path, 2, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer, 2, 2, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.gridLayout_6 = QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.result_plot = plotwidget(self.groupBox_3)
        self.result_plot.setObjectName(u"result_plot")
        self.result_plot.setMinimumSize(QSize(0, 0))
        self.result_plot.setMaximumSize(QSize(16777215, 500))

        self.gridLayout_6.addWidget(self.result_plot, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(400, 0))
        self.groupBox_4.setMaximumSize(QSize(400, 16777215))
        self.gridLayout_7 = QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.animation_btn = QPushButton(self.groupBox_4)
        self.animation_btn.setObjectName(u"animation_btn")

        self.gridLayout_7.addWidget(self.animation_btn, 1, 0, 1, 2)

        self.result_table = QTableWidget(self.groupBox_4)
        self.result_table.setObjectName(u"result_table")

        self.gridLayout_7.addWidget(self.result_table, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.gridLayout_9 = QGridLayout(self.tab_6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox_6 = QGroupBox(self.tab_6)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_11 = QGridLayout(self.groupBox_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.cost_plot = plotwidget(self.groupBox_6)
        self.cost_plot.setObjectName(u"cost_plot")
        self.cost_plot.setMinimumSize(QSize(300, 0))
        self.cost_plot.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout_11.addWidget(self.cost_plot, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_6)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(200, 16777215))
        self.gridLayout_10 = QGridLayout(self.groupBox_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_10.addWidget(self.label_11, 4, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_10.addWidget(self.label_12, 2, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_10.addWidget(self.label_13, 0, 0, 1, 1)

        self.ASTAR_time_line = QLineEdit(self.groupBox_5)
        self.ASTAR_time_line.setObjectName(u"ASTAR_time_line")
        self.ASTAR_time_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.ASTAR_time_line, 0, 1, 1, 1)

        self.CSO_time_line = QLineEdit(self.groupBox_5)
        self.CSO_time_line.setObjectName(u"CSO_time_line")
        self.CSO_time_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.CSO_time_line, 2, 1, 1, 1)

        self.TSPGA_time_line = QLineEdit(self.groupBox_5)
        self.TSPGA_time_line.setObjectName(u"TSPGA_time_line")
        self.TSPGA_time_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.TSPGA_time_line, 4, 1, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_5, 0, 1, 1, 1)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_12 = QGridLayout(self.tab_4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_13 = QGridLayout(self.groupBox_7)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.cost_table = QTableWidget(self.groupBox_7)
        self.cost_table.setObjectName(u"cost_table")

        self.gridLayout_13.addWidget(self.cost_table, 0, 0, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")

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
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Mapa", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parametry", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Rozmiar:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Algorytm:", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Algorytm A-STAR", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Odleg\u0142o\u015b\u0107 robot\u00f3w:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Waga terenu:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Waga dystansu robot\u00f3w:", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Algorytm CSO", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Iteracje:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Liczba karaluch\u00f3w:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Widzialno\u015b\u0107:", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Algorytm TSP GA", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Mutacja [%]:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Rozmiar populacji:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Potomstwo [%]:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Liczba generacji:", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Rankignowe:", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Elity:", None))
        self.image_radio.setText(QCoreApplication.translate("MainWindow", u"Z obrazu", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Typ mapy:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Szum:", None))
        self.generate_map_btn.setText(QCoreApplication.translate("MainWindow", u"Generuj map\u0119", None))
        self.algorithm_type.setItemText(0, QCoreApplication.translate("MainWindow", u"A-STAR", None))
        self.algorithm_type.setItemText(1, QCoreApplication.translate("MainWindow", u"CSO", None))
        self.algorithm_type.setItemText(2, QCoreApplication.translate("MainWindow", u"TSP GA", None))

        self.generator_radio.setText(QCoreApplication.translate("MainWindow", u"Z generatora", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Punkt stop:", None))
        self.map_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Wzg\u00f3rza", None))
        self.map_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Linie", None))
        self.map_type.setItemText(2, QCoreApplication.translate("MainWindow", u"Skos", None))
        self.map_type.setItemText(3, QCoreApplication.translate("MainWindow", u"Z\u0119by", None))
        self.map_type.setItemText(4, QCoreApplication.translate("MainWindow", u"Kanion", None))
        self.map_type.setItemText(5, QCoreApplication.translate("MainWindow", u"\u0141uk", None))
        self.map_type.setItemText(6, QCoreApplication.translate("MainWindow", u"Labirynt", None))
        self.map_type.setItemText(7, QCoreApplication.translate("MainWindow", u"Szum", None))

        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Menu", None))
        self.openFile_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj z pliku", None))
        self.info_lab.setText("")
        self.read_image_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj obraz", None))
        self.file_path.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Punkty pocz\u0105tkowe", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Wykres wynikowy", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Tabela rezultat\u00f3w", None))
        self.animation_btn.setText(QCoreApplication.translate("MainWindow", u"Wy\u015bwietl animacj\u0119", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Rezultaty", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Wykres kosztu", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Czasy wykonania", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"TSP GA:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"CSO:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"A-STAR:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Statystyki", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Tabela", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Tabela koszt\u00f3w", None))
    # retranslateUi

