import random
import sys
import time

from config import SEED, PROBLEM_INSTANCES_INDICES
from problem import Problem
from src.constraints_validator import get_num_of_violated_hard_constraints, \
    get_num_of_violated_soft_constraints
from timetable import Timetable

if __name__ == "__main__":
    #   Seed the whole program
    seed = SEED if (len(sys.argv) < 2 or sys.argv[1] == 'None') else sys.argv[1]
    random.seed(seed)

    for problem_instance_index in PROBLEM_INSTANCES_INDICES:
        start_time = time.time()

        problem_instance = Problem(problem_instance_index=problem_instance_index)
        problem_instance.initialize()

        timetable = Timetable(problem=problem_instance)
        timetable.initialize_slots()

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

        end_time = time.time()
        time_elapsed = end_time - start_time
        print(
            f"Problem instance {problem_instance_index + 1} took {time_elapsed} seconds to solve."
        )
        break
