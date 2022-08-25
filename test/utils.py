import unittest

from lib import utils


class TestUtils(unittest.TestCase):
    def test_cycle00(self):
        actual = utils.cycle(['A', 'B'], [0, 1])
        expected = ['B', 'A']
        self.assertEqual(expected, actual)


    def test_cycle01(self):
        actual = utils.cycle(['A', 'B', 'C', 'D', 'E', 'F'], [1, 2, 5])
        expected = ['A', 'F', 'B', 'D', 'E', 'C']
        self.assertEqual(expected, actual)


    def test_flatten00(self):
        actual = utils.flatten([[1, 2], [3, 4, 5], []])
        expected = [1, 2, 3, 4, 5]
        actual = expected
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
