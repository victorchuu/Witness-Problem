from .greedyAlgorithms import GreedyAlgorithm

from src.witnessproblem import Instance, Graph, Route, Testimony, fitness

import random


INFINITY = 1000000000
NO_FIRST_VERTEX_PROVIDED = -1


class GreedyTestimonies(GreedyAlgorithm):


    def __init__(self, first_vertex = NO_FIRST_VERTEX_PROVIDED):
        self.first_vertex = first_vertex


    def run(self, instance: Instance, src = NO_FIRST_VERTEX_PROVIDED, override_initial_pop=None):

        # Note that the testimonies are in a hash set, thus they will be iterated in a arbitrary order. 
        # Consecutive executions of this algorithm, with the same inputs, may lead to different solutions.
        # If you wish to make this algorithm determinist, an ordered set should be used instead.
        self.testimonies: {Testimony} = { T 
                        for witness in instance.testimoniesByWitness 
                        for T in witness
                        if not T.negative } # Greedy algorithm only works with positive testimonies
        self.graph: Graph = instance.graph

        if src == NO_FIRST_VERTEX_PROVIDED:
            src = self.first_vertex
        if src == NO_FIRST_VERTEX_PROVIDED : 
            src = random.randint(0, instance.graph.V - 1)

        best_route_found = self.greedyTestimonies(src)

        return fitness(instance, best_route_found), best_route_found
    

    def __str__(self):
        return "GreedyTestimonies Algorithm"
    

    def greedyTestimonies(self, src):
        time = 0
        R: Route = Route()
        R.startAt(src)

        while True :
            
            (bestTestimony, bestVertex, arrivalTime) = self.bestTestimonyFrom(time, src)

            if bestTestimony == None:
                break

            self.graph.buildShortestRoute(src, bestVertex, arrivalTime - time, R)
            (time, src) = (arrivalTime, bestVertex)
            self.testimonies.remove(bestTestimony)

        return R
    
    def bestTestimonyFrom(self, time, src):
        unreachable = list()
        maxReachableTestimonies = 0
        (bestTestimony, bestVertex, bestArrivalTime) = (None, None, INFINITY)

        for T in self.testimonies :         # Among all testimonies and their reachable vertices
            isReachable = False             # We find the one that maximizes 'numberOfReachableTestimonies'
            for vert in T.possibleVertices :
                
                arrivaltime = max(T.a, time + self.graph.bestDist(src,vert))
                if arrivaltime <= T.b : 
                    isReachable = True

                    numOfReachables = self.numberOfReachableTestimonies(vert, arrivaltime)

                    if numOfReachables > maxReachableTestimonies or (numOfReachables == maxReachableTestimonies and arrivaltime < bestArrivalTime):
                        maxReachableTestimonies = numOfReachables
                        (bestTestimony, bestVertex, bestArrivalTime) = (T, vert, arrivaltime)

            if not isReachable:
                unreachable.append(T)

        for T in unreachable:
                self.testimonies.remove(T)

        return (bestTestimony, bestVertex, bestArrivalTime)


    def numberOfReachableTestimonies(self, vert, time) :
        count = 0
        for T in self.testimonies :
            for v in T.possibleVertices :
                if time + self.graph.bestDist(vert, v) <= T.b :
                    count += 1
                    break
        return count 