import random
import sys
import time

from chromosome_generator import ChromosomeGenerator
from chromosome import Chromosome
from src.common.config import SEED, PROBLEM_INSTANCE_INDEX
from grammar import GrammarGenerator
from grammatical_evolution import GrammaticalEvolution
from src.common.problem import Problem
from src.common.timetable import Timetable
from src.common.constraints_validator import get_num_of_violated_hard_constraints, get_num_of_violated_soft_constraints

if __name__ == "__main__":
    problem_instance_index: int = int(
        PROBLEM_INSTANCE_INDEX if (len(sys.argv) < 2 or sys.argv[1] == 'None') else sys.argv[1]
    )

    seed: int = SEED if (len(sys.argv) < 3 or sys.argv[2] == 'None') else sys.argv[2]
    random.seed(seed)

    print("------------------------------------------------------------")
    print(f"Seed: {seed}\n")

    start_time: float = time.time()

    grammar_generator = GrammarGenerator(terminal_set=['room', 'course', 'day', 'period'])
    chromosome_generator = ChromosomeGenerator()

    grammatical_evolution = GrammaticalEvolution(
        chromosome_generator=chromosome_generator,
        grammar_generator=grammar_generator
    )

    problem_instance: Problem = Problem(problem_instance_index=problem_instance_index)
    problem_instance.initialize()
    print(f"Problem instance {problem_instance_index + 1} initialized.", end="\n\n")

    timetable: Timetable = Timetable(problem_instance)
    timetable.initialize_slots()

    best_solution: Chromosome = grammatical_evolution.run(timetable)
    best_solution.timetable.print()

    print("\nBest solution: ", best_solution.phenotype)
    print("Hard constraints cost: ", best_solution.hard_constraints_cost)
    print("Soft constraints cost: ", best_solution.soft_constraints_cost)
    end_time: float = time.time()
    time_elapsed: float = end_time - start_time
    print(
        f"\nProblem instance {problem_instance_index + 1} took {time_elapsed} seconds to solve."
    )

    print("------------------------------------------------------------")
