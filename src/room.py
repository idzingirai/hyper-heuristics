class Room:

    def __init__(self, room_content_list: str):
        room_content_list = room_content_list.split()

        self.room_id = room_content_list[0]
        self.room_capacity = int(room_content_list[1])
