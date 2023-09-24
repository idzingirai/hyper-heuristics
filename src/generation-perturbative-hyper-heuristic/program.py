import random
import re
import warnings
from typing import List

import numpy as np
from chromosome import Chromosome
from chromosome_generator import ChromosomeGenerator
from config import *
from eval import evaluate_expression
from grammar import GrammarGenerator


class GrammaticalEvolution:

    def __init__(self, chromosome_generator: ChromosomeGenerator, grammar_generator: GrammarGenerator):
        self.best_solution = None
        warnings.filterwarnings("ignore")
        self._chromosome_generator = chromosome_generator
        self._grammar = grammar_generator.get_grammar()
        self._terminal_set = grammar_generator.get_terminal_set()
        self._population_size = POPULATION_SIZE
        self._tournament_size = TOURNAMENT_SIZE
        self._max_num_of_generations = MAX_GENERATIONS
        self._crossover_probability = CROSSOVER_PROBABILITY
        self._mutation_probability = MUTATION_PROBABILITY

    def __generate_initial_population(self) -> List[Chromosome]:
        """
        Generates the initial population of chromosomes.
        :return: The initial population of chromosomes.
        """
        return [self._chromosome_generator.generate_chromosome() for _ in range(self._population_size)]

    def __selection(self, population: List[Chromosome]) -> Chromosome:
        """
        Selects a chromosome from the population.
        :param population of chromosomes.
        :return: The selected chromosome.
        """
        tournament = random.sample(population, self._tournament_size)
        return min(tournament, key=lambda chromosome: chromosome.fitness)

    def __crossover(self, first_chromosome: Chromosome, second_chromosome: Chromosome) -> None:
        """
        Performs single point crossover between two chromosomes.
        :param first_chromosome: The first parent.
        :param second_chromosome: The second parent.
        :return: None.
        """

        first_chromosome_codons = first_chromosome.codons
        second_chromosome_codons = second_chromosome.codons

        first_index = random.randint(0, len(first_chromosome_codons) - 1)
        second_index = random.randint(0, len(second_chromosome_codons) - 1)

        first_chromosome.codons = first_chromosome_codons[:first_index] + second_chromosome_codons[second_index:]
        second_chromosome.codons = second_chromosome_codons[:second_index] + first_chromosome_codons[first_index:]

    def __mutation(self, chromosome: Chromosome) -> Chromosome:
        """
        Mutates a chromosome.
        :param chromosome: The chromosome to mutate.
        :return: The mutated chromosome.
        """
        index = random.randint(0, len(chromosome.codons) - 1)
        chromosome.codons[index] = random.randrange(256)
        return chromosome

    def __map(self, chromosome: Chromosome) -> None:
        """
        Maps a chromosome to a phenotype.
        :param chromosome: The chromosome to map.
        :return: None.
        """

        codons: List[int] = chromosome.codons
        self.current_codon = 0

        starting_symbol: str = next(iter(self._grammar.keys()))
        stack: List[str] = [starting_symbol]
        phenotype: str = ''

        while stack:
            symbol = stack.pop()

            if self.current_codon >= len(codons):
                self.current_codon = 0
                del codons
                codons = self._chromosome_generator.generate_codons()

            if symbol not in self._grammar:
                phenotype = phenotype + ' ' + symbol
            else:
                choices = self._grammar[symbol]
                num_of_choices = len(choices)

                index = 0 if num_of_choices == 1 else codons[self.current_codon] % len(choices)
                self.current_codon += 0 if num_of_choices == 1 else 1

                production = choices[index]
                tokens = production.split()
                stack.extend(reversed(tokens))

        del codons
        del stack
        chromosome.phenotype = phenotype

    def __evaluate(self, row, expression):
        for token in self._terminal_set:
            index = np.where(self._terminal_set == token)[0][0]
            pattern = r'\b' + token + r'\b'
            expression = re.sub(pattern, str(row[index]), expression)

        return evaluate_expression(expression)

    def __calculate_fitness(self, chromosome: Chromosome, x, y) -> None:
        pass

    def train(self, x, y) -> None:
        """
        Trains the algorithm.
        :param x: The x values for the training set.
        :param y: The y values for the training set.
        :return: None.
        """

        # Generate the initial population.
        population = self.__generate_initial_population()

        # Map via BNF grammar and calculate fitness.
        for chromosome in population:
            self.__map(chromosome)

        #   Replace chromosomes with single element in phenotype or with phenotype length > 1000
        population = [chromosome for chromosome in population if
                      len(chromosome.phenotype.split()) > 1 and len(chromosome.phenotype) < 1000]
        while len(population) < self._population_size:
            chromosome = self._chromosome_generator.generate_chromosome()
            self.__map(chromosome)

            if len(chromosome.phenotype.split()) > 1 and len(chromosome.phenotype) < 1000:
                population.append(chromosome)

        #   Evaluate fitness of each chromosome
        for chromosome in population:
            self.__calculate_fitness(chromosome, x, y)

        # Sort the population by fitness.
        population.sort(key=lambda candidate: candidate.fitness)

        #  Save the best solution.
        best_solution = population[0].__copy__()
        num_of_generations = 0
        while num_of_generations < self._max_num_of_generations and best_solution.fitness > 3:
            first_chromosome = self.__selection(population)
            second_chromosome = self.__selection(population)

            # Crossover.
            if random.random() < self._crossover_probability:
                self.__crossover(first_chromosome, second_chromosome)

            # Mutation.
            if random.random() < self._mutation_probability:
                self.__mutation(first_chromosome)
                self.__mutation(second_chromosome)

            # Map via BNF grammar and calculate fitness.
            children_valid = False

            self.__map(first_chromosome)
            if len(first_chromosome.phenotype.split()) > 1 and len(first_chromosome.phenotype) < 1000:
                self.__calculate_fitness(first_chromosome, x, y)
                population.append(first_chromosome)
                children_valid = True

            self.__map(second_chromosome)
            if len(second_chromosome.phenotype.split()) > 1 and len(second_chromosome.phenotype) < 1000:
                self.__calculate_fitness(second_chromosome, x, y)
                population.append(second_chromosome)
                children_valid = True

            if children_valid:
                # Sort the population by fitness.
                population.sort(key=lambda candidate: candidate.fitness)

                # Remove the worst solutions from the population.
                population = population[:self._population_size]

                if population[0].fitness < best_solution.fitness:
                    best_solution = population[0].__copy__()

            num_of_generations += 1
            print('Generation: ' + str(num_of_generations) + ' Fitness: ' + str(best_solution.fitness))

        self.best_solution = best_solution
        print(
            f"[] Best Best Solution After Training Fitness ({FITNESS_FUNCTION}): {str(round(best_solution.fitness, 4))}"
        )

        print(f"[] Best Solution After Training Phenotype: {best_solution.phenotype}")

    def test(self, x, y) -> None:
        """
        Tests the best solution.
        :param x: The x values for the testing set.
        :param y: The y values for the testing set.
        :return: None.
        """

        self.__calculate_fitness(self.best_solution, x, y)

        print(
            f"[] Best Solution After Testing Fitness ({FITNESS_FUNCTION}): {str(round(self.best_solution.fitness, 4))}"
        )
