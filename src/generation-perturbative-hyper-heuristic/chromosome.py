import sys
from typing import List, Optional


class Chromosome:
    """
    A chromosome is a representation of a solution to a problem.
    """

    def __init__(
            self,
            codons: List[int],
            hard_constraints_cost: int = sys.maxsize,
            soft_constraints_cost: int = sys.maxsize,
            phenotype: Optional[str] = None
    ):
        self.codons: List[int] = codons
        self.hard_constraints_cost: int = hard_constraints_cost
        self.soft_constraints_cost: int = soft_constraints_cost
        self.phenotype: Optional[str] = phenotype

    def __copy__(self):
        """
        Copies the chromosome.
        :return: A copy of the chromosome.
        """
        return Chromosome(self.codons.copy(), self.hard_constraints_cost, self.soft_constraints_cost, self.phenotype)

    def clone(self) -> 'Chromosome':
        """
        Clones the chromosome.
        :return: A clone of the chromosome.
        """
        clone_codons: List[int] = [codon for codon in self.codons]
        return Chromosome(clone_codons)
