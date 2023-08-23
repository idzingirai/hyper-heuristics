from itertools import combinations
from typing import List

from constraint import Constraint
from course import Course
from curriculum import Curriculum
from room import Room
from slot import Slot
from timetable import Timetable


#   For Hard Constraints
def _get_number_of_conflict_violations(curricula: List[Curriculum], slot: Slot) -> int:
    """
        Two courses of the same curriculum must not be scheduled at the same time.
        :param curricula: List[Curriculum]
        :param slot: Slot
        :return: number_of_violations
    """

    number_of_violations: int = 0

    # get all course ids in the slot
    course_ids: List[str] = [course.course_id for course, _ in slot.course_room_pairs]
    course_combinations: List[List[str]] = list(combinations(course_ids, 2))

    course_combination: List[str]
    for course_combination in course_combinations:

        curriculum: Curriculum
        for curriculum in curricula:
            if (
                    course_combination[0] in curriculum.course_ids
                    and course_combination[1] in curriculum.course_ids
            ):
                number_of_violations += 1

    return number_of_violations


def _get_number_of_room_occupancy_violations(slot: Slot) -> int:
    """
        Each room must only be scheduled once in a period.
        :param slot: Slot
        :return: number_of_violations
    """
    room_ids: List[str] = [room.room_id for _, room in slot.course_room_pairs if room is not None]
    return len(room_ids) - len(set(room_ids))


def _get_number_of_teacher_violations(slot: Slot) -> int:
    """
        Each teacher must not be scheduled more than once in a period
        :param slot: Slot
        :return: number_of_violations
    """
    teacher_ids: List[str] = [course.teacher_id for course, _ in slot.course_room_pairs]
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
        course_id_list: List[str] = [course.course_id for course, room in slot.course_room_pairs]
        if constraint.course_id in course_id_list:
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

            course: Course
            for course, _ in slot.course_room_pairs:
                if course.course_id == course_id:
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


#  For Soft Constraints
def _get_number_of_room_capacity_violations(schedule: List[List[Slot]]) -> int:
    """
    The number of students in a scheduled course must not exceed the room capacity.
    :param schedule: List[List[Slot]]
    :return: number_of_violations
    """

    number_of_violations: int = 0

    day: List[Slot]
    slot: Slot
    for day in schedule:
        for slot in day:

            course: Course
            room: Room
            for course, room in slot.course_room_pairs:
                if course.number_of_students > room.room_capacity:
                    number_of_violations += 1

    return number_of_violations


def _get_course(course_id: str, courses: List[Course]) -> Course:
    """
    Helper function to get a course from a list of courses.
    :param course_id:
    :param courses:
    :return: course object
    """

    for course in courses:
        if course.course_id == course_id:
            return course


def _get_number_of_minimum_working_days_violations(
        courses: List[Course],
        schedule: List[List[Slot]]
) -> int:
    """
    Each course must be scheduled at least the number of times specified in the problem.
    :param courses: List[Course]
    :param schedule: List[List[Slot]]
    :return: number_of_violations: int
    """

    number_of_violations: int = 0

    for x in range(0, len(schedule)):
        for y in range(0, len(schedule[x])):
            for course, _ in schedule[x][y].course_room_pairs:
                for a in range(x + 1, len(schedule)):
                    for b in range(0, len(schedule[a])):
                        for course2, _ in schedule[a][b].course_room_pairs:
                            if course.course_id == course2.course_id:
                                if (
                                        abs(a - x)
                                        < _get_course(course.course_id, courses).min_working_days
                                ):
                                    number_of_violations += 1

    return number_of_violations


def _check_if_course_is_in_curriculum(
        first_course: str,
        course_ids: List[str],
        curricula: List[Curriculum]
) -> bool:
    """
    Helper function to check if any of the courses in a list of courses and the given course are in the same curriculum.
    :param first_course: str
    :param course_ids: List[str]
    :param curricula: List[Curriculum]
    :return: whether the courses are in the same curriculum
    """

    for curriculum in curricula:
        for course_id in curriculum.course_ids:
            if first_course in curriculum.course_ids and course_id in course_ids:
                return True
    return False


def _get_number_of_curriculum_compactness_violations(
        curricula: List[Curriculum],
        schedule: List[List[Slot]]
) -> int:
    """
    Courses of the same curriculum should be adjacent to each other.
    :param curricula:
    :param schedule:
    :return: number_of_violations
    """

    number_of_violations: int = 0

    for x in range(0, len(schedule)):
        for y in range(0, len(schedule[x])):
            for course, _ in schedule[x][y].course_room_pairs:
                for index in range(y + 1, len(schedule[x])):
                    course_ids: List[str] = [
                        course.course_id for course, _ in schedule[x][index].course_room_pairs
                    ]
                    if not _check_if_course_is_in_curriculum(
                            course.course_id,
                            course_ids,
                            curricula
                    ):
                        number_of_violations += 1

    return number_of_violations


def _get_number_of_room_stability_violations(
        schedule: List[List[Slot]]
) -> int:
    """
    Courses should be scheduled in the same room as much as possible.
    :param schedule: List[List[Slot]]
    :return: number_of_violations
    """

    number_of_violations: int = 0
    course_first_room_map: dict = {}

    for day_slots in schedule:
        for slot in day_slots:
            for course, room in slot.course_room_pairs:
                if course.course_id not in course_first_room_map:
                    course_first_room_map[course.course_id] = room.room_id
                if room.room_id != course_first_room_map[course.course_id]:
                    number_of_violations += 1

    return number_of_violations


def get_num_of_violated_soft_constraints(timetable: Timetable) -> int:
    number_of_constraints_violated: int = 0
    courses = timetable.problem.courses
    schedule = timetable.schedule

    number_of_constraints_violated += _get_number_of_room_capacity_violations(schedule)
    number_of_constraints_violated += _get_number_of_room_stability_violations(schedule)
    number_of_constraints_violated += _get_number_of_minimum_working_days_violations(
        courses,
        schedule
    )

    number_of_constraints_violated += _get_number_of_curriculum_compactness_violations(
        timetable.problem.curricula,
        schedule
    )

    return number_of_constraints_violated


def get_num_of_violated_hard_constraints(timetable: Timetable) -> int:
    """
    Validates the timetable and returns the number of hard constraints violated.
    :return: number_of_hard_constraints_violated
    """

    number_of_constraints_violated: int = 0
    schedule: List[List[Slot]] = timetable.schedule
    curricula: List[Curriculum] = timetable.problem.curricula

    number_of_constraints_violated += _get_number_of_lecture_allocations_violations(
        timetable.courses,
        schedule
    )

    day: List[Slot]
    slot: Slot
    for day in schedule:
        for slot in day:
            number_of_constraints_violated += _get_number_of_conflict_violations(curricula, slot)
            number_of_constraints_violated += _get_number_of_room_occupancy_violations(slot)
            number_of_constraints_violated += _get_number_of_teacher_violations(slot)

    number_of_constraints_violated += _get_number_of_unavailability_violations(
        timetable.constraints,
        schedule
    )

    return number_of_constraints_violated
