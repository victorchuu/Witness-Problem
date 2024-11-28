from .testimonyVerifier import TestimonyVerifier
from src.witnessproblem import Instance, Route, RouteIterator

def truthtellingWitnesses(instance, visitedTestimonies):
    witnessMap = {}
    visitedTestimoniesByWitness = {witnessIdx: [] for witnessIdx in range(len(instance.testimoniesByWitness))}
    for (witnessIdx, testimonyIdx) in visitedTestimonies:
        visitedTestimoniesByWitness[witnessIdx].append(testimonyIdx)

    for witnessIdx in range(len(instance.testimoniesByWitness)):
        witnessMap[witnessIdx] = 0
        for testimonyIdx in visitedTestimoniesByWitness[witnessIdx]:
            isNegative = instance.testimoniesByWitness[witnessIdx][testimonyIdx].negative
            witnessMap[witnessIdx] += (-1)**isNegative # positive: +1 ,  negative: -1

    return sum(1 for (witness, correct) in witnessMap.items() if correct==instance.precompute.positiveTestimoniesByWitness[witness])



# Since collidingTestimoniesSet is cached, and expected to be O(1)
# Then the fitness function becomes linear in the number of testimonies!
def visited_testimonies(instance, route): 
    it = RouteIterator(route)
    visitedTestimonies = set()
    while True :        
        visitedTestimonies = visitedTestimonies | instance.precompute.collidingTestimoniesSet(it.vertex, it.a, it.b)
        if not it.next(route):
            break
    return visitedTestimonies  

"""
The fitness function is the sum of the number of witnesses that are telling the truth.
To do so, visited_testimonies calculates all the testimonies, positive or negative, that collide with the given route
Then, truthtellingWitnesses calculates the number of witnesses that are telling the truth, based on the visited testimonies.
"""
def fitness(instance, route):
    return truthtellingWitnesses(instance, visited_testimonies(instance, route))


"""
Deprecated - less efficient than the other method, yet it has been tested that both output the same results
"""
def old_fitness(instance: Instance, route: Route) :
    verifier = TestimonyVerifier(instance.graph, route)
    return sum(map(verifier.allTestimoniesRight, instance.testimoniesByWitness))