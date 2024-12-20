import random
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from src.witnessproblem import Route, RouteIterator


@dataclass_json
@dataclass
class Testimony :
    possibleVertices: list[int]
    a: int
    b: int
    negative: bool = field(default=False)

        
    def __post_init__(self) :
        if self.possibleVertices is None:
            self.possibleVertices = []
        if self.a is None:
            self.a = 0
        if self.b is None:
            self.b = 0
        if self.negative is None:
            self.negative = False

    def __hash__(self):
        return hash((tuple(self.possibleVertices), self.a, self.b, self.negative))

    def __eq__(self, other):
            if isinstance(other, Testimony):
                return (self.possibleVertices, self.a, self.b, self.negative) == (other.possibleVertices, other.a, other.b, other.negative)
            return False

    def __lt__(self, other) :
        return self.a < other.a
    
    def reachable(self, instance, vert, time):
        for v in self.possibleVertices:
            if time + instance.graph.bestDist(vert, v) <= self.b:
                return True
        return False
    

# Uses random, not thought to be tested
# TODO: Move to a separate file, together with random generation stuff
def generateIntervalTestimonies(actor_route: Route, vertex: int, a: int, b: int, probability=1):
    testimonies = []
    actor = RouteIterator(actor_route)
    loop_condition = True
    while loop_condition:

        if actor.vertex == vertex and not (actor.b < a or b < actor.a): ## If actor's route crosses our interval
            first_time_together = max(a, actor.a)
            last_time_together = min(b, actor.b)
            if random.uniform(0,1) <= probability:
                testimonies.append(Testimony([vertex], first_time_together, last_time_together))
        loop_condition = actor.next(actor_route)

    return testimonies


# TODO: Used specifically to generate "realistic instances" and should be moved together
def generateNegativeTestimonies(testimonies: [Testimony], vertex: int, a: int, b: int):
    intervals_together = sorted([(testimony.a, testimony.b) for testimony in testimonies])
    negative_testimonies = []
    first_time_not_seen = a
    for (arrival_time, leave_time) in intervals_together:
        if first_time_not_seen <= arrival_time - 1:
            negative_testimonies.append(Testimony([vertex], first_time_not_seen, arrival_time - 1, negative=True))
        first_time_not_seen = leave_time + 1
    if first_time_not_seen <= b:
        negative_testimonies.append(Testimony([vertex], first_time_not_seen, b, negative=True))
    return negative_testimonies


### Not in use. Should call generateNegativeTestimonies in each interation
def generateTruthtellerTestimonies(actor_route: Route, witness_route: Route):
    witness = RouteIterator(witness_route)
    testimonies = []
    loop_condition = True
    while loop_condition:
        testimonies.extend(generateIntervalTestimonies(actor_route, witness.vertex, witness.a, witness.b))
        loop_condition = witness.next(witness_route)

    return testimonies
