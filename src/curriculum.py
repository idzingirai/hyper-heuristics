from typing import List

from course import Course


class Curriculum:

    def __init__(self, curricula_content_list: str):
        curricula_content_list = curricula_content_list.split()

        self.curricula_id: str = curricula_content_list[0]
        self.number_of_courses: int = int(curricula_content_list[1])
        self.courses: List[Course] = []
