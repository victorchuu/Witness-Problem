import random
from src.witnessproblem import Edge, Instance, Testimony


class RandomInstanceGenerator:


    def __init__(self,
                 vertices = 10, 
                 avg_vertex_degree = 4,
                 max_vertex_distance = 9, 
                 undirected_graph = True,
                 witnesses = 20, 
                 max_testimonies_per_witness = 1,
                 max_time_window = 24, 
                 max_interval_length = 5, 
                 max_vertices_per_testimony = 1, 
                 negative_testimonies_rate = 0
                 ):
        
        self.vertices = vertices

        # For undirected graphs, one undirected edge counts as two directed edges, one in each direction
        self.directed_edges = vertices * avg_vertex_degree
        assert self.directed_edges <= vertices*(vertices-1)
        self.max_vertex_distance = max_vertex_distance
        self.undirected_graph = undirected_graph

        self.max_time_window = max_time_window

        self.witnesses = witnesses
        self.max_testimonies_per_witness = max_testimonies_per_witness
        self.max_interval_length = max_interval_length
        self.max_vertices_per_testimony = max_vertices_per_testimony
        self.negative_testimonies_rate = negative_testimonies_rate

    
    def create(self, fileName, numCases):
        string = str(numCases) + '\n'
        for _ in range(numCases) :
            instance = Instance()
            self.randomInstance(instance)
            string += instance.writeToFile()

        with open('instances/' + fileName,'w') as f:
            f.write(string)


    def randomInstance(self, instance: Instance):
        self.random_graph(instance.graph)
        self.random_witnesses(instance)


    def random_graph(self, graph):
        graph.V = self.vertices
        graph.adjList = [[] for _ in range(self.vertices)]
        graph.E = self.directed_edges
        if self.undirected_graph and graph.E % 2 == 1 :
            graph.E += 1

        i = 0
        while i < graph.E :
            u = random.randint(0, self.vertices - 1)
            v = random.randint(0, self.vertices - 1)

            invalid_edge = u == v or any(edge.vertex == v for edge in graph.adjList[u])
            if invalid_edge: 
                continue

            distance = random.randint(1, self.max_vertex_distance)
            i += 1
            graph.adjList[u].append(Edge(v,distance))
            if(self.undirected_graph) :
                i += 1
                graph.adjList[v].append(Edge(u,distance))

    
    def random_witnesses(self, instance) :
        actual_vertices_per_testimony = min(instance.graph.V, self.max_vertices_per_testimony)
        instance.testimoniesByWitness = [[] for _ in range(self.witnesses)]

        for witness in range(self.witnesses) :
            num_testimonies = random.randint(1 , self.max_testimonies_per_witness)

            instance.testimoniesByWitness[witness] = []

            for i in range(num_testimonies) :
                interval_length = random.randint(0, self.max_interval_length)
                a = random.randint(0, self.max_time_window - interval_length)
                b = a + interval_length
                instance.testimoniesByWitness[witness].append(self.randomTestimony(instance.graph.V, a, b,actual_vertices_per_testimony))
                instance.maxTime = max(instance.maxTime, b)
        

    def randomTestimony(self, totalVertices, a, b, vertices_per_testimony) :
        num_vertices = random.randint(1 , vertices_per_testimony)
        return Testimony(
            vertices=random.sample(list(range(totalVertices)), num_vertices),
            a = a,
            b = b,
            negative = random.uniform(0, 1) < self.negative_testimonies_rate
        )


I1 = RandomInstanceGenerator(
    vertices = 15,
    avg_vertex_degree = 5, 
    max_vertex_distance = 5, 
    witnesses = 50, 
    max_testimonies_per_witness = 1, 
    max_time_window =  12, 
    max_interval_length = 4, 
    max_vertices_per_testimony = 1, 
    negative_testimonies_rate = 0
    )

I2 = RandomInstanceGenerator(
    vertices = 20, 
    avg_vertex_degree = 5, 
    max_vertex_distance = 5, 
    witnesses = 250, 
    max_testimonies_per_witness = 2, 
    max_time_window = 12, 
    max_interval_length = 10, 
    max_vertices_per_testimony = 2, 
    negative_testimonies_rate = 0
    )


I3 = RandomInstanceGenerator(
    vertices = 100, 
    avg_vertex_degree = 10, 
    max_vertex_distance = 10, 
    witnesses = 500, 
    max_testimonies_per_witness = 2, 
    max_time_window = 200, 
    max_interval_length = 10, 
    max_vertices_per_testimony = 5, 
    negative_testimonies_rate = 0
    )

I4 = RandomInstanceGenerator(
    vertices = 500, 
    avg_vertex_degree = 10, 
    max_vertex_distance = 10, 
    witnesses = 250, 
    max_testimonies_per_witness = 2, 
    max_time_window = 500, 
    max_interval_length = 20, 
    max_vertices_per_testimony = 5, 
    negative_testimonies_rate = 0
    )