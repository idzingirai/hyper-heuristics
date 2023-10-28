import random
from typing import List, Tuple, Optional

from src.common.constraint import Constraint
from src.common.constraints_validator import get_num_of_violated_soft_constraints
from src.common.course import Course
from src.common.curriculum import Curriculum
from src.common.problem import Problem
from src.common.room import Room
from src.common.slot import Slot


class Timetable:

    def __init__(self, problem: Problem):
        self.problem: Problem = problem
        self.constraints: List[Constraint] = self.problem.constraints
        self.rooms: List[Room] = self.problem.rooms
        self.courses: List[Course] = self.problem.courses
        self.curricula: List[Curriculum] = self.problem.curricula

        self.schedule: List[List[Slot]] = [
            [Slot() for _ in range(problem.number_of_periods_per_day)]
            for _ in range(problem.number_of_days)
        ]

        self.course_and_first_room = {}
        for course in self.courses:
            self.course_and_first_room[course.course_id] = ""

    def _get_course(self, course_id: str) -> Course:
        """
            Helper function to get a course by its id.
            :param course_id: str
            :return: Course
        """

        return [course for course in self.courses if course.course_id == course_id][0]

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

    def _violating_room_occupancy_constraint(self, day: int, period: int, course_id: str) -> bool:
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
            calculate the number of feasible periods in the timetable at the current point of
             construction are given priority for the course
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
                if self._violating_room_occupancy_constraint(day, period, course_id):
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

    def _get_room_for_course(
            self,
            course_id: str,
            first_room: str,
            course_room_pairs: List[Tuple[Course, Room]]
    ) -> Room:
        """
            Returns the room for a course based on the room occupancy constraint and feasibility
            :param course_id: str
            :param course_room_pairs: List[Tuple[Course, Room]]
            :return: Room
        """

        course = self._get_course(course_id)
        number_of_students = course.number_of_students

        occupied_rooms_ids = [room.room_id for _, room in course_room_pairs]

        available_rooms = [
            room for room in self.rooms
            if room.room_capacity >= number_of_students and room.room_id not in occupied_rooms_ids
        ]

        available_rooms.sort(key=lambda room: room.room_capacity)

        if len(available_rooms) > 0:
            for room in available_rooms:
                if room.room_id == first_room:
                    return room
            return available_rooms[0]
        else:
            not_occupied_rooms = [
                room for room in self.rooms if room.room_id not in occupied_rooms_ids
            ]

            if len(not_occupied_rooms) == 0:
                for room in self.rooms:
                    if room.room_id == first_room:
                        return room.clone()
                    elif room.room_capacity >= number_of_students:
                        return room.clone()

            not_occupied_rooms.sort(key=lambda room: room.room_capacity, reverse=True)
            return not_occupied_rooms[0]

    def _calculate_soft_constraint(
            self,
            course_id: str,
            feasible_slots: List[Tuple[int, int]]
    ) -> int:
        """"
            Calculates the soft constraint cost for each feasible slot and returns the index of the slot with the
            smallest cost
            :param course_id: str
            :param feasible_slots: List[Tuple[int, int]]
            :return: int
        """

        slots_costs = []
        course: Course = self._get_course(course_id)

        for day, period in feasible_slots:
            room: Room = self._get_room_for_course(
                course_id,
                self.course_and_first_room[course_id],
                self.schedule[day][period].course_room_pairs
            )

            self.schedule[day][period].course_room_pairs.append((course, room))
            slots_costs.append(
                get_num_of_violated_soft_constraints(
                    self.schedule,
                    self.problem.curricula,
                    self.courses
                )
            )
            self.schedule[day][period].course_room_pairs.remove(
                self.schedule[day][period].course_room_pairs[-1])

        index_of_smallest_cost = 0
        smallest_cost = slots_costs[index_of_smallest_cost]

        for index in range(1, len(slots_costs)):
            if slots_costs[index] <= smallest_cost:
                smallest_cost = slots_costs[index]
                index_of_smallest_cost = index

        return index_of_smallest_cost

    def get_feasible_slot(self, course_id: str, retry: bool) -> Tuple[int, int, Optional[Room]]:
        """
            Returns a feasible slot for a course in the timetable in the form of a tuple (day, period, room)
            :param course_id: str
            :return: Tuple[int, int, Room]
        """

        teacher_id = [
            course.teacher_id for course in self.courses if course.course_id == course_id
        ][0]

        feasible_slots: List[Tuple[int, int]] = []

        for day in range(len(self.schedule)):
            for period in range(len(self.schedule[day])):
                if (
                        not self._already_in_slot(day, period, course_id) and
                        not self._violating_unavailability_constraint(day, period, course_id) and
                        not self._violating_curriculum_constraint(day, period, course_id) and
                        not self._violating_teacher_constraint(day, period, teacher_id) and
                        not self._violating_room_occupancy_constraint(day, period, course_id)
                ):
                    feasible_slots.append((day, period))

        if len(feasible_slots) > 0:
            feasible_slot_index = (
                self._calculate_soft_constraint(course_id, feasible_slots)
                if retry is False else random.randint(0, len(feasible_slots) - 1)
            )
            day, period = feasible_slots[feasible_slot_index]

            first_room_id = self.course_and_first_room[course_id]

            room = self._get_room_for_course(
                course_id,
                first_room_id,
                self.schedule[day][period].course_room_pairs
            )

            if first_room_id == "":
                self.course_and_first_room[course_id] = room.room_id
            return day, period, room

        return -1, -1, None

    def clone(self):
        """
            Clones the timetable.
            :return: Timetable
        """

        timetable = Timetable(self.problem)
        timetable.schedule = [
            [slot.clone() for slot in day] for day in self.schedule
        ]

        return timetable

    def initialize_slots(self) -> None:
        """
            Initializes the slots of the timetable.
            :return: None
        """

        number_of_lectures_left_to_be_scheduled_dict: dict = {
            course.course_id: course.number_of_lectures for course in self.courses
        }

        retry: bool = False

        while any(
                number_of_lectures_left_to_be_scheduled_dict[course.course_id] > 0
                for course in self.courses
        ):
            saturation_degree_dict = self._get_saturation_degree_dict()

            for course_id in list(saturation_degree_dict.keys()):
                if number_of_lectures_left_to_be_scheduled_dict[course_id] == 0:
                    del saturation_degree_dict[course_id]

            course_id = list(saturation_degree_dict.keys())[0]
            course = [course for course in self.courses if course.course_id == course_id][0]
            day, period, room = self.get_feasible_slot(course_id, retry)

            if day == -1 and period == -1 and room is None:
                self._clear_slots()
                number_of_lectures_left_to_be_scheduled_dict = {
                    course.course_id: course.number_of_lectures for course in self.courses
                }
                retry = True
                continue

            self.schedule[day][period].course_room_pairs.append((course, room))
            number_of_lectures_left_to_be_scheduled_dict[course_id] -= 1

    def print(self):
        """
            Print a 2d array of the timetable (on each slot print the course id and not the room in course room pairs
            :return: void
        """

        for day in self.schedule:

            current_slot_index: int = 0
            for slot in day:
                course_room_ids_pairs = [
                    (course.course_id, room.room_id) for course, room in slot.course_room_pairs
                ]

                if current_slot_index == len(day) - 1:
                    print([course_room_ids_pairs], end="\n")
                else:
                    print([course_room_ids_pairs], end=" - ")
                current_slot_index += 1
        print()

    def _clear_slots(self):
        """
            Clears all the slots in the timetable.
            :return: void
        """

        self.schedule = [
            [Slot() for _ in range(self.problem.number_of_periods_per_day)]
            for _ in range(self.problem.number_of_days)
        ]
