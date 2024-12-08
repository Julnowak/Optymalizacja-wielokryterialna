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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QWidget)

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
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 3)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)

        self.start_btn = QPushButton(self.centralwidget)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setMinimumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.start_btn, 0, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.class_table = QTableWidget(self.centralwidget)
        self.class_table.setObjectName(u"class_table")
        self.class_table.setMinimumSize(QSize(0, 200))

        self.gridLayout.addWidget(self.class_table, 2, 3, 1, 3)

        self.criterium_select = QComboBox(self.centralwidget)
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.addItem("")
        self.criterium_select.setObjectName(u"criterium_select")
        self.criterium_select.setMinimumSize(QSize(300, 0))

        self.gridLayout.addWidget(self.criterium_select, 0, 2, 1, 2)

        self.load_btn = QPushButton(self.centralwidget)
        self.load_btn.setObjectName(u"load_btn")
        self.load_btn.setMinimumSize(QSize(150, 40))

        self.gridLayout.addWidget(self.load_btn, 0, 0, 1, 1)

        self.ranking_table = QTableWidget(self.centralwidget)
        self.ranking_table.setObjectName(u"ranking_table")
        self.ranking_table.setMinimumSize(QSize(0, 200))

        self.gridLayout.addWidget(self.ranking_table, 4, 0, 1, 3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 3)

        self.graph = plotwidget(self.centralwidget)
        self.graph.setObjectName(u"graph")

        self.gridLayout.addWidget(self.graph, 4, 3, 1, 3)

        self.alternatives_table = QTableWidget(self.centralwidget)
        self.alternatives_table.setObjectName(u"alternatives_table")
        self.alternatives_table.setMinimumSize(QSize(0, 200))
        self.alternatives_table.verticalHeader().setHighlightSections(True)

        self.gridLayout.addWidget(self.alternatives_table, 2, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Klasy", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Alternatywy z kryteriami", None))
        self.start_btn.setText(QCoreApplication.translate("MainWindow", u"Stw\u00f3rz ranking", None))
        self.criterium_select.setItemText(0, QCoreApplication.translate("MainWindow", u"FUZZY TOPSIS", None))
        self.criterium_select.setItemText(1, QCoreApplication.translate("MainWindow", u"UTA DIS", None))
        self.criterium_select.setItemText(2, QCoreApplication.translate("MainWindow", u"SP CS", None))
        self.criterium_select.setItemText(3, QCoreApplication.translate("MainWindow", u"RSM", None))

        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Wczytaj dane z pliku", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Stworzony ranking", None))
    # retranslateUi

