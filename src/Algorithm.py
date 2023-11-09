from abc import ABC, abstractmethod
from src.witnessproblem import Instance

class Algorithm(ABC):

    @abstractmethod
    def run(self, instance: Instance):
        pass

    def __str__(self):
        return "nope"
