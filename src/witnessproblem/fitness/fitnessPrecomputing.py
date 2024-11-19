from src.utils.binarySearch import *
from functools import lru_cache

""" This class represents and chronologically sorts all the time events that appear in the testimonies 
If there are 2 intervals
    - I1 = [2,7]
    - I2 = [4,8]
Then there will be 4 testimony events, sorted like
    - At 2, I1 opens
    - At 4, I2 opens
    - At 7, I1 closes
    - At 8, I2 closes
"""
class TestimonyEvent:


    def __init__(self, eventTime, isOpen: bool, witnessIndex, testimonyIndex, openIntervalsSet=set()):
        self.eventTime: int = eventTime
        self.isOpen: bool = isOpen

        self.hashkey = (witnessIndex, testimonyIndex)
        self.openIntervalsSet = openIntervalsSet


    def __lt__(self, other):
        return self.eventTime < other.eventTime or ( self.eventTime == other.eventTime and self.isOpen )

    def __eq__(self, other):
        return self.eventTime == other.eventTime and self.isOpen == other.isOpen and self.hashkey == other.hashkey and self.openIntervalsSet == other.openIntervalsSet


""" This assigns to every testimony event, the set of intervals that are open right before that point in time
If there are 2 intervals
    - I1 = [2,7]
    - I2 = [4,8]
Then there will be 4 testimony events:
    - At 2, I1 opens  -- open intervals before this = {}
    - At 4, I2 opens  -- open intervals = {I1}
    - At 7, I1 closes -- open intervals = {I1, I2}
    - At 8, I2 closes -- open intervals = {I2}
"""
def sortAndPrecomputeOpenIntervals(testimonyEvents: [TestimonyEvent]):
        testimonyEvents.sort()    
        openIntervalsSet = set()
        for event in testimonyEvents:
            event.openIntervalsSet = openIntervalsSet.copy()
            if event.isOpen:
                openIntervalsSet.add(event.hashkey)
            else :
                openIntervalsSet.remove(event.hashkey)
            
        
""" The precomputation consists of creating a sorted list of testimony events for each vertex in the graph
    This will simplify answering the question: If the actor visited the vertex v, during the interval [a,b],
        - How many testimonies are true?
        - How many witnesses are truthtellers?
    Continuing the previous example, if the actor was in the vertex at time 5, we will search in the list L = (2,4,7,8)
        - L.binarySearch(5) = "At 7, I1 closes -- open intervals = {I1, I2}"
        Then we know that the actor visited the testimonies whose intervals are I1 and I2
"""
class FitnessPrecomputation:


    def __init__(self):
        self.eventsByVertex: [[TestimonyEvent]] = None
        self.positiveTestimoniesByWitness: [int] = None


    def start(self, instance):
        self.eventsByVertex = [[] for _ in range(instance.graph.V)]
        self.positiveTestimoniesByWitness = [0] * len(instance.testimoniesByWitness)

        for witnessId, witness in enumerate(instance.testimoniesByWitness):
            for testimonyId, testimony in enumerate(witness):
                if not testimony.negative:
                    self.positiveTestimoniesByWitness[witnessId] += 1
                
                for vertex in testimony.possibleVertices:
                    self.eventsByVertex[vertex].append(TestimonyEvent(testimony.a, True, witnessId, testimonyId))
                    self.eventsByVertex[vertex].append(TestimonyEvent(testimony.b, False, witnessId, testimonyId))

        for eventList in self.eventsByVertex:
            sortAndPrecomputeOpenIntervals(eventList)


    # Fitness operation will be called a lot of times.
    # Since the output of this function only depends on the instance, not on the route, it is worth it to cache its results!
    @lru_cache(maxsize=None)
    def collidingTestimoniesSet(self, vertex: int, begin: int, end: int):
        eventList = self.eventsByVertex[vertex]
        id = firstFalseIndexBinarySerch(0, len(eventList), lambda i: eventList[i].eventTime < begin)

        if id >= len(eventList):
            return set()
        
        collidingTestimonies = eventList[id].openIntervalsSet.copy()
        while id < len(eventList) and eventList[id].eventTime <= end :
            if eventList[id].isOpen:
                collidingTestimonies.add(eventList[id].hashkey)
            id += 1

        return collidingTestimonies
