import unittest
from unittest.mock import patch

from src.geneticOperators import initial_population
from src.geneticOperators.mutation import mutate
from src.witnessproblem import Graph, Instance, Route

class TestMutation(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.createGridGraph(3, 1)
        self.instance = Instance(self.graph, [])
        self.instance.maxTime = 5


    @patch('src.geneticOperators.mutation.appendRandomRoute')
    def test_mutate_creates_new_route_when_input_length_is_smaller_than_two(self, mock_appendRandomRoute):
        # Arrange
        graph = Graph()
        instance = Instance(graph, [])
        instance.maxTime = 10
        route = Route()

        # Act
        mutate(instance, route)

        # Assert
        mock_appendRandomRoute.assert_called_once_with(graph, -1, instance.maxTime, route)


    @patch('random.randint', side_effect = [1, 2])
    @patch('src.geneticOperators.mutation.appendRandomRoute')
    def test_mutate_single_vertex_route(self, mock_appendRandomRoute, mock_randint):
        # Arrange
        route = Route(vertex=[0,1,2,5,8], time=[0,0,0,0,0], leaveTime=[0,1,2,3,4])

        mock_appendRandomRoute.return_value = Route(vertex=[0,1,4,5], time=[0,0,0,0], leaveTime=[0,1,2,3])

        # Act
        mutate_route = mutate(self.instance, route)

        # Assert
        mid_route = Route(vertex=[0,1], time=[0,0], leaveTime=[0,1])
        mock_appendRandomRoute.assert_called_once_with(self.graph, 5, 2, mid_route)

        self.assertEqual(mutate_route, Route(vertex=[0, 1, 4, 5, 8], time=[0, 0, 0, 0, 0], leaveTime=[0, 1, 2, 3, 4]))
    

if __name__ == '__main__':
    unittest.main()