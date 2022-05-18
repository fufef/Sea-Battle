from PyQt5 import QtWidgets, QtCore, QtGui
#import partie as pa
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, Qt


class GamePreparing(QtWidgets.QFrame):
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

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(840, 600, 100, 50))
        self.start_btn.setObjectName("start_btn")
        #self.start_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.start_btn.setFont(QtGui.QFont('Times', 22))
        self.start_btn.clicked.connect(self.start_game_action)

        self.clear_btn = QtWidgets.QPushButton(self)
        self.clear_btn.setGeometry(QtCore.QRect(640, 600, 100, 50))
        self.clear_btn.setObjectName("clear_btn")
        # self.clear_btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.clear_btn.setFont(QtGui.QFont('Times', 22))
        # self.clear_btn.clicked.connect(self.start_game_action)

        ships = QtWidgets.QLabel("ships:", self)
        ships.setGeometry(QtCore.QRect(80, 60, 100, 80))
        ships.setFont(QtGui.QFont('Times', 22))

        self.setObjectName("PreparingWindow")
        #self.setStyleSheet("#PreparingWindow{border-image:url(resources/background.png)}")
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(550, 60, 180, 230)
        #self.layout.setGeometry(QtCore.QRect(550, 60, 180, 180))
        self.layout.setSpacing(0)
        self.draw_field()

        self.movingButton = None
        self.button = QtWidgets.QPushButton('', self)
        self.button.setFixedSize(100,100)
        self.button.move(100, 350)
        self.button.installEventFilter(self)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(20, 20, 431, 491))
        self.widget.setObjectName("widget")
        self.comboBox = QtWidgets.QComboBox(self.widget)

        self.setLayout(self.layout)
        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.start_btn.setText(_translate("Preparing", "start"))
        self.clear_btn.setText(_translate("Preparing", "clear"))

    def draw_field(self):
        for row, rank in enumerate('1234567890'):
            for col, file in enumerate('abcdefghij'):
                square = QWidget(self)
                square.setObjectName(file + rank)
                square.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                square.setStyleSheet('background-color: #FCFCEE; border: 1px solid black;')
                self.layout.addWidget(square, row, col)
        nums = QtWidgets.QLabel("1\n2\n3\n4\n5\n6\n7\n8\n9\n10", self)
        nums.setGeometry(QtCore.QRect(500, 65, 300, 500))
        nums.setFont(QtGui.QFont('Times', 25))
        lets = QtWidgets.QLabel("a  b  c  d  e  f  g  h  i  j", self)
        lets.setGeometry(QtCore.QRect(565, 10, 500, 50))
        lets.setFont(QtGui.QFont('Times', 26))

    def eventFilter(self, source, event):
        if source in (self.button, self.comboBox):
            if event.type() == QtCore.QEvent.MouseButtonPress and \
                    event.button() == QtCore.Qt.LeftButton:
                self.movingButton = source
                self.startPos = event.pos()
            elif event.type() == QtCore.QEvent.MouseMove and self.movingButton:
                self.movingButton.move(source.pos() + event.pos() - self.startPos)
            elif event.type() == QtCore.QEvent.MouseButtonRelease and self.movingButton:
                self.movingButton.move(source.pos() + event.pos() - self.startPos)
                self.movingButton = None
        return super().eventFilter(source, event)

    def back_menu_action(self):
        self.main_window.change_window(0)

    def start_game_action(self):
        self.main_window.change_window(2)

    def dragMoveEvent(self, a0: QtGui.QDragMoveEvent) -> None:
        pass

