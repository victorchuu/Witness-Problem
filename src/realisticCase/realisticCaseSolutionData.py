from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from src.witnessproblem import Route

@dataclass_json
@dataclass
class RealisticCaseSolutionData:
    base_similarity: float
    lying_witnesses: int
    actor_route: Route
