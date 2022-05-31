class Field:
    def __init__(self, n):
        self.size = n
        self.field = [[(None, False) for j in range(n)] for i in range(n)]
        self.ships = dict()

    def update_field(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            if ship in self.ships:
                old_start, old_orientation = self.ships[ship]

                # TODO rewrite using ship.ship_span_cells
                for i in range(ship.size):
                    if old_orientation == 0:
                        self.field[old_start[0] + i][old_start[1]] = (None, False)
                    else:
                        self.field[old_start[0]][old_start[1] + i] = (None, False)

            self.ships[ship] = (location, ship.orientation)
            # TODO rewrite using ship.ship_span_cells
            for i in range(ship.size):
                if ship.orientation == 0:
                    self.field[location[0] + i][location[1]] = (ship, True)
                else:
                    self.field[location[0]][location[1] + i] = (ship, True)

    def update_battlefield(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            for i in range(ship.size):
                if ship.orientation == 0:
                    self.field[location[0] + i][location[1]] = (ship, False)
                else:
                    self.field[location[0]][location[1] + i] = (ship, False)

    def is_allows(self, ship):
        for i in self.ships:
            if i != ship and all((j in (-1, 0, 1) for j in ship.distance_in_directions(i))):
                return False

        return True

    def is_possible_to_rotate(self, ship):
        ship.orientation = 1 - ship.orientation
        result = self.is_allows(ship)
        ship.orientation = 1 - ship.orientation
        return result

    def clear(self):
        for i in range(self.size):
            for j in range(self.size):
                self.field[i][j] = (None, False)

        for i in self.ships.keys():
            i.cell_location = (-1, -1)

        self.ships.clear()

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

    def delete_marks(self):
        for i in range(self.size):
            for j in range(self.size):
                self.field[i][j] = (self.field[i][j][0], False)
