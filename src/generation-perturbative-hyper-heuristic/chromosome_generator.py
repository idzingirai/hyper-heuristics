import random
from typing import List

from chromosome import Chromosome
from src.common.config import UPPER_BOUND, LOWER_BOUND


class ChromosomeGenerator:
    def __init__(self):
        self.lower_bound: int = LOWER_BOUND
        self.upper_bound: int = UPPER_BOUND

    def generate_chromosome(self) -> Chromosome:
        """
        Generates a chromosome with a random number of codons.
        :return: A chromosome with a random number of codons.
        """
        return Chromosome(self.generate_codons())

    def generate_codons(self) -> List[int]:
        """
        Generates a list of codons of random size.
        :return: A list of codons of random size.
        """
        number_of_codons: int = random.randint(self.lower_bound, self.upper_bound)
        return [random.randrange(256) for _ in range(number_of_codons)]
