from typing import List

from constraint import Constraint
from course import Course
from curriculum import Curriculum
from problem import Problem
from room import Room
from slot import Slot


class Timetable:

    def __init__(self, problem: Problem):
        self.problem: Problem = problem
        self.constraints: List[Constraint] = self.problem.constraints
        self.rooms: List[Room] = self.problem.rooms
        self.courses: List[Course] = self.problem.courses

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

    def _already_in_slot(self, day: int, period: int, course_id: str) -> bool:
        """
            Helper function to check if a course is already in a slot.
            :param day: int
            :param period: int
            :param course_id: str
            :return: bool
        """

        course_ids_in_slot: List[str] = [
            course.course_id for course, room in self.schedule[day][period].course_room_pairs
        ]

        return course_id in course_ids_in_slot

    def _violating_unavailability_constraint(self, day: int, period: int, course_id: str) -> bool:
        """
            Helper function to check if a slot violates an unavailability constraint.
            :param day: int
            :param period: int
            :param course_id: str
            :return: bool
        """

        course_constraints = [
            constraint for constraint in self.constraints
            if constraint.course_id == course_id
        ]

        return any(
            constraint.day == day and constraint.period == period for constraint in
            course_constraints
        )

    def _violating_curriculum_constraint(self, day: int, period: int, course_id: str) -> bool:
        """
            Helper function to check if a slot violates a curriculum constraint.
            :param day: int
            :param period: int
            :param course_id: str
            :return: bool
        """

        course_ids_in_slot: List[str] = [
            course.course_id for course, room in self.schedule[day][period].course_room_pairs
        ]

        c_id: str
        for c_id in course_ids_in_slot:

            curriculum: Curriculum
            for curriculum in self.problem.curricula:
                if c_id in curriculum.course_ids and course_id in curriculum.course_ids:
                    return True

        return False

    def _violating_teacher_constraint(self, day: int, period: int, teacher_id: str) -> bool:
        """
            Helper function to check if a slot violates a teacher constraint.
            :param day: int
            :param period: int
            :param teacher_id: str
            :return: bool
        """

        teacher_ids_in_slot: List[str] = [
            course.teacher_id for course, room in self.schedule[day][period].course_room_pairs
        ]

        return teacher_id in teacher_ids_in_slot

    def _violating_room_capacity_constraint(self, day: int, period: int, course_id: str) -> bool:
        """
            Helper function to check if a slot violates a room capacity constraint.
            :param day: int
            :param period:  int
            :param course_id: str
            :return: bool
        """

        course = [course for course in self.courses if course.course_id == course_id][0]
        course_room_pairs = self.schedule[day][period].course_room_pairs

        if len(course_room_pairs) == len(self.rooms):
            return True

        occupied_room_ids = [room.room_id for _, room in course_room_pairs]
        available_rooms = [
            room for room in self.rooms
            if (
                    room.room_capacity >= course.number_of_students
                    and room.room_id not in occupied_room_ids
            )
        ]

        return len(available_rooms) == 0

    def _calculate_saturation_degree(self, course_id: str, teacher_id: str) -> int:
        """
            calculate the number of feasible periods in the timetable at the current point of construction are given priority for the course
            :param course_id: str
            :param teacher_id: str
            :return: int
        """

        saturation_degree = self.problem.number_of_days * self.problem.number_of_periods_per_day

        for day in range(len(self.schedule)):
            for period in range(len(self.schedule[day])):
                if self._already_in_slot(day, period, course_id):
                    saturation_degree -= 1
                if self._violating_unavailability_constraint(day, period, course_id):
                    saturation_degree -= 1
                if self._violating_curriculum_constraint(day, period, course_id):
                    saturation_degree -= 1
                if self._violating_teacher_constraint(day, period, teacher_id):
                    saturation_degree -= 1
                if self._violating_room_capacity_constraint(day, period, course_id):
                    saturation_degree -= 1

        return saturation_degree

    def _get_saturation_degree_dict(self):
        """"
            Generates and returns a dictionary of the saturation degree of each course
            :return: dict
        """
        saturation_degree_dict = {
            course.course_id: self._calculate_saturation_degree(
                course.course_id,
                course.teacher_id
            ) for course in self.courses
        }

        sorted_courses = sorted(
            self.courses,
            key=lambda course: (
                saturation_degree_dict[course.course_id],
                -course.number_of_students
            )
        )

        return {
            course.course_id: saturation_degree_dict[course.course_id] for course in sorted_courses
        }

    def initialize_slots(self) -> None:
        """
            Initializes the slots of the timetable.
            :return: None
        """

        number_of_lectures_left_to_be_scheduled_dict: dict = {
            course.course_id: course.number_of_lectures for course in self.courses
        }

        # while there are courses left to be scheduled
        while any(
                number_of_lectures_left_to_be_scheduled_dict[course.course_id] > 0
                for course in self.courses
        ):
            saturation_degree_dict = self._get_saturation_degree_dict()

            # get first course in saturation_degree_dict
            course_id = list(saturation_degree_dict.keys())[0]

            # decrement number of lectures left to be scheduled for course
            number_of_lectures_left_to_be_scheduled_dict[course_id] -= 1
            break

    def print(self):
        """
        Print a 2d array of the timetable (on each slot print the course id and not the room in course room pairs
        :return: void
        """
        "[ [A, B], [C, D] ] example"

        for day in self.schedule:
            for slot in day:
                course_ids = [course.course_id for course, room in slot.course_room_pairs]
                print(course_ids, end=" ")
            print()
        print()
