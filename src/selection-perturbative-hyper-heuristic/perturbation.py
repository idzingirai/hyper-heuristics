from typing import Tuple

from acceptance import MoveAcceptance
from config import NUMBER_OF_GENERATIONS
from constraints_validator import get_num_of_violated_soft_constraints, \
    get_num_of_violated_hard_constraints
from problem import Problem
from selection import select_low_level_heuristic
from timetable import Timetable


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


def selection_perturbation_hyper_heuristic(
        problem: Problem,
        low_level_heuristics: dict,
        move_acceptance: MoveAcceptance
) -> Timetable:
    timetable: Timetable = Timetable(problem=problem)
    timetable.initialize_slots()

    overall_best_timetable: Timetable = timetable.clone()

    generation: int
    for count in range(NUMBER_OF_GENERATIONS):
        heuristic_name: str = select_low_level_heuristic(low_level_heuristics)
        heuristic = low_level_heuristics[heuristic_name][1]

        clone_timetable: Timetable = timetable.clone()
        clone_timetable: Timetable = heuristic(clone_timetable)

        if move_acceptance.iterated_limited_threshold_acceptance(timetable, clone_timetable):
            timetable: Timetable = clone_timetable
            low_level_heuristics[heuristic_name][0] += 1

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
            low_level_heuristics[heuristic_name][0] -= 1

    return timetable
