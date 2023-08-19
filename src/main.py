import random
import sys

from config import SEED, PROBLEM_INSTANCES_INDICES
from problem import Problem
from src.constraints_validator import Validator
from timetable import Timetable

if __name__ == "__main__":
    #   Seed the whole program
    seed = SEED if (len(sys.argv) < 2 or sys.argv[1] == 'None') else sys.argv[1]
    random.seed(seed)

    for problem_instance_index in PROBLEM_INSTANCES_INDICES:
        problem_instance = Problem(problem_instance_index=problem_instance_index)
        problem_instance.initialize()

        timetable = Timetable(problem=problem_instance)

        validator = Validator(timetable)
        print(validator.get_violated_hard_constraints())

        break
