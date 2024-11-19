import unittest
from unittest.mock import patch, Mock
from src.witnessproblem import Graph, Instance, Route, Testimony, fitness


TES_1 = 0
TES_2 = 1
TES_3 = 2
POSITIVE = Testimony([0],0,0)
NEGATIVE = Testimony([0],0,0,negative=True)

class FitnessTestCase(unittest.TestCase):


    def test_fitness_2_testimonies_route_only_visits_one(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE],
            [POSITIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [1,1]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0)},
            {(TES_2,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 1)



    def test_fitness_2_testimonies_route_visits_both(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE],
            [POSITIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [1,1]
        route = Route(vertex=[0,0], time=[0,0], leaveTime=[0,1])
        colliding_testimonies = [
            {(TES_1,0)},
            {(TES_2,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 2)

    def test_fitness_2_negative_testimonies_route_visits_one(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [NEGATIVE],
            [NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [0,0]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 1)


    def test_fitness_2_negative_testimonies_route_visits_both(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [NEGATIVE],
            [NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [0,0]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0),(TES_2,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 0)

    
    def test_fitness_1_witness_with_2_testimonies_route_visits_both(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE, POSITIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [2]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0), (TES_1,1)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 1)

    def test_fitness_1_witness_with_2_testimonies_route_visits_one(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE, POSITIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [2]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 0)


    def test_fitness_1_witness_with_2_testimonies_one_negative_route_visits_both(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE, NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [1]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0), (TES_1,1)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 0)


    def test_fitness_1_witness_with_2_negative_testimonies_route_visits_one(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [NEGATIVE, NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [0]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 0)

    
    def test_fitness_1_witness_with_2_testimonies_one_negative_route_visits_positive(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE, NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [1]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,0)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 1)

    
    def test_fitness_1_witness_with_2_testimonies_one_negative_route_visits_negative(self):
        # Arrange
        instance = Instance(Graph(), [])
        instance.testimoniesByWitness = [
            [POSITIVE, NEGATIVE],
        ]
        instance.precompute.positiveTestimoniesByWitness = [1]
        route = Route(vertex=[0], time=[0], leaveTime=[0])
        colliding_testimonies = [
            {(TES_1,1)},
        ]
        instance.precompute.collidingTestimoniesSet = Mock(side_effect=colliding_testimonies)

        # Act
        result = fitness(instance, route)

        # Assert
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()