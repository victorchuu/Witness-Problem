from .route import Route
from .edge import Edge
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
import rustworkx as rx


INFINITY = 1000000000
NO_VERTEX = -1
LINE_BREAK = '\n'

@dataclass_json
@dataclass
class Graph:
    V: int
    E: int
    adjList: list[list[Edge]]
    
    def __init__(self, V = 0, E = 0, adjList = [[Edge]]):
        self.V = V
        self.E = E
        self.adjList = adjList


    def applyFloyd(self) :
        # Initial status for Floyd's algorithm
        self.bestDistanceMatrix = [ [INFINITY for _ in range(self.V)] for _ in range(self.V) ]
        self.realDist = [ [INFINITY for _ in range(self.V)] for _ in range(self.V) ]
        self.floydPath = [ [i for _ in range(self.V)] for i in range(self.V) ]
        for vertex in range(self.V) :
            for edge in self.adjList[vertex]:
                self.realDist[vertex][edge.vertex] = edge.distance
                self.bestDistanceMatrix[vertex][edge.vertex] = edge.distance
            self.bestDistanceMatrix[vertex][vertex] = 0
            self.realDist[vertex][vertex] = 0

        
        # Floyd's algorithm
        for k in range(self.V) :
            for i in range(self.V) :
                for j in range(self.V) :
                    if self.bestDistanceMatrix[i][k] + self.bestDistanceMatrix[k][j] < self.bestDistanceMatrix[i][j] :
                        self.bestDistanceMatrix[i][j] = self.bestDistanceMatrix[i][k] + self.bestDistanceMatrix[k][j]
                        self.floydPath[i][j] = self.floydPath[k][j]



    # Returns the distance between two vertices taking the edge that connects them directly
    # Note that this could not be the best distance
    # Expects the 2 inputs to be connected by an edge, or else it will throw an exception
    def directDist(self, u, v):
        if self.realDist[u][v] >= INFINITY:
            raise Exception(f"directDist() was called with non adjacent vertices, ({u}, {v})")
        return self.realDist[u][v]
    

    def bestDist(self, u, v) :
        return self.bestDistanceMatrix[u][v]

        
    # Returns the closest vertex to src, among all the vertices in destinies
    def closestVertex(self, src, destinies: [int]) -> (int, int) :
        (distance, destiny) = (INFINITY, NO_VERTEX)
        for v in destinies: 
            d = self.bestDistanceMatrix[src][v]
            if d < distance :
                (distance, destiny) = (d, v)
        return (destiny, distance)


    # TODO: MOVE TO ANOTHER MODULE AND ADD UNIT TESTS
    # Builds a shortest distance route from src to dest, that waits the needed time in the last vertex until it lasts t.
    # Uses Floyd's algorithm path reconstruction
    def buildShortestRoute(self, src, dest, time, route: Route) :
        if src != dest :
            k = self.floydPath[src][dest]
            self.buildShortestRoute(src, k , 0, route)
            route.vertex.append(dest)
            route.time.append(0)
            route.leaveTime.append(route.leaveTime[-1] + self.bestDistanceMatrix[k][dest])
        if time != 0 :
            route.time[-1] += time - self.bestDistanceMatrix[src][dest]
            route.leaveTime[-1] += time - self.bestDistanceMatrix[src][dest]

    
    def createGridGraph(self, n: int, distance: int):
        self.V = n*n
        self.E = 2*2*n*(n-1)
        self.adjList = [[] for _ in range(self.V)]

        ## Horizontal paths
        for row in range(0, self.V, n):
            for col in range(row + 1, row + n):
                self.adjList[col - 1].append(Edge(col, 1))
                self.adjList[col].append(Edge(col - 1, 1))

        ## Vertical paths
        for col in range(0, n):
            for row in range(col + n, col + self.V, n):
                self.adjList[row - n].append(Edge(row, 1))
                self.adjList[row].append(Edge(row - n, 1))


        self.applyFloyd()


def custom_graph_serializer(graph: Graph) -> str:

    if not hasattr(graph, "digraph"):
        graph.digraph = rx.PyDiGraph()
        graph.digraph.add_nodes_from(range(graph.V))
        for edges in graph.adjList:
            for edge in edges:
                graph.digraph.add_edge(edge.vertex, edges.index(edge), edge.distance)
    return rx.node_link_json(graph.digraph, edge_attrs=lambda x: {"dist": str(x)})


def custom_graph_deserializer(graph_str: str) -> Graph:
    digraph = rx.parse_node_link_json(graph_str, edge_attrs=lambda x: int(x["dist"]))
    V = len(digraph.nodes())
    E = len(digraph.edge_list())
    graph = Graph(V=V, E=E)
    graph.digraph = digraph  
    return graph


# Create a custom Marshmallow field
class CustomGraphField(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        # Use a custom encoder during serialization
        return custom_graph_serializer(value)
    """
    def _deserialize(self, value, attr, data, **kwargs):
        return custom_graph_deserializer(value)
    """
