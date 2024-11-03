from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .graph import Graph
from .testimony import Testimony
from .fitness.fitnessPrecomputing import FitnessPrecomputation

LINE_BREAK = '\n'
    
@dataclass_json
@dataclass
class Instance :
    graph: Graph
    testimoniesByWitness: list[list[Testimony]]
    
    def __post_init__(self):
        if len(self.testimoniesByWitness) > 0:
            self.maxTime = max([ max([testimony.b for testimony in witness ]) for witness in self.testimoniesByWitness])
        else:
            self.maxTime = 0

        # Precomputed information for the fitness function 
        self.precompute = FitnessPrecomputation()
        self.precompute.collidingTestimoniesSet.cache_clear()
        self.precompute.start(self)


    def getTestimonyList(self) -> list[Testimony]:
        return [T for witn in self.testimoniesByWitness for T in witn]
