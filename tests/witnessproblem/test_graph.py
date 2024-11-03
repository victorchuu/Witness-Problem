import unittest

from src.witnessproblem import Graph, Edge

class TestGraph(unittest.TestCase):


    def test_graph_initialization(self):
        # Act
        graph = Graph()

        # Assert
        self.assertEqual(graph.V, 0)
        self.assertEqual(graph.E, 0)
        self.assertEqual(graph.adjList, [[Edge]])
        self.assertEqual(graph.realDist, [[int]])
        self.assertEqual(graph.bestDistanceMatrix, [[int]])
        self.assertEqual(graph.floydPath, [[int]])


    def test_graph_create_grid_graph(self):
        # Act        
        graph = test_grid_graph()

        # Assert
        self.assertEqual(graph.V, 9)
        self.assertEqual(graph.E, 24)
        self.assertEqual(len(graph.adjList), 9)

        # Assert all distances are 1
        self.assertTrue(all([edge.distance == 1 for edges in graph.adjList for edge in edges]))

        print(graph.to_json())


    def test_floyd_algorithm_in_grid_graph(self):
        # Act
        graph = test_grid_graph()

        # Assert
        expected_distance_matrix = [
            [0, 1, 2, 1, 2, 3, 2, 3, 4],
            [1, 0, 1, 2, 1, 2, 3, 2, 3],
            [2, 1, 0, 3, 2, 1, 4, 3, 2],
            [1, 2, 3, 0, 1, 2, 1, 2, 3],
            [2, 1, 2, 1, 0, 1, 2, 1, 2],
            [3, 2, 1, 2, 1, 0, 3, 2, 1],
            [2, 3, 4, 1, 2, 3, 0, 1, 2],
            [3, 2, 3, 2, 1, 2, 1, 0, 1],
            [4, 3, 2, 3, 2, 1, 2, 1, 0]
        ]
        self.assertEqual(graph.bestDistanceMatrix, expected_distance_matrix)


    def test_direct_dist(self):
        # Arrange
        graph = test_grid_graph()

        # Act
        dist = graph.directDist(0, 1)

        # Assert
        self.assertEqual(dist, 1)


    def test_directDist_throws_exception_when_vertices_are_not_connected(self):
        # Arrange
        graph = test_grid_graph()

        # Act
        with self.assertRaises(Exception):
            graph.directDist(0, 2)


    def test_closest_vertex(self):
        # Arrange
        graph = test_grid_graph()

        # Act
        closest_vertex, distance = graph.closestVertex(0, [1, 3, 4, 6])

        # Assert
        self.assertEqual(closest_vertex, 1)
        self.assertEqual(distance, 1)

def test_grid_graph():
    graph = Graph()
    graph.createGridGraph(3, 1)
    return graph


if __name__ == '__main__':
    unittest.main()