from typing import List


class Curriculum:

    def __init__(self, curricula_content: str):
        curricula_content_list = curricula_content.split()

        self.curricula_id: str = curricula_content_list[0]
        self.number_of_courses: int = int(curricula_content_list[1])
        self.course_ids: List[str] = []
