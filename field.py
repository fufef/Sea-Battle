class Field:
    def __init__(self, n):
        self.size = n
        self.field = [[(None, False) for j in range(n)] for i in range(n)]
        self.ships = set()

    def update_field(self, location, ship):
        if 0 <= location[0] <= self.size and 0 <= location[1] <= self.size:
            self.ships.add(ship)
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
