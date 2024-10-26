#!/Users/victor/opt/anaconda3/envs/witness/bin/python

import datetime
import sys

SELECTED_POPULATION = 150

from src.geneticAlgorithm.geneticAlgorithm import GeneticAlgorithm
from src.witnessproblem import Instance

def executeOnInstance(filename, mutationProb, crossoverRate):

    algorithm = GeneticAlgorithm(
        numGenerations = 100, 
        populationSize = SELECTED_POPULATION, 
        mutationProbability = mutationProb,
        crossoverRate = crossoverRate,
        localSearchProb = lambda a,b: 0,
    )

    with open(filename) as inFile:
        num_instances = int(inFile.readline())

        if num_instances != 1:
            raise "ExecuteOnInstance only supports files with once instance for now!"

        instance = Instance()
        instance.readFromFile(inFile) 

        return -algorithm.run(instance)


# Useful function to print errors.
def target_runner_error(msg):
    now = datetime.datetime.now()
    print(str(now) + " [MY ERROR]: " + msg)
    sys.exit(1)

if __name__=='__main__':

    if len(sys.argv) < 5:
        print("\nUsage: ./target-runner.py <configuration_id> <instance_id> <seed> <instance_path_name> <list of parameters>\n")
        sys.exit(1)

    # Get the parameters as command line arguments.
    configuration_id = sys.argv[1]
    instance_id = sys.argv[2]
    seed = sys.argv[3]
    instance = sys.argv[4]
    cand_params = sys.argv[5:]

    mutationProb = None
    crossoverRate = None    
    maxLocalSearchProb = None
    while cand_params:
        param = cand_params.pop(0)
        value = cand_params.pop(0)

        if param == "--mutationProb":
            mutationProb = float(value)
        elif param == "--crossoverRate":
            crossoverRate = float(value)
        # elif param == "--maxLocalSearchProb":
        #     maxLocalSearchProb = float(value)
        else:
            target_runner_error("unknown parameter %s" % (param))
    
    if mutationProb == None:
        target_runner_error("--mutationProb parameter must be selected")
    if crossoverRate == None:
        target_runner_error("--crossoverRate parameter must be selected")
    # if maxLocalSearchProb == None:
    #     target_runner_error("--maxLocalSearchProb parameter must be selected")



    output = executeOnInstance(
        filename=instance,
        mutationProb=mutationProb,
        crossoverRate=crossoverRate,
        # maxLocalSearchProb=maxLocalSearchProb    
    )
    print(output)

    sys.exit(0)


