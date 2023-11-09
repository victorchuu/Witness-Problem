import random
from src.Algorithm import Algorithm
from src.geneticOperators import initial_population, crossover, mutate, localSearch
from src.witnessproblem import fitness


""" Useful function for testing if we are generating invalid routes """
def checkRoutes(graph, population):
    for route in population:
        totalTime = route.time[0]
        for i in range(1, len(route.vertex)):
            totalTime += graph.directDist(route.vertex[i-1],route.vertex[i])
            totalTime += route.time[i]


class GeneticAlgorithm(Algorithm):
        def __init__(self, 
                     mutation = mutate, 
                     crossover = crossover, 
                     fit = fitness, 
                     initialPopulation = initial_population, 
                     localSearch = localSearch,
                     numGenerations = 100, 
                     populationSize = 100, 
                     tournamentParticipants = 4,
                     crossoverRate = 0.7, 
                     mutationProbability = 0.6, 
                     localSearchProb = lambda it, max: (it/max) * 0.2
                     ):
            self.crossover = crossover
            self.mutation = mutation
            self.fitness = fit
            self.initialPopulation = initialPopulation
            self.localSearch = localSearch

            self.numGenerations = numGenerations
            self.populationSize = populationSize
            self.numParents = round(populationSize * crossoverRate)
            self.numParents = int(self.numParents if self.numParents % 2 == 0 else self.numParents - 1)
            self.numSurvivors = self.populationSize - self.numParents
            self.mutationProbability = mutationProbability
            self.localSearchProb = localSearchProb
            self.k = tournamentParticipants
            self.instance = None
        

        def fit(self, individual):    
                return self.fitness(self.instance, individual)
        

        def cross(self, p1, p2):         
            return self.crossover(self.instance, p1, p2)
        

        def runAndReturnGrowthCurve(self, instance):
            self.instance = instance
            population = self.initialPopulation(instance, self.populationSize)
            bestSolutions = [0]
            for i in range(self.numGenerations):    
                population = self.iteration(population, bestSolutions, i)
            return max(bestSolutions), bestSolutions


        def run(self, instance): 
            self.instance = instance
            population = self.initialPopulation(instance, self.populationSize)
            bestSolutions = [0]
            for i in range(self.numGenerations):    
                population = self.iteration(population, bestSolutions, i)
            return max(bestSolutions)


        def iteration(self, population, bestSolutions, i):
            fitnessValues = list(map(self.fit, population))
            bestSolutions.append(max(fitnessValues))

            population,fitnessValues = self.mapLocalSearchWithProbability(population, fitnessValues, self.localSearchProb(i, self.numGenerations))

            survivors = self.tournamentSelection(population, fitnessValues, self.numSurvivors, self.k) 
            parents = self.tournamentSelection(population, fitnessValues,  self.numParents, self.k)
            sons = self.applyCrossover(parents)

            population = self.mapMutateWithProbability(survivors + sons, self.mutationProbability)

            return population


        def tournamentSelection(self, population, fitnessValues, numTournaments, numParticipants):
            chosenPopulation = []
            populationIndex = range(len(population))
            p = 0.7
            for _ in range(numTournaments):
                participantsIndex = random.sample(populationIndex, numParticipants)
                participantsIndex.sort(key = lambda i : -fitnessValues[i])
                pending = True
                for candidateIndex in participantsIndex :
                    if pending and random.uniform(0,1) < p:
                        chosenPopulation.append(population[candidateIndex])
                        pending = False
                        break
                if pending: 
                    chosenPopulation.append(population[participantsIndex[0]])

            return chosenPopulation 


        def applyCrossover(self, parents):
            sons = []
            for i in range(len(parents)//2):
                son1, son2 = self.cross(parents[2*i],parents[2*i+1])
                sons.append(son1)
                sons.append(son2)
            return sons


        def __src__(self) :
            return "Genetic Algorithm:\tpopulationSize: "+str(self.populationSize)+"\tgenerations: "+str(self.numGenerations)+"\tmutationRate: "+str(self.mutationProbability)
        

        def mapMutateWithProbability(self, population, prob):
            return [self.mutation(self.instance, x) if random.uniform(0, 1) < prob else x
                    for x in population ]
        
        
        def mapLocalSearchWithProbability(self, population, fitnessValues, prob):
            return zip(*[self.localSearch(self.instance, x[0], x[1]) if random.uniform(0, 1) < prob else x
                    for x in zip(population,fitnessValues) ])