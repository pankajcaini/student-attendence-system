
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.login_option, name='login-options'),
    path('admin/', admin.site.urls),

    # Teacher
    path('teacher-login/', views.teacher_login, name='teacher-login'),
    path('teacher-home-page/', views.teacher_homepage, name="teacher-home-page"),
    path('attendence/<int:lecture_id>/', views.attendence, name="attendence"),
    path('insert-attendence-status/', views.mark_attendance),
    path('teacher-logout/', views.teacher_logout, name="teacher-logout"),

    # Student
    path('student-login/', views.student_login, name="student-login"),
    path('student-home-page/', views.student_home_page, name="student-home-page"),
    path('student-logout/', views.student_logout, name="student-logout"),
    path('student-attendence-record/<int:lecture_id>/', views.student_attendence_record, name="student-attendence-record"),
]
