import unittest
from src.witnessproblem.testimony import Testimony

class TestTestimony(unittest.TestCase):

    def test_init(self):
        vertices = [1, 2, 3]
        a = 4
        b = 5
        negative = True
        testimony = Testimony(vertices, a, b, negative)
        self.assertEqual(testimony.possibleVertices, vertices)
        self.assertEqual(testimony.a, a)
        self.assertEqual(testimony.b, b)
        self.assertEqual(testimony.negative, negative)


    def test_lt(self):
        # Arrange
        testimony1 = Testimony(vertices=[1, 2, 3], a=4, b=5, negative=True)
        testimony2 = Testimony(vertices=[1, 2, 3], a=5, b=6, negative=False)

        # Act & Assert
        self.assertLess(testimony1, testimony2)

if __name__ == '__main__':
    unittest.main()