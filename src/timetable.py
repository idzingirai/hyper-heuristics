from typing import List

from problem import Problem
from slot import Slot


class Timetable:

    def __init__(self, problem: Problem):
        self.problem: Problem = problem

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

    def _initialize_slots(self) -> None:
        """
            Initializes the slots of the timetable.
            :return: None
        """
        constraints = self.problem.constraints







