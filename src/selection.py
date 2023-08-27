import random


def select_low_level_heuristic(low_level_heuristics: dict) -> str:
    """
        Reinforcement Learning: Selects a low level heuristic based on performance score from previous usage.
        :param low_level_heuristics: dict
        :return: str
    """
    max_value = max(item[0] for item in low_level_heuristics.values())
    best_heuristics_names = [
        heuristic_name for heuristic_name, values in low_level_heuristics.items()
        if values[0] == max_value
    ]
    return random.choice(best_heuristics_names)
