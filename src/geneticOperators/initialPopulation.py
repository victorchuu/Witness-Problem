from src.witnessproblem import Instance, Route
from .randomRoute import appendRandomRoute


def initial_population(instance: Instance, size):
    population = []    
    for j in range(size) :
        population.append(Route()) 
        appendRandomRoute(instance.graph, -1, instance.maxTime, population[j])
    return population