class Constraint:

    def __init__(self, constraint_content: str):
        constraint_content_list = constraint_content.split()

        self.course_id: str = constraint_content_list[0]
        self.day: int = int(constraint_content_list[1])
        self.period: int = int(constraint_content_list[2])
