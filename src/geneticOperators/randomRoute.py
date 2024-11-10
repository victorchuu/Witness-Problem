import math
import random

from src.witnessproblem import Graph, Route


NO_VERTEX_SELECTED = -1


def appendRandomRoute(graph: Graph, dest, time, route: Route) :
    
    if len(route) > 0:
        src = route.vertex[-1]
    elif dest == NO_VERTEX_SELECTED: 
        src = random.choice(range(graph.V))
        route.startAt(src)
    else: 
        possibleSources = [v for v in range(graph.V) 
                           if graph.bestDist(v, dest) <= time]
        src = random.choice(possibleSources)
        route.startAt(src)
        
    if dest == NO_VERTEX_SELECTED : 
        possibleDestinies = [v for v in range(graph.V) if graph.bestDist(src, v) <= time]
        if len(possibleDestinies) == 0:
            route.time[-1] = time
            return
        dest = random.choice(possibleDestinies)
    
    randomRouteRecursive(graph, src, dest, time, route)
    return route


def randomRouteRecursive(graph, src, dest, time, route: Route) :  
    if src == dest:
        route.sleep_for(time)
        return route


    possible_adjacents = [edge for edge in graph.adjList[src] 
                         if edge.distance + graph.bestDist(edge.vertex, dest) <= time]
    edge = random.choice(possible_adjacents)

    # We try to wait in the current vertex
    spare_time = time - (edge.distance + graph.bestDist(edge.vertex, dest))
    wait_time = random_time_to_wait(spare_time)
    route.sleep_for(wait_time)
    time = time - wait_time
    
    route.vertex.append(edge.vertex)
    route.time.append(0)
    route.leaveTime.append(route.leaveTime[-1] + edge.distance)
    randomRouteRecursive(graph, edge.vertex, dest, time - edge.distance, route)
    

def random_time_to_wait(time):
    """
    Different configurations in configuring the waiting time can lead to really different populations!!
    Here are some options I explored

    coefficient = 4 # 1, 2, 3,...

    # We want the numbers close to 0 to be more likely. Otherwise we will generate short routes, with high waiting times
    z = random.random()**coefficient
    return math.floor(time * z)
    """
    # Another option is to use a geometric distribution
    z = geometric_distribution(p = 0.35) - 1
    while z > time:
        z = geometric_distribution(p = 0.35) - 1
    return z


def geometric_distribution(p):
    u = random.random()
    return math.ceil(math.log(1 - u) / math.log(1 - p))