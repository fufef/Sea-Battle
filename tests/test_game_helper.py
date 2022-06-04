import unittest

from PyQt5 import QtCore

from field import Field
from game import GameHelper


class get_cell_coords_tests(unittest.TestCase):
    def test_calculates_correctly_zero_cell(self):
        result = GameHelper.get_cell_coords(QtCore.QPointF(650, 175))
        self.assertEqual(result, (0, 0))

    def test_calculates_correctly_without_rounding(self):
        result = GameHelper.get_cell_coords(QtCore.QPointF(695, 220))
        self.assertEqual(result, (1, 1))

    def test_calculates_correctly_with_upper_rounding(self):
        result = GameHelper.get_cell_coords(QtCore.QPointF(730, 220))
        self.assertEqual(result, (1, 1))

    def test_calculates_correctly_with_lower_rounding(self):
        result = GameHelper.get_cell_coords(QtCore.QPointF(690, 220))
        self.assertEqual(result, (0, 1))


class choose_tests(unittest.TestCase):
    def test_choose_cells_4(self):
        field = Field(5)
        s = {(i, j): False for i in range(field.size) for j in range(field.size)}
        count = 0
        GameHelper.choose(field, s, 4)
        for i in s.keys():
            if s[i]:
                count += 1
        print(s)
        self.assertGreaterEqual(count, 4)

    def test_choose_cells_3(self):
        field = Field(5)
        s = {(i, j): False for i in range(field.size) for j in range(field.size)}
        count = 0
        GameHelper.choose(field, s, 3)
        for i in s.keys():
            if s[i]:
                count += 1
        print(s)
        self.assertGreaterEqual(count, 3)

    def test_choose_cells_2(self):
        field = Field(5)
        s = {(i, j): False for i in range(field.size) for j in range(field.size)}
        count = 0
        GameHelper.choose(field, s, 2)
        for i in s.keys():
            if s[i]:
                count += 1
        print(s)
        self.assertGreaterEqual(count, 2)

    def test_choose_cells_1(self):
        field = Field(5)
        s = {(i, j): False for i in range(field.size) for j in range(field.size)}
        count = 0
        GameHelper.choose(field, s, 1)
        for i in s.keys():
            if s[i]:
                count += 1
        print(s)
        self.assertGreaterEqual(count, 1)


class rnd_choose_tests(unittest.TestCase):
    def test_choose_cells_correct_x(self):
        s = {(i, j): False for i in range(5) for j in range(5)}
        cell = GameHelper.rnd_choose(s)
        self.assertTrue(0 <= cell[0][0] <= 4)

    def test_choose_cells_correct_y(self):
        s = {(i, j): False for i in range(5) for j in range(5)}
        cell = GameHelper.rnd_choose(s)
        self.assertTrue(0 <= cell[0][1] <= 4)

    def test_choose_cells_correct_status(self):
        s = {(i, j): False for i in range(5) for j in range(5)}
        cell = GameHelper.rnd_choose(s)
        self.assertTrue(0 <= cell[1] <= 1)


class check_pos_tests(unittest.TestCase):
    def test_returns_false_when_x(self):
        result = GameHelper.check_pos(QtCore.QPointF(700, 100))
        self.assertEqual(result, False)

    def test_returns_false_when_y(self):
        result = GameHelper.check_pos(QtCore.QPointF(200, 200))
        self.assertEqual(result, False)

    def test_returns_true_when_x_and_y(self):
        result = GameHelper.check_pos(QtCore.QPointF(700, 200))
        self.assertEqual(result, True)
