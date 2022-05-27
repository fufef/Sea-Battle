import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from ship import *
from field import Field
from random import randint


class Game(QtWidgets.QFrame):
    def __init__(self, main_window, user_field: Field):
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
        self.user_field = user_field
        self.enemy_field = Field(10)

        self.layout_user = QGridLayout()
        self.layout_user.setSpacing(0)
        self.draw_field(self.layout_user)
        self.layout_comp = QGridLayout()
        self.layout_comp.setSpacing(0)
        self.draw_field(self.layout_comp)
        self.lay = QHBoxLayout(self)
        self.lay.addLayout(self.layout_user)
        self.lay.addLayout(self.layout_comp)
        self.lay.setSpacing(100)
        self.lay.setContentsMargins(100, 175, 100, 175)

        self.show_ships(self.user_field.ships, (100, 175))
        self.fill_field(self.enemy_field)
        self.installEventFilter(self)

        self.is_all_at_sea = True
        self.prev_cell = (-1, -1)

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

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton \
                and self.check_pos(event.pos()):
            startPos = event.pos()

            loc = self.get_cell_coords(startPos)
            print(loc)
            res = self.enemy_field.shoot(loc)

            pic = QtWidgets.QLabel(self)
            if res == 'dead':
                sh = self.enemy_field.field[loc[0]][loc[1]][0]
                dx = 0
                dy = 0
                if sh.orientation == 0:
                    dx = 1
                else:
                    dy = 1
                for i in range(sh.size):
                    pic = QtWidgets.QLabel(self)
                    pic.setPixmap(QtGui.QPixmap('resources/krov.png'))
                    pic.setFixedSize(45, 45)
                    pic.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
                    pic.move(QtCore.QPoint(650 + 45 * (sh.cell_location[0] + dx * i), 175 + 45 * (sh.cell_location[1] + dy * i)))
                    pic.show()
            else:
                if res == 'past':
                    pic.setPixmap(QtGui.QPixmap('resources/mimo.png'))
                else:
                    pic.setPixmap(QtGui.QPixmap('resources/bang.png'))
                pic.setFixedSize(45, 45)
                pic.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
                pic.move(QtCore.QPoint(650 + 45 * loc[0], 175 + 45 * loc[1]))
                pic.show()

            self.check_end_game(self.enemy_field)
            self.enemy_move()

        return super().eventFilter(source, event)

    def get_cell_coords(self, pos: QtCore.QPoint):
        return (pos.x() - 650) // 45, (pos.y() - 175) // 45

    def show_ships(self, ships, offset):
        for i in ships:
            ship = QtWidgets.QWidget(self)
            if i.orientation == 0:
                ship.setFixedSize(i.size * 45, 45)
            else:
                ship.setFixedSize(45, i.size * 45)
            ship.move(QtCore.QPoint(offset[0] + i.cell_location[0] * 45, offset[1] + i.cell_location[1] * 45))
            ship.setStyleSheet('background-color: #FFFF00; border: 1px solid black;')

    def fill_field(self, field: Field):
        s = {(i, j): False for i in range(field.size) for j in range(field.size)}
        self.choose(field, s, 4)
        for i in range(2):
            self.choose(field, s, 3)
        for i in range(3):
            self.choose(field, s, 2)
        for i in range(4):
            self.choose(field, s, 1)
        #self.show_ships(field.ships, (100 + 450 + 100, 175))
        for i in field.ships:
            field.update_battlefield(i.cell_location, i)

    def choose(self, field: Field, s, le):
        r, o = self.rnd_choose(s)
        cells = [(r[0] + i, r[1] + j) for i in range((1 - o) * le + 1) for j in range(o * le + 1)]
        while not all((i in s and not s[i] for i in cells)):
            r, o = self.rnd_choose(s)
            cells = [(r[0] + i, r[1] + j) for i in range((1 - o) * le + 1) for j in range(o * le + 1)]

        c = Ship(le, r, o)
        c.cell_location = r
        field.ships[c] = (c.location, c.orientation)
        for i in cells:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    x, y = i[0] + dx, i[1] + dy
                    if 0 <= x < 10 and 0 <= y < 10:
                        s[(x, y)] = True

    def rnd_choose(self, s):
        r = random.choice(tuple(s.keys()))
        while s[r]:
            r = random.choice(tuple(s.keys()))
        o = randint(0, 1)
        return r, o

    def check_pos(self, location: QtCore.QPoint):
        if 650 <= location.x() <= 1100 and 175 <= location.y() <= 175 + 450:
            return True
        return False

    def enemy_move(self):
        cell = (-1, -1)
        if self.is_all_at_sea:
            cell = (randint(0, 9), randint(0, 9))
            while self.user_field.field[cell[0]][cell[1]][1]:
                cell = (randint(0, 9), randint(0, 9))
            print(cell)
            res = self.user_field.shoot(cell)
            if res == 'injured':
                self.prev_cell = cell
                self.is_all_at_sea = False
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if abs(i + j) == 1 and 0 <= self.prev_cell[0] + i < 10 and 0 <= self.prev_cell[1] + j < 10 and not \
                            self.user_field.field[self.prev_cell[0] + i][self.prev_cell[1] + j][1]:
                        cell = (self.prev_cell[0] + i, self.prev_cell[1] + j)
                        break
                if cell == (-1, -1):
                    continue
            print('ха!', cell)
            res = self.user_field.shoot(cell)
            self.prev_cell = cell
            if res != 'injured':
                self.is_all_at_sea = True

        if res == 'dead':
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= cell[0] + i < 10 and 0 <= cell[1] + j < 10:
                        self.user_field.field[cell[0] + i][cell[1] + j] = \
                            (self.user_field.field[cell[0] + i][cell[1] + j][0], True)
            print(self.user_field.field[cell[0]][cell[1]])
            sh = self.user_field.field[cell[0]][cell[1]][0]
            dx = 0
            dy = 0
            if sh.orientation == 0:
                dx = 1
            else:
                dy = 1
            for i in range(sh.size):
                pic = QtWidgets.QLabel(self)
                pic.setPixmap(QtGui.QPixmap('resources/krov.png'))
                pic.setFixedSize(45, 45)
                pic.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
                pic.move(
                    QtCore.QPoint(100 + 45 * (sh.cell_location[0] + dx * i), 175 + 45 * (sh.cell_location[1] + dy * i)))
                pic.show()
        else:
            pic = QtWidgets.QLabel(self)
            if res == 'past':
                pic.setPixmap(QtGui.QPixmap('resources/mimo.png'))
            else:
                pic.setPixmap(QtGui.QPixmap('resources/bang.png'))
            pic.setFixedSize(45, 45)
            pic.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            pic.move(QtCore.QPoint(100 + 45 * cell[0], 175 + 45 * cell[1]))
            pic.show()
        self.check_end_game(self.user_field)

    def back_menu_action(self):
        self.main_window.change_window(1)

    def check_end_game(self, field):
        if all((i.status == 'dead' for i in field.ships)):
            if field == self.user_field:
                self.complete_game("You lost(((")
            else:
                self.complete_game("You win!!!")

    def complete_game(self, text: str):
        r = QtWidgets.QFrame(self.main_window)
        l = QtWidgets.QLabel(r)
        l.setFont(QtGui.QFont("Times", 60))
        l.move(QtCore.QPoint(400, 300))
        l.setText(text)
        self.main_window.change_window(3, r)
