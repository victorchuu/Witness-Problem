from typing import List
import csv
import datetime
import matplotlib.pyplot as plt
from src.geneticOperators import initial_population_with_greedy

from src.witnessproblem import Instance
from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm

 
def transposeCSV(input_file: str):
    with open(input_file, 'r') as infile:
        csv_data = [line.strip().split(',') for line in infile]

    transposed_data = list(map(list, zip(*csv_data)))

    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(transposed_data)


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


def executeAlgorithms(algorithms, filename, getDataGatherer, suffix='', startIn=0, endIn=-1):
    output_file = 'solutions/' + filename + suffix + '.csv'

    with open('instances/' + filename + '.txt') as inFile, getDataGatherer(output_file, filename, algorithms) as dataGatherer:

        print(f"Starting Execution at {datetime.datetime.now().strftime('%H:%M:%S')}")

        instances: list[Instance] = Instance.schema().loads(inFile.readline(), many=True)

        for i, instance in enumerate(instances):

            if i < startIn:
                continue
            if i == endIn:
                break

            dataGatherer.start(instance)
            instance.graph.applyFloyd()

            override_initial_pop = initial_population_with_greedy(instance, 150)
            for alg, repetitions in algorithms:
                dataGatherer.record_algorithm_data(alg, instance, override_initial_pop, repetitions)
                
            dataGatherer.write_data(i)
            print(f"Finished instance #{i} at {datetime.datetime.now().strftime('%H:%M:%S')}")

    transposeCSV(output_file)
    
