from src.witnessproblem import Instance, Route, fitness
from src.Algorithm import Algorithm


MAX_VERTICES_IN_GRAPH = 20
MAX_INSTANCE_TIME = 20


# The search algorithm itearates ALL the possible routes, and picks the one with best fitness
# It starts with a route consisting of just the initial vertex, and recursively constructs all the possible routes
# It's pretty basic, doesn't do any Branch and bound. There is a lot of room for improvement here
def recursiveSearch(route: Route, instance: Instance, time, currentVertex) :

    if time <= 0 :
        return fitness(instance, route)
    
    bestSolution = fitness(instance, route)

    # For each adjacent vertex, we try to move the route there
    for edge in instance.graph.adjList[currentVertex] :
        route.vertex.append(edge.vertex)
        route.time.append(0)
        route.leaveTime.append(edge.distance + route.leaveTime[-1])

        bestSolution = max(bestSolution, recursiveSearch(route, instance, time - edge.distance, edge.vertex))

        del route.vertex[-1]
        del route.time[-1]
        del route.leaveTime[-1]

    # We also try to stay in the curent vertex 1 unit of time
    route.time[-1] += 1
    route.leaveTime[-1] += 1
    bestSolution = max(bestSolution, recursiveSearch(route, instance, time - 1, currentVertex) )
    route.time[-1] -= 1
    route.leaveTime[-1] -= 1

    return bestSolution


def unsafeToRunSearchAlgorithm(instance: Instance):
    # Protecting me aagainst myself
    warn_message = "Ignoring execution of search algorithm for this instance: "
    if instance.graph.V > MAX_VERTICES_IN_GRAPH:
        print(warn_message, f"Too many vertices in graph: {instance.graph.V}")
        return True
    if instance.maxTime > MAX_INSTANCE_TIME:
        print(warn_message, f"Time window is too big: {instance.maxTime}")
        return True
    return False
    

def optimalSolution(instance: Instance) :   
    if unsafeToRunSearchAlgorithm(instance):
        return -1

    maximum = 0
    for vertex in range(instance.graph.V) :
        route = Route()
        route.startAt(vertex)
        maximum = max([maximum, recursiveSearch(route, instance, instance.maxTime, vertex)])

    return maximum


class SearchAlgorithm(Algorithm):


    def __init__(self):
        super()


    def run(self, instance):
        return optimalSolution(instance)


    def __str__(self):
        return "Optimal solutions"