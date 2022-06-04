class Field:
    def __init__(self, n):
        self.size = n
        self.field = [[(None, False) for j in range(n)] for i in range(n)]
        self.ships = dict()

    def update_field(self, location, ship):
        """Updates locations and orientations of user ships"""
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            if ship in self.ships:
                old_start, old_orientation = self.ships[ship]
                self.update_ship(old_orientation, old_start, ship, None, False)

            self.ships[ship] = (location, ship.orientation)
            self.update_ship(ship.orientation, location, ship, ship, True)

    def update_ship(self, old_orientation, old_start, old_ship, new_ship, new_ship_status):
        for i in range(old_ship.size):
            if old_orientation == 0:
                self.field[old_start[0] + i][old_start[1]] = (new_ship, new_ship_status)
            else:
                self.field[old_start[0]][old_start[1] + i] = (new_ship, new_ship_status)

    def update_battlefield(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            self.update_ship(ship.orientation, location, ship, ship, False)

    def is_allows(self, ship):
        """Checks if it's possible to put a ship"""
        for i in self.ships:
            if i != ship and all((j in (-1, 0, 1) for j in ship.distance_in_directions(i))):
                return False

        return True

    def is_possible_to_rotate(self, ship):
        """Checks if it's possible to rotate a ship"""
        ship.orientation = 1 - ship.orientation
        result = self.is_allows(ship)
        ship.orientation = 1 - ship.orientation
        return result

    def clear(self):
        """Deletes all ships from battlefield"""
        for i in range(self.size):
            for j in range(self.size):
                self.field[i][j] = (None, False)

        for i in self.ships.keys():
            i.cell_location = (-1, -1)

        self.ships.clear()

    def shoot(self, location):
        """Shoots in cell and returns status of user action"""
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
