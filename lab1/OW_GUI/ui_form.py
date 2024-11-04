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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
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
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.load_btn = QPushButton(self.groupBox_2)
        self.load_btn.setObjectName(u"load_btn")

        self.gridLayout_7.addWidget(self.load_btn, 1, 1, 1, 1)

        self.save_btn = QPushButton(self.groupBox_2)
        self.save_btn.setObjectName(u"save_btn")

        self.gridLayout_7.addWidget(self.save_btn, 1, 3, 1, 1)

        self.addVal_btn = QPushButton(self.groupBox_2)
        self.addVal_btn.setObjectName(u"addVal_btn")

        self.gridLayout_7.addWidget(self.addVal_btn, 1, 0, 1, 1)

        self.deleteVal_btn = QPushButton(self.groupBox_2)
        self.deleteVal_btn.setObjectName(u"deleteVal_btn")

        self.gridLayout_7.addWidget(self.deleteVal_btn, 1, 2, 1, 1)

        self.info_lab = QLabel(self.groupBox_2)
        self.info_lab.setObjectName(u"info_lab")

        self.gridLayout_7.addWidget(self.info_lab, 1, 4, 1, 1)

        self.valuesTable = QTableWidget(self.groupBox_2)
        self.valuesTable.setObjectName(u"valuesTable")

        self.gridLayout_7.addWidget(self.valuesTable, 0, 0, 1, 5)


        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 2, 2)

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

        self.lab1 = QLabel(self.groupBox_4)
        self.lab1.setObjectName(u"lab1")
        self.lab1.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_5.addWidget(self.lab1, 1, 0, 1, 1)

        self.point_num = QSpinBox(self.groupBox_4)
        self.point_num.setObjectName(u"point_num")
        self.point_num.setMinimum(1)
        self.point_num.setMaximum(999999999)
        self.point_num.setValue(10)

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

        self.lab2 = QLabel(self.groupBox_4)
        self.lab2.setObjectName(u"lab2")

        self.gridLayout_5.addWidget(self.lab2, 1, 1, 1, 2)

        self.odch_num = QDoubleSpinBox(self.groupBox_4)
        self.odch_num.setObjectName(u"odch_num")
        self.odch_num.setSingleStep(0.010000000000000)

        self.gridLayout_5.addWidget(self.odch_num, 2, 1, 1, 2)

        self.mean_num = QDoubleSpinBox(self.groupBox_4)
        self.mean_num.setObjectName(u"mean_num")
        self.mean_num.setMinimum(-99999999999999997168788049560464200849936328366177157906432.000000000000000)
        self.mean_num.setMaximum(999999999999999993220948674361627976461708441944064.000000000000000)
        self.mean_num.setSingleStep(0.010000000000000)

        self.gridLayout_5.addWidget(self.mean_num, 2, 0, 1, 1)


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
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)

        self.benchmark_btn = QPushButton(self.groupBox_3)
        self.benchmark_btn.setObjectName(u"benchmark_btn")

        self.gridLayout_3.addWidget(self.benchmark_btn, 2, 4, 1, 1)

        self.algorithm_select = QComboBox(self.groupBox_3)
        self.algorithm_select.addItem("")
        self.algorithm_select.addItem("")
        self.algorithm_select.addItem("")
        self.algorithm_select.setObjectName(u"algorithm_select")

        self.gridLayout_3.addWidget(self.algorithm_select, 0, 1, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 2, 0, 1, 4)

        self.start_btn = QPushButton(self.groupBox_3)
        self.start_btn.setObjectName(u"start_btn")

        self.gridLayout_3.addWidget(self.start_btn, 2, 5, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox_3, 2, 1, 1, 2)


        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)

        self.box.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_8 = QGridLayout(self.tab_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.graph = PlotWidget(self.tab_4)
        self.graph.setObjectName(u"graph")

        self.gridLayout_8.addWidget(self.graph, 0, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(150, 16777215))
        self.gridLayout_10 = QGridLayout(self.groupBox_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_10.addWidget(self.label_6, 2, 3, 1, 1)

        self.label_7 = QLabel(self.groupBox_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.gridLayout_10.addWidget(self.label_7, 4, 3, 1, 1)

        self.czas_line = QLineEdit(self.groupBox_5)
        self.czas_line.setObjectName(u"czas_line")
        self.czas_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.czas_line, 3, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_5)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_10.addWidget(self.label_8, 8, 3, 1, 1)

        self.plot_line = QLineEdit(self.groupBox_5)
        self.plot_line.setObjectName(u"plot_line")
        self.plot_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.plot_line, 9, 3, 1, 1)

        self.por_line = QLineEdit(self.groupBox_5)
        self.por_line.setObjectName(u"por_line")
        self.por_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.por_line, 1, 3, 1, 1)

        self.nzd_line = QLineEdit(self.groupBox_5)
        self.nzd_line.setObjectName(u"nzd_line")
        self.nzd_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.nzd_line, 5, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_10.addWidget(self.label_3, 0, 3, 1, 1)

        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_10.addWidget(self.label_9, 6, 3, 1, 1)

        self.wym_line = QLineEdit(self.groupBox_5)
        self.wym_line.setObjectName(u"wym_line")
        self.wym_line.setReadOnly(True)

        self.gridLayout_10.addWidget(self.wym_line, 7, 3, 1, 1)


        self.gridLayout_8.addWidget(self.groupBox_5, 0, 1, 1, 1)

        self.box.addTab(self.tab_4, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_9 = QGridLayout(self.tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.benchmark_table = QTableWidget(self.tab)
        if (self.benchmark_table.columnCount() < 2):
            self.benchmark_table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.benchmark_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.benchmark_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.benchmark_table.rowCount() < 3):
            self.benchmark_table.setRowCount(3)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.benchmark_table.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.benchmark_table.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.benchmark_table.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(0, 0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(1, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(1, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(2, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.benchmark_table.setItem(2, 1, __qtablewidgetitem10)
        self.benchmark_table.setObjectName(u"benchmark_table")
        self.benchmark_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.benchmark_table.setAlternatingRowColors(True)
        self.benchmark_table.horizontalHeader().setCascadingSectionResizes(False)
        self.benchmark_table.horizontalHeader().setMinimumSectionSize(100)
        self.benchmark_table.horizontalHeader().setDefaultSectionSize(500)
        self.benchmark_table.horizontalHeader().setProperty("showSortIndicator", False)
        self.benchmark_table.horizontalHeader().setStretchLastSection(True)
        self.benchmark_table.verticalHeader().setMinimumSectionSize(100)
        self.benchmark_table.verticalHeader().setDefaultSectionSize(150)
        self.benchmark_table.verticalHeader().setProperty("showSortIndicator", True)
        self.benchmark_table.verticalHeader().setStretchLastSection(True)

        self.gridLayout_9.addWidget(self.benchmark_table, 0, 0, 1, 1)

        self.box.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_11 = QGridLayout(self.tab_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.regresja = PlotWidget(self.tab_2)
        self.regresja.setObjectName(u"regresja")

        self.gridLayout_11.addWidget(self.regresja, 0, 0, 1, 1)

        self.regresja_2 = PlotWidget(self.tab_2)
        self.regresja_2.setObjectName(u"regresja_2")

        self.gridLayout_11.addWidget(self.regresja_2, 0, 1, 1, 1)

        self.box.addTab(self.tab_2, "")

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
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Edytor warto\u015bci", None))
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj z pliku", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Zapisz", None))
        self.addVal_btn.setText(QCoreApplication.translate("MainWindow", u"Dodaj", None))
        self.deleteVal_btn.setText(QCoreApplication.translate("MainWindow", u"Usu\u0144", None))
        self.info_lab.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Generacja", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Rozk\u0142ad:", None))
        self.lab1.setText(QCoreApplication.translate("MainWindow", u"\u015arednia:", None))
        self.generation_btn.setText(QCoreApplication.translate("MainWindow", u"Generuj", None))
        self.sort_btn.setText(QCoreApplication.translate("MainWindow", u"Sortuj", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Liczba obiekt\u00f3w:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Kryterium:", None))
        self.distribution_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Eksponencjalny", None))
        self.distribution_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Jednostajny", None))
        self.distribution_select.setItemText(2, QCoreApplication.translate("MainWindow", u"Gaussa", None))
        self.distribution_select.setItemText(3, QCoreApplication.translate("MainWindow", u"Poissona", None))

        self.lab2.setText(QCoreApplication.translate("MainWindow", u"Odchylenie:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Edytor kryteri\u00f3w", None))
        self.addCrit_btn.setText(QCoreApplication.translate("MainWindow", u"Dodaj", None))
        self.deleteCrit_btn.setText(QCoreApplication.translate("MainWindow", u"Usu\u0144", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Akcje", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Algorytm:", None))
        self.benchmark_btn.setText(QCoreApplication.translate("MainWindow", u"Benchmark", None))
        self.algorithm_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Naiwny bez filtracji", None))
        self.algorithm_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Naiwny z filtracj\u0105", None))
        self.algorithm_select.setItemText(2, QCoreApplication.translate("MainWindow", u"Oparty o punkt idealny", None))

        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Rozwi\u0105\u017c", None))
        self.box.setTabText(self.box.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Panel", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Dane do algorytmu", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Czas wykonania [ms]", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Ilo\u015b\u0107 punkt\u00f3w niezdominowanych [%]", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Wykres", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Liczba por\u00f3wna\u0144", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Wymiar", None))
        self.box.setTabText(self.box.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Wykres", None))
        ___qtablewidgetitem = self.benchmark_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Czas wykonywania (ms)", None));
        ___qtablewidgetitem1 = self.benchmark_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Ilo\u015b\u0107 por\u00f3wna\u0144", None));
        ___qtablewidgetitem2 = self.benchmark_table.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Naiwny bez filtracji", None));
        ___qtablewidgetitem3 = self.benchmark_table.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Naiwny z filtracj\u0105", None));
        ___qtablewidgetitem4 = self.benchmark_table.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Opwrty o punkt idealny", None));

        __sortingEnabled = self.benchmark_table.isSortingEnabled()
        self.benchmark_table.setSortingEnabled(False)
        self.benchmark_table.setSortingEnabled(__sortingEnabled)

        self.box.setTabText(self.box.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Benchmark", None))
        self.box.setTabText(self.box.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Wyniki", None))
    # retranslateUi

