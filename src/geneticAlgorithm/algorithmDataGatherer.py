from abc import ABC, abstractmethod
import csv
import time

from src.realisticCase import RealisticCaseSolutionData
from src.witnessproblem import fitness, Route


class AlgorithmDataGatherer(ABC):

    @abstractmethod
    def __enter__(self):
        pass    

    @abstractmethod
    def start(self, instance):
        pass


    @abstractmethod
    def record_algorithm_data(self, algorithm, instance, override_initial_pop, repetitions):
        pass

    @abstractmethod
    def write_data(self, index):
        pass
        
    @abstractmethod
    def __exit__(self):
        pass


class CSVDataGatherer(AlgorithmDataGatherer):


    def __init__(self, output_file, instance_name, algorithms):
        self.output_file = output_file
        self.instance_name = instance_name
        self.algorithms = algorithms


    def __enter__(self):        
        self.outFile = open(self.output_file,'w')
        self.writer = csv.writer(self.outFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow([self.instance_name] + [str(alg[0]) for alg in self.algorithms])
        return self

    
    def start(self, instance):
        self.meanSolutions = list()
        self.maxSolutions = list()
        self.elapsedTime = list()


    def record_algorithm_data(self, algorithm, instance, override_initial_pop, repetitions):

        startTime = time.time()
        print("-",end='')
        solutions = list()
        for _ in range(repetitions):
            sol, _ = algorithm.run(instance, override_initial_pop=override_initial_pop)
            solutions.append(sol)

        self.meanSolutions.append(sum(solutions)/repetitions)
        self.maxSolutions.append(max(solutions))
        self.elapsedTime.append((time.time() - startTime)/repetitions)


    def write_data(self, index):
        self.writer.writerow([f"Mean #{index}"] + self.meanSolutions)
        self.writer.writerow([f"Max #{index}"] + self.maxSolutions)
        self.writer.writerow([f"Time #{index}"] + self.elapsedTime)
        
        
    def __exit__(self, x,y,z):
        self.outFile.close()




class RealisticInstanceDataGatherer(AlgorithmDataGatherer):


    def __init__(self, output_file, instance_name, algorithms, end_vertices):
        self.output_file = output_file
        self.instance_name = instance_name
        self.algorithms = algorithms
        self.end_vertices = end_vertices


    def __enter__(self):        
        self.outFile = open(self.output_file,'w')
        self.writer = csv.writer(self.outFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.writer.writerow([self.instance_name] + [str(alg[0]) for alg in self.algorithms])
        
        with open('solutions/' + self.instance_name + '.txt') as file:
            self.correctRoutes = iter(RealisticCaseSolutionData.schema().loads(file.readline(), many=True))
        return self

    
    def start(self, instance):
        self.meanSolutions = list()
        self.maxSolutions = list()
        self.meanEndVertexHits = list()
        self.elapsedTime = list()

        self.solution = next(self.correctRoutes)
        actor_route = self.solution.actor_route

        self.correct_end_vertex = actor_route.vertex[-1]
        self.original_fitness = fitness(instance, actor_route)


    def record_algorithm_data(self, algorithm, instance, override_initial_pop, repetitions):

        startTime = time.time()
        print("-",end='')
        solution = list()
        end_vertex_hits = list()
        for _ in range(repetitions):
            sol, route = algorithm.run(instance, override_initial_pop=override_initial_pop)
            solution.append(sol)
            algorithm_end_vertex = route.vertex[-1]
            distance_to_correct_end_vertex = instance.graph.bestDist(algorithm_end_vertex, self.correct_end_vertex)
            is_correct_end_vertex = 1 == sum(\
                map(lambda end_vertex: distance_to_correct_end_vertex >= instance.graph.bestDist(algorithm_end_vertex, end_vertex), self.end_vertices))
            end_vertex_hits.append(1 if is_correct_end_vertex else 0)

        self.meanSolutions.append(sum(solution)/repetitions)
        self.maxSolutions.append(max(solution))
        self.meanEndVertexHits.append(sum(end_vertex_hits)/repetitions)
        self.elapsedTime.append((time.time() - startTime)/repetitions)

    def write_data(self, index):
        self.writer.writerow([f"Mean ({self.solution.base_similarity}; {int(self.solution.lying_witnesses)})"] + self.meanSolutions)
        self.writer.writerow([f"Max ({self.solution.base_similarity}; {int(self.solution.lying_witnesses)})"] + self.maxSolutions)
        self.writer.writerow([f"Mean hits ({self.solution.base_similarity}; {int(self.solution.lying_witnesses)})"] + self.meanEndVertexHits)
        self.writer.writerow([f"real fitness ({self.solution.base_similarity}; {int(self.solution.lying_witnesses)})"] + [self.original_fitness for _ in self.maxSolutions])
        self.writer.writerow([f"Time ({self.solution.base_similarity}; {int(self.solution.lying_witnesses)})"] + self.elapsedTime)
        
    def __exit__(self, x,y,z):
        self.outFile.close()
