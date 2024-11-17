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
        self.assertIsInstance(instance.graph, Graph)
        self.assertEqual(instance.testimoniesByWitness, [])
        self.assertEqual(instance.maxTime, 0)
        self.assertIsInstance(instance.precompute, FitnessPrecomputation)
        self.assertEqual(instance.precompute.collidingTestimoniesSet.cache_info().hits, 0)



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


    # Execute this only if NOT using custom_graph_deserializer
    def test_transform_from_old_format_to_new(self):
        filename = 'realCase'
        # Arrange
        with open(f'instances/{filename}.txt') as inFile:
            serialized_instances = inFile.readline()
        
        # Act
        instances: list[Instance] = Instance.schema().loads(serialized_instances, many=True)
        re_serialized_instances = Instance.schema().dumps(instances, many=True)

        # Assert
        with open(f'instances/new-{filename}.txt', 'w') as outFile:
            outFile.write(re_serialized_instances)


    # Execute this only if using custom_graph_deserializer
    def test_new_format_deserialize(self):
        # Arrange
        with open('instances/new-I5.txt') as inFile:
            serialized_instances = inFile.readline()
        
        # Act
        instances: list[Instance] = Instance.schema().loads(serialized_instances, many=True)
        re_serialized_instances = Instance.schema().dumps(instances, many=True)

        # Assert
        self.assertEqual(serialized_instances, re_serialized_instances)


if __name__ == '__main__':
    unittest.main()