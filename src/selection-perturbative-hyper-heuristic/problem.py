import os
from typing import List

from config import DATA_PATH
from constraint import Constraint
from course import Course
from curriculum import Curriculum
from room import Room


class Problem:
    def __init__(self, problem_instance_index: int):
        problem_instance_filenames_list: List[str] = os.listdir(DATA_PATH)
        self.selected_problem_instance_filename: str = problem_instance_filenames_list[
            problem_instance_index
        ]
        self.file_content: List[str] | None = None

        self.name: str | None = None
        self.number_of_courses: int | None = None
        self.number_of_rooms: int | None = None
        self.number_of_days: int | None = None
        self.number_of_periods_per_day: int | None = None
        self.number_of_curricula: int | None = None
        self.number_of_constraints: int | None = None

        self.courses: List[Course] | None = None
        self.rooms: List[Room] | None = None
        self.curricula: List[Curriculum] | None = None
        self.constraints: List[Constraint] | None = None

    def _extract_basic_information(self) -> None:
        """
            Extracts the basic information from the file content.
            :return: None
        """

        self.name = self.file_content[0].split(": ", 1)[1]
        self.number_of_courses = int(self.file_content[1].split(": ", 1)[1])
        self.number_of_rooms = int(self.file_content[2].split(": ", 1)[1])
        self.number_of_days = int(self.file_content[3].split(": ", 1)[1])
        self.number_of_periods_per_day = int(self.file_content[4].split(": ", 1)[1])
        self.number_of_curricula = int(self.file_content[5].split(": ", 1)[1])
        self.number_of_constraints = int(self.file_content[6].split(": ", 1)[1])

    def _extract_courses(self) -> None:
        """
            Extracts the courses from the file content.
            :return: None
        """

        courses_string_index: int = self.file_content.index("COURSES:\n")
        self.courses = []

        for course_index in range(
                courses_string_index + 1,
                courses_string_index + 1 + self.number_of_courses
        ):
            course: Course = Course(course_content=self.file_content[course_index])
            self.courses.append(course)

    def _extract_rooms(self) -> None:
        """
            Extracts the rooms from the file content.
            :return: None
        """

        rooms_string_index: int = self.file_content.index("ROOMS:\n")
        self.rooms = []

        for room_index in range(
                rooms_string_index + 1,
                rooms_string_index + 1 + self.number_of_rooms
        ):
            room: Room = Room(room_content=self.file_content[room_index])
            self.rooms.append(room)

    def _extract_curricula(self) -> None:
        """
            Extracts the curricula from the file content.
            :return: None
        """

        curricula_string_index: int = self.file_content.index("CURRICULA:\n")
        self.curricula = []

        for curricula_index in range(
                curricula_string_index + 1,
                curricula_string_index + 1 + self.number_of_curricula
        ):
            curriculum: Curriculum = Curriculum(
                curricula_content=self.file_content[curricula_index]
            )

            for course in self.courses:
                if course.course_id in self.file_content[curricula_index].split():
                    curriculum.course_ids.append(course.course_id)
            self.curricula.append(curriculum)

    def _extract_constraints(self) -> None:
        """
            Extracts the constraints from the file content.
            :return: None
        """

        constraints_string_index: int = self.file_content.index("UNAVAILABILITY_CONSTRAINTS:\n")
        self.constraints = []

        for constraint_index in range(
                constraints_string_index + 1,
                constraints_string_index + 1 + self.number_of_constraints
        ):
            constraint = Constraint(constraint_content=self.file_content[constraint_index])
            self.constraints.append(constraint)

    def initialize(self) -> None:
        """
            Initializes the problem instance. Reads the file and extracts the information.
            :return: None
        """
        with open(
                os.path.join(DATA_PATH, self.selected_problem_instance_filename),
                "r"
        ) as problem_instance_file:
            self.file_content = problem_instance_file.readlines()
            self._extract_basic_information()
            self._extract_courses()
            self._extract_rooms()
            self._extract_curricula()
            self._extract_constraints()
