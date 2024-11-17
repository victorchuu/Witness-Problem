import unittest
from unittest.mock import call, patch

from src.realisticCase.realisticCaseInstanceGenerator import RealisticCaseInstanceGenerator
from src.witnessproblem import Graph, Route

INSTANCE_TIME = 8

class TestRealisticCaseInstanceGenerator(unittest.TestCase):

    def setUp(self):
        self.systemUnderTest = RealisticCaseInstanceGenerator()

    
    @patch("random.randint", side_effect=[INSTANCE_TIME])
    def test_case1(self, mock_randint):
        # Arrange
        graph = Graph()
        graph.createGridGraph(3, 1)
        init_vertex = 0
        end_vertex = 8

        # Act
        route = self.systemUnderTest.generate_actor_route(graph, init_vertex, end_vertex)

        # Assert
        self.assertEqual(route.vertex[0], init_vertex)
        self.assertEqual(route.vertex[-1], end_vertex)
        self.assertEqual(route.leaveTime[-1], INSTANCE_TIME)



    @patch("src.realisticCase.realisticCaseInstanceGenerator.generateIntervalTestimonies")
    @patch("src.realisticCase.realisticCaseInstanceGenerator.generateNegativeTestimonies")
    def test_generateTestimonies(self, mock_generateNegativeTestimonies, mock_generateIntervalTestimonies):
        # Arrange
        mock_generateIntervalTestimonies.side_effect=[
            ["Testimony 1", "Testimony 2"],
            ["Noise 1"], 
            ["Noise 2"]
        ]
        mock_generateNegativeTestimonies.return_value = ["Negative 1", "Negative 2"]
        self.systemUnderTest.maxTime = INSTANCE_TIME
        actor_route = Route(vertex=[0])
        route1 = Route(vertex=[1])
        route2 = Route(vertex=[2])
        moving_individuals = [(route1, 0.05), (route2, 0.1)]
        vertex = 2

        # Act
        testimonies = self.systemUnderTest.generateTestimonies(actor_route, moving_individuals, vertex)

        # Assert
        self.assertEqual(testimonies, ['Testimony 1', 'Testimony 2', 'Noise 1', 'Noise 2', 'Negative 1', 'Negative 2'])
        self.assertEqual(mock_generateIntervalTestimonies.call_count, 3)
        mock_generateIntervalTestimonies.assert_has_calls([
            call(actor_route, vertex, 0, 8, probability=0.95),
            call(route1, vertex, 0, 8, probability=0.05),
            call(route2, vertex, 0, 8, probability=0.1),
        ])
        mock_generateNegativeTestimonies.assert_called_once_with(['Testimony 1', 'Testimony 2', 'Noise 1', 'Noise 2'], vertex, 0, 8)
        
    
if __name__ == '__main__':
    unittest.main()