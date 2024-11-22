import unittest

from src.solutions.optimal.optimalSolution import optimalSolution
from src.witnessproblem import Instance, RandomInstanceGenerator, Route, fitness
from tests.testdata.testInstances import grid_graph_instance, grid_graph_instance_2, get_tiny_instances

class TestOptimalSolution(unittest.TestCase):

    def test_optimal_solution_on_grid_graph(self):
        # Arrange
        instance = grid_graph_instance()

        # Act
        result, route = optimalSolution(instance)

        # Assert
        self.assertEqual(result, 5)


    def test_optimal_solution_on_grid_graph_2(self):
        # Arrange
        instance = grid_graph_instance_2()

        # Act
        result, route = optimalSolution(instance)

        # Assert
        self.assertEqual(result, 9)

    def test_on_randomly_generated_instances(self):
        # Arrange
        instances: list[Instance] = get_tiny_instances()

        # Act
        results = [optimalSolution(instance) for instance in instances]

        # Assert
        solutions = [pair[0] for pair in results]
        self.assertEqual(solutions, [10, 12, 15, 15, 13, 13, 9, 12, 13, 16])


TINY_INSTANCES = RandomInstanceGenerator(
    vertices = 10,
    avg_vertex_degree = 3, 
    max_vertex_distance = 5, 
    witnesses = 50, 
    max_testimonies_per_witness = 5, 
    max_time_window = 6, 
    max_interval_length = 3, 
    max_vertices_per_testimony = 3, 
    negative_testimonies_rate = 0.3
)

if __name__ == '__main__':
    unittest.main()