from typing import List, Optional


class Chromosome:
    """
    A chromosome is a representation of a solution to a problem.
    """

    def __init__(self, codons: List[int], fitness: float = 0.0, phenotype: str or None = None):
        self.codons: List[int] = codons
        self.fitness: float = fitness
        self.phenotype: Optional[str] = phenotype

    def __copy__(self):
        """
        Copies the chromosome.
        :return: A copy of the chromosome.
        """
        return Chromosome(self.codons.copy(), self.fitness, self.phenotype)

    def clone(self) -> 'Chromosome':
        """
        Clones the chromosome.
        :return: A clone of the chromosome.
        """
        clone_codons: List[int] = [codon for codon in self.codons]
        return Chromosome(clone_codons)
