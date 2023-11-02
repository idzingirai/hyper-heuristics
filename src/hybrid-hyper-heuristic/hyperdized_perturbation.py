from typing import Tuple, List

from hyperdized_selection import select_low_level_heuristic
from src.common.acceptance import MoveAcceptance
from src.common.chromosome import Chromosome
from src.common.config import NUMBER_OF_GENERATIONS
from src.common.constraints_validator import get_num_of_violated_soft_constraints, \
    get_num_of_violated_hard_constraints
from src.common.generation_perturbative import single_move, swap_slots, swap_lectures
from src.common.timetable import Timetable


def get_constraints_violation_cost(timetable: Timetable) -> Tuple[int, int]:
    """
        Returns the number of violated hard and soft constraints.
        :param timetable: Timetable
        :return: Tuple[int, int]
    """

    number_of_violated_hard_constraints: int = get_num_of_violated_hard_constraints(
        timetable.schedule,
        timetable.constraints,
        timetable.curricula,
        timetable.courses
    )

    number_of_violated_soft_constraints: int = get_num_of_violated_soft_constraints(
        timetable.schedule,
        timetable.curricula,
        timetable.courses
    )

    return number_of_violated_hard_constraints, number_of_violated_soft_constraints


def perform_perturbation(chromosome: Chromosome, timetable: Timetable) -> Timetable:
    """
    Performs a perturbation on the timetable.
    :param timetable: The timetable to perturb.
    :return: The perturbed timetable.
    """
    move_acceptance: MoveAcceptance = MoveAcceptance()
    previous_timetable: Timetable = chromosome.timetable.clone() if chromosome.timetable else timetable.clone()
    current_timetable: Timetable = previous_timetable.clone()
    best_timetable: Timetable = previous_timetable.clone()

    expression: str = chromosome.phenotype
    expression_tokens: List[str] = expression.split()

    for index in range(1, len(expression_tokens)):
        if expression_tokens[index] == "single_move()":
            current_timetable = single_move(current_timetable)
        elif expression_tokens[index] == 'swap_slots()':
            current_timetable = swap_slots(current_timetable)
        elif expression_tokens[index] == 'swap_lectures()':
            current_timetable = swap_lectures(current_timetable)
        else:
            continue

    return best_timetable


def selection_perturbation_hyper_heuristic(
        timetable: Timetable,
        low_level_heuristics: List[Chromosome],
        move_acceptance: MoveAcceptance
) -> Timetable:
    overall_best_timetable: Timetable = timetable.clone()

    generation: int
    for count in range(NUMBER_OF_GENERATIONS):
        selected_heuristic: Chromosome = select_low_level_heuristic(low_level_heuristics)

        clone_timetable: Timetable = timetable.clone()
        clone_timetable: Timetable = perform_perturbation(selected_heuristic, clone_timetable)

        if move_acceptance.iterated_limited_threshold_acceptance(timetable, clone_timetable):
            timetable: Timetable = clone_timetable
            selected_heuristic.reinforcement_learning_score += 1

            ns_num_of_vhc, ns_num_of_shc = get_constraints_violation_cost(timetable)
            os_num_of_vhc, os_num_of_shc = get_constraints_violation_cost(overall_best_timetable)

            if (
                    ns_num_of_vhc < os_num_of_vhc or
                    (ns_num_of_vhc == os_num_of_vhc and ns_num_of_shc < os_num_of_shc)
            ):
                overall_best_timetable: Timetable = timetable.clone()

            if ns_num_of_vhc == 0 and ns_num_of_shc == 0:
                break
        else:
            selected_heuristic.reinforcement_learning_score -= 1

    return overall_best_timetable
