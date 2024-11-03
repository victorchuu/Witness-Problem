from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Interval:
    a: int
    b: int

    def __lt__(self, other):
        return self.a < other.a

    def are_intervals_disjoint(I1, I2):
        return I1.b < I2.a or I2.b < I1.a