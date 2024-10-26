from .graph import Graph
from .testimony import Testimony
from .fitness.fitnessPrecomputing import FitnessPrecomputation

LINE_BREAK = '\n'
    
class Instance :
    
    def __init__(self) :
        self.graph: Graph = Graph()
        self.testimoniesByWitness: [[Testimony]] = []
        self.maxTime: int = 0

        # Precomputed information for the fitness function 
        self.precompute = FitnessPrecomputation()
        self.precompute.collidingTestimoniesSet.cache_clear()


    # TODO: Use standard formatting such as JSON
    def readFromFile(self, file) :
        self.graph.readFromFile(file)
        numWitnesses = int(file.readline())
        self.testimoniesByWitness = [ [ Testimony().readFromFile(file) for _ in range(int(file.readline())) ] for _ in range(numWitnesses) ]
        self.maxTime = max([ max([testimony.b for testimony in witness ]) for witness in self.testimoniesByWitness])
        self.precompute.start(self)


    # TODO: Use standard formatting such as JSON
    def __str__(self) : 
        string = f"{self.graph}\nNumber of witnesses: {len(self.testimoniesByWitness)}\n"
        for index, witness in enumerate(self.testimoniesByWitness) : 
            string += f"\nWitness {index} has {len(witness)} testimonies\n"
            string += '\n'.join([str(test) for test in witness])

        return string


    # TODO: Use standard formatting such as JSON
    def writeToFile(self) :
        string = self.graph.writeToFile()
        string += str(len(self.testimoniesByWitness)) + LINE_BREAK # Number of witnesses
        return string + LINE_BREAK.join([
                str(len(testimonies)) + LINE_BREAK + LINE_BREAK.join([t.writeToFile() for t in testimonies]) for testimonies in self.testimoniesByWitness 
            ]) + LINE_BREAK
    

    def getTestimonyList(self) -> [Testimony]:
        return [T for witn in self.testimoniesByWitness for T in witn]
