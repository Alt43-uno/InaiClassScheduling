
class Professor:
    def __init__(self, id, name):
        self.Id = id
        self.Name = name
        self.CourseClasses = []

    def addCourseClass(self, courseClass):
        self.CourseClasses.append(courseClass)
        
    def __eq__(self, rhs):
        return self.Id == rhs.Id
