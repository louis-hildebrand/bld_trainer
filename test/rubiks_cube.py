import unittest

from lib.rubiks_cube import Color as C, Move, RubiksCube
from lib.utils import flatten


class TestRubiksCube(unittest.TestCase):
    def test_apply_R(self):
        actual = RubiksCube().apply([Move.R])
        expected = RubiksCube(
            [C.WHITE, C.GREEN, C.RED, C.BLUE, C.ORANGE, C.YELLOW],
            [
                C.WHITE, C.GREEN, C.GREEN, C.WHITE,
                C.GREEN, C.YELLOW, C.YELLOW, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.WHITE, C.BLUE, C.BLUE, C.WHITE,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.BLUE, C.BLUE, C.YELLOW
            ],
            [
                C.WHITE, C.GREEN, C.WHITE, C.WHITE,
                C.GREEN, C.YELLOW, C.GREEN, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.BLUE, C.BLUE, C.BLUE, C.WHITE,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.BLUE, C.YELLOW, C.YELLOW
            ]
        )
        self.assertEqual(expected, actual)


    def test_apply_R_prime(self):
        actual = RubiksCube().apply([Move.R_PRIME])
        expected = RubiksCube(
            [C.WHITE, C.GREEN, C.RED, C.BLUE, C.ORANGE, C.YELLOW],
            [
                C.WHITE, C.BLUE, C.BLUE, C.WHITE,
                C.GREEN, C.WHITE, C.WHITE, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.YELLOW, C.BLUE, C.BLUE, C.YELLOW,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.GREEN, C.GREEN, C.YELLOW
            ],
            [
                C.WHITE, C.BLUE, C.WHITE, C.WHITE,
                C.GREEN, C.WHITE, C.GREEN, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.BLUE, C.BLUE, C.BLUE, C.YELLOW,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.GREEN, C.YELLOW, C.YELLOW
            ]
        )
        self.assertEqual(expected, actual)


    def test_apply_R2(self):
        actual = RubiksCube().apply([Move.R2])
        expected = RubiksCube(
            [C.WHITE, C.GREEN, C.RED, C.BLUE, C.ORANGE, C.YELLOW],
            [
                C.WHITE, C.YELLOW, C.YELLOW, C.WHITE,
                C.GREEN, C.BLUE, C.BLUE, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.GREEN, C.BLUE, C.BLUE, C.GREEN,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.WHITE, C.WHITE, C.YELLOW
            ],
            [
                C.WHITE, C.YELLOW, C.WHITE, C.WHITE,
                C.GREEN, C.BLUE, C.GREEN, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.BLUE, C.BLUE, C.BLUE, C.GREEN,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.YELLOW, C.WHITE, C.YELLOW, C.YELLOW
            ]
        )
        self.assertEqual(expected, actual)


    def test_apply_M2(self):
        actual = RubiksCube().apply([Move.M2])
        expected = RubiksCube(
            centers = [C.YELLOW, C.BLUE, C.RED, C.GREEN, C.ORANGE, C.WHITE],
            edges = [
                C.YELLOW, C.WHITE, C.YELLOW, C.WHITE,
                C.BLUE, C.GREEN, C.BLUE, C.GREEN,
                C.RED, C.RED, C.RED, C.RED,
                C.GREEN, C.BLUE, C.GREEN, C.BLUE,
                C.ORANGE, C.ORANGE, C.ORANGE, C.ORANGE,
                C.WHITE, C.YELLOW, C.WHITE, C.YELLOW
            ]
        )
        self.assertEqual(expected, actual)

    def test_apply_Z2(self):
        actual = RubiksCube().apply([Move.Z2])
        centers = [C.YELLOW, C.GREEN, C.ORANGE, C.BLUE, C.RED, C.WHITE]
        expected = RubiksCube(
            centers,
            flatten([[c] * 4 for c in centers]),
            flatten([[c] * 4 for c in centers])
        )
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
