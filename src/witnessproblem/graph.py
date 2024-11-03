from .route import Route
from .edge import Edge
from dataclasses import dataclass
from dataclasses_json import dataclass_json


INFINITY = 1000000000
NO_VERTEX = -1
LINE_BREAK = '\n'

@dataclass_json
@dataclass
class Graph :
    V: int
    E: int
    adjList: list[list[Edge]]
    
    def __init__(self, V = 0, E = 0, adjList = [[Edge]]):
        self.V = V
        self.E = E
        self.adjList = adjList
        self.realDist = [[int]]

        # Shortest distance (and its path) between any pair of vertices, calulated with Floyd's algorithm
        self.bestDistanceMatrix = [[int]] 
        self.floydPath = [[int]]
                

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
    

    def readFromFile(self, file) :
        
        line = file.readline().split()
        self.V, self.E = int(line[0]), int(line[1])

        self.adjList = [[] for _ in range(self.V)]

        for _ in range(self.E):
            line = file.readline().split()
            (source, destiny, distance) = map(int, line)

            if source >= self.V or destiny >= self.V or distance <= 0:
                raise Exception(f"wrong graph, edge: {source} --> {destiny,} ({distance})")
            self.adjList[source].append(Edge(destiny, distance))

        self.applyFloyd()


    def writeToFile(self) :
        string = f"{self.V} {self.E}"
        if self.E :
            string += LINE_BREAK

        return string + LINE_BREAK.join([f"{source} {edge.vertex} {edge.distance}" for source, edgesList in enumerate(self.adjList) for edge in edgesList]) + LINE_BREAK


    # Prints the matrix in a more human-readable way
    def __str__(self) : 
        string = f"Vertices: {self.V}, Edges: {self.E}\n"
        for source in range(len(self.adjList)) :
            for edge in self.adjList[source] :
                string += f"{source} --> {edge.vertex} ({edge.vertex})\n"
        return string
    
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


            