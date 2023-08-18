class Room:

    def __init__(self, room_content: str):
        room_content_list = room_content.split()

        self.room_id = room_content_list[0]
        self.room_capacity = int(room_content_list[1])
