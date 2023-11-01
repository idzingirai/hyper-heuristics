import sys
from typing import List, Optional

from src.common.timetable import Timetable


class Chromosome:
    """
    A chromosome is a representation of a solution to a problem.
    """

    def __init__(
            self,
            codons: List[int],
            hard_constraints_cost: int = sys.maxsize,
            soft_constraints_cost: int = sys.maxsize,
            phenotype: Optional[str] = None,
            timetable: Optional[Timetable] = None
    ):
        self.codons: List[int] = codons
        self.hard_constraints_cost: int = hard_constraints_cost
        self.soft_constraints_cost: int = soft_constraints_cost
        self.phenotype: Optional[str] = phenotype
        self.timetable: Optional[Timetable] = timetable

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
        return Chromosome(
            [codon for codon in self.codons],
            self.hard_constraints_cost,
            self.soft_constraints_cost,
            self.phenotype,
            self.timetable.clone() if self.timetable else None
        )
