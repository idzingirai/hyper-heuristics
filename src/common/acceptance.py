from src.common.config import MAX_ITERATIONS, THRESHOLD
from src.common.constraints_validator import get_num_of_violated_hard_constraints, \
    get_num_of_violated_soft_constraints
from src.common.timetable import Timetable


class MoveAcceptance:
    def __init__(self):
        self.iterations = 0
        self.max_iterations = MAX_ITERATIONS
        self.threshold = THRESHOLD

    def iterated_limited_threshold_acceptance(
            self,
            current_solution: Timetable,
            new_solution: Timetable
    ) -> bool:
        """
            This method implements the iterated limited threshold acceptance algorithm.
            :param current_solution: Timetable
            :param new_solution: Timetable
            :return: bool
        """
        (
            cs_hard_constraints_cost,
            cs_soft_constraints_cost,
            ns_hard_constraints_cost,
            ns_soft_constraints_cost
        ) = MoveAcceptance.get_constraints(current_solution, new_solution)

        if (
                ns_hard_constraints_cost < cs_hard_constraints_cost or
                (
                        ns_hard_constraints_cost == cs_hard_constraints_cost
                        and ns_soft_constraints_cost < cs_soft_constraints_cost
                )
        ):
            self.iterations = 0
            return True
        elif (
                self.iterations >= self.max_iterations and
                ns_hard_constraints_cost == cs_hard_constraints_cost and
                ns_soft_constraints_cost - cs_soft_constraints_cost <= self.threshold
        ):
            self.iterations = 0
            return True
        else:
            self.iterations += 1
            return False

    @staticmethod
    def accept_equal_and_improving(current_solution: Timetable, new_solution: Timetable) -> bool:
        """
            This method implements the accept equal and improving algorithm.
            :param current_solution: Timetable
            :param new_solution: Timetable
            :return: bool
        """
        (
            cs_hard_constraints_cost,
            cs_soft_constraints_cost,
            ns_hard_constraints_cost,
            ns_soft_constraints_cost
        ) = MoveAcceptance.get_constraints(current_solution, new_solution)

        if (
                ns_hard_constraints_cost <= cs_hard_constraints_cost or
                (
                        ns_hard_constraints_cost == cs_hard_constraints_cost
                        and ns_soft_constraints_cost <= cs_soft_constraints_cost
                )
        ):
            return True
        else:
            return False

    @staticmethod
    def get_constraints(current_solution, new_solution):
        cs_hard_constraints_cost = get_num_of_violated_hard_constraints(
            current_solution.schedule,
            current_solution.constraints,
            current_solution.curricula,
            current_solution.courses
        )
        ns_hard_constraints_cost = get_num_of_violated_hard_constraints(
            new_solution.schedule,
            new_solution.constraints,
            new_solution.curricula,
            new_solution.courses
        )
        cs_soft_constraints_cost = get_num_of_violated_soft_constraints(
            current_solution.schedule,
            current_solution.curricula,
            current_solution.courses
        )
        ns_soft_constraints_cost = get_num_of_violated_soft_constraints(
            new_solution.schedule,
            new_solution.curricula,
            new_solution.courses
        )
        return cs_hard_constraints_cost, cs_soft_constraints_cost, ns_hard_constraints_cost, ns_soft_constraints_cost

    @staticmethod
    def accept_improving(current_solution: Timetable, new_solution: Timetable) -> bool:
        """
            This method implements the accept improving algorithm.
            :param current_solution: Timetable
            :param new_solution: Timetable
            :return: bool
        """
        (
            cs_hard_constraints_cost,
            cs_soft_constraints_cost,
            ns_hard_constraints_cost,
            ns_soft_constraints_cost
        ) = MoveAcceptance.get_constraints(current_solution, new_solution)

        if (
                ns_hard_constraints_cost < cs_hard_constraints_cost or
                (
                        ns_hard_constraints_cost == cs_hard_constraints_cost
                        and ns_soft_constraints_cost < cs_soft_constraints_cost
                )
        ):
            return True
        else:
            return False
