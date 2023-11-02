import random
from typing import List

from src.common.chromosome import Chromosome


def select_low_level_heuristic(low_level_heuristics: List[Chromosome]) -> Chromosome:
    """
        Reinforcement Learning: Selects a low level heuristic based on performance score from previous usage.
        :param low_level_heuristics: dict
        :return: str
    """
    max_value = max(item.reinforcement_learning_score for item in low_level_heuristics)
    best_heuristics = [
        heuristic for heuristic in low_level_heuristics
        if heuristic.reinforcement_learning_score == max_value
    ]

    return random.choice(best_heuristics)
