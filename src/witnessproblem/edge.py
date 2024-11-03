from dataclasses import dataclass
from dataclasses_json import dataclass_json


NO_VERTEX = -1
NO_DISTANCE = -1

@dataclass_json
@dataclass
class Edge:
    vertex: int = NO_VERTEX
    distance: int = NO_DISTANCE

    def __gt__(self, other):
        return self.distance > other.distance
