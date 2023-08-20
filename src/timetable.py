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
        self.constraints: List[Constraint] = self.problem.constraints

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

    def _select_free_slot(self, course_id: str) -> (int, int):
        course_constraints: List[Constraint] = [
            constraint for constraint in self.constraints if constraint.course_id == course_id
        ]

        x: int
        y: int

        for x in range(len(self.schedule)):
            for y in range(len(self.schedule[x])):
                if len(self.schedule[x][y].course_room_pair) == 0:
                    if not _violating_unavailability_constraint(x, y, course_constraints):
                        return x, y
        return -1, -1

    def _get_random_slot(self, course_id: str) -> (int, int):
        #   Get slot with the least number of courses
        #   If there are multiple slots with the same number of courses, select one randomly
        course_constraints: List[Constraint] = [
            constraint for constraint in self.constraints if constraint.course_id == course_id
        ]
        day_index: int = 0
        period_index: int = 0
        min_number_of_courses: int = len(self.schedule[day_index][period_index].course_room_pair)

        for x in range(len(self.schedule)):
            for y in range(len(self.schedule[x])):
                if len(self.schedule[x][y].course_room_pair) < min_number_of_courses:
                    min_number_of_courses = len(self.schedule[x][y].course_room_pair)
                    if not _violating_unavailability_constraint(x, y, course_constraints):
                        day_index = x
                        period_index = y
                elif len(self.schedule[x][y].course_room_pair) == min_number_of_courses:
                    if not _violating_unavailability_constraint(x, y, course_constraints):
                        if random.randint(0, 1) == 0:
                            day_index = x
                            period_index = y

        return day_index, period_index

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
                    day, period = self._get_random_slot(course.course_id)

                room = self._get_room_with_capacity(course.number_of_students)
                self.schedule[day][period].course_room_pair.append((course, room))
