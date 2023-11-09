from src.witnessproblem import Instance, Graph, Route, Testimony, fitness
from .greedyAlgorithms import GreedyAlgorithm

import random

INFINITY = 1000000000
NO_FIRST_VERTEX_PROVIDED = -1

class GreedyDistance(GreedyAlgorithm):


    def __str__(self):
        return "GreedyDistance Algorithm"
    

    def run(self, instance: Instance, src = NO_FIRST_VERTEX_PROVIDED):

        # Note that the testimonies are in a hash set, thus they will be iterated in a arbitrary order. 
        # Consecutive executions of this algorithm, with the same inputs, may lead to different solutions.
        # If you want to make this algorithm determinist, an ordered set should be used instead.
        self.testimonies: {Testimony} = { T 
                        for witness in instance.testimoniesByWitness 
                        for T in witness
                        if not T.negative }
        self.graph: Graph = instance.graph

        if src == NO_FIRST_VERTEX_PROVIDED : 
            src = random.randint(0, instance.graph.V - 1)

        return fitness(instance, self.greedyDistance(src))
    

    def greedyDistance(self, src):

        R: Route = Route()
        R.startAt(src)
        time = 0

        while True :
            
            (closestTestimony, destiny, bestArrivalTime) = self.bestTestimonyFrom(time, src)

            if closestTestimony == None :
                break

            self.testimonies.remove(closestTestimony)
            self.graph.buildShortestRoute(src, destiny, bestArrivalTime - time, R)
            src = destiny
            time = bestArrivalTime
            
        return R


    def bestTestimonyFrom(self, time, src): 

        (closestTestimony, destiny, bestArrivalTime) = (None, -1, INFINITY)
        unreachable: [Testimony] = list()

        for T in self.testimonies :

            (vert, dist) = self.graph.closestVertex(src, T.possibleVertices)

            arrival_time = max(time + dist, T.a)
            if arrival_time > T.b :
                unreachable.append(T)
            elif arrival_time < bestArrivalTime: 
                (closestTestimony, destiny, bestArrivalTime) = (T, vert, arrival_time)

        for T in unreachable:
            self.testimonies.remove(T)

        return (closestTestimony, destiny, bestArrivalTime)