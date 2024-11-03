import unittest
from src.witnessproblem import Edge

class TestEdge(unittest.TestCase):
    

    def test_edge_initialization(self):
        # Act
        edge = Edge(1, 10)

        # Assert
        self.assertEqual(edge.vertex, 1)
        self.assertEqual(edge.distance, 10)

    def test_edge_default_initialization(self):
        # Act
        edge = Edge()

        # Assert
        self.assertEqual(edge.vertex, -1)
        self.assertEqual(edge.distance, -1)

    def test_edge_comparison(self):
        # Arrange
        edge1 = Edge(1, 10)
        edge2 = Edge(2, 20)

        # Act & Assert
        self.assertTrue(edge2 > edge1)

    def test_serialising(self):
        # Arrange
        edge = Edge(1, 10)

        # Act& Assert
        self.assertEqual(edge.to_json(), '{"vertex": 1, "distance": 10}')

    def test_deserialising(self):
        # Act
        edge = Edge.from_json('{"vertex": 1, "distance": 10}')

        # Act& Assert
        self.assertEqual(edge, Edge(1, 10))