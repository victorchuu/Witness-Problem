from src.witnessproblem import Instance, Route, RouteIterator
from src.utils.binarySearch import *


import random


def crossover(instance, p1, p2) :          
    return succesor(instance, p1, p2) , succesor(instance, p2, p1)


def succesor(instance: Instance, p1: Route, p2: Route):
    graph = instance.graph
    son = Route()

    # Select a random index in p1, such that departing from p1[index] we're able to reach p2's last vertex
    p2_reachable = lambda i : graph.bestDist(p1.vertex[i], p2.vertex[-1]) <= instance.maxTime - p1.leaveTime[i]
    if not p2_reachable(0):
        return p1
    max_index = lastTrueIndexBinarySearch(0, len(p1) - 1, p2_reachable)
    i = random.randint(0, max_index) 

    it = RouteIterator(p1, copy_to=son) 
    it.advance(p1, i, copy_to=son)

    # Select the first index in p2 reachable departing from p1[index]
    leave_time = it.b
    src = it.vertex
    unreachable_from_src = lambda x: leave_time + graph.bestDist(src, p2.vertex[x]) > p2.leaveTime[x]
    j = firstFalseIndexBinarySerch(0, len(p2), unreachable_from_src)

    graph.buildShortestRoute(src, p2.vertex[j] , p2.leaveTime[j] - leave_time , son) 

    it2 = RouteIterator(p2, start_at = j)
    it2.advance_to_end(p2, copy_to=son)

    return son
