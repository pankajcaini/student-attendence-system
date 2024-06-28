from django.db import models



class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name



class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, default=None)
    duration = models.IntegerField()
    number_of_semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name



class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name



class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=255, unique=True)
    enroll_number = models.CharField(max_length=255, unique=True)
    admission_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    session = models.CharField(max_length=255)
    password = models.CharField(max_length=20, default="unitstu@1234")

    def __str__(self):
        return self.student_name



class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email_id = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField()
    password = models.CharField(max_length=20, default="unit@1234")

    def __str__(self):
        return self.name




class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    room_number = models.CharField(max_length=255)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)

    
    class Meta:
        unique_together = ('teacher', 'start_time')


    def __str__(self):
        return f"Lecture {self.lecture_id} - {self.subject.subject_name}"




class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='Absent')
    date = models.DateField(auto_now_add=True)



    class Meta:
        unique_together = ('student', 'lecture', 'date')

    def __str__(self):
        return f"{self.student} - {self.lecture} - {self.date} - {self.status}"
    

