import random
from typing import List

from constraint import Constraint
from course import Course
from problem import Problem
from room import Room
from slot import Slot


def _violating_unavailability_constraint(
        day: int,
        period: int,
        course_constraints: List[Constraint]
) -> bool:
    """
        Helper function to check if a slot violates an unavailability constraint.
        :param day: int
        :param period: int
        :param course_constraints: List[Constraint]
        :return: bool
    """

    constraint: Constraint
    for constraint in course_constraints:
        if constraint.day == day and constraint.period == period:
            return True
    return False


class Timetable:

    def __init__(self, problem: Problem):
        self.problem: Problem = problem

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

    def _select_free_slot(self, course_id: str) -> (int, int):
        constraints: List[Constraint] = self.problem.constraints
        course_constraints: List[Constraint] = [
            constraint for constraint in constraints if constraint.course.course_id == course_id
        ]

        x: int
        y: int

        for x in range(len(self.schedule)):
            for y in range(len(self.schedule[x])):
                if len(self.schedule[x][y].course_room_pair) == 0:
                    if not _violating_unavailability_constraint(x, y, course_constraints):
                        return x, y
        return -1, -1

    def _get_random_slot(self) -> (int, int):
        while True:
            day = random.randint(0, self.problem.number_of_days - 1)
            period = random.randint(0, self.problem.number_of_periods_per_day - 1)

            if not _violating_unavailability_constraint(day, period, self.problem.constraints):
                return day, period

    def _get_room_with_capacity(self, number_of_students) -> Room:
        for room in self.problem.rooms:
            if room.room_capacity >= number_of_students:
                return room

    def initialize_slots(self) -> None:
        """
            Initializes the slots of the timetable.
            :return: None
        """
        courses = self.problem.courses

        course: Course
        for course in courses:
            for _ in range(course.number_of_lectures):
                day: int
                period: int
                day, period = self._select_free_slot(course.course_id)

                if day == -1 and period == -1:
                    day, period = self._get_random_slot()

                room = self._get_room_with_capacity(course.number_of_students)
                self.schedule[day][period].course_room_pair.append((course, room))