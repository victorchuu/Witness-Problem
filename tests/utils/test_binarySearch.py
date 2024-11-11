import unittest
from src.utils.binarySearch import lastTrueIndexBinarySearch, firstFalseIndexBinarySerch

class TestBinarySearch(unittest.TestCase):

    def test_last_true_index_binary_search(self):
        # Arrange
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.comparisons_counter = 0
        def comparison(i):
            self.comparisons_counter += 1
            return array[i] < 7

        # Act
        result = lastTrueIndexBinarySearch(0, len(array) - 1, comparison)

        # Assert
        self.assertEqual(result, 5)
        self.assertEqual(self.comparisons_counter, 3)


    def test_last_true_index_binary_search_with_lambda_operation(self):
        # Arrange
        array = [1, -2, 3, -4, 5, -6, 7, -8, 9, -10]
        self.comparisons_counter = 0
        def comparison(i):
            self.comparisons_counter += 1
            return array[i]**2 < 50

        # Act
        result = lastTrueIndexBinarySearch(0, len(array) - 1, comparison)

        # Assert
        self.assertEqual(result, 6) # 7**2 = 49 < 50
        self.assertEqual(self.comparisons_counter, 3)


    def test_last_true_index_binary_search(self):
        # Arrange
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.comparisons_counter = 0
        def comparison(i):
            self.comparisons_counter += 1
            return array[i] < 5

        # Act
        result = firstFalseIndexBinarySerch(0, len(array) - 1, comparison)

        # Assert
        self.assertEqual(result, 4)
        self.assertEqual(self.comparisons_counter, 3)


if __name__ == '__main__':
    unittest.main()