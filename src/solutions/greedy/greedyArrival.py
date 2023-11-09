from .greedyAlgorithms import GreedyAlgorithm
from .fcfs import firstComeFirstServed
from src.witnessproblem import Instance, Testimony, fitness

import random


NO_FIRST_VERTEX_PROVIDED = -1


class GreedyArrival(GreedyAlgorithm):

    def run(self, instance: Instance, src = NO_FIRST_VERTEX_PROVIDED):

        # Sorts testimonies from earlier to later arrival time
        testimonies: [Testimony] = instance.getTestimonyList()
        testimonies.sort(key = lambda tes : tes.a) 

        # If no initial vertex is provided, we find a random one that satisties the first testimony
        if src == NO_FIRST_VERTEX_PROVIDED :
            src = random.choice(testimonies[0].possibleVertices)

        return fitness(instance, firstComeFirstServed(instance.graph, testimonies, src))

    def __str__(self):
        return "GreedyArrival Algorithm"