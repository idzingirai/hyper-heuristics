class Course:

    def __init__(self, course_content: str):
        self.course_content = course_content
        course_content_list = course_content.split()

        self.course_id = course_content_list[0]
        self.teacher_id = course_content_list[1]
        self.number_of_lectures = int(course_content_list[2])
        self.min_working_days = int(course_content_list[3])
        self.number_of_students = int(course_content_list[4])

    def clone(self):
        return Course(self.course_content)
