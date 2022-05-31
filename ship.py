from PyQt5 import QtWidgets, QtCore

INFINITY = 1000


class Ship:
    def __init__(self, size: int, location: (int, int), orientation=0):
        self.size = size
        self.location = location
        self.orientation = orientation
        self.cell_location = (-1, -1)
        self.status = 'live'
        self.button = None
        self.cell_status = ['live' for i in range(self.size)]

    @property
    def ship_span_cells(self):
        for i in range(self.size):
            if self.orientation == 0:
                yield self.cell_location[0] + i, self.cell_location[1]
            else:
                yield self.cell_location[0], self.cell_location[1] + i

    def distance_in_directions(self, other):
        if self.cell_location[0] < 0 or other.cell_location[0] < 0:
            return INFINITY, INFINITY

        self_span = list(self.ship_span_cells)
        other_span = list(other.ship_span_cells)

        cells_distances = ((abs(i[0] - j[0]), abs(i[1] - j[1])) for i in self_span for j in other_span)
        return min(cells_distances, key=sum)


class ShipButton(QtWidgets.QPushButton):
    def __init__(self, parent, ship):
        super().__init__(parent)
        self.ship = ship
        self.init_location = QtCore.QPoint(ship.location[0], ship.location[1])

    def transform(self):
        self.ship.orientation = 1 - self.ship.orientation
        size = self.size()
        self.setFixedSize(size.height(), size.width())

    def ship_alignment(self):
        field_loc = QtCore.QPoint(550, 60)
        if self.check_pos(self.ship.location, self.ship.orientation):
            delta = self.ship.location - field_loc
            self.ship.cell_location = (delta.x() // 45, delta.y() // 45)
            self.ship.location = field_loc + QtCore.QPoint(45 * self.ship.cell_location[0],
                                                           45 * self.ship.cell_location[1])

    def check_pos(self, location: QtCore.QPoint, orientation: int):
        max_x = 1000
        max_y = 510
        dt = self.ship.size * 45
        if orientation == 0:
            max_x -= dt
        else:
            max_y -= dt
        if 550 <= location.x() <= max_x + 25 and 60 <= location.y() <= max_y + 25:
            return True
        return False
