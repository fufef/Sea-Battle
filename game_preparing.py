from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRect, Qt


class GamePreparing(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.screen_size = (main_window.size().width(), main_window.size().height())
        self.main_window = main_window
        self.backMenu_btn = QtWidgets.QPushButton(self)
        self.backMenu_btn.setGeometry(QtCore.QRect(25, 25, 55, 45))
        self.backMenu_btn.setObjectName("backMenu_btn")
        self.backMenu_btn.setIcon(QtGui.QIcon('resources/arrow_white.png'))
        self.backMenu_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n")
        self.backMenu_btn.setIconSize(QtCore.QSize(55, 40))
        self.backMenu_btn.clicked.connect(self.back_menu_action)

        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setFont(QtGui.QFont('BankGothic Md BT', 30))

        self.setObjectName("GameWindow")
        self.setStyleSheet("#GameWindow{border-image:url(resources/background.png)}")

    def back_menu_action(self):
        self.main_window.change_window(0)

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        pass

