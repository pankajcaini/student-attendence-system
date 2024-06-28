from django.contrib import admin
from .models import Department, Course, Subject, Student, Teacher, Lecture, Attendance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name')
    search_fields = ('department_name',)
    list_filter = ('department_name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'duration', 'number_of_semester', 'department')
    search_fields = ('course_name',)
    list_filter = ('department',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # list_display = ('subject_id', 'subject_name', 'course', 'year', 'semester', 'department')
    list_display = ('subject_id', 'subject_name', 'department', 'course', 'year', 'semester')
    search_fields = ('subject_name',)
    list_filter = ('course', 'department')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'phone_number', 'email', 'roll_number', 'enroll_number', 'admission_date', 'course', 'year', 'semester', 'department', 'session')
    search_fields = ('student_name', 'roll_number', 'enroll_number', 'email')
    list_filter = ('course', 'department', 'year', 'semester')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'name', 'phone_number', 'email_id', 'address', 'salary', 'date_joined')
    search_fields = ('name', 'email_id', 'phone_number')
    list_filter = ('date_joined',)

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('lecture_id', 'teacher', 'subject', 'course', 'year', 'semester', 'room_number', 'start_time', 'end_time')
    search_fields = ('lecture_id', 'teacher__name', 'subject__subject_name', 'course__course_name')
    list_filter = ('teacher', 'subject', 'course', 'year', 'semester')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lecture', 'status', 'date')
    search_fields = ('student__student_name', 'lecture__lecture_id', 'status')
    list_filter = ('status', 'date', 'lecture')

    def student_name(self, obj):
        return obj.student.student_name
    student_name.admin_order_field = 'student__student_name'
    student_name.short_description = 'Student Name'

    def lecture_id(self, obj):
        return obj.lecture.lecture_id
    lecture_id.admin_order_field = 'lecture__lecture_id'
    lecture_id.short_description = 'Lecture ID'


