import unittest

from src.witnessproblem import Interval    
from parameterized import parameterized

class TestInterval(unittest.TestCase):


    def test_interval_initialization(self):
        # Act
        interval = Interval(1, 5)

        # Assert
        self.assertEqual(interval.a, 1)
        self.assertEqual(interval.b, 5)

    def test_interval_comparison(self):
        # Arrange
        interval1 = Interval(1, 5)
        interval2 = Interval(2, 6)

        # Act & Assert
        self.assertTrue(interval1 < interval2)

    @parameterized.expand([
        (1, 5, 6, 10, True),
        (1, 5, 2, 3, False),
        (1, 5, 5, 7, False),
    ])
    def test_are_intervals_disjoint(self, a1, b1, a2, b2, expected):
        # Arrange
        interval1 = Interval(a1, b1)
        interval2 = Interval(a2, b2)

        # Act & Assert
        self.assertEqual(interval1.are_intervals_disjoint(interval2), expected)