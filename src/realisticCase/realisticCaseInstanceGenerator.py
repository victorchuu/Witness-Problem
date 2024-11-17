from src.witnessproblem import Graph, Instance, Route, Testimony, generateIntervalTestimonies, generateNegativeTestimonies
from src.geneticOperators import appendRandomRoute, NO_VERTEX_SELECTED

import random

STREET_DISTANCE = 1

MOVING_INDIVIDUALS = 10
PARTNERS_IN_CRIME = 3


class RealisticCaseInstanceGenerator:

    def __init__(self, 
                 base_similarity = 0.2, 
                 grid_size: int = 7, 
                 static_witnesses = 20, 
                 lying_witnesses = 0,
                 testimonies_per_lying_witness = 3):
        self.BASE_SIMILARITY = base_similarity
        self.GRID_SIZE = grid_size
        self.STATIC_WITNESSES = static_witnesses
        self.LYING_WITNESSES = lying_witnesses
        self.TESTIMONIES_PER_LYING_WITNESS = testimonies_per_lying_witness
        assert self. GRID_SIZE % 2 == 1

        

    def generate_actor_route(self, graph, startAt, endAt):
        self.maxTime = random.randint(self.GRID_SIZE, 2*self.GRID_SIZE)

        actor_route = Route()
        actor_route.startAt(startAt)
        appendRandomRoute(graph, endAt, self.maxTime, actor_route)
        return actor_route


    def get_random_route(self, graph):
        random_route = Route()
        appendRandomRoute(graph, NO_VERTEX_SELECTED, self.maxTime, random_route)
        return random_route


    def calculateSimilarity(self, index: int):
        return self.BASE_SIMILARITY / (2**(index))


    def generateTestimonies(self, actor_route: Route, moving_individuals: list[(Route, int)], vertex: int):
        # Generate correct testimonies
        testimonies = generateIntervalTestimonies(actor_route, vertex, 0, self.maxTime, probability=0.95)

        # Generate unintentonally wrong testimonies, caused by mistakes with similar individuals
        for (route, similarity) in moving_individuals:
            noise_testimonies = generateIntervalTestimonies(route, vertex, 0, self.maxTime, probability=similarity)
            testimonies.extend(noise_testimonies)

        # Fill the blanks with negative testimonies
        return testimonies + generateNegativeTestimonies(testimonies, vertex, 0, self.maxTime)
    

    def generateRandomTestimony(self, graph):
        a = random.randint(0, self.maxTime)
        b = random.randint(0, self.maxTime)
        if a > b:
            a,b = b,a

        vertex = random.randint(0, graph.V-1)

        return Testimony([vertex], a, b)


    def generateInstance(self):
        # Cenerate Grid graph
        graph = Graph()
        graph.createGridGraph(self.GRID_SIZE, STREET_DISTANCE)

        # Generate actor's route, starting from the center and finishing in one corner of the map
        center = self.GRID_SIZE**2//2
        corners = [0, self.GRID_SIZE-1, self.GRID_SIZE**2-1, self.GRID_SIZE**2-self.GRID_SIZE]
        end_vertex = random.choice(corners)
        actor_route = self.generate_actor_route(graph, startAt=center, endAt=end_vertex)

        # Generate witnesses
        truthtelling_witnesses = self.STATIC_WITNESSES - self.LYING_WITNESSES

        static_witness_vertices = random.sample(range(graph.V - 1), truthtelling_witnesses)
        moving_individuals = [(self.get_random_route(graph), self.calculateSimilarity(index)) for index in range(MOVING_INDIVIDUALS)]
        testimoniesByWitness = [self.generateTestimonies(actor_route, moving_individuals, vertex) for vertex in static_witness_vertices]\
            + [[self.generateRandomTestimony(graph) for _ in range(self.TESTIMONIES_PER_LYING_WITNESS)] for _ in range(self.LYING_WITNESSES)]
        
        # getCenterTestimony = lambda : Testimony([center], 0, 0)
        # testimoniesByWitness = [[getCenterTestimony()] + tests for tests in testimoniesByWitness]

        instance = Instance(graph, testimoniesByWitness)

        return instance, actor_route