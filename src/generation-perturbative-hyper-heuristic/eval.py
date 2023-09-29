from chromosome import Chromosome
from constraints_validator import get_num_of_violated_hard_constraints, get_num_of_violated_soft_constraints
from timetable import Timetable


def _perform_perturbation(chromosome: Chromosome, timetable: Timetable) -> Timetable:
    """
    Performs a perturbation on the timetable.
    :param timetable: The timetable to perturb.
    :return: The perturbed timetable.
    """
    return timetable


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
