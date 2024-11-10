import unittest
from unittest.mock import patch

from src.geneticOperators import initial_population, make_route_wait_in_last_vertex
from src.witnessproblem import Instance, Graph, Route


class TestInitialPopulation(unittest.TestCase):


    def setUp(self):
        self.instance = Instance(Graph(), [])
        self.size = 10

    
    @patch('src.geneticOperators.initialPopulation.appendRandomRoute')
    def test_initial_population(self, mock_appendRandomRoute):
        # Arrange
        population_size = 3

        # Act
        population = initial_population(self.instance, population_size)

        # Assert
        self.assertEqual(mock_appendRandomRoute.call_count, population_size)
        self.assertEqual(len(population), population_size)


        

    def test_make_route_wait_in_last_vertex(self):
        # Arrange
        route = Route()
        route.vertex = [1,2,3]
        route.time = [0,0,0]
        route.leaveTime = [0, 2, 4]
        instance = Instance(Graph(), [])
        instance.maxTime = 10

        # Act
        make_route_wait_in_last_vertex(route, instance)

        # Assert
        self.assertEqual(route.time, [0,0,6])
        self.assertEqual(route.leaveTime, [0,2,10])

