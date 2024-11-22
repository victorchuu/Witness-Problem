import unittest
import rustworkx as rx

from src.witnessproblem.fitness.fitnessPrecomputing import FitnessPrecomputation, TestimonyEvent
from src.witnessproblem import Graph, Instance, Testimony

V1 = 0
V2 = 1
V3 = 2
digraph = rx.PyDiGraph()
digraph.add_nodes_from(range(3))
GRAPH = Graph(digraph=digraph)
TES1 = (0,0)
TES2 = (1,0)

COLLIDING_INTERVALS_INSTANCE = Instance(GRAPH, [
    [Testimony([V1], 2, 7)],
    [Testimony([V1, V2], 4, 8, negative=True)],
])

CONTAINED_INTERVALS_INSTANCE = Instance(GRAPH, [
    [Testimony([V1], 2, 7)],
    [Testimony([V1, V2], 3, 6, negative=True)],
])

DISJOINT_INTERVALS_INSTANCE = Instance(GRAPH, [
    [Testimony([V1], 2, 4)],
    [Testimony([V1, V2], 8, 10, negative=True)],
])

class TestTestimonyEvent(unittest.TestCase):

    def test_fitnessPrecomputation_for_colliding_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(COLLIDING_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.eventsByVertex[V1], [
            TestimonyEvent(2, True, 0, 0, openIntervalsSet=set()),
            TestimonyEvent(4, True, 1, 0, openIntervalsSet={TES1}),
            TestimonyEvent(7, False, 0, 0, openIntervalsSet={TES1,TES2}),
            TestimonyEvent(8, False, 1, 0, openIntervalsSet={TES2}),
        ])
        self.assertEqual(precompute.eventsByVertex[V2], [
            TestimonyEvent(4, True, 1, 0, openIntervalsSet=set()),
            TestimonyEvent(8, False, 1, 0, openIntervalsSet={TES2}),
        ])
        self.assertEqual(precompute.eventsByVertex[V3], [])
        self.assertEqual(precompute.positiveTestimoniesByWitness, [1,0])


    def test_fitnessPrecomputation_for_contained_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(CONTAINED_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.eventsByVertex[V1], [
            TestimonyEvent(2, True, 0, 0, openIntervalsSet=set()),
            TestimonyEvent(3, True, 1, 0, openIntervalsSet={TES1}),
            TestimonyEvent(6, False, 1, 0, openIntervalsSet={TES1,TES2}),
            TestimonyEvent(7, False, 0, 0, openIntervalsSet={TES1}),
        ])
        self.assertEqual(precompute.eventsByVertex[V2], [
            TestimonyEvent(3, True, 1, 0, openIntervalsSet=set()),
            TestimonyEvent(6, False, 1, 0, openIntervalsSet={TES2}),
        ])
        self.assertEqual(precompute.eventsByVertex[V3], [])
        self.assertEqual(precompute.positiveTestimoniesByWitness, [1,0])


    def test_fitnessPrecomputation_for_disjoint_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(DISJOINT_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.eventsByVertex[V1], [
            TestimonyEvent(2, True, 0, 0, openIntervalsSet=set()),
            TestimonyEvent(4, False, 0, 0, openIntervalsSet={TES1}),
            TestimonyEvent(8, True, 1, 0, openIntervalsSet=set()),
            TestimonyEvent(10, False, 1, 0, openIntervalsSet={TES2}),
        ])
        self.assertEqual(precompute.eventsByVertex[V2], [
            TestimonyEvent(8, True, 1, 0, openIntervalsSet=set()),
            TestimonyEvent(10, False, 1, 0, openIntervalsSet={TES2}),
        ])
        self.assertEqual(precompute.eventsByVertex[V3], [])
        self.assertEqual(precompute.positiveTestimoniesByWitness, [1,0])


    def test_collidingTestimoniesSet_for_colliding_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(COLLIDING_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 0, 0), set())
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 2, 2), {TES1})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 4, 4), {TES1,TES2})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 7, 7), {TES1,TES2})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 8, 8), {TES2})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 9, 9), set())


    def test_collidingTestimoniesSet_for_contained_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(CONTAINED_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 0, 0), set())
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 2, 2), {TES1})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 3, 3), {TES1,TES2})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 7, 7), {TES1})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 9, 9), set())
        

    def test_collidingTestimoniesSet_for_disjoint_intervals(self):
        # Arrange
        precompute = FitnessPrecomputation()

        # Act
        precompute.start(DISJOINT_INTERVALS_INSTANCE)

        # Assert
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 0, 0), set())
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 2, 2), {TES1})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 5, 5), set())
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 8, 8), {TES2})
        self.assertEqual(precompute.collidingTestimoniesSet(V1, 11, 11), set())

        self.assertEqual(precompute.collidingTestimoniesSet(V1, 1, 9), {TES1,TES2})


    


if __name__ == '__main__':
    unittest.main()