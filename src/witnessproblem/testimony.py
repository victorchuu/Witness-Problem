from .graph import Interval


class Testimony :
    
    def __init__(self, vertices: [int] = [], a = 0, b = 0, negative = False) :
        self.possibleVertices: [int] = vertices
        self.a: int = a
        self.b: int = b
        self.negative: bool = negative


    def readFromFile(self, file) :
        self.negative = file.readline() == 'N'
        self.possibleVertices = [int(x) for x in file.readline().split()]
        line = file.readline().split()
        self.a, self.b = int(line[0]), int(line[1])
        return self


    def writeToFile(self) :
        return f"{'N' if self.negative else 'Y'}\n{' '.join(map(str,self.possibleVertices))}\n{self.a} {self.b}"

    # Print in a human-readable way    
    def __str__(self) :
        return f"{'┐' if self.negative else '' } Vertices: {self.possibleVertices}, \tInterval: [{self.a}, {self.b}]"


    def __lt__(self, other) :
        return self.a < other.a
