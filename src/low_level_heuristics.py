import random
from typing import List, Tuple

from timetable import Timetable


def single_move(timetable: Timetable) -> Timetable:
    """"
        moves a single lecture selected a new feasible slot
        :param timetable: Timetable
        :return: Timetable
    """

    scheduled_slots: List[Tuple[int, int]] = []

    for day in range(len(timetable.schedule)):
        for period in range(len(timetable.schedule[day])):
            if len(timetable.schedule[day][period].course_room_pairs) > 0:
                scheduled_slots.append((day, period))

    day, period = scheduled_slots[random.randint(0, len(scheduled_slots) - 1)]
    slot = timetable.schedule[day][period]

    random_course_index = random.randint(0, len(slot.course_room_pairs) - 1)
    course_room_pair = slot.course_room_pairs[random_course_index]

    timetable.schedule[day][period].course_room_pairs.pop(random_course_index)

    course_id = course_room_pair[0].course_id
    new_day, new_period, room = timetable.get_feasible_slot(course_id)

    timetable.schedule[new_day][new_period].course_room_pairs.append(course_room_pair)

    return timetable


def swap_slots(timetable: Timetable) -> Timetable:
    """
    Swap two slots selected at random of the timetable
    :param timetable:
    :return: timetable
    """

    first_selected_day = random.randint(0, len(timetable.schedule) - 1)
    first_selected_period = random.randint(0, len(timetable.schedule[first_selected_day]) - 1)
    second_selected_day = random.randint(0, len(timetable.schedule) - 1)
    second_selected_period = random.randint(0, len(timetable.schedule[second_selected_day]) - 1)

    first_slot = timetable.schedule[first_selected_day][first_selected_period].clone()
    second_slot = timetable.schedule[second_selected_day][second_selected_period].clone()

    timetable.schedule[first_selected_day][first_selected_period] = second_slot
    timetable.schedule[second_selected_day][second_selected_period] = first_slot

    return timetable
