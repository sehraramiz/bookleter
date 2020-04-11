# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bookleter-gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys, pkg_resources, pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, qApp
from .Booklet import Book


class MainWindow(QtWidgets.QWidget):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(320, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QtCore.QSize(320, 480))
        font = QtGui.QFont()
        font.setPointSize(30)
        main_window.setFont(font)
        main_window.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(220, 220, 220);\n"
"background-color: rgb(236, 236, 236);")
        main_window.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        main_window.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.file_path_label = QtWidgets.QLabel(self.centralwidget)
        self.file_path_label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.file_path_label.setFont(font)
        self.file_path_label.setToolTip("")
        self.file_path_label.setAlignment(QtCore.Qt.AlignCenter)
        self.file_path_label.setObjectName("file_path_label")
        self.gridLayout.addWidget(self.file_path_label, 9, 0, 1, 7)
        self.make_booklet_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.make_booklet_button.sizePolicy().hasHeightForWidth())
        self.make_booklet_button.setSizePolicy(sizePolicy)
        self.make_booklet_button.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.make_booklet_button.setFont(font)
        self.make_booklet_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(77, 200, 112);")
        self.make_booklet_button.setObjectName("make_booklet_button")
        self.gridLayout.addWidget(self.make_booklet_button, 24, 0, 1, 6)
        self.margins_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.margins_label.setFont(font)
        self.margins_label.setToolTip("")
        self.margins_label.setToolTipDuration(2)
        self.margins_label.setObjectName("margins_label")
        self.gridLayout.addWidget(self.margins_label, 7, 0, 1, 1)
        self.start_page_label = QtWidgets.QLabel(self.centralwidget)
        self.start_page_label.setMaximumSize(QtCore.QSize(70, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_page_label.setFont(font)
        self.start_page_label.setObjectName("start_page_label")
        self.gridLayout.addWidget(self.start_page_label, 3, 0, 1, 1)
        self.start_page_number = QtWidgets.QTextEdit(self.centralwidget)
        self.start_page_number.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_page_number.setFont(font)
        self.start_page_number.setToolTip("")
        self.start_page_number.setToolTipDuration(2)
        self.start_page_number.setStatusTip("")
        self.start_page_number.setWhatsThis("")
        self.start_page_number.setObjectName("start_page_number")
        self.gridLayout.addWidget(self.start_page_number, 3, 2, 1, 1)
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.browse_button.setFont(font)
        self.browse_button.setToolTip("")
        self.browse_button.setToolTipDuration(2)
        self.browse_button.setStatusTip("")
        self.browse_button.setWhatsThis("")
        self.browse_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(77, 200, 112);")
        self.browse_button.setObjectName("browse_button")
        self.gridLayout.addWidget(self.browse_button, 0, 2, 1, 4)
        self.book_direction_combobox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.book_direction_combobox.sizePolicy().hasHeightForWidth())
        self.book_direction_combobox.setSizePolicy(sizePolicy)
        self.book_direction_combobox.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.book_direction_combobox.setFont(font)
        self.book_direction_combobox.setToolTip("")
        self.book_direction_combobox.setToolTipDuration(2)
        self.book_direction_combobox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.book_direction_combobox.setAutoFillBackground(False)
        self.book_direction_combobox.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(77, 200, 112);\n"
"")
        self.book_direction_combobox.setFrame(True)
        self.book_direction_combobox.setObjectName("book_direction_combobox")
        self.book_direction_combobox.addItem("")
        self.book_direction_combobox.addItem("")
        self.gridLayout.addWidget(self.book_direction_combobox, 2, 2, 1, 4)
        self.input_file_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.input_file_label.setFont(font)
        self.input_file_label.setObjectName("input_file_label")
        self.gridLayout.addWidget(self.input_file_label, 0, 0, 1, 2)
        self.end_page_number = QtWidgets.QTextEdit(self.centralwidget)
        self.end_page_number.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.end_page_number.setFont(font)
        self.end_page_number.setToolTip("")
        self.end_page_number.setToolTipDuration(2)
        self.end_page_number.setWhatsThis("")
        self.end_page_number.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.end_page_number.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.end_page_number.setObjectName("end_page_number")
        self.gridLayout.addWidget(self.end_page_number, 4, 2, 1, 1)
        self.book_direction_label = QtWidgets.QLabel(self.centralwidget)
        self.book_direction_label.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.book_direction_label.setFont(font)
        self.book_direction_label.setToolTip("")
        self.book_direction_label.setToolTipDuration(2)
        self.book_direction_label.setObjectName("book_direction_label")
        self.gridLayout.addWidget(self.book_direction_label, 2, 0, 1, 1)
        self.end_page_label = QtWidgets.QLabel(self.centralwidget)
        self.end_page_label.setMaximumSize(QtCore.QSize(70, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.end_page_label.setFont(font)
        self.end_page_label.setObjectName("end_page_label")
        self.gridLayout.addWidget(self.end_page_label, 4, 0, 1, 1)
        self.margins_percentage = QtWidgets.QTextEdit(self.centralwidget)
        self.margins_percentage.setMaximumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.margins_percentage.setFont(font)
        self.margins_percentage.setToolTip("")
        self.margins_percentage.setToolTipDuration(2)
        self.margins_percentage.setObjectName("margins_percentage")
        self.gridLayout.addWidget(self.margins_percentage, 7, 2, 1, 1)
        self.log_label = QtWidgets.QLabel(self.centralwidget)
        self.log_label.setMinimumSize(QtCore.QSize(0, 0))
        self.log_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.log_label.setFont(font)
        self.log_label.setToolTipDuration(2)
        self.log_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.log_label.setAlignment(QtCore.Qt.AlignCenter)
        self.log_label.setObjectName("log_label")
        self.gridLayout.addWidget(self.log_label, 23, 0, 1, 6)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        self.make_booklet_button.clicked.connect(self.make_booklet)
        self.browse_button.clicked.connect(self.browse_file)
        QtCore.QMetaObject.connectSlotsByName(main_window)

        self.pdf_file_path = ""

        about = QAction('&About', self)        
        about.setStatusTip('About Bookleter')
        about.triggered.connect(self.show_about_window)

        main_window.statusBar()

        menubar = main_window.menuBar()
        fileMenu = menubar.addMenu('&Yo!')
        fileMenu.addAction(about)

    def show_about_window(self):
            msg = QtWidgets.QMessageBox(self)
            ABOUT_TEXT = """
                The Bookleter {}
                New Version: https://github.com/reinenichts/bookleter/releases/new
                Github: https://github.com/reinenichts/bookleter
                Booklets Story: https://virgool.io/@mohsenbarzegar/d/nkkuh18xnbyk
            """.format(pkg_resources.get_distribution("bookleter").version)
            msg.setText(ABOUT_TEXT)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.show()

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
            direction_options = ["rtl", "ltr"]
            print(self.book_direction_combobox.currentIndex())
            self.log_label.setText("Making Booklet\nPlease Wait")
            new_book = Book(
                self.pdf_file_path,
                int(self.start_page_number.toPlainText()),
                int(self.end_page_number.toPlainText()),
                direction_options[self.book_direction_combobox.currentIndex()],
                self.margins_percentage.toPlainText())
            new_book.make_booklet()
            if not new_book.check_booklet_is_created():
                msg.setText('Please restart the app for another book')
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.show()
                return
            self.log_label.setText("Your booklet is ready!")
            msg.setText("Your booklet is ready!\nRestart the app for another book\nBooklet File: {}\nBooklet Test File: {}".format(
                    new_book.final_pdf_name, new_book.test_pdf_name))
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.show()

    def browse_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QtWidgets.QFileDialog.getOpenFileName()", "","Pdf Files (*.pdf)", options=options)
        if file_path:
            self.pdf_file_path = file_path
            self.file_path_label.setText(pathlib.Path(file_path).name)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Bookleter"))
        self.book_direction_combobox.setCurrentText(_translate("main_window", "Right to Left"))
        self.book_direction_combobox.setItemText(0, _translate("main_window", "Right to Left"))
        self.book_direction_combobox.setItemText(1, _translate("main_window", "Left to Right"))
        self.input_file_label.setText(_translate("main_window", "Enter Pdf File"))
        self.log_label.setText(_translate("main_window", "Log"))
        self.log_label.hide()
        self.browse_button.setText(_translate("main_window", "Browse"))
        self.book_direction_label.setText(_translate("main_window", "Book Direction"))
        self.margins_label.setText(_translate("main_window", "Margins"))
        self.start_page_label.setText(_translate("main_window", "Start Page :"))
        self.end_page_label.setText(_translate("main_window", "End Page :"))
        self.make_booklet_button.setText(_translate("main_window", "Make My Booklet"))
        self.file_path_label.setText(_translate("main_window", "/"))

def gui_main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    gui_main()
