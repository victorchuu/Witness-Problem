import unittest
from unittest.mock import patch

from src.geneticOperators import crossover
from src.witnessproblem import Graph, Instance, Route

class TestCrossover(unittest.TestCase):


    def setUp(self):
        graph = Graph()
        graph.createGridGraph(3,1)
        self.instance = Instance(graph, [])


    def test_crossover(self):
        # Arrange
        self.instance.maxTime = 3
        route1 = Route(vertex=[3,4,5], time=[0,0,0], leaveTime=[0,1,2])
        route2 = Route(vertex=[1,4,7], time=[0,0,0], leaveTime=[0,1,2])

        # Act
        child1, child2 = crossover(self.instance, route1, route2)

        self.assertEqual(child1, Route(vertex=[3, 4, 7], time=[0, 0, 0], leaveTime=[0, 1, 2]))
        self.assertEqual(child2, Route(vertex=[1, 4, 5], time=[0, 0, 0], leaveTime=[0, 1, 2]))


    @patch('random.randint', return_value=1)
    def test_crossover_2(self, mock_randint):
        # Arrange
        self.instance.maxTime = 10
        route1 = Route(vertex=[6, 7, 8, 5, 2], time=[0, 0, 1, 0, 5], leaveTime=[0, 1, 3, 4, 10])
        route2 = Route(vertex=[5, 4, 1, 2, 5, 2, 5, 8, 7], time=[0, 2, 0, 0, 0, 0, 0, 0, 0], leaveTime=[0, 3, 4, 5, 6, 7, 8, 9, 10])

        # Act
        child1, child2 = crossover(self.instance, route1, route2)

        # Assert
        self.assertEqual(child1, Route(vertex=[6, 7, 4, 1, 2, 5, 2, 5, 8, 7], time=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], leaveTime=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10]))
        self.assertEqual(child2, Route(vertex=[5, 4, 5, 2], time=[0, 2, 0, 5], leaveTime=[0, 3, 4, 10]))



if __name__ == '__main__':
    unittest.main()