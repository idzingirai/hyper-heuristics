from typing import List

from course import Course
from room import Room


class Slot:

    def __init__(self):
        self.course_room_pair: List[Course, Room] = []
