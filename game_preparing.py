from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from ship import *
from field import Field
from game import Game


class GamePreparing(QtWidgets.QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.startPos = None
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
        self.start_btn.setFont(QtGui.QFont('Times', 22))
        self.start_btn.clicked.connect(self.start_game_action)

        self.clear_btn = QtWidgets.QPushButton(self)
        self.clear_btn.setGeometry(QtCore.QRect(640, 600, 100, 50))
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.setFont(QtGui.QFont('Times', 22))
        self.clear_btn.clicked.connect(self.clear_field)

        ships = QtWidgets.QLabel("ships:", self)
        ships.setGeometry(QtCore.QRect(80, 60, 100, 80))
        ships.setFont(QtGui.QFont('Times', 22))

        self.setObjectName("PreparingWindow")
        self.setContentsMargins(0, 0, 0, 0)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(550, 60, 200, 290)
        self.layout.setSpacing(0)
        self.user_field = Field(10)
        self.draw_field()

        self.ships = []
        self.movingButton = None
        self.draw_ships()

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
        nums.setGeometry(QtCore.QRect(500, 35, 300, 500))
        nums.setFont(QtGui.QFont('Times', 22))
        lets = QtWidgets.QLabel("a  b  c  d  e  f  g  h  i  j", self)
        lets.setGeometry(QtCore.QRect(565, 10, 500, 50))
        lets.setFont(QtGui.QFont('Times', 24))

    def draw_ships(self):
        self.ships.append(Ship(4, (50, 150)))
        for i in range(2):
            self.ships.append(Ship(3, (50, 200 + i * 50)))
        for i in range(3):
            self.ships.append(Ship(2, (50, 300 + i * 50)))
        for i in range(4):
            self.ships.append(Ship(1, (50, 450 + i * 50)))
        for i in self.ships:
            self.init_ship(i)

    def init_ship(self, i):
        i.button = ShipButton(self, i)
        i.button.setFixedSize(i.size * 45, 45)
        i.button.move(*i.location)
        i.button.installEventFilter(self)

    def clear_field(self):
        """Deletes all ships from battlefield"""
        self.user_field.clear()
        for i in self.ships:
            if i.orientation != 0:
                i.button.transform()
            i.button.move(i.button.init_location)

    def eventFilter(self, source, event):
        if source in ([i.button for i in self.ships] + [None]):
            ship = source.ship

            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                self.movingButton = source
                self.startPos = event.pos()

            if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.RightButton:
                if not source.check_pos(source.pos(), ship.orientation):
                    source.transform()
                elif source.check_pos(source.pos(), 1 - ship.orientation) and \
                        self.user_field.is_possible_to_rotate(ship):
                    source.transform()
                    self.user_field.update_field(source.ship.cell_location, source.ship)
            elif event.type() == QtCore.QEvent.MouseMove and self.movingButton:
                self.movingButton.move(source.pos() + event.pos() - self.startPos)
            elif event.type() == QtCore.QEvent.MouseButtonRelease and self.movingButton:
                self.movingButton.move(source.pos() + event.pos() - self.startPos)
                self.movingButton.ship.location = self.movingButton.pos()
                self.movingButton.ship_alignment()
                if self.movingButton.check_pos(source.pos(), self.movingButton.ship.orientation):
                    if self.user_field.is_allows(self.movingButton.ship):
                        self.movingButton.move(self.movingButton.ship.location)
                        self.user_field.update_field(self.movingButton.ship.cell_location, self.movingButton.ship)
                    else:
                        if self.movingButton.ship.orientation != 0:
                            self.movingButton.transform()
                        self.movingButton.move(self.movingButton.init_location)
                        self.movingButton.ship.cell_location = (-1, -1)

                self.movingButton = None
                print(self.user_field.field)
        return super().eventFilter(source, event)

    def back_menu_action(self):
        self.main_window.change_window(0)

    def start_game_action(self):
        self.user_field.delete_marks()
        self.main_window.change_window(2, Game(self.main_window, self.user_field))

