from acceptance import MoveAcceptance
from chromosome import Chromosome
from constraints_validator import get_num_of_violated_hard_constraints, get_num_of_violated_soft_constraints
from perturbative import *


def _perform_perturbation(chromosome: Chromosome, timetable: Timetable) -> Timetable:
    """
    Performs a perturbation on the timetable.
    :param timetable: The timetable to perturb.
    :return: The perturbed timetable.
    """
    move_acceptance: MoveAcceptance = MoveAcceptance()
    previous_timetable: Timetable = chromosome.timetable.clone() if chromosome.timetable else timetable.clone()
    current_timetable: Timetable = previous_timetable.clone()
    best_timetable: Timetable = previous_timetable.clone()

    expression: str = chromosome.phenotype
    expression_tokens: List[str] = expression.split()

    for index in range(1, len(expression_tokens)):
        if expression_tokens[index] == "single_move()":
            current_timetable = single_move(current_timetable)
        elif expression_tokens[index] == 'swap_slots()':
            current_timetable = swap_slots(current_timetable)
        elif expression_tokens[index] == 'swap_lectures()':
            current_timetable = swap_lectures(current_timetable)
        else:
            continue

    if expression_tokens[0] == "ILTA":
        if move_acceptance.iterated_limited_threshold_acceptance(previous_timetable, current_timetable):
            best_timetable = current_timetable.clone()
    elif expression_tokens[0] == "AEI":
        if move_acceptance.accept_equal_and_improving(previous_timetable, current_timetable):
            best_timetable = current_timetable.clone()
    else:
        if move_acceptance.accept_improving(previous_timetable, current_timetable):
            best_timetable = current_timetable.clone()

    return best_timetable


def calculate_fitness(chromosome: Chromosome, timetable: Timetable) -> None:
    """
    Calculates the fitness of a chromosome.
    :param chromosome: The chromosome to calculate the fitness of.
    :param timetable: The timetable to evaluate.
    :return: None.
    """
    perturbed_timetable: Timetable = _perform_perturbation(chromosome, timetable)

    num_of_violated_soft_constraints = get_num_of_violated_soft_constraints(
        perturbed_timetable.schedule,
        perturbed_timetable.curricula,
        perturbed_timetable.courses
    )

    num_of_violated_hard_constraints = get_num_of_violated_hard_constraints(
        perturbed_timetable.schedule,
        perturbed_timetable.constraints,
        perturbed_timetable.curricula,
        perturbed_timetable.courses
    )


    chromosome.timetable = perturbed_timetable.clone()
    chromosome.hard_constraints_cost = num_of_violated_hard_constraints
    chromosome.soft_constraints_cost = num_of_violated_soft_constraints
