from src.Algorithm import Algorithm
from .greedyAlgorithms import GreedyAlgorithm
from src.witnessproblem import Instance, Route


class PersistentGreedyAlgorithm(Algorithm):
    

    def __init__(self, greedyAlgorithm: GreedyAlgorithm):
        self.greedyAlgorithm = greedyAlgorithm


    def run(self, instance: Instance, override_initial_pop=None):
        results = [self.greedyAlgorithm.run(instance, src = v) for v in range(instance.graph.V)]
        maximum = -1
        best_route = Route()

        for (fitness_result, route) in results:
            if fitness_result > maximum:
                maximum = fitness_result
                best_route = route

        return maximum, best_route


    def __str__(self):
        return f"Persistent {str(self.greedyAlgorithm)}"
    