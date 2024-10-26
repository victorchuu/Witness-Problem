from typing import List
import csv
import time
import datetime
import matplotlib.pyplot as plt
from src.geneticOperators import initial_population_with_greedy

from src.witnessproblem import fitness
from src.witnessproblem.route import Route
from src.witnessproblem import Instance
from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm

 
def transposeCSV(input_file: str):
    with open(input_file, 'r') as infile:
        csv_data = [line.strip().split(',') for line in infile]

    transposed_data = list(map(list, zip(*csv_data)))

    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(transposed_data)


def executeAlgorithmsToCSV(algorithms, filename, suffix='', startIn=0, endIn=-1):
    output_file = 'solutions/' + filename + suffix + '.csv'
    with open('instances/' + filename + '.txt') as inFile, open(output_file,'w') as outFile :
        writer = csv.writer(outFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([filename] + [str(alg[0]) for alg in algorithms])
        print(f"Starting Execution at {datetime.datetime.now().strftime('%H:%M')}")

        num_instances = int(inFile.readline())
        for i in range(num_instances):
            instance = Instance()
            instance.readFromFile(inFile) 
            if i < startIn:
                continue
            if i == endIn:
                break

            meanSolutions = list()
            maxSolutions = list()
            elapsedTime = list()
            override_initial_pop = initial_population_with_greedy(instance, 150)
            print("Calculated the initial population")
            for alg, repetitions in algorithms:
                startTime = time.time()
                print("-",end='')
                solution = list()
                for _ in range(repetitions):
                    sol, _ = alg.run(instance, override_initial_pop=override_initial_pop)
                    solution.append(sol)
                meanSolutions.append(sum(solution)/repetitions)
                maxSolutions.append(max(solution))
                elapsedTime.append((time.time() - startTime)/repetitions)
                
            writer.writerow([f"Mean #{i}"] + meanSolutions)
            writer.writerow([f"Max #{i}"] + maxSolutions)
            writer.writerow([f"Time #{i}"] + elapsedTime)
            print(f"Finished instance #{i} at {datetime.datetime.now().strftime('%H:%M')} with means {meanSolutions} and max {maxSolutions}")

    transposeCSV(output_file)
    return solution


def executeAlgorithmsGraph(algorithms: List[GeneticAlgorithm], filename, legend):
    with open('instances/' + filename + '.txt') as inFile:
        casos = int(inFile.readline())
        solution = list()
        for _ in range(casos):
            instance = Instance()
            instance.readFromFile(inFile)  
            for alg in algorithms :
                _,growthCurve = alg.runAndReturnGrowthCurve(instance)
                solution.append(growthCurve)
        for j in range(len(solution)):
            plt.plot(solution[j][1:], label=f"{legend[j]}")
            plt.legend()


def executeAlgorithmsRealCaseToCSV(algorithms, filename, end_vertices, suffix='', startIn=0):
    output_file = 'solutions/' + filename + suffix + '.csv'

    with open('instances/' + filename + '.txt') as inFile, \
         open('solutions/' + filename + '.txt') as correctRouteFile, \
         open(output_file,'w') as outFile :
        writer = csv.writer(outFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([filename] + [str(alg[0]) for alg in algorithms])
        print(f"Starting Execution at {datetime.datetime.now().strftime('%H:%M')}")

        num_instances = int(inFile.readline())
        for i in range(num_instances):
            instance = Instance()
            instance.readFromFile(inFile)
            
            instance_parameters = [float(x) for x in correctRouteFile.readline().split()]
            actor_route = Route()
            actor_route.readFromFile(correctRouteFile)
            if i < startIn:
                continue

            meanSolutions = list()
            maxSolutions = list()
            meanEndVertexHits = list()
            elapsedTime = list()
            override_initial_pop = initial_population_with_greedy(instance, 150)
            print("Calculated the initial population")
            correct_end_vertex = actor_route.vertex[-1]

            for alg, repetitions in algorithms:
                startTime = time.time()
                print("-",end='')
                solution = list()
                end_vertex_hits = list()
                for _ in range(repetitions):
                    sol, route = alg.run(instance, override_initial_pop=override_initial_pop)
                    solution.append(sol)
                    algorithm_end_vertex = route.vertex[-1]
                    distance_to_correct_end_vertex = instance.graph.bestDist(algorithm_end_vertex, correct_end_vertex)
                    is_correct_end_vertex = 1 == sum(\
                        map(lambda end_vertex: distance_to_correct_end_vertex >= instance.graph.bestDist(algorithm_end_vertex, end_vertex),end_vertices))
                    end_vertex_hits.append(1 if is_correct_end_vertex else 0)

                meanSolutions.append(sum(solution)/repetitions)
                maxSolutions.append(max(solution))
                meanEndVertexHits.append(sum(end_vertex_hits)/repetitions)
                elapsedTime.append((time.time() - startTime)/repetitions)

            original_fitness = fitness(instance, actor_route)
                
            writer.writerow([f"Mean ({instance_parameters[0]}; {int(instance_parameters[1])})"] + meanSolutions)
            writer.writerow([f"Max ({instance_parameters[0]}; {int(instance_parameters[1])})"] + maxSolutions)
            writer.writerow([f"Mean hits ({instance_parameters[0]}; {int(instance_parameters[1])})"] + meanEndVertexHits)
            writer.writerow([f"real fitness ({instance_parameters[0]}; {int(instance_parameters[1])})"] + [original_fitness for _ in maxSolutions])
            writer.writerow([f"Time ({instance_parameters[0]}; {int(instance_parameters[1])})"] + elapsedTime)
            print(f"Finished instance ({instance_parameters[0]}; {int(instance_parameters[1])}) at {datetime.datetime.now().strftime('%H:%M')} with means {meanSolutions} and max {maxSolutions}")

    transposeCSV(output_file)
