from .route import Route
from .edge import Edge
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from marshmallow import fields
import rustworkx as rx


INFINITY = 1000000000
NO_VERTEX = -1
LINE_BREAK = '\n'

class Graph:
    
    def __init__(self, digraph: rx.PyDiGraph = rx.PyDiGraph()):
        self.digraph = digraph
        self.V = len(digraph.nodes())
        self.E = len(digraph.edge_list())

    
    def get_adjacents(self, vertex: int) -> list[Edge]:
        return [Edge(vertex=edge[1], distance=edge[2]) for edge in self.digraph.out_edges(vertex)]


    def applyFloyd(self) :
        floyd_distance_matrix, self.floydPath = rx.digraph_floyd_warshall_successor_and_distance(self.digraph, weight_fn = lambda x: x)
        self.bestDistanceMatrix = [[INFINITY if x == float('inf') else int(x) for x in row] for row in floyd_distance_matrix]


    # Returns the distance between two vertices taking the edge that connects them directly
    # Note that this could not be the best distance
    # Expects the 2 inputs to be connected by an edge, or else it will throw an exception
    def directDist(self, u, v):
        return self.digraph.get_edge_data(u, v)
    

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


    def buildShortestPath(self, src, dest):
        path = []

        curr = src
        while curr != dest:
            curr = self.floydPath[curr, dest]
            path.append(curr)
        
        return path

    # Builds a shortest distance route from src to dest, that waits the needed time in the last vertex until it lasts t.
    # Uses Floyd's algorithm path reconstruction
    def buildShortestRoute(self, src, dest, time, route: Route):
        assert route.vertex[-1] == src

        path = self.buildShortestPath(src, dest)

        for vertex in path:
            route.vertex.append(vertex)
            route.time.append(0)
            route.leaveTime.append(route.leaveTime[-1] + self.bestDistanceMatrix[src][vertex])

        if time != 0 :
            route.time[-1] += time - self.bestDistanceMatrix[src][dest]
            route.leaveTime[-1] += time - self.bestDistanceMatrix[src][dest]


    
    def createGridGraph(self, n: int, distance: int):
        self.digraph.add_nodes_from(range(n*n))
        self.V = n*n

        self.E = 2*2*n*(n-1)

        ## Horizontal paths
        for row in range(0, self.V, n):
            for col in range(row + 1, row + n):
                self.digraph.add_edge(col - 1, col, distance)
                self.digraph.add_edge(col, col - 1, distance)
        ## Vertical paths
        for col in range(0, n):
            for row in range(col + n, col + self.V, n):
                self.digraph.add_edge(row - n, row, distance)
                self.digraph.add_edge(row, row - n, distance)

        self.applyFloyd()


def custom_graph_serializer(graph: Graph) -> str:

    if not hasattr(graph, "digraph"):
        graph.digraph = rx.PyDiGraph()
        graph.digraph.add_nodes_from(range(graph.V))
        for vertex, adjacentEdges in enumerate(graph.adjList):
            for edge in adjacentEdges:
                graph.digraph.add_edge(vertex, edge.vertex, edge.distance)
    return rx.node_link_json(graph.digraph, edge_attrs=lambda x: {"dist": str(x)})


def custom_graph_deserializer(graph_str: str) -> Graph:
    digraph = rx.parse_node_link_json(graph_str, edge_attrs=lambda x: int(x["dist"]))
    return Graph(digraph=digraph)


# Create a custom Marshmallow field
class CustomGraphField(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        # Use a custom encoder during serialization
        return custom_graph_serializer(value)
    
    def _deserialize(self, value, attr, data, **kwargs):
        return custom_graph_deserializer(value)
