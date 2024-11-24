import unittest
from src.geneticOperators import localSearch
from src.witnessproblem import Route, fitness
from tests.testdata.testInstances import grid_graph_instance, grid_graph_instance_2

class LocalSearchTests(unittest.TestCase):

    def test_localSearch_on_grid_graph(self):
        # Arrange
        instance = grid_graph_instance()
        route = Route(vertex=[3, 6, 7, 8, 7], time=[0, 0, 0, 0, 0], leaveTime=[0, 1, 2, 3, 4])
        fit_value = fitness(instance, route)

        # Act
        new_route, new_fit_value = localSearch(instance, route, fit_value)

        # Assert
        self.assertEqual(fit_value, 1)
        self.assertEqual(new_fit_value, 5)
        self.assertEqual(new_route.vertex, [3, 4, 5, 8, 7])


    def test_localSearch_on_grid_graph_2(self):
        # Arrange
        instance = grid_graph_instance_2()
        route = Route(vertex=[5, 6, 7, 8, 7], time=[0, 0, 0, 0, 0], leaveTime=[0, 1, 2, 3, 4])
        fit_value = fitness(instance, route)

        # Act
        new_route, new_fit_value = localSearch(instance, route, fit_value)

        # Assert
        self.assertEqual(fit_value, 5)
        self.assertEqual(new_fit_value, 8)
        self.assertEqual(new_route.vertex, [5, 4, 5, 8, 7])


if __name__ == '__main__':
    unittest.main()
