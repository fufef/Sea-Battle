class Field:
    def __init__(self, n):
        self.size = n
        self.field = [[(None, False) for j in range(n)] for i in range(n)]
        self.ships = dict()

    def update_field(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            if ship in self.ships:
                old_start, old_orientation = self.ships[ship]

                for i in range(ship.size):
                    if old_orientation == 0:
                        self.field[old_start[0] + i][old_start[1]] = (None, False)
                    else:
                        self.field[old_start[0]][old_start[1] + i] = (None, False)

            self.ships[ship] = (location, ship.orientation)
            for i in range(ship.size):
                if ship.orientation == 0:
                    self.field[location[0] + i][location[1]] = (ship, False)
                else:
                    self.field[location[0]][location[1] + i] = (ship, False)

    def update_battlefield(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            for i in range(ship.size):
                if ship.orientation == 0:
                    self.field[location[0] + i][location[1]] = (ship, False)
                else:
                    self.field[location[0]][location[1] + i] = (ship, False)

    def clear_field(self):
        for i in range(self.size):
            for j in range(self.size):
                self.field[i][j] = (None, False)

    def shoot(self, location):
        cell = self.field[location[0]][location[1]][0]
        if cell is not None:
            cell.status = 'injured'
            t = abs(location[0] - cell.cell_location[0])
            if t == 0:
                t = abs(location[1] - cell.cell_location[1])
            cell.cell_status[t] = 'injured'
            if all((i == 'injured' for i in cell.cell_status)):
                cell.status = 'dead'
            self.field[location[0]][location[1]] = (cell, True)

            print(cell.status)
            return cell.status
        self.field[location[0]][location[1]] = (cell, True)
        print('past')
        return 'past'
