from PyQt5 import QtWidgets, QtCore


class Ship:
    def __init__(self, size: int, location: (int, int)):
        self.size = size
        self.location = location
        self.orientation = 0
        self.cell_location = (-1, -1)
        self.status = 0
        self.button = None
        self.cell_status = [0 for i in range(self.size)]


class ShipButton(QtWidgets.QPushButton):
    def __init__(self, parent, ship):
        super().__init__(parent)
        self.ship = ship

    def transform(self):
        self.ship.orientation = int(not self.ship.orientation)
        size = self.size()
        self.setFixedSize(size.height(), size.width())

    def ship_alignment(self):
        field_loc = QtCore.QPoint(550, 60)
        if self.check_pos(self.ship.location, self.ship.orientation):
            delta = self.ship.location - field_loc
            self.ship.cell_location = (delta.x() // 45, delta.y() // 45)
            self.ship.location = field_loc + QtCore.QPoint(45 * self.ship.cell_location[0], 45 * self.ship.cell_location[1])
            self.move(self.ship.location)

    def check_pos(self, location: QtCore.QPoint, orientation: int):
        max_x = 1000
        max_y = 510
        dt = (self.ship.size - 1) * 45
        if orientation == 0:
            max_x -= dt
        else:
            max_y -= dt
        if 550 <= location.x() <= max_x and 60 <= location.y() <= max_y:
            return True
        return False
