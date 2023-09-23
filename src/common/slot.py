from typing import List, Tuple

from src.common.course import Course
from src.common.room import Room


class Slot:

    def __init__(self):
        self.course_room_pairs: List[Tuple[Course, Room]] = []

    def clone(self):
        slot = Slot()

        for course, room in self.course_room_pairs:
            slot.course_room_pairs.append((course.clone(), room.clone()))
        return slot
