class Field:
    def __init__(self, n):
        self.size = n
        self.field = [[(None, False) for j in range(n)] for i in range(n)]
        self.ships = []

    def update_field(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            self.ships.append(ship)
            for i in range(ship.size):
                if ship.orientation == 0:
                    self.field[location[1]][location[0] + i] = (ship, False)
                else:
                    self.field[location[1] + i][location[0]] = (ship, False)
