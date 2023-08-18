import os
from typing import List

import config
from course import Course
from curriculum import Curriculum
from room import Room
from constraint import Constraint


class Problem:
    def __init__(self, problem_instance_index: int):
        problem_instance_filenames_list = os.listdir(config.DATA_PATH)
        self.selected_problem_instance_filename = problem_instance_filenames_list[
            problem_instance_index
        ]
        self.name: str | None = None
        self.courses: List[Course] | None = None
        self.rooms: List[Room] | None = None
        self.curricula: List[Curriculum] | None = None
        self.constraints: List[Constraint] | None = None

    def _extract_basic_information(self, file_content: List[str]):
        """
            Extracts the basic information from the file content.
            :param file_content
            :return: extracted information
        """

        self.name = file_content[0].split(": ", 1)[1]
        number_of_courses: int = int(file_content[1].split(": ", 1)[1])
        number_of_rooms: int = int(file_content[2].split(": ", 1)[1])
        number_of_days: int = int(file_content[3].split(": ", 1)[1])
        number_of_periods_per_day: int = int(file_content[4].split(": ", 1)[1])
        number_of_curricula: int = int(file_content[5].split(": ", 1)[1])
        number_of_constraints: int = int(file_content[6].split(": ", 1)[1])

        return (
            number_of_constraints,
            number_of_courses,
            number_of_curricula,
            number_of_days,
            number_of_periods_per_day,
            number_of_rooms
        )

    def _extract_courses(self, file_content: List[str], number_of_courses: int) -> None:
        """
            Extracts the courses from the file content.
            :param file_content
            :param number_of_courses to extract
            :return: None
        """

        courses_string_index: int = file_content.index("COURSES:\n")
        self.courses = []

        for course_index in range(
                courses_string_index + 1,
                courses_string_index + 1 + number_of_courses
        ):
            course = Course(file_content[course_index])
            self.courses.append(course)

    def _extract_rooms(self, file_content: List[str], number_of_rooms: int) -> None:
        """
            Extracts the rooms from the file content.
            :param file_content
            :param number_of_rooms
            :return: None
        """

        rooms_string_index = file_content.index("ROOMS:\n")
        self.rooms = []
        for room_index in range(
                rooms_string_index + 1,
                rooms_string_index + 1 + number_of_rooms
        ):
            room = Room(file_content[room_index])
            self.rooms.append(room)

    def _extract_curricula(self, file_content: List[str], number_of_curriculums: int) -> None:
        """
            Extracts the curricula from the file content.
            :param file_content
            :param number_of_curriculums
            :return: None
        """
        curricula_string_index = file_content.index("CURRICULA:\n")
        self.curricula = []

        for curricula_index in range(
                curricula_string_index + 1,
                curricula_string_index + 1 + number_of_curriculums
        ):
            curriculum = Curriculum(file_content[curricula_index])
            for course in self.courses:
                if course.course_id in file_content[curricula_index].split():
                    curriculum.courses.append(course)
            self.curricula.append(curriculum)

    def _extract_constraints(self, file_content, number_of_constraints):
        constraints_string_index = file_content.index("UNAVAILABILITY_CONSTRAINTS:\n")
        self.constraints = []
        for constraint_index in range(
                constraints_string_index + 1,
                constraints_string_index + 1 + number_of_constraints
        ):
            constraint = Constraint(file_content[constraint_index], self.courses)
            self.constraints.append(constraint)

    def initialize(self):
        with open(
                f"{config.DATA_PATH}{self.selected_problem_instance_filename}",
                "r"
        ) as problem_instance_file:
            file_content = problem_instance_file.readlines()

            (
                number_of_constraints,
                number_of_courses,
                number_of_curriculum,
                number_of_days,
                number_of_periods_per_day,
                number_of_rooms
            ) = self._extract_basic_information(file_content)

            self._extract_courses(file_content, number_of_courses)
            self._extract_rooms(file_content, number_of_rooms)
            self._extract_curricula(file_content, number_of_curriculum)
            self._extract_constraints(file_content, number_of_constraints)