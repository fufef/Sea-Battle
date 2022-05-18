from PyQt5 import QtWidgets, QtCore, QtGui
#import partie as pa
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt


class Game(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.screen_size = (main_window.size().width(), main_window.size().height())
        self.main_window = main_window
        self.backMenu_btn = QtWidgets.QPushButton(self)
        self.backMenu_btn.setGeometry(QtCore.QRect(25, 20, 55, 45))
        self.backMenu_btn.setObjectName("backMenu_btn")
        self.backMenu_btn.setIcon(QtGui.QIcon('resources/arrow_black.png'))
        self.backMenu_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.backMenu_btn.setIconSize(QtCore.QSize(55, 40))
        self.backMenu_btn.clicked.connect(self.back_menu_action)

        self.setObjectName("GameWindow")
        #self.setStyleSheet("#GameWindow{border-image:url(resources/background.png)}")
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setContentsMargins(0, 0, 0, 0)

        self.layout_user = QGridLayout()
        self.layout_user.setContentsMargins(550, 60, 180, 230)
        self.layout_user.setSpacing(0)
        self.draw_field(self.layout_user)
        self.setLayout(self.layout_user)

        self.layout_comp = QGridLayout()
        self.layout_comp.setContentsMargins(20, 60, 500, 230)
        self.layout_comp.setSpacing(0)
        self.draw_field(self.layout_comp)
        self.setLayout(self.layout_comp)

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

    def draw_field(self, layout):
        for row, rank in enumerate('1234567890'):
            for col, file in enumerate('abcdefghij'):
                square = QWidget(self)
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                square.setStyleSheet('background-color: #FCFCEE; border: 1px solid black;')
                layout.addWidget(square, row, col)
        # nums = QtWidgets.QLabel("1\n2\n3\n4\n5\n6\n7\n8\n9\n10", self)
        # nums.setGeometry(QtCore.QRect(500, 65, 300, 500))
        # nums.setFont(QtGui.QFont('Times', 25))
        # lets = QtWidgets.QLabel("a  b  c  d  e  f  g  h  i  j", self)
        # lets.setGeometry(QtCore.QRect(565, 10, 500, 50))
        # lets.setFont(QtGui.QFont('Times', 26))

    def back_menu_action(self):
        self.main_window.change_window(0)

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        pass

