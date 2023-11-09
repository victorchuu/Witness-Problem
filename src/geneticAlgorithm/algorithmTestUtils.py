from typing import List
import csv
import time
import datetime
import matplotlib.pyplot as plt

from src.witnessproblem import Instance
from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm

 
def transposeCSV(input_file: str):
    with open(input_file, 'r') as infile:
        csv_data = [line.strip().split(',') for line in infile]

    transposed_data = list(map(list, zip(*csv_data)))

    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(transposed_data)


def executeAlgorithmsToCSV(algorithms, filename, suffix='', startIn=0):
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

            meanSolutions = list()
            maxSolutions = list()
            elapsedTime = list()
            for alg, repetitions in algorithms:
                startTime = time.time()
                solution = list()
                for _ in range(repetitions):
                    solution.append(alg.run(instance))
                meanSolutions.append(sum(solution)/repetitions)
                maxSolutions.append(max(solution))
                elapsedTime.append((time.time() - startTime)/repetitions)
                
            writer.writerow([f"Mean #{i}"] + meanSolutions)
            writer.writerow([f"Max #{i}"] + maxSolutions)
            writer.writerow([f"Time #{i}"] + elapsedTime)
            print(f"Finished instance #{i} at {datetime.datetime.now().strftime('%H:%M')}")

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
