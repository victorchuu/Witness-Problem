import random
from src.witnessproblem import Route, RouteIterator
from .randomRoute import appendRandomRoute, NO_VERTEX_SELECTED


MAX_MUTATION_INTERVAL = 10


def mutate(instance, route) :

    if len(route.vertex) < 2 :
        randomNewRoute = Route()
        appendRandomRoute(instance.graph, NO_VERTEX_SELECTED, instance.maxTime, randomNewRoute)
        return randomNewRoute

    i = random.randint(0, len(route.vertex) - 1)
    j = (i + random.randint(1, MAX_MUTATION_INTERVAL) ) % len(route.vertex)
    while j == i :
        j = (i + random.randint(1, MAX_MUTATION_INTERVAL) ) % len(route.vertex)

    if i < j: 
        return mutate_interval(instance, route, i, j)
    else :
        firstMutation = mutate_interval(instance, route, i, NO_VERTEX_SELECTED)
        return mutate_interval(instance, firstMutation, NO_VERTEX_SELECTED, j)


def mutate_interval(instance, route, i, j):
    R = Route()

    # Copy the route: R[0...i] = route[0...i]
    if i >= 0 :
        it = RouteIterator(route, copy_to=R)
        it.advance(route, i, copy_to=R)
        depart_from = it.b 
    else :
        it = RouteIterator(route, None)
        depart_from = 0
        
    # Advance without copyng route[i] --> route [j]
    if j == NO_VERTEX_SELECTED :
        destiny = NO_VERTEX_SELECTED
        arrive_at = instance.maxTime
    else :
        it.advance(route, j)
        destiny = it.vertex
        arrive_at = it.a

    # Append a new random route R[i...k]
    appendRandomRoute(instance.graph, destiny, arrive_at - depart_from, R)
    
    # Copy the route: R[k...] = route[j...]
    if j != NO_VERTEX_SELECTED and j < len(route.vertex) :
        R.time[-1] += route.time[j]
        R.leaveTime[-1] += route.time[j]
        it.advance_to_end(route, copy_to=R)
    return R