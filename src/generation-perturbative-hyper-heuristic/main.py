import random
import sys
import time

from config import SEED, PROBLEM_INSTANCE_INDEX
from src.common.problem import Problem
from src.common.timetable import Timetable

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

    timetable: Timetable = Timetable(problem_instance)
    timetable.initialize_slots()
    timetable.print()

    end_time: float = time.time()
    time_elapsed: float = end_time - start_time
    print(
        f"Problem instance {problem_instance_index + 1} took {time_elapsed} seconds to solve."
    )

    print("------------------------------------------------------------")
