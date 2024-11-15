from src.witnessproblem import Instance, Route, fitness
from src.Algorithm import Algorithm
from collections import deque


MAX_VERTICES_IN_GRAPH = 20
MAX_INSTANCE_TIME = 20


# The search algorithm itearates ALL the possible routes, and picks the one with best fitness
# It starts with the routes consisting of just an initial vertex, and constructs all the possible routes
# It's pretty basic, doesn't do any Branch and bound. There is a lot of room for improvement here
def iterativeSearch(instance: Instance):

    queue = deque()
    maximum = 0

    for vertex in range(instance.graph.V):
        initial_route = Route()
        initial_route.startAt(vertex)
        queue.append(initial_route)

    while queue:
        route = queue.popleft()
        if route.leaveTime[-1] >= instance.maxTime:
            maximum = max(maximum, fitness(instance, route))

        if route.leaveTime[-1] < instance.maxTime:
            current_vertex = route.vertex[-1]

            for edge in instance.graph.adjList[current_vertex]:
                new_route = Route(route.vertex[:], route.time[:], route.leaveTime[:])
                new_route.vertex.append(edge.vertex)
                new_route.time.append(0)
                new_route.leaveTime.append(edge.distance + new_route.leaveTime[-1])
                queue.append(new_route)

            new_route = Route(route.vertex[:], route.time[:], route.leaveTime[:])
            new_route.time[-1] += 1
            new_route.leaveTime[-1] += 1
            queue.append(new_route)

    return maximum


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

    return iterativeSearch(instance)


class SearchAlgorithm(Algorithm):


    def __init__(self):
        super()


    def run(self, instance):
        return optimalSolution(instance)


    def __str__(self):
        return "Optimal solutions"