import random
from typing import List, Tuple, Optional

from constraint import Constraint
from course import Course
from problem import Problem
from room import Room
from slot import Slot


class Timetable:

    def __init__(self, problem: Problem):
        self.problem: Problem = problem
        self.constraints: List[Constraint] = self.problem.constraints

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

    def _violating_unavailability_constraint(
            self,
            day: int,
            period: int,
            course_id: str
    ) -> bool:
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

    def _violating_curriculum_constraint(
            self,
            day: int,
            period: int,
            course_id: str,
    ) -> bool:
        """
            Helper function to check if a slot violates a curriculum constraint.
            :param day: int
            :param period: int
            :param course_id: str
            :return: bool
        """
        # get the list of courses ids in the slot
        course_ids_in_slot: List[str] = [
            course.course_id for course, room in self.schedule[day][period].course_room_pair
        ]

        for c_id in course_ids_in_slot:
            for curriculum in self.problem.curricula:
                if c_id in curriculum.course_ids and course_id in curriculum.course_ids:
                    return True

        return False

    def _violating_teacher_constraint(
            self,
            teacher_id: str,
            course_room_pairs: List[Tuple[Course, Room]]
    ) -> bool:
        """
            Helper function to check if a slot violates a teacher constraint.
            :param teacher_id: str
            :param course_room_pairs: List[Tuple[Course, Room]]
            :return: bool
        """
        teacher_ids_in_slot: List[str] = [
            course.teacher_id for course, room in course_room_pairs
        ]

        return teacher_id in teacher_ids_in_slot

    def _select_free_slot(self, course: Course) -> Tuple[int, int, Optional[Room]]:
        free_slots: List[Tuple[int, int]] = []
        for day in range(len(self.schedule)):
            for period in range(len(self.schedule[day])):
                if len(self.schedule[day][period].course_room_pair) == 0:
                    free_slots.append((day, period))

        free_slots_not_violating_unavailability_constraint: List[Tuple[int, int]] = []
        for day, period in free_slots:
            if not self._violating_unavailability_constraint(day, period, course.course_id):
                free_slots_not_violating_unavailability_constraint.append((day, period))

        if free_slots_not_violating_unavailability_constraint:
            day, period = random.choice(free_slots_not_violating_unavailability_constraint)
            room = self._get_room_with_capacity(
                course.number_of_students,
                self.schedule[day][period].course_room_pair
            )
            if room:
                return day, period, room

        return -1, -1, None

    def _get_feasible_slot(self, course: Course) -> Tuple[int, int, Optional[Room]]:
        for x in range(len(self.schedule)):
            for y in range(len(self.schedule[x])):
                if not self._violating_unavailability_constraint(x, y, course.course_id):
                    if not self._violating_curriculum_constraint(x, y, course.course_id):
                        course_room_pairs = self.schedule[x][y].course_room_pair

                        if (
                                len(course_room_pairs) < self.problem.number_of_rooms - 1
                                and not self._violating_teacher_constraint(
                                    course.teacher_id,
                                    course_room_pairs
                                )
                        ):

                            room = self._get_room_with_capacity(
                                course.number_of_students,
                                self.schedule[x][y].course_room_pair
                            )
                            if room:
                                return x, y, room

        return -1, -1, None

    def _get_room_with_capacity(
            self,
            number_of_students,
            course_room_pairs: List[Tuple[Course, Room]]
    ) -> Room | None:
        occupied_room_ids = [room.room_id for _, room in course_room_pairs]
        available_rooms = [
            room for room in self.problem.rooms
            if room.room_capacity >= number_of_students and room.room_id not in occupied_room_ids
        ]

        if available_rooms:
            return min(
                available_rooms,
                key=lambda room: room.room_capacity
            ).clone()
        else:
            all_rooms = self.problem.rooms

            # get any room that is not in the occupied_room_ids
            available_rooms = [
                room for room in all_rooms
                if room.room_id not in occupied_room_ids
            ]

            if not available_rooms:
                return random.choice(self.problem.rooms).clone()

            return max(
                available_rooms,
                key=lambda room: room.room_capacity
            ).clone()

    def initialize_slots(self) -> None:
        """
            Initializes the slots of the timetable.
            :return: None
        """
        course_dict = {course.course_id: 0 for course in self.problem.courses}

        constraint: Constraint
        for constraint in self.problem.constraints:
            course_dict[constraint.course_id] += 1

        sorted_courses: List[Course] = sorted(
            self.problem.courses,
            key=lambda course: course_dict[course.course_id], reverse=True
        )

        course: Course
        for course in sorted_courses:
            for _ in range(course.number_of_lectures):
                day, period, room = self._select_free_slot(course)

                if day == -1 and period == -1 and room is None:
                    day, period, room = self._get_feasible_slot(course)

                self.schedule[day][period].course_room_pair.append((course, room))