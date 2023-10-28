from common import config, constraints_validator, timetable


class MoveAcceptance:
    def __init__(self):
        self.iterations = 0
        self.max_iterations = config.MAX_ITERATIONS
        self.threshold = config.THRESHOLD

    def iterated_limited_threshold_acceptance(
            self,
            current_solution: timetable.Timetable,
            new_solution: timetable.Timetable
    ) -> bool:
        """
            This method implements the iterated limited threshold acceptance algorithm.
            :param current_solution: Timetable
            :param new_solution: Timetable
            :return: bool
        """
        cs_hard_constraints_cost = constraints_validator.get_num_of_violated_hard_constraints(
            current_solution.schedule,
            current_solution.constraints,
            current_solution.curricula,
            current_solution.courses
        )

        ns_hard_constraints_cost = constraints_validator.get_num_of_violated_hard_constraints(
            new_solution.schedule,
            new_solution.constraints,
            new_solution.curricula,
            new_solution.courses
        )

        cs_soft_constraints_cost = constraints_validator.get_num_of_violated_soft_constraints(
            current_solution.schedule,
            current_solution.curricula,
            current_solution.courses
        )

        ns_soft_constraints_cost = constraints_validator.get_num_of_violated_soft_constraints(
            new_solution.schedule,
            new_solution.curricula,
            new_solution.courses
        )

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
