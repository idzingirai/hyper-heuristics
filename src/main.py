import random
import sys
import time

from config import SEED, PROBLEM_INSTANCES_INDICES
from problem import Problem
from src.constraints_validator import Validator
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

        # print 2d array of slots
        for day in timetable.schedule:
            for slot in day:
                print(len(slot.course_room_pair), end=" ")
            print()

        validator = Validator(timetable)
        print(validator.get_violated_hard_constraints())

        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Problem instance {problem_instance_index} took {time_elapsed} seconds to solve.")
        break
