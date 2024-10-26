from src.solutions.greedy import GreedyDistance, PersistentGreedyAlgorithm, GreedyTestimonies
from src.witnessproblem import Instance, Route
from .randomRoute import appendRandomRoute


def initial_population(instance: Instance, size: int):
    population = []    
    for j in range(size) :
        population.append(Route()) 
        appendRandomRoute(instance.graph, -1, instance.maxTime, population[j])
    return population


def initial_population_with_greedy(instance: Instance, size: int):
    times_distance = 10
    times_testimonies = 10

    greedy_distance = GreedyDistance()
    greedy_testimonies = GreedyTestimonies()

    population = [
        greedy_distance.run(instance) for _ in range(times_distance)
    ]

    population.extend([
        greedy_testimonies.run(instance) for _ in range(times_testimonies)
    ])

    ## Fix greedy routes so they wait in the last vertex till the end of the instance
    for _, r in population:
        remaining_time = instance.maxTime - r.leaveTime[-1]
        r.time[-1] += remaining_time
        r.leaveTime[-1] += remaining_time

    population = [r for _,r in population]

    population.extend(initial_population(instance, size - times_distance - times_testimonies))

    return population
