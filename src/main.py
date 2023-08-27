import random
import sys
import time

from acceptance import MoveAcceptance
from config import SEED, PROBLEM_INSTANCE_INDEX
from constraints_validator import get_num_of_violated_hard_constraints, \
    get_num_of_violated_soft_constraints
from low_level_heuristics import single_move, swap_slots
from perturbation import selection_perturbation_hyper_heuristic
from problem import Problem
from timetable import Timetable

if __name__ == "__main__":
    problem_instance_index: int = int(
        PROBLEM_INSTANCE_INDEX if (len(sys.argv) < 2 or sys.argv[1] == 'None') else sys.argv[1]
    )

    seed: int = SEED if (len(sys.argv) < 3 or sys.argv[2] == 'None') else sys.argv[2]
    random.seed(seed)

    start_time: float = time.time()

    print("------------------------------------------------------------")
    print(f"Seed: {seed}\n")
    print(f"Problem instance {problem_instance_index + 1}")
    problem_instance: Problem = Problem(problem_instance_index=problem_instance_index)
    problem_instance.initialize()
    print(f"Problem instance {problem_instance_index + 1} initialized.", end="\n\n")

    print(f"Starting selection perturbation hyper-heuristic.")
    move_acceptance: MoveAcceptance = MoveAcceptance()
    low_level_heuristic = {
        "single_move": [0, single_move],
        "swap_slots": [0, swap_slots]
    }

    timetable: Timetable = selection_perturbation_hyper_heuristic(
        problem=problem_instance,
        move_acceptance=move_acceptance,
        low_level_heuristics=low_level_heuristic
    )

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

    print("Hard constraints cost before solving: ", number_of_violated_hard_constraints)
    print(
        "Soft constraints cost before solving: ",
        number_of_violated_soft_constraints,
        end="\n\n"
    )

    timetable.print()

    end_time: float = time.time()
    time_elapsed: float = end_time - start_time
    print(
        f"Problem instance {problem_instance_index + 1} took {time_elapsed} seconds to solve."
    )

    print("------------------------------------------------------------")
