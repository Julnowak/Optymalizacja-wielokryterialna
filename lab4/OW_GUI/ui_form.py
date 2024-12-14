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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QWidget)

from plotwidget import plotwidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
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
        self.load_btn = QPushButton(self.tab)
        self.load_btn.setObjectName(u"load_btn")
        self.load_btn.setMinimumSize(QSize(150, 40))

        self.gridLayout_2.addWidget(self.load_btn, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.criterium_select = QComboBox(self.tab)
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.setObjectName(u"criterium_select")
        self.criterium_select.setMinimumSize(QSize(300, 0))

        self.gridLayout_2.addWidget(self.criterium_select, 0, 2, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.start_btn = QPushButton(self.tab)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setMinimumSize(QSize(150, 40))

        self.gridLayout_2.addWidget(self.start_btn, 0, 5, 1, 1)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 3)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 3, 1, 3)

        self.alternatives_table = QTableWidget(self.tab)
        self.alternatives_table.setObjectName(u"alternatives_table")
        self.alternatives_table.setMinimumSize(QSize(0, 200))
        self.alternatives_table.verticalHeader().setHighlightSections(True)

        self.gridLayout_2.addWidget(self.alternatives_table, 2, 0, 1, 3)

        self.class_table = QTableWidget(self.tab)
        self.class_table.setObjectName(u"class_table")
        self.class_table.setMinimumSize(QSize(0, 200))

        self.gridLayout_2.addWidget(self.class_table, 2, 3, 1, 3)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 200))
        self.gridLayout_5 = QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.lower_bound = QSpinBox(self.groupBox)
        self.lower_bound.setObjectName(u"lower_bound")

        self.gridLayout_5.addWidget(self.lower_bound, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)

        self.sample_num = QSpinBox(self.groupBox)
        self.sample_num.setObjectName(u"sample_num")
        self.sample_num.setMinimum(1)
        self.sample_num.setValue(5)

        self.gridLayout_5.addWidget(self.sample_num, 1, 4, 1, 1)

        self.upper_bound = QSpinBox(self.groupBox)
        self.upper_bound.setObjectName(u"upper_bound")
        self.upper_bound.setValue(10)

        self.gridLayout_5.addWidget(self.upper_bound, 1, 2, 1, 1)

        self.variant_select = QComboBox(self.groupBox)
        self.variant_select.addItem("")
        self.variant_select.addItem("")
        self.variant_select.setObjectName(u"variant_select")

        self.gridLayout_5.addWidget(self.variant_select, 0, 1, 1, 2)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_5.addWidget(self.label_11, 1, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)

        self.metric_select = QComboBox(self.groupBox)
        self.metric_select.addItem("")
        self.metric_select.addItem("")
        self.metric_select.setObjectName(u"metric_select")

        self.gridLayout_5.addWidget(self.metric_select, 0, 4, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 0, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_5.addWidget(self.label_4, 2, 0, 1, 1)

        self.opti_type = QComboBox(self.groupBox)
        self.opti_type.addItem("")
        self.opti_type.addItem("")
        self.opti_type.setObjectName(u"opti_type")

        self.gridLayout_5.addWidget(self.opti_type, 2, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 3, 0, 2, 6)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_4 = QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.gridLayout_4.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 50))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)

        self.ranking_table = QTableWidget(self.tab_2)
        self.ranking_table.setObjectName(u"ranking_table")
        self.ranking_table.setMinimumSize(QSize(0, 200))

        self.gridLayout_4.addWidget(self.ranking_table, 1, 1, 1, 1)

        self.graph = plotwidget(self.tab_2)
        self.graph.setObjectName(u"graph")
        self.graph.setMinimumSize(QSize(600, 0))

        self.gridLayout_4.addWidget(self.graph, 1, 0, 2, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
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
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj dane z pliku", None))
        self.criterium_select.setItemText(0, QCoreApplication.translate("MainWindow", u"FUZZY TOPSIS", None))
        self.criterium_select.setItemText(1, QCoreApplication.translate("MainWindow", u"UTA DIS", None))
        self.criterium_select.setItemText(2, QCoreApplication.translate("MainWindow", u"SP CS", None))
        self.criterium_select.setItemText(3, QCoreApplication.translate("MainWindow", u"RSM", None))

        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Stw\u00f3rz ranking", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Alternatywy z kryteriami", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Klasy", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Parametry specyficzne dla algorytm\u00f3w:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Granice:", None))
        self.variant_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Ci\u0105g\u0142y", None))
        self.variant_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Dyskretny", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Liczba pr\u00f3bek:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Wariant:", None))
        self.metric_select.setItemText(0, QCoreApplication.translate("MainWindow", u"Euklidesowa", None))
        self.metric_select.setItemText(1, QCoreApplication.translate("MainWindow", u"Czebyszewa", None))

        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Miara:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Typ:", None))
        self.opti_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Minimalizacja", None))
        self.opti_type.setItemText(1, QCoreApplication.translate("MainWindow", u"Maksymalizacja", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Ustawienia", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Stworzony ranking", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Wykres", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Wyniki", None))
    # retranslateUi

