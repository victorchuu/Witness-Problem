from src.solutions.greedy import GreedyDistance, PersistentGreedyAlgorithm
from src.witnessproblem import Instance, Route, fitness, truthtellingWitnesses, visited_testimonies
from src.Algorithm import Algorithm
import heapq


MAX_VERTICES_IN_GRAPH = 20
MAX_INSTANCE_TIME = 20

def reachable_positive_testimonies(instance, vert, time) :
    return {(witnessIdx, testimonyIdx) \
        for witnessIdx, testimonies in enumerate(instance.testimoniesByWitness) \
            for testimonyIdx, t in enumerate(testimonies) \
                if (not t.negative) and (t.reachable(instance, vert, time))}


"""
To calculate an upper bound for all posible children of the current subroute:
- We add all the testimonies that the route already verifies-
- We assume it will verify all the positive testimonies reachable from the last vertex
- We assume it will not visit any negative testimony
Then, we calculate all truthteller witnesses given these assumptions
"""
def calculateUpperBound(instance: Instance, route: Route):
    assumed_visited_testimonies = visited_testimonies(instance, route) | reachable_positive_testimonies(instance, route.vertex[-1], route.leaveTime[-1])
    return truthtellingWitnesses(instance, assumed_visited_testimonies)


def push_solution_if_worth_it(instance: Instance, route: Route, maximum: int, queue: list):
    upper_bound = calculateUpperBound(instance, route)
    if upper_bound > maximum:
        heapq.heappush(queue, (-upper_bound * (route.leaveTime[-1] + 1), route))

# The search algorithm iterates ALL the possible routes, and picks the one with best fitness
# It starts with the routes consisting of just an initial vertex, and constructs all the possible routes
def optimalSolution(instance: Instance):

    queue = []
    maximum,best_route = PersistentGreedyAlgorithm(GreedyDistance()).run(instance)

    for vertex in range(instance.graph.V):
        initial_route = Route()
        initial_route.startAt(vertex)
        push_solution_if_worth_it(instance, initial_route, maximum, queue)

    while queue:
        priority, route = heapq.heappop(queue)
        if route.leaveTime[-1] >= instance.maxTime:
            fit_value = fitness(instance, route)
            if fit_value > maximum:
                maximum = fit_value
                best_route = route

        else:
            upper_bound = calculateUpperBound(instance, route)
            if upper_bound <= maximum:
                continue
            current_vertex = route.vertex[-1]

            for edge in instance.graph.get_adjacents(current_vertex):
                new_route = Route(route.vertex[:], route.time[:], route.leaveTime[:])
                new_route.vertex.append(edge.vertex)
                new_route.time.append(0)
                new_route.leaveTime.append(edge.distance + new_route.leaveTime[-1])
                push_solution_if_worth_it(instance, new_route, maximum, queue)

            new_route = Route(route.vertex[:], route.time[:], route.leaveTime[:])
            new_route.time[-1] += 1
            new_route.leaveTime[-1] += 1
            push_solution_if_worth_it(instance, new_route, maximum, queue)

    return maximum, best_route


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


class SearchAlgorithm(Algorithm):


    def __init__(self):
        super()


    def run(self, instance, override_initial_pop=None):
        if unsafeToRunSearchAlgorithm(instance):
            return -1

        return optimalSolution(instance)


    def __str__(self):
        return "Optimal solutions"