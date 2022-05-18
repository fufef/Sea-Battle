from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication



class Menu(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName("MenuWindow")
        #self.setStyleSheet("#MenuWindow{border-image:url(resources/background_menu.png)}")

        #QFontDatabase.addApplicationFont("resources/BNKGOTHM.TTF")
        font = QtGui.QFont("Times", 32)
        style = "background-color: rgba(255, 255, 255, 0); color: rgb(0, 0, 0);"

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(450, 350, 300, 100))
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(lambda: self.main_window.change_window(1))
        self.start_btn.setStyleSheet(style)



        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.start_btn.setText(_translate("Menu", "play"))
