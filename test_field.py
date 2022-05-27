import unittest
from PyQt5 import QtGui
from field import Field
from ship import Ship


class update_field_tests(unittest.TestCase):
    def test_empty_field(self):
        field = Field(1)
        self.assertEqual(field.field, [[(None, False)]])

    def test_update_one_cell_field(self):
        field = Field(1)
        ship = Ship(1, (0, 0))
        field.update_field((0, 0), ship)
        self.assertEqual(field.field, [[(ship, False)]])

    def test_update_field(self):
        field = Field(3)
        ship1 = Ship(1, (0, 0))
        ship2 = Ship(2, (0, 0), 1)
        ship3 = Ship(2, (0, 0))
        field.update_field((0, 0), ship1)
        field.update_field((0, 1), ship2)
        field.update_field((1, 1), ship3)
        self.assertEqual(field.field, [[(ship1, False), (ship2, False), (ship2, False)],
                                       [(None, False), (ship3, False), (None, False)],
                                       [(None, False), (ship3, False), (None, False)]])


class shooting_tests(unittest.TestCase):
    def test_shoot_past(self):
        field = Field(1)
        self.assertEqual(field.shoot((0, 0)), 'past')

    def test_shoot_dead(self):
        field = Field(1)
        ship = Ship(1, (0, 0))
        ship.cell_location = (0, 0)
        field.update_field((0, 0), ship)
        self.assertEqual(field.shoot((0, 0)), 'dead')

    def test_shoot_injured(self):
        field = Field(2)
        ship = Ship(2, (0, 0), 1)
        ship.cell_location = (0, 0)
        field.update_field((0, 0), ship)
        self.assertEqual(field.shoot((0, 0)), 'injured')

    def test_shoot(self):
        field = Field(3)
        ship1 = Ship(1, (0, 0))
        ship2 = Ship(2, (0, 0), 1)
        ship3 = Ship(2, (0, 0))
        field.update_field((0, 0), ship1)
        ship1.cell_location = (0, 0)
        field.update_field((0, 1), ship2)
        ship2.cell_location = (0, 1)
        field.update_field((1, 1), ship3)
        ship3.cell_location = (1, 1)
        self.assertEqual(field.shoot((0, 0)), 'dead')
        self.assertEqual(field.shoot((0, 1)), 'injured')
        self.assertEqual(field.shoot((0, 2)), 'dead')
        self.assertEqual(field.shoot((1, 1)), 'injured')
        self.assertEqual(field.shoot((2, 1)), 'dead')


class clearing_tests(unittest.TestCase):
    def test_clear_cleared(self):
        field = Field(1)
        field.clear_field()
        self.assertEqual(field.field, [[(None, False)]])

    def test_clear_field(self):
        field = Field(3)
        ship1 = Ship(1, (0, 0))
        ship2 = Ship(2, (0, 0), 1)
        ship3 = Ship(2, (0, 0))
        field.update_field((0, 0), ship1)
        field.update_field((0, 1), ship2)
        field.update_field((1, 1), ship3)
        field.clear_field()
        self.assertEqual(field.field, [[(None, False), (None, False), (None, False)],
                                       [(None, False), (None, False), (None, False)],
                                       [(None, False), (None, False), (None, False)]])
