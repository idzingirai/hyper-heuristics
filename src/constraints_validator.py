from typing import List

from constraint import Constraint
from course import Course
from curriculum import Curriculum
from slot import Slot
from src.problem import Problem
from timetable import Timetable


def _get_number_of_conflict_violations(curricula: List[Curriculum], slot: Slot) -> int:
    """
        Two courses of the same curriculum must not be scheduled at the same time.
        :param curricula: List[Curriculum]
        :param slot: Slot
        :return: number_of_violations
    """

    number_of_violations: int = 0

    a: Course
    b: Course
    idx: int
    for idx, a in enumerate(slot.course_room_pair):
        for b in slot.course_room_pair[idx + 1:]:

            curriculum: Curriculum
            for curriculum in curricula:
                if a.course_id in curriculum.courses and b.course_id in curriculum.courses:
                    number_of_violations += 1

    return number_of_violations


def _get_number_of_room_occupancy_violations(slot: Slot) -> int:
    """
        Each room must only be scheduled once in a period.
        :param slot: Slot
        :return: number_of_violations
    """
    room_ids: List[str] = [room.room_id for _, room in slot.course_room_pair]
    return len(room_ids) - len(set(room_ids))


def _get_number_of_teacher_violations(slot: Slot) -> int:
    """
        Each teacher must not be scheduled more than once in a period
        :param slot: Slot
        :return: number_of_violations
    """
    teacher_ids: List[str] = [course.teacher_id for course, _ in slot.course_room_pair]
    return len(teacher_ids) - len(set(teacher_ids))


def _get_number_of_unavailability_violations(
        constraints: List[Constraint],
        schedule: List[List[Slot]]
) -> int:
    """
        The unavailability constraints must not be violated.
        :param constraints: List[Constraint]
        :param schedule: List[List[Slot]]
        :return: number_of_violations
    """
    number_of_violations: int = 0

    constraint: Constraint
    for constraint in constraints:
        slot: Slot = schedule[constraint.day][constraint.period]
        course_id_list: List[str] = [course.course_id for course, room in slot.course_room_pair]
        if constraint.course.course_id in course_id_list:
            number_of_violations += 1

    return number_of_violations


def _get_number_of_lectures(course_id: str, schedule: List[List[Slot]]) -> int:
    """
        Helper function to get the number of lectures of a course in a schedule.
        :param course_id: str
        :param schedule: List[List[Slot]]
        :return: number of lectures of a course in a schedule
    """

    number_of_lectures: int = 0

    day: List[Slot]
    slot: Slot
    for day in schedule:
        for slot in day:
            if len(slot.course_room_pair) > 0 and slot.course_room_pair[0].course_id == course_id:
                number_of_lectures += 1

    return number_of_lectures


def _get_number_of_lecture_allocations_violations(
        courses: List[Course],
        schedule: List[List[Slot]]
) -> int:
    """
        Each course must be scheduled exactly the number of times specified in the problem.
        :param courses: List[Course]
        :param schedule: List[List[Slot]]
        :return: number_of_violations
    """

    number_of_violations: int = 0

    course: Course
    for course in courses:
        if _get_number_of_lectures(course.course_id, schedule) != course.number_of_lectures:
            number_of_violations += 1

    return number_of_violations


class Validator:

    def __init__(self, timetable: Timetable):
        self.timetable = timetable

    def get_violated_soft_constraints(self) -> int:
        return 0

    def get_violated_hard_constraints(self) -> int:
        """
        Validates the timetable and returns the number of hard constraints violated.
        :return: number_of_hard_constraints_violated
        """

        number_of_constraints_violated: int = 0

        timetable = self.timetable
        timetable_problem: Problem = timetable.problem
        schedule: List[List[Slot]] = timetable.schedule

        number_of_constraints_violated += _get_number_of_lecture_allocations_violations(
            timetable_problem.courses,
            schedule
        )

        day: List[Slot]
        slot: Slot
        for day in schedule:
            for slot in day:
                number_of_constraints_violated += _get_number_of_conflict_violations(
                    timetable_problem.curricula,
                    slot
                )

                number_of_constraints_violated += _get_number_of_room_occupancy_violations(slot)
                number_of_constraints_violated += _get_number_of_teacher_violations(slot)

        number_of_constraints_violated += _get_number_of_unavailability_violations(
            timetable_problem.constraints,
            schedule
        )

        return number_of_constraints_violated
