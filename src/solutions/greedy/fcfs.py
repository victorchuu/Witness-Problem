from src.witnessproblem import Graph, Route, Testimony


""" First come first served greedy:
    This greedy method will iterate through all the Testimonies T[0..n] and:
        - If T[i] can be reached from the current time and vertex, it moves the route to satisfy it
        - If T[i] cannot be reached from the current time and vertex, ignores it
"""
def firstComeFirstServed(graph: Graph, testimonies: [Testimony], src) :

    R: Route = Route()
    R.startAt(src)
    time = 0

    for T in testimonies :

        (destiny, distance) = graph.closestVertex(src, T.possibleVertices)

        if time + distance <= T.b:
            arrival = max(T.a, time + distance)

            # This continues the route 
            #   - From src to destiny
            #   - With duration: arrival - time
            #   - If the provided time is more than needed, it waits in the last vertex
            graph.buildShortestRoute(src, destiny, arrival - time , R)
            (src, time) = (destiny, arrival)
    return R