# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui-qt/bookleter-gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(240, 320)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.start_page_number = QtWidgets.QTextEdit(self.centralwidget)
        self.start_page_number.setGeometry(QtCore.QRect(90, 70, 41, 31))
        self.start_page_number.setPlaceholderText("")
        self.start_page_number.setObjectName("start_page_number")
        self.end_page_number = QtWidgets.QTextEdit(self.centralwidget)
        self.end_page_number.setGeometry(QtCore.QRect(160, 70, 41, 31))
        self.end_page_number.setObjectName("end_page_number")
        self.margins = QtWidgets.QTextEdit(self.centralwidget)
        self.margins.setGeometry(QtCore.QRect(90, 150, 51, 31))
        self.margins.setObjectName("margins")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 40, 52, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 61, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 80, 16, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 52, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 160, 52, 13))
        self.label_5.setObjectName("label_5")
        self.make_booklet_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_booklet_button.setGeometry(QtCore.QRect(60, 240, 111, 21))
        self.make_booklet_button.setObjectName("make_booklet_button")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 110, 51, 22))
        self.comboBox.setObjectName("comboBox")
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(20, 200, 181, 23))
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(90, 30, 111, 31))
        self.browse.setObjectName("browse")
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        self.make_booklet_button.clicked.connect(self.make_booklet)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def make_booklet(self):
        print("clicked!")

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "MainWindow"))
        self.label.setText(_translate("main_window", "your pdf"))
        self.label_2.setText(_translate("main_window", "from page"))
        self.label_3.setText(_translate("main_window", "to"))
        self.label_4.setText(_translate("main_window", "direction"))
        self.label_5.setText(_translate("main_window", "margins"))
        self.make_booklet_button.setText(_translate("main_window", "Make My Booklet"))
        self.browse.setText(_translate("main_window", "Browse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
