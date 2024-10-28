# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QWidget)

from plotwidget import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.box = QTabWidget(self.centralwidget)
        self.box.setObjectName(u"box")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_4 = QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame = QFrame(self.tab_3)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.groupBox_4 = QGroupBox(self.frame)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 200))
        self.groupBox_4.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.groupBox_4.setAcceptDrops(False)
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setCheckable(False)
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_5.addWidget(self.label_3, 1, 0, 1, 1)

        self.mean_num = QSpinBox(self.groupBox_4)
        self.mean_num.setObjectName(u"mean_num")
        self.mean_num.setMinimum(-99)

        self.gridLayout_5.addWidget(self.mean_num, 2, 0, 1, 1)

        self.odch_num = QSpinBox(self.groupBox_4)
        self.odch_num.setObjectName(u"odch_num")
        self.odch_num.setMinimum(-99)

        self.gridLayout_5.addWidget(self.odch_num, 2, 1, 1, 2)

        self.point_num = QSpinBox(self.groupBox_4)
        self.point_num.setObjectName(u"point_num")
        self.point_num.setMinimum(1)
        self.point_num.setMaximum(999999999)

        self.gridLayout_5.addWidget(self.point_num, 2, 3, 1, 1)

        self.generation_btn = QPushButton(self.groupBox_4)
        self.generation_btn.setObjectName(u"generation_btn")

        self.gridLayout_5.addWidget(self.generation_btn, 3, 0, 1, 1)

        self.sort_btn = QPushButton(self.groupBox_4)
        self.sort_btn.setObjectName(u"sort_btn")

        self.gridLayout_5.addWidget(self.sort_btn, 3, 1, 1, 1)

        self.criterium_num = QSpinBox(self.groupBox_4)
        self.criterium_num.setObjectName(u"criterium_num")
        self.criterium_num.setMinimum(1)

        self.gridLayout_5.addWidget(self.criterium_num, 3, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_5.addWidget(self.label_4, 1, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_5.addWidget(self.label_5, 3, 2, 1, 1)

        self.distribution_select = QComboBox(self.groupBox_4)
        self.distribution_select.addItem("")
        self.distribution_select.addItem("")
        self.distribution_select.addItem("")
        self.distribution_select.addItem("")
        self.distribution_select.setObjectName(u"distribution_select")

        self.gridLayout_5.addWidget(self.distribution_select, 0, 1, 1, 2)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_5.addWidget(self.label_6, 1, 1, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox_4, 1, 0, 2, 1)

        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.addCrit_btn = QPushButton(self.groupBox)
        self.addCrit_btn.setObjectName(u"addCrit_btn")

        self.gridLayout_6.addWidget(self.addCrit_btn, 1, 0, 1, 1)

        self.deleteCrit_btn = QPushButton(self.groupBox)
        self.deleteCrit_btn.setObjectName(u"deleteCrit_btn")

        self.gridLayout_6.addWidget(self.deleteCrit_btn, 1, 1, 1, 1)

        self.criteriaTable = QTableWidget(self.groupBox)
        if (self.criteriaTable.columnCount() < 2):
            self.criteriaTable.setColumnCount(2)
        if (self.criteriaTable.rowCount() < 1):
            self.criteriaTable.setRowCount(1)
        self.criteriaTable.setObjectName(u"criteriaTable")
        self.criteriaTable.setAutoScrollMargin(16)
        self.criteriaTable.setRowCount(1)
        self.criteriaTable.setColumnCount(2)
        self.criteriaTable.horizontalHeader().setCascadingSectionResizes(False)
        self.criteriaTable.horizontalHeader().setProperty("showSortIndicator", False)
        self.criteriaTable.horizontalHeader().setStretchLastSection(True)
        self.criteriaTable.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_6.addWidget(self.criteriaTable, 0, 0, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(16777215, 140))
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.animation_btn = QPushButton(self.groupBox_3)
        self.animation_btn.setObjectName(u"animation_btn")

        self.gridLayout_3.addWidget(self.animation_btn, 2, 0, 1, 2)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.start_btn = QPushButton(self.groupBox_3)
        self.start_btn.setObjectName(u"start_btn")

        self.gridLayout_3.addWidget(self.start_btn, 2, 4, 1, 2)

        self.stop_btn = QPushButton(self.groupBox_3)
        self.stop_btn.setObjectName(u"stop_btn")

        self.gridLayout_3.addWidget(self.stop_btn, 2, 2, 1, 1)

        self.benchmark_btn = QPushButton(self.groupBox_3)
        self.benchmark_btn.setObjectName(u"benchmark_btn")

        self.gridLayout_3.addWidget(self.benchmark_btn, 2, 3, 1, 1)

        self.algorithm_select = QComboBox(self.groupBox_3)
        self.algorithm_select.addItem("")
        self.algorithm_select.addItem("")
        self.algorithm_select.addItem("")
        self.algorithm_select.setObjectName(u"algorithm_select")

        self.gridLayout_3.addWidget(self.algorithm_select, 0, 1, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox_3, 2, 1, 1, 2)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.addVal_btn = QPushButton(self.groupBox_2)
        self.addVal_btn.setObjectName(u"addVal_btn")

        self.gridLayout_7.addWidget(self.addVal_btn, 1, 0, 1, 1)

        self.load_btn = QPushButton(self.groupBox_2)
        self.load_btn.setObjectName(u"load_btn")

        self.gridLayout_7.addWidget(self.load_btn, 1, 1, 1, 1)

        self.deleteVal_btn = QPushButton(self.groupBox_2)
        self.deleteVal_btn.setObjectName(u"deleteVal_btn")

        self.gridLayout_7.addWidget(self.deleteVal_btn, 1, 2, 1, 1)

        self.save_btn = QPushButton(self.groupBox_2)
        self.save_btn.setObjectName(u"save_btn")

        self.gridLayout_7.addWidget(self.save_btn, 1, 3, 1, 1)

        self.valuesTable = QTableWidget(self.groupBox_2)
        self.valuesTable.setObjectName(u"valuesTable")

        self.gridLayout_7.addWidget(self.valuesTable, 0, 0, 1, 4)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 2, 2)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.box.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_8 = QGridLayout(self.tab_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.graph = PlotWidget(self.tab_4)
        self.graph.setObjectName(u"graph")

        self.gridLayout_8.addWidget(self.graph, 0, 0, 1, 1)

        self.box.addTab(self.tab_4, "")

        self.gridLayout.addWidget(self.box, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.box.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Generacja", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Rozk\u0142ad:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u015arednia:", None))
        self.generation_btn.setText(QCoreApplication.translate("MainWindow", u"Generuj", None))
        self.sort_btn.setText(QCoreApplication.translate("MainWindow", u"Sortuj", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Liczba obiekt\u00f3w:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Kryterium:", None))
        self.distribution_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Eksponencjalny", None))
        self.distribution_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Jednostajny", None))
        self.distribution_select.setItemText(2, QCoreApplication.translate("MainWindow", u"Gaussa", None))
        self.distribution_select.setItemText(3, QCoreApplication.translate("MainWindow", u"Poissona", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Odchylenie:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Edytor kryteri\u00f3w", None))
        self.addCrit_btn.setText(QCoreApplication.translate("MainWindow", u"Dodaj", None))
        self.deleteCrit_btn.setText(QCoreApplication.translate("MainWindow", u"Usu\u0144", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Akcje", None))
        self.animation_btn.setText(QCoreApplication.translate("MainWindow", u"Renderuj animacj\u0119", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Algorytm:", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Rozwi\u0105\u017c", None))
        self.stop_btn.setText(QCoreApplication.translate("MainWindow", u"Przerwij", None))
        self.benchmark_btn.setText(QCoreApplication.translate("MainWindow", u"Benchmark", None))
        self.algorithm_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Naiwny bez filtracji", None))
        self.algorithm_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Naiwny z filtracj\u0105", None))
        self.algorithm_select.setItemText(2, QCoreApplication.translate("MainWindow", u"Oparty o punkt idealny", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Edytor warto\u015bci", None))
        self.addVal_btn.setText(QCoreApplication.translate("MainWindow", u"Dodaj", None))
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj z pliku", None))
        self.deleteVal_btn.setText(QCoreApplication.translate("MainWindow", u"Usu\u0144", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Zapisz", None))
        self.box.setTabText(self.box.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Panel", None))
        self.box.setTabText(self.box.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Wyniki", None))
    # retranslateUi

