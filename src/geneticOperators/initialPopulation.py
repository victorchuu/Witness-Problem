from src.solutions.greedy import GreedyDistance, GreedyTestimonies
from src.witnessproblem import Instance, Route
from .randomRoute import appendRandomRoute


def initial_population(instance: Instance, size: int):
    population = []    
    for j in range(size) :
        population.append(Route()) 
        appendRandomRoute(instance.graph, -1, instance.maxTime, population[j])
    return population


def initial_population_with_greedy(instance: Instance, size: int):
    times_distance = 20

    greedy_distance = GreedyDistance()

    population = [
        greedy_distance.run(instance) for _ in range(times_distance)
    ]

    population = [make_route_wait_in_last_vertex(r, instance) for _, r in population]

    population.extend(initial_population(instance, size - times_distance))

    return population


def make_route_wait_in_last_vertex(route: Route, instance: Instance):
    remaining_time = instance.maxTime - route.leaveTime[-1]
    route.time[-1] += remaining_time
    route.leaveTime[-1] += remaining_time
    return route
