from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
from datetime import datetime


from .graph import Graph, CustomGraphField, custom_graph_serializer, custom_graph_deserializer
from .testimony import Testimony
from .fitness.fitnessPrecomputing import FitnessPrecomputation

LINE_BREAK = '\n'

    
@dataclass_json
@dataclass
class Instance :
    graph: Graph = field(
        metadata=config(
            encoder=custom_graph_serializer,
            decoder=custom_graph_deserializer,
            mm_field=CustomGraphField()
        )
    )
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
