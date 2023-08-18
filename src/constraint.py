from typing import List

from course import Course
from src.course import Course


def _get_course(course_id: str, courses: List[Course]) -> Course | None:
    for course in courses:
        if course.course_id == course_id:
            return course
    return None


class Constraint:

    def __init__(self, constraint_content_list: str, courses: List[Course]):
        constraint_content_list = constraint_content_list.split()

        self.course: Course = _get_course(constraint_content_list[0], courses)
        self.day: int = int(constraint_content_list[1])
        self.period: int = int(constraint_content_list[2])
