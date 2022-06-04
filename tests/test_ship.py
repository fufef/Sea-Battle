import unittest

from ship import Ship


class constructor_tests(unittest.TestCase):
    def test_status(self):
        ship = Ship(2, (0, 0))
        self.assertEqual(ship.status, 'live')

    def test_status(self):
        ship = Ship(2, (0, 0))
        self.assertEqual(ship.cell_status, ['live', 'live'])


class ship_span_cells_tests(unittest.TestCase):
    def test_works_when_out_of_bound(self):
        ship = Ship(1, (0, 0))
        for i in ship.ship_span_cells:
            self.assertEqual(i, (-1, -1))

    def test_works_when_out_of_bound(self):
        ship = Ship(1, (1, 1))
        for i in ship.ship_span_cells:
            self.assertEqual(i, (-1, -1))


class ship_span_cells_tests(unittest.TestCase):
    def test_calculates_when_the_same_ship(self):
        ship = Ship(1, (1, 1))
        ship.cell_location = (1, 1)
        result = ship.distance_in_directions(ship)
        self.assertEqual(result, (0, 0))

    def test_calculates_when_different_x(self):
        ship = Ship(1, (1, 1))
        ship.cell_location = (1, 1)
        ship2 = Ship(1, (2, 1))
        ship2.cell_location = (2, 1)
        result = ship.distance_in_directions(ship2)
        self.assertEqual(result, (1, 0))

    def test_calculates_when_different_y(self):
        ship = Ship(1, (1, 1))
        ship.cell_location = (1, 1)
        ship2 = Ship(1, (1, 2))
        ship2.cell_location = (1, 2)
        result = ship.distance_in_directions(ship2)
        self.assertEqual(result, (0, 1))

    def test_calculates_when_different_y_and_x(self):
        ship = Ship(1, (1, 1))
        ship.cell_location = (1, 1)
        ship2 = Ship(1, (2, 2))
        ship2.cell_location = (2, 2)
        result = ship.distance_in_directions(ship2)
        self.assertEqual(result, (1, 1))

    def test_calculates_when_incorrect_x_or_y(self):
        ship = Ship(1, (-1, 1))
        ship.cell_location = (1, 1)
        result = ship.distance_in_directions(ship)
        self.assertEqual(result, (1000, 1000))
