from src.Algorithm import Algorithm
from .greedyAlgorithms import GreedyAlgorithm
from src.witnessproblem import Instance


class PersistentGreedyAlgorithm(Algorithm):
    

    def __init__(self, greedyAlgorithm: GreedyAlgorithm):
        self.greedyAlgorithm = greedyAlgorithm


    def run(self, instance: Instance):
        return max(
            [self.greedyAlgorithm.run(instance, src = v)
                for v in range(instance.graph.V)]
        )


    def __str__(self):
        return f"Persistent {str(self.greedyAlgorithm)}"
    