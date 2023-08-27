from acceptance import MoveAcceptance
from constraints_validator import get_num_of_violated_soft_constraints, \
    get_num_of_violated_hard_constraints
from problem import Problem
from selection import select_low_level_heuristic
from timetable import Timetable


def selection_perturbation_hyper_heuristic(
        problem: Problem,
        low_level_heuristics: dict,
        move_acceptance: MoveAcceptance
) -> Timetable:
    timetable: Timetable = Timetable(problem=problem)
    timetable.initialize_slots()

    generation: int
    for count in range(10000):
        heuristic_name: str = select_low_level_heuristic(low_level_heuristics)
        heuristic = low_level_heuristics[heuristic_name][1]

        clone_timetable: Timetable = timetable.clone()
        clone_timetable: Timetable = heuristic(clone_timetable)

        if move_acceptance.iterated_limited_threshold_acceptance(timetable, clone_timetable):
            timetable: Timetable = clone_timetable
            low_level_heuristics[heuristic_name][0] += 1

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

            # print("Hard constraints cost before solving: ", number_of_violated_hard_constraints)
            # print("Soft constraints cost before solving: ", number_of_violated_soft_constraints)

            if number_of_violated_hard_constraints == 0 and number_of_violated_soft_constraints == 0:
                break
        else:
            low_level_heuristics[heuristic_name][0] -= 1

    return timetable
