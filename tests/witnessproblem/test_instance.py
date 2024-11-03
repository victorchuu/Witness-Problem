import unittest


from src.witnessproblem import Instance
from src.witnessproblem import Graph
from src.witnessproblem import Testimony
from src.witnessproblem.fitness.fitnessPrecomputing import FitnessPrecomputation


class TestInstance(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.testimoniesByWitness = []

    def test_initialization(self):
        # Act
        instance = Instance(self.graph, self.testimoniesByWitness)

        # Assert
        self.assertIsInstance(self.instance.graph, Graph)
        self.assertEqual(self.instance.testimoniesByWitness, [])
        self.assertEqual(self.instance.maxTime, 0)
        self.assertIsInstance(self.instance.precompute, FitnessPrecomputation)
        self.assertEqual(self.instance.precompute.collidingTestimoniesSet.cache_info().hits, 0)



    def test_get_testimony_list(self):
        # Arrange
        testimony1 = Testimony(a=1,b=1,possibleVertices=[])    
        testimony2 = Testimony(a=2,b=2,possibleVertices=[])
        testimony3 = Testimony(a=3,b=3,possibleVertices=[])
        instance = Instance(self.graph, [[testimony1, testimony2], [testimony3]])


        # Act
        testimonies = instance.getTestimonyList()

        # Assert
        self.assertEqual(testimonies, [testimony1, testimony2, testimony3])


if __name__ == '__main__':
    unittest.main()