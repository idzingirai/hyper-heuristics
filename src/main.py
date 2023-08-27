import random
import sys
import time

from config import SEED, PROBLEM_INSTANCES_INDICES
from constraints_validator import get_num_of_violated_hard_constraints, \
    get_num_of_violated_soft_constraints
from problem import Problem
from src.acceptance import MoveAcceptance
from src.low_level_heuristics import single_move
from timetable import Timetable


def selection_perturbation_hyper_heuristic(problem: Problem):
    move_acceptance = MoveAcceptance()

    #   1. Generate an initial solution
    problem.initialize()
    timetable = Timetable(problem=problem)
    timetable.initialize_slots()

    print("Perturbation")

    for count in range(10000):
        clone_timetable = timetable.clone()
        clone_timetable = single_move(clone_timetable)
        if move_acceptance.iterated_limited_threshold_acceptance(timetable, clone_timetable):
            timetable = clone_timetable

        print(
            "Hard constraints cost before solving: ",
            get_num_of_violated_hard_constraints(
                timetable.schedule,
                timetable.constraints,
                timetable.curricula,
                timetable.courses
            )
        )

        print(
            "Soft constraints cost before solving: ",
            get_num_of_violated_soft_constraints(
                timetable.schedule,
                timetable.curricula,
                timetable.courses
            )
        )


if __name__ == "__main__":
    seed = SEED if (len(sys.argv) < 2 or sys.argv[1] == 'None') else sys.argv[1]
    random.seed(seed)

    for problem_instance_index in PROBLEM_INSTANCES_INDICES:
        start_time = time.time()

        #   0. Initialize the problem instance
        problem_instance = Problem(problem_instance_index=problem_instance_index)
        problem_instance.initialize()


        selection_perturbation_hyper_heuristic(problem=problem_instance)

        end_time = time.time()
        time_elapsed = end_time - start_time
        print(
            f"Problem instance {problem_instance_index + 1} took {time_elapsed} seconds to solve."
        )
        break
