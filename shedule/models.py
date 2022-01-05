from django.db import models

class Professor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

ROOMS = (
    ("501", "501"),
    ("501a", "501a"),
    ("502", "502"),
    ("503", "503"),
    ("504", "504"),
    ("505", "505"),
    ("506", "506"),
    ("507", "507"),
    ("508", "508"),
    ("509", "509"),
    ("510", "510"),
    ("511", "511"),
    
)

class Room(models.Model):
    name = models.CharField(max_length=15, choices=ROOMS)
    size = models.IntegerField(default=40)

    def __str__(self):
        return f"{self.name}"

GROUPS = (
    # 21
    ('AIN-1-21', 'AIN-1-21'),
    ('AIN-2-21', 'AIN-2-21'),
    ('AIN-3-21', 'AIN-3-21'),
    ('WIN-1-21', 'WIN-1-21'),
    ('MIN-1-21', 'MIN-1-21'),
    # 20
    ('AIN-1-20', 'AIN-1-20'),
    ('AIN-2-20', 'AIN-2-20'),
    ('AIN-3-20', 'AIN-3-20'),
    ('WIN-1-20', 'WIN-1-20'),
    ('MIN-1-20', 'MIN-1-20'),
    # 19
    ('AIN-1-19', 'AIN-1-19'),
    ('AIN-2-19', 'AIN-2-19'),
    ('AIN-3-19', 'AIN-3-19'),
    ('WIN-1-19', 'WIN-1-19'),
    ('MIN-1-19', 'MIN-1-19'),
    # 18
    ('AIN-1-18', 'AIN-1-18'),
    ('AIN-2-18', 'AIN-2-18'),
    ('AIN-3-18', 'AIN-3-18'),
    ('WIN-1-18', 'WIN-1-18'),
    ('MIN-1-18', 'MIN-1-18'),
    # admin
    ('admin', 'admin'),
)

class Group(models.Model):
    name = models.CharField(max_length=15, choices=GROUPS)
    size = models.IntegerField(default=40)

    def __str__(self):
        return f"{self.name}"

class Class(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="classes")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classes")
    duration = models.IntegerField(default=1)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return f"[{self.groups}] - {self.course} - {self.professor}"
