from dataclasses import dataclass


NO_VERTEX = -1
NO_DISTANCE = -1

    
@dataclass
class Edge:
    vertex: int = NO_VERTEX
    distance: int = NO_DISTANCE

    def __gt__(self, other):
        return self.distance > other.distance

    def __str__(self):
        return f"vertex: {self.vertex},\tdistance: {self.distance}"