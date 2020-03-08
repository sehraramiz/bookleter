# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bookleter-gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from .Booklet import Book


class MainWindow(QtWidgets.QWidget):
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
        self.margins_percentage = QtWidgets.QTextEdit(self.centralwidget)
        self.margins_percentage.setGeometry(QtCore.QRect(90, 150, 51, 31))
        self.margins_percentage.setObjectName("margins_percentage")
        self.input_file_label = QtWidgets.QLabel(self.centralwidget)
        self.input_file_label.setGeometry(QtCore.QRect(20, 40, 52, 13))
        self.input_file_label.setObjectName("input_file_label")
        self.start_page_number_label = QtWidgets.QLabel(self.centralwidget)
        self.start_page_number_label.setGeometry(QtCore.QRect(20, 80, 61, 16))
        self.start_page_number_label.setObjectName("start_page_number_label")
        self.end_page_number_label = QtWidgets.QLabel(self.centralwidget)
        self.end_page_number_label.setGeometry(QtCore.QRect(140, 80, 16, 16))
        self.end_page_number_label.setObjectName("end_page_number_label")
        self.book_direction_label = QtWidgets.QLabel(self.centralwidget)
        self.book_direction_label.setGeometry(QtCore.QRect(20, 120, 52, 13))
        self.book_direction_label.setObjectName("book_direction_label")
        self.margins_label = QtWidgets.QLabel(self.centralwidget)
        self.margins_label.setGeometry(QtCore.QRect(20, 160, 52, 13))
        self.margins_label.setObjectName("margins_label")
        self.make_booklet_button = QtWidgets.QPushButton(self.centralwidget)
        self.make_booklet_button.setGeometry(QtCore.QRect(60, 240, 111, 21))
        self.make_booklet_button.setObjectName("make_booklet_button")
        self.book_direction_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.book_direction_combobox.setGeometry(QtCore.QRect(90, 110, 51, 22))
        self.book_direction_combobox.setObjectName("book_direction_combobox")
        # self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progress_bar.setGeometry(QtCore.QRect(20, 200, 181, 23))
        # self.progress_bar.setProperty("value", 24)
        # self.progress_bar.setObjectName("progress_bar")
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(90, 30, 111, 31))
        self.browse_button.setObjectName("browse_button")
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        self.make_booklet_button.clicked.connect(self.make_booklet)
        self.browse_button.clicked.connect(self.browse_file)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.book_direction_combobox.addItems(["rtl", "ltr"])
        self.pdf_file_path = ""


    def make_booklet(self):
        print(self.book_direction_combobox.currentText())
        msg = QtWidgets.QMessageBox(self)
        if not len(self.pdf_file_path):
            msg.setText('Please select a pdf file with browse button')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.show()
        elif not len(self.start_page_number.toPlainText()) or not len(self.end_page_number.toPlainText()):
            msg.setText('Please enter start and end page numbers')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.show()
        elif not len(self.margins_percentage.toPlainText()):
            msg.setText('Please enter margins percentage')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.show()    
        else:
            new_book = Book(
                self.pdf_file_path,
                int(self.start_page_number.toPlainText()),
                int(self.end_page_number.toPlainText()),
                self.book_direction_combobox.currentText(),
                self.margins_percentage.toPlainText())
            new_book.make_booklet()
            msg.setText('Your book is ready!')
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.show()


    def browse_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QtWidgets.QFileDialog.getOpenFileName()", "","Pdf Files (*.pdf)", options=options)
        if fileName:
            self.pdf_file_path = fileName
            print(fileName)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Bookleter"))
        self.input_file_label.setText(_translate("main_window", "your pdf"))
        self.start_page_number_label.setText(_translate("main_window", "from page"))
        self.end_page_number_label.setText(_translate("main_window", "to"))
        self.book_direction_label.setText(_translate("main_window", "direction"))
        self.margins_label.setText(_translate("main_window", "margins"))
        self.make_booklet_button.setText(_translate("main_window", "Make My Booklet"))
        self.browse_button.setText(_translate("main_window", "Browse"))

def gui_main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())