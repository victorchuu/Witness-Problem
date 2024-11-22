from src.witnessproblem import Graph, Route, RouteIterator, fitness, truthtellingWitnesses


MAX_NEIGHBOUR_DIST = 8


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


"""
Once a best neighbour is found, this method creates the route object of that neighbour.
Such route is created by keeping the segments R[0...i] and R[j...n] of the original route,
  and apppending the shortest path from i to j in between
  R[0...i] + SHORTEST[I...j] + R[j...n]
"""
def createRoute(instance, route, bestIndex):
    if bestIndex == None:
        return route
    i, j = bestIndex
    neighbour = Route()
    it = RouteIterator(route, neighbour)
    while it.index < i:
        it.next(route, neighbour)
    instance.graph.buildShortestRoute(route.vertex[i], route.vertex[j], route.leaveTime[j] - route.leaveTime[i], neighbour)
    while it.index < j:
        it.next(route)
    while it.next(route, neighbour) :
        pass
    return neighbour

"""
This function returns the set of testimonies visited by the shortest sub-route that goes from src to dest
starting at time initialTime and ending at time endTime
- It leverages Floyd algorithm precomputation to find the shortest path between src and dest
- It leverages instance precumoutation to find the testimonies visited at a given vertex and time
"""
def getShortestRouteVisitedTestimonies(graph: Graph, precompute, src, dest, initialTime, endTime) :

    acc = set()
    acc |= precompute.collidingTestimoniesSet(dest, initialTime + graph.bestDistanceMatrix[src][dest], endTime)

    shortest_path = graph.buildShortestPath(src, dest)
    for v in shortest_path:
        time = initialTime + graph.bestDistanceMatrix[src][v]
        acc |= precompute.collidingTestimoniesSet(v, time, time)
    return acc

"""
This function generates the best neighbour of a route.
- To find the neighbours of a route, we will modify "small" segments of the route, 
  by selecting all i < j combinations such that j - i < MAX_NEIGHBOUR_DIST
  and inserting the shortest path between route[i] and route[j] in between.
- We will then compute the fitness value of each neighbour and return the one with the best fitness value
- Instead of creating each neighbour route and then calculating its fitness, we can calculate the fitness values
  before creating the route, leveraging graph and instance precomputed values. We will only create the route
  of the selected neighbour.
"""
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
        
"""
Generic local search algorithm schema
- We find the neighbours of a route
- We pick the one with best fitness value
- If it is better than the current route, we replace it and repeat the process
"""
def localSearch(instance, route, bestFitness):
    hits = 0
    while True:
        route, fit = bestNeighbour(instance, route, bestFitness)
        if fit > bestFitness:
            hits += 1
            bestFitness = fit
        else:
            return route, bestFitness, hits