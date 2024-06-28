from django.shortcuts import render, redirect, HttpResponse
from app.models import Lecture, Teacher, Student, Attendance, Subject
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import date


months = {
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July'
}


weekday  = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

YEAR = {
    1:"1st Year",
    2:"2nd Year",
    3:"3rd Year",
    4:"4th Year",
    5:"5th Year",
    6:"6th Year",
    7:"7th Year",
    8:"8th Year"
}

SEM = {
    1:"1st Sem",
    2:"2nd Sem",
    3:"3rd Sem",
    4:"4th Sem",
    5:"5th Sem",
    6:"6th Sem",
    7:"7th Sem",
    8:"8th Sem"
}


def login_option(request):
    return render(request, 'login_options.html')





def teacher_login(request):

    teacher_id = request.session.get('teacher-id', None)
    if teacher_id is not None:
        return redirect('teacher-home-page')

    if request.method == 'GET':
        return render(request, 'teacher_login.html',{'credential_error':False,
                                                     'phone_number':'',
                                                     'password':''})
    
    if request.method == 'POST':
        phone_number = request.POST['phone-number']
        password = request.POST['password']
        try:
            teacher = Teacher.objects.get(phone_number=phone_number, password=password)
            request.session['teacher-id'] = teacher.teacher_id
            request.session['user-type'] = 'teacher'
            return redirect('teacher-home-page')
        except Teacher.DoesNotExist: # Wrong credential
            return render(request, 'teacher_login.html',{'credential_error':True,
                                                         'phone_number':phone_number,
                                                         'password':password} )

def teacher_homepage(request):
    
    teacher_id = request.session.get('teacher-id', None)
    if teacher_id is None:
        return redirect('teacher-login')
    
    teacher = Teacher.objects.get(pk=teacher_id)
    lecs = Lecture.objects.filter(teacher=teacher).order_by('start_time')
    
    today_date = date.today()
    hyphen = "-"

    context = {
        'teacher':teacher,
        'lectures':lecs,
        'date': str(today_date.day) + hyphen + str(months[today_date.month]) + hyphen + str(today_date.year)+ " | " + weekday[today_date.weekday()]
        }

    return render(request, 'lectures.html', context)

def attendence(request, lecture_id):

    teacher_id = request.session.get('teacher-id', None)
    if teacher_id is None:
        return redirect('teacher-login')
    
    try:
        lecture = Lecture.objects.get(pk=lecture_id)
    except Lecture.DoesNotExist:
        return redirect('teacher-home-page')
    
    teacher_id_in_lecture = lecture.teacher.teacher_id

    if teacher_id != teacher_id_in_lecture:
        return redirect('teacher-home-page')
    

    course = lecture.course
    year = lecture.year
    semester = lecture.semester
    count = Attendance.objects.filter(lecture=lecture, date=date.today()).count()


    if count == 0: # attendence not taken
        students = Student.objects.filter(course=course, year=year, semester=semester).values('student_id','student_name')
        today_date = date.today()
        hyphen = "-"
        context = {
            'students':students,
            'lecture_id':lecture_id, 
            'student':lecture.subject.subject_name,
            'date': str(today_date.day) + hyphen + str(months[today_date.month]) + hyphen + str(today_date.year)+ " | " + weekday[today_date.weekday()],
            'course': course.short_name + YEAR[year] + SEM[semester]
            }
        return render(request, 'attendence.html', context)
    

    else: # attendence  taken already
        res = Attendance.objects.filter(lecture=lecture, date=date.today())
        today_date = date.today()
        hyphen = "-"
        context = {
            'date': str(today_date.day) + hyphen + str(months[today_date.month]) + hyphen + str(today_date.year)+ " | " + weekday[today_date.weekday()],
            'course': f"{course.short_name}  {YEAR[year]}  {SEM[semester]}",
            'recs':res,
            'subject':lecture.subject.subject_name
        }
        return render(request, 'attendence_record.html', context)

@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_status = data.get('attendance_status', {})
            lecture_id = data.get('lecture_id')

            lecture = get_object_or_404(Lecture, pk=lecture_id)

            for student_id, status in attendance_status.items():
                student = get_object_or_404(Student, pk=student_id)
                attendance = Attendance(student=student, lecture=lecture, status=status)
                attendance.save()

            return JsonResponse({'status': 'success', 'message': 'Attendance recorded successfully.'})

        except (ValueError, KeyError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def teacher_logout(request):
    request.session.flush()
    return redirect('login-options')






# Student 
def student_login(request):

    teacher_id = request.session.get('teacher-id', None)
    if teacher_id is not None:
        return redirect('teacher-home-page')

    student_id = request.session.get('student-id', None)
    if student_id is not None:
        return redirect('student-home-page')
    

    if request.method == 'GET':
        return render(request, 'student_login.html', {'credential_error':False})


    if request.method == 'POST':
        phone_number = request.POST['phone-number']
        password = request.POST['password']

       
        try:
            student =  Student.objects.get(phone_number=phone_number, password=password)
            request.session['student-id'] = student.student_id
            request.session['user-type'] = 'student'
            return redirect('student-home-page')
        except:
            return render(request, 'student_login.html', {'credential_error':True})



def student_home_page(request):

    student_id = request.session.get('student-id', None)
    if student_id is None:
        return redirect('student-login')
    
    student = Student.objects.get(pk=student_id)
    course = student.course
    year = student.year
    semester = student.semester
    department = student.department
    subjects = Subject.objects.filter(course=course, year=year, semester=semester, department=department)

    for sub in subjects:
        print(sub)
    
    records = []
    for subject in subjects:
        try:
            lecture = Lecture.objects.get(subject=subject, course=course, year=year, semester=semester)
        except Lecture.DoesNotExist:
            continue
        attendence = Attendance.objects.filter(student=student, lecture=lecture)

        subject_name = lecture.subject.subject_name
        total_lecture = attendence.count()
        present = attendence.filter(status="present").count()
        absent = attendence.filter(status="absent").count()
        teacher_name = lecture.teacher.name
        percentage = 0

        if total_lecture != 0:
            tmp = (present/total_lecture) * 100 
            percentage = str(tmp) + "%"
        
    
        records.append({
            'lecture_id':lecture.lecture_id,
            'subject_name':subject_name,
            'total_lecture':total_lecture,
            'present':present,
            'absent':absent,
            'percentage':percentage,
            'teacher_name':teacher_name
        })

    return render(request, 'student-home-page.html', {'records':records})





def student_attendence_record(request, lecture_id):
    student_id = request.session.get('student-id', None)
    if student_id is None:
        return redirect('student-login')
    
    lecture = Lecture.objects.get(pk=lecture_id)
    recs = Attendance.objects.filter(
        student = Student.objects.get(pk=student_id),
        lecture =  lecture
    )

    return render(request, 'student-attendence-record.html', {'recs':recs,'subject':lecture.subject.subject_name})
    






def student_logout(request):
    request.session.flush()
    return redirect('login-options')