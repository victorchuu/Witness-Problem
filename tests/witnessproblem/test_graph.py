import rustworkx as rx
import unittest

from src.witnessproblem import Graph, Edge

class TestGraph(unittest.TestCase):


    def test_graph_initialization(self):
        # Act
        graph = Graph()

        # Assert
        self.assertEqual(graph.V, 0)
        self.assertEqual(graph.E, 0)


    def test_graph_create_grid_graph(self):
        # Act        
        graph = test_grid_graph()

        # Assert
        self.assertEqual(graph.V, 9)
        self.assertEqual(graph.E, 24)

        self.assertTrue(all([graph.digraph.get_edge_data(edge[0],edge[1]) == 1 for edge in graph.digraph.edge_list()]))


    def test_get_adjacents(self):
        # Arrange        
        graph = test_grid_graph()

        # Act        
        adjacents = graph.get_adjacents(4)

        # Assert
        self.assertEqual(len(adjacents), 4)
        self.assertCountEqual(adjacents, [
            Edge(1, 1),
            Edge(3, 1),
            Edge(5, 1),
            Edge(7, 1)
        ])


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

        self.assertEquals(graph.bestDistanceMatrix, expected_distance_matrix)


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