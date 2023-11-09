from src.witnessproblem import Graph, Route, RouteIterator, fitness, truthtellingWitnesses


MAX_NEIGHBOUR_DIST = 6


"""
The neighbours of a route R = R[1...n] are created by selecting i, j in the interval [0, n], such that j - i < MAX_NEIGHBOUR_DIST
Then keeping the segments R[0...i] and R[j...n] of the route, and apppending the shortest path from i to j in between
  R[0...i] + SHORTEST[I...j] + R[j...n]

Precomputing all the testimonies visited by R[0...i] and by R[j...n], (for every i and j) will save us time when computing the fitness value of a neighbour
This will be efficient or not depending on the total amount of neighbours for each route. 
If we dont generate many of them, it may be better to compute their fitness values individually.
"""
class VisitedTestimonies() :

    def __init__(self, instance, route):

        # until[i] = set of all the visited testimonies in route[0...i]
        self.until = []
        
        # since[j] = set of all the visited testimonies in route[j...n]
        self.since = []
        
        self.compute(instance, route)


    def compute(self, instance, route):
        it = RouteIterator(route)
        visitedByVertex = []
        while True :        
            visitedByVertex.append(instance.precompute.collidingTestimoniesSet(it.vertex, it.a, it.b))
            if not it.next(route):
                break

        testimonies = set()
        for visits in visitedByVertex:
            testimonies |= visits
            self.until.append(testimonies.copy())
        
        testimonies = set()
        for visits in reversed(visitedByVertex):
            testimonies |= visits
            self.since.append(testimonies.copy())
        self.since.reverse()



def createRoute(instance, route, bestIndex):
    if bestIndex == None:
        return route
    i, j = bestIndex
    neighbour = Route()
    it = RouteIterator(route, neighbour)
    while it.index < i:
        it.next(route, neighbour)                                        # < ---------- arrival time ---------- > - < --- leave time --- >
    instance.graph.buildShortestRoute(route.vertex[i], route.vertex[j], route.leaveTime[j] - route.leaveTime[i], neighbour)
    while it.index < j:
        it.next(route)
    while it.next(route, neighbour) :
        pass
    return neighbour


# Returns the testimonies visited by the route generated with buildShortestRoute()
def getShortestRouteVisitedTestimonies(graph: Graph, precompute, src, dest, initialTime, endTime) :

    acc = set()
    acc |= precompute.collidingTestimoniesSet(dest, initialTime + graph.bestDistanceMatrix[src][dest], endTime)

    while src != dest :
        dest = graph.floydPath[src][dest]
        time = initialTime + graph.bestDistanceMatrix[src][dest]
        acc |= precompute.collidingTestimoniesSet(dest, time, time)
    return acc


def bestNeighbour(instance, route, bestFitness):
    visited_testimonies = VisitedTestimonies(instance, route)
    bestIndex = None
    i = 0

    while i < len(route.vertex):
        for j in range(i + 2, i + MAX_NEIGHBOUR_DIST):
            if j >= len(route.vertex):
                break

            visits = getShortestRouteVisitedTestimonies(instance.graph, instance.precompute, 
                src=route.vertex[i], dest=route.vertex[j],
                initialTime=route.leaveTime[i], endTime=route.leaveTime[j] - route.time[j])
            fit = truthtellingWitnesses(instance, visited_testimonies.until[i] | visits | visited_testimonies.since[j])
            if fit > bestFitness:
                bestFitness = fit
                bestIndex = (i, j)
        i += 1
    
    return createRoute(instance, route, bestIndex), bestFitness
        

def localSearch(instance, route, bestFitness):
    hits = 0 # Uncomment to test the improvements made by the local search in tests.ipynb
    while True:
        route, fit = bestNeighbour(instance, route, bestFitness)
        if fit > bestFitness:
            hits += 1
            bestFitness = fit
        else:
            return route, bestFitness  , hits