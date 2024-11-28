import sys
import time

import src.geneticAlgorithm.algorithmTestUtils as tst
from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm
from src.solutions.greedy import GreedyDistance, GreedyTestimonies, PersistentGreedyAlgorithm
from src.solutions.optimal.optimalSolution import SearchAlgorithm
from src.geneticAlgorithm.algorithmDataGatherer import CSVDataGatherer

if len(sys.argv) < 4:
    print('Usage: python runRealCase.py <startIn> <endIn> <filename> [algorithms]')
    exit()

startIn = int(sys.argv[1])
endIn = int(sys.argv[2])
filename = sys.argv[3]

print(f"Start in: {startIn}, End in: {endIn}")
if endIn <= startIn:
    print("ERROR: End must be greater than start")
    exit()

INSTANCE_SETS = {'I1','I2','I3','I4','I5','I6','I7','I8','I9','I10'}

# If filename is not a valid instance set, exit
if filename not in INSTANCE_SETS:
    print("ERROR: Invalid filename")
    exit()

RUN_ONCE = 1
RUNS_PER_INSTANCE = 10
SECONDS_PER_INSTANCE = 20

GENETIC_ALGORITHMS = [
    (GeneticAlgorithm(populationSize=150, numGenerations=100, mutationProbability=0.651, crossoverRate=0.8321, localSearchProb=lambda x,y: 0), RUNS_PER_INSTANCE),
    (GeneticAlgorithm(populationSize=150, numGenerations=100, mutationProbability=0.7194,crossoverRate=0.7344, localSearchProb=lambda step,totalSteps: step/totalSteps * 0.2104), RUNS_PER_INSTANCE),]


TIMED_GENETIC_ALGORITHMS = [
    (GeneticAlgorithm(populationSize=150, numGenerations=100, mutationProbability=0.651, crossoverRate=0.8321, localSearchProb=lambda x,y: 0, stop_condition=lambda _,start_time: time.time() - start_time > SECONDS_PER_INSTANCE), RUNS_PER_INSTANCE),
    (GeneticAlgorithm(populationSize=150, numGenerations=100, mutationProbability=0.7194,crossoverRate=0.7344, localSearchProb=lambda step,totalSteps: step/totalSteps * 0.2104, stop_condition=lambda _,start_time: time.time() - start_time > SECONDS_PER_INSTANCE), RUNS_PER_INSTANCE),]

GREEDY_ALGORITHMS = [
    (PersistentGreedyAlgorithm(GreedyDistance()), RUN_ONCE),
    (GreedyTestimonies(), RUNS_PER_INSTANCE),
]

EXACT_ALGORITHMS = [(SearchAlgorithm(), RUN_ONCE)]

used_algorithms = []

for algorithm in sys.argv[4:]:
    if algorithm == 'genetic':
        used_algorithms.extend(GENETIC_ALGORITHMS)
    elif algorithm == 'timed-genetic':
        used_algorithms.extend(TIMED_GENETIC_ALGORITHMS)
    elif algorithm == 'greedy':
        used_algorithms.extend(GREEDY_ALGORITHMS)
    elif algorithm == 'exact':
        used_algorithms.extend(EXACT_ALGORITHMS)
    else:
        print(f"ERROR: Invalid algorithm name '{algorithm}'. possible values are 'genetic', 'timed-genetic', 'greedy' and 'exact'")

print(f"Using algorithms: {used_algorithms}")
tst.executeAlgorithms(used_algorithms, filename, CSVDataGatherer, suffix=f'-{startIn}-{endIn}', startIn=startIn, endIn=endIn)
