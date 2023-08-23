from typing import List, Tuple

from course import Course
from room import Room


class Slot:

    def __init__(self):
        self.course_room_pairs: List[Tuple[Course, Room]] = []
