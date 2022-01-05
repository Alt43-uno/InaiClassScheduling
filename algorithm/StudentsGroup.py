
class StudentsGroup:
    
    def __init__(self, id, name, numberOfStudents):
        self.Id = id
        self.Name = name
        self.NumberOfStudents = numberOfStudents
        self.CourseClasses = []

    
    def addClass(self, course_class):
        self.CourseClasses.append(course_class)

    def __hash__(self):
        return hash(self.Id)

    
    def __eq__(self, rhs):
        return self.Id == rhs.Id

    def __ne__(self, other):
        
        
        return not (self == other)
