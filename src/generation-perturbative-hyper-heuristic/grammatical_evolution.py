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
from timetable import Timetable


def __mutation(chromosome: Chromosome) -> Chromosome:
    """
    Mutates a chromosome.
    :param chromosome: The chromosome to mutate.
    :return: The mutated chromosome.
    """
    index = random.randint(0, len(chromosome.codons) - 1)
    chromosome.codons[index] = random.randrange(256)
    return chromosome


def __crossover(first_chromosome: Chromosome, second_chromosome: Chromosome) -> None:
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

    def __map(self, chromosome: Chromosome) -> None:
        """
        Maps a chromosome to a phenotype.
        :param chromosome: The chromosome to map.
        :return: None.
        """
        codons: List[int] = chromosome.codons
        self.current_codon: int = 0

        starting_symbol: str = next(iter(self._grammar.keys()))
        print(starting_symbol)
        stack: List[str] = [starting_symbol]
        phenotype: str = ''

        while stack:
            symbol: str = stack.pop()

            if self.current_codon >= len(codons):
                self.current_codon = 0
                del codons
                codons: List[int] = self._chromosome_generator.generate_codons()

            if symbol not in self._grammar:
                phenotype: str = phenotype + ' ' + symbol
            else:
                choices = self._grammar[symbol]
                num_of_choices = len(choices)

                index = 0 if num_of_choices == 1 else codons[self.current_codon] % len(choices)
                self.current_codon += 0 if num_of_choices == 1 else 1

                production = choices[index]
                tokens = [str(production)] if isinstance(production, int)  else production.split()
                stack.extend(reversed(tokens))

        del codons
        del stack
        chromosome.phenotype = phenotype
        print(phenotype)

    def run(self, timetable: Timetable):
        population = self.__generate_initial_population()

        for chromosome in population:
            self.__map(chromosome)
