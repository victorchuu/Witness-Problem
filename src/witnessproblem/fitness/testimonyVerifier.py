from src.witnessproblem import Graph, Interval, Route, RouteIterator, Testimony

class TestimonyVerifier:


    def __init__(self, graph: Graph, route: Route):
        self.visitsByVertex = markVisitsByVertex(graph, route)

    
    def allTestimoniesRight(self, testimonies: [Testimony]) :
        for testimony in testimonies :
            if not self.isTestimonyTrue(testimony): 
                return False
        return True
    

    def isTestimonyTrue(self, testimony: Testimony) :
        for vertex in testimony.possibleVertices : 
            for visitInterval in self.visitsByVertex[vertex] : 
                if not visitInterval.areIntervalsDisjoint(Interval(testimony.a, testimony.b)) : 
                    return not testimony.negative
        return testimony.negative



def markVisitsByVertex(graph: Graph, route: Route) -> [[Interval]] :
    visitsByVertex: [[Interval]] = [[] for _ in range(graph.V)]

    it = RouteIterator(route)
    while True:
        visitsByVertex[it.vertex].append(Interval(it.a, it.b))  
        if not it.next(route):
            break  

    return visitsByVertex