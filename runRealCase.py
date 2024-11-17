import sys

from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm
from src.solutions.greedy import GreedyDistance, GreedyTestimonies, PersistentGreedyAlgorithm
import src.geneticAlgorithm.algorithmTestUtils as tst
from src.geneticAlgorithm.algorithmDataGatherer import RealisticInstanceDataGatherer

if len(sys.argv) < 3:
    print('Usage: python runRealCase.py <startIn> <endIn>')
    exit()

startIn = int(sys.argv[1])
endIn = int(sys.argv[2])

print(f"Start in: {startIn}, End in: {endIn}")
if endIn <= startIn:
    print("ERROR: End must be greater than start")
    exit()

GRID_SIZE = 9
FILENAME = 'realCase'
RUNS_PER_INSTANCE = 10
RUN_ONCE = 1

genetic_algorithms = [
    (PersistentGreedyAlgorithm(GreedyDistance()), RUN_ONCE),
    (GreedyTestimonies(), RUNS_PER_INSTANCE),
    (GeneticAlgorithm(populationSize=150, numGenerations = 100, mutationProbability=0.651 , crossoverRate=0.8321, localSearchProb=lambda x,y: 0), RUNS_PER_INSTANCE),
    (GeneticAlgorithm(populationSize=150, numGenerations = 100, mutationProbability=0.7194, crossoverRate=0.7344, localSearchProb=lambda step,totalSteps: step/totalSteps * 0.2104), RUNS_PER_INSTANCE)
]

corners = [0, GRID_SIZE-1, GRID_SIZE**2-1, GRID_SIZE**2-GRID_SIZE]
getDataGatherer = lambda a,b,c: RealisticInstanceDataGatherer(a,b,c,end_vertices=corners)
tst.executeAlgorithms(genetic_algorithms, FILENAME, getDataGatherer, suffix=f'-{startIn}-{endIn}', startIn=startIn, endIn=endIn)
