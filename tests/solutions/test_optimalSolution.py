import unittest

from src.solutions.optimal.optimalSolution import optimalSolution
from src.witnessproblem import Graph, Instance, Testimony, RandomInstanceGenerator

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
        with open('instances/tiny.txt') as inFile:
            instances: list[Instance] = Instance.schema().loads(inFile.readline(), many=True)
            [instance.graph.applyFloyd() for instance in instances]

        # Act
        results = [optimalSolution(instance)[0] for instance in instances]

        # Assert
        self.assertEqual(results, [10, 12, 15, 15, 13, 13, 9, 12, 13, 16])


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

def grid_graph_instance():
    graph = Graph()
    graph.createGridGraph(3, 1)
    instance = Instance(graph, get_grid_graph_testimonies())
    return instance


def grid_graph_instance_2():
    graph = Graph()
    graph.createGridGraph(3, 1)
    instance = Instance(graph, [[testimony] for witness in get_grid_graph_testimonies() for testimony in witness])
    return instance


def get_grid_graph_testimonies():
    return [
        [
            Testimony(possibleVertices=[3], a=0, b=2),
            Testimony(possibleVertices=[1, 7], a=3, b=4),
        ],
        [
            Testimony(possibleVertices=[2, 4], a=1, b=1),
        ],
        [
            Testimony(possibleVertices=[1, 3], a=2, b=3),
            Testimony(possibleVertices=[8], a=0, b=2),
        ],
        [
            Testimony(possibleVertices=[6, 7], a=1, b=4),
            Testimony(possibleVertices=[1, 4], a=0, b=1),
        ],
        [
            Testimony(possibleVertices=[2, 5], a=2, b=3),
        ],
        [
            Testimony(possibleVertices=[3, 8], a=1, b=4),
            Testimony(possibleVertices=[1, 5], a=0, b=2),
        ],
        [
            Testimony(possibleVertices=[3, 5], a=1, b=1),
            Testimony(possibleVertices=[7], a=2, b=4),
        ],
    ]

if __name__ == '__main__':
    unittest.main()