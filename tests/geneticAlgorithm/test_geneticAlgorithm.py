import unittest
from unittest.mock import Mock, patch

from src.geneticAlgorithm import GeneticAlgorithm


POPULATION = ['individual1', 'individual2', 'individual3']
POPULATION_FITNESS = [1, 3, 1]
LOCAL_SEARCH_POPULATION = ['i1', 'i2', 'i3']
LOCAL_SEARCH_FITNESS = [4, 5, 6]
SURVIVORS, PARENTS = ['survivor1'], ['p1', 'p2']
SONS = ['son1', 'son2']
MUTATED_POPULATION = ['m1', 'm2', 'm3']


def mock_iteration():
    genetic_algorithm = GeneticAlgorithm()
    genetic_algorithm.fit = Mock()
    genetic_algorithm.fit.side_effect = POPULATION_FITNESS

    genetic_algorithm.mapLocalSearchWithProbability = Mock()
    genetic_algorithm.mapLocalSearchWithProbability.return_value = LOCAL_SEARCH_POPULATION, LOCAL_SEARCH_FITNESS
    
    genetic_algorithm.tournamentSelection = Mock()
    genetic_algorithm.tournamentSelection.side_effect = SURVIVORS, PARENTS

    genetic_algorithm.applyCrossover = Mock()
    genetic_algorithm.applyCrossover.return_value = SONS

    genetic_algorithm.mapMutateWithProbability = Mock()
    genetic_algorithm.mapMutateWithProbability.return_value = MUTATED_POPULATION

    return genetic_algorithm




class TestGeneticAlgorithm(unittest.TestCase):

 
    def test_fit_calls_fitness_method_and_returns_output(self):
        # Arrange
        mock_fit = Mock()
        mock_fit.return_value = 'result'
        genetic_algorithm = GeneticAlgorithm(fit=mock_fit)
        genetic_algorithm.instance = 'instance'
    
        # Act
        result = genetic_algorithm.fit('individual')
        
        # Assert
        mock_fit.assert_called_with('instance', 'individual')
        self.assertEqual(result, 'result')


    def test_cross_calls_crossover_method_and_returns_output(self):
        # Arrange
        mock_crossover = Mock()
        mock_crossover.return_value = 'result'
        genetic_algorithm = GeneticAlgorithm(crossover=mock_crossover)
        genetic_algorithm.instance = 'instance'
    
        # Act
        result = genetic_algorithm.cross('p1', 'p2')
        
        # Assert
        mock_crossover.assert_called_with('instance', 'p1', 'p2')
        self.assertEqual(result, 'result')

    
    def test_applyCrossover_calls_cross_method_for_each_pair_of_parents(self):
        # Arrange
        genetic_algorithm = GeneticAlgorithm()
        genetic_algorithm.crossover = Mock()
        genetic_algorithm.crossover.return_value = ('son', 'son')
        genetic_algorithm.instance = 'instance'
        parents = ['p1', 'p2', 'p3', 'p4']
    
        # Act
        sons = genetic_algorithm.applyCrossover(parents)
        
        # Assert
        genetic_algorithm.crossover.assert_any_call('instance', 'p1', 'p2')
        genetic_algorithm.crossover.assert_any_call('instance', 'p3', 'p4')
        self.assertEqual(genetic_algorithm.crossover.call_count, 2)

        self.assertEqual(sons, ['son', 'son', 'son', 'son'])


    @patch('random.uniform')
    def test_mapMutateWithProbability_calls_mutate_method_for_each_individual(self, mock_random):
        # Arrange
        genetic_algorithm = GeneticAlgorithm()
        genetic_algorithm.mutation = Mock()
        genetic_algorithm.mutation.return_value = 'mutation'

        population = ['individual1', 'individual2', 'individual3']
        MUTATION_PROBABILITY = 0.5
        mock_random.side_effect = [0.1, 0.6, 0.4]

        # Act
        mutated_population = genetic_algorithm.mapMutateWithProbability(population, MUTATION_PROBABILITY)

        # Assert
        self.assertEqual(genetic_algorithm.mutation.call_count, 2)
        self.assertEqual(mutated_population, ['mutation', 'individual2', 'mutation'])
        
    """
    Tests that the method receives 
        - An array of individuals
        - An array with their fitness values
        - A probability of local search p
    and returns an array of individuals, with the local search applied with probability p
    """
    @patch('random.uniform')
    def test_mapLocalSearchWithProbability(self, mock_random):
        # Arrange
        genetic_algorithm = GeneticAlgorithm()
        genetic_algorithm.localSearch = Mock()
        genetic_algorithm.localSearch.return_value = 'better_individual', 'fitness'
        genetic_algorithm.instance = 'instance'

        population = ['individual1', 'individual2', 'individual3']
        fitness_values = [1, 2, 3]
        PROBABILITY = 0.5
        mock_random.side_effect = [0.1, 0.6, 0.4]

        # Act
        mutated_population, new_fitness_values = genetic_algorithm.mapLocalSearchWithProbability(population, fitness_values, PROBABILITY)

        # Assert
        self.assertEqual(genetic_algorithm.localSearch.call_count, 2)
        genetic_algorithm.localSearch.assert_any_call('instance', 'individual1', 1)
        genetic_algorithm.localSearch.assert_any_call('instance', 'individual3', 3)

        self.assertEqual(mutated_population, ('better_individual', 'individual2', 'better_individual'))
        self.assertEqual(new_fitness_values, ('fitness', 2, 'fitness'))



    def test_iteration_finds_the_best_individual(self):
        # Arrange
        genetic_algorithm = mock_iteration()

        best_solutions = [2]

        # Act
        _, best_individual = genetic_algorithm.iteration(POPULATION, best_solutions, 0)

        # Assert
        self.assertEqual(best_individual, 'individual2')
        self.assertEqual(best_solutions, [2, 3])


    def test_iteration(self):
        # Arrange
        genetic_algorithm = mock_iteration()
        NUM_SURVIVORS, NUM_PARENTS, TOURNAMENTS, PROBABILITY = 1, 2, 4, 0.5
        genetic_algorithm.numSurvivors = NUM_SURVIVORS
        genetic_algorithm.numParents = NUM_PARENTS
        genetic_algorithm.k = TOURNAMENTS
        genetic_algorithm.mutationProbability = PROBABILITY

        # Act
        new_population, _ = genetic_algorithm.iteration(POPULATION, [], 0)

        # Assert
        genetic_algorithm.mapLocalSearchWithProbability.assert_called_with(POPULATION, POPULATION_FITNESS, 0.0)
        
        genetic_algorithm.tournamentSelection.assert_any_call(LOCAL_SEARCH_POPULATION, LOCAL_SEARCH_FITNESS, NUM_SURVIVORS, TOURNAMENTS)
        genetic_algorithm.tournamentSelection.assert_any_call(LOCAL_SEARCH_POPULATION, LOCAL_SEARCH_FITNESS, NUM_PARENTS, TOURNAMENTS)
        genetic_algorithm.applyCrossover.assert_called_with(PARENTS)

        genetic_algorithm.mapMutateWithProbability.assert_called_with(['survivor1', 'son1', 'son2'], PROBABILITY)
        self.assertEqual(new_population, MUTATED_POPULATION)


if __name__ == '__main__':
    unittest.main()