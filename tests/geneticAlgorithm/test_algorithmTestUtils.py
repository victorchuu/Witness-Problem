import unittest
from unittest.mock import Mock, patch

from src.geneticAlgorithm.algorithmDataGatherer import CSVDataGatherer, RealisticInstanceDataGatherer
from src.witnessproblem import Route
from src.geneticAlgorithm import GeneticAlgorithm
from src.geneticAlgorithm.algorithmTestUtils import transposeCSV, executeAlgorithms


class TestGeneticAlgorithm(unittest.TestCase):


    @patch('time.time')
    def test_executeAlgorithmsToCSV(self, time):
        # Arrange
        REPETITIONS = 3
        algorithm1 = GeneticAlgorithm()
        algorithm1.run = Mock()
        algorithm1.run.side_effect = [(1, ''), (2, ''), (3, ''), (1, ''), (2, ''), (3, '')]

        algorithm2 = GeneticAlgorithm()
        algorithm2.run = Mock()
        algorithm2.run.side_effect = [(4, ''), (5, ''), (6, ''), (4, ''), (5, ''), (6, '')]
        
        algorithms = [(algorithm1, REPETITIONS), (algorithm2, REPETITIONS)]

        time.side_effect = [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2]

        # Act
        executeAlgorithms(algorithms, 'I1', CSVDataGatherer, suffix='-unittest',  startIn=2, endIn=4)

        # Assert
        with open('solutions/I1-unittest.csv', 'r') as csv_file:
            csv_data = csv_file.read()

        expected_csv_data = 'I1,Mean #2,Max #2,Time #2,Mean #3,Max #3,Time #3\n' + \
            'nope,2.0,3,0.6666666666666666,2.0,3,0.6666666666666666\n' + \
            'nope,5.0,6,0.6666666666666666,5.0,6,0.6666666666666666\n'
        
        self.assertEqual(csv_data, expected_csv_data)

    @patch('time.time')
    def test_executeAlgorithmsRealCaseToCSV(self, time):
        # Arrange
        REPETITIONS = 3

        CORRECT_ROUTE = Route()
        CORRECT_ROUTE.vertex = [0]
        WRONT_ROUTE = Route()
        WRONT_ROUTE.vertex = [1]

        algorithm1 = GeneticAlgorithm()
        algorithm1.run = Mock()
        algorithm1.run.side_effect = [(1, CORRECT_ROUTE), (2, WRONT_ROUTE), (3, WRONT_ROUTE), 
                                      (1, CORRECT_ROUTE), (2, WRONT_ROUTE), (3, WRONT_ROUTE)]

        algorithm2 = GeneticAlgorithm()
        algorithm2.run = Mock()
        algorithm2.run.side_effect = [(4, CORRECT_ROUTE), (5, WRONT_ROUTE), (6, WRONT_ROUTE), 
                                      (6, CORRECT_ROUTE), (5, WRONT_ROUTE), (6, WRONT_ROUTE)]
        
        algorithms = [(algorithm1, REPETITIONS), (algorithm2, REPETITIONS)]

        time.side_effect = [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2]
        end_vertices = [0]
        dataGatherer = lambda a,b,c: RealisticInstanceDataGatherer(a,b,c,end_vertices)

        # Act
        executeAlgorithms(algorithms, 'realCase', dataGatherer, suffix='-unittest',  startIn=2, endIn=4)

        # Assert
        with open('solutions/realCase-unittest.csv', 'r') as csv_file:
            csv_data = csv_file.read()

        expected_csv_data = 'realCase,Mean (0.0; 2),Max (0.0; 2),Mean hits (0.0; 2),real fitness (0.0; 2),Time (0.0; 2),Mean (0.0; 3),Max (0.0; 3),Mean hits (0.0; 3),real fitness (0.0; 3),Time (0.0; 3)\n' + \
            'nope,2.0,3,1.0,23,0.6666666666666666,2.0,3,1.0,22,0.6666666666666666\n' + \
            'nope,5.0,6,1.0,23,0.6666666666666666,5.666666666666667,6,1.0,22,0.6666666666666666\n'
        
        self.assertEqual(csv_data, expected_csv_data)


