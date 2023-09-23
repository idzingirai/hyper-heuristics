class Room:

    def __init__(self, room_content: str):
        self.room_content = room_content
        self.room_content_list = room_content.split()

        self.room_id = self.room_content_list[0]
        self.room_capacity = int(self.room_content_list[1])

    def clone(self):
        return Room(self.room_content)
