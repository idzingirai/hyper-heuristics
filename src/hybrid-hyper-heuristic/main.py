import random
import sys
import time
from typing import List

from src.common.chromosome import Chromosome
from src.common.chromosome_generator import ChromosomeGenerator
from src.common.grammar import GrammarGenerator
from src.common.grammatical_evolution import GrammaticalEvolution

sys.path.append("../../")

from src.common.config import PROBLEM_INSTANCE_INDEX, SEED
from src.common.constraints_validator import get_num_of_violated_soft_constraints, get_num_of_violated_hard_constraints
from src.common.problem import Problem
from src.common.timetable import Timetable

if __name__ == '__main__':
    problem_instance_index: int = int(
        PROBLEM_INSTANCE_INDEX
        if (len(sys.argv) < 2 or sys.argv[1] == 'None')
        else sys.argv[1]
    )

    seed: int = int(
        SEED if
        (len(sys.argv) < 3 or sys.argv[2] == 'None')
        else sys.argv[2]
    )

    random.seed(seed)

    start_time: float = time.time()

    print("------------------------------------------------------------")
    print(f"Seed: {seed}\n")
    print(f"Problem instance {problem_instance_index + 1}")
    problem_instance: Problem = Problem(problem_instance_index=problem_instance_index)
    problem_instance.initialize()
    print(f"Problem instance {problem_instance_index + 1} initialized.", end="\n\n")

    grammar_generator = GrammarGenerator(terminal_set=['room', 'course', 'day', 'period'])
    chromosome_generator = ChromosomeGenerator()

    grammatical_evolution = GrammaticalEvolution(
        chromosome_generator=chromosome_generator,
        grammar_generator=grammar_generator
    )

    timetable: Timetable = Timetable(problem_instance)
    timetable.initialize_slots()

    best_n_solutions: List[Chromosome] = grammatical_evolution.run(timetable, 5)

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
