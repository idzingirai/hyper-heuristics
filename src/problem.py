import os
from typing import List

import config
from course import Course
from room import Room


class Problem:
    def __init__(self, problem_instance_index: int):
        problem_instance_filenames_list = os.listdir(config.DATA_PATH)
        self.selected_problem_instance_filename = problem_instance_filenames_list[
            problem_instance_index
        ]
        self.name: str | None = None
        self.courses: List[Course] | None = None
        self.rooms: List[Room] | None = None

    def _extract_basic_information(self, file_content: List[str]):
        """
        Extracts the basic information from the file content.
        :param file_content:
        :return: extracted information
        """

        self.name = file_content[0].split(": ", 1)[1]
        number_of_courses = int(file_content[1].split(": ", 1)[1])
        number_of_rooms = int(file_content[2].split(": ", 1)[1])
        number_of_days = int(file_content[3].split(": ", 1)[1])
        number_of_periods_per_day = int(file_content[4].split(": ", 1)[1])
        number_of_curricula = int(file_content[5].split(": ", 1)[1])
        number_of_constraints = int(file_content[6].split(": ", 1)[1])

        return (
            number_of_constraints,
            number_of_courses,
            number_of_curricula,
            number_of_days,
            number_of_periods_per_day,
            number_of_rooms
        )

    def initialize(self):
        with open(
                f"{config.DATA_PATH}{self.selected_problem_instance_filename}",
                "r"
        ) as problem_instance_file:
            file_content = problem_instance_file.readlines()

            (
                number_of_constraints,
                number_of_courses,
                number_of_curricula,
                number_of_days,
                number_of_periods_per_day,
                number_of_rooms
            ) = self._extract_basic_information(file_content)

            print(number_of_courses)
            print(number_of_rooms)
            print(number_of_days)
            print(number_of_periods_per_day)
            print(number_of_curricula)
            print(number_of_constraints)
