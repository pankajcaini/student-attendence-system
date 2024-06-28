# Student Attendance System

This project is a Django-based student attendance system that provides three panels: one for students, one for teachers, and one for administrators.

## Technologies Used

- HTML
- CSS
- JavaScript
- Django
- SQLite

## Features

### Teacher Panel
- Teachers can log in to view a list of lectures they need to deliver on a particular day, with additional information such as lecture timing and room number.
- The current lecture is highlighted.
- By clicking on a particular lecture, teachers can see a list of students enrolled in that course.
- Teachers can mark each student as present or absent.
- A search bar is provided to search for a student by name.
- After marking attendance, teachers can submit the attendance record.

### Student Panel
- Students need to log in first.
- After logging in, students will see a list of all subjects along with additional information such as the total number of lectures, the number of lectures attended, the number of absences, and the attendance percentage.
- The name of the teacher for each subject is also displayed.
- When a student clicks on a particular subject, they will get a detailed attendance record, including a list of dates and whether the student was present or absent on each date.

### Admin Panel
The admin panel allows the administrator to manage the following:
1. Department information
2. Teacher information
3. Lecture information, including which teacher will teach which subject to which course, and the timing of the lectures
4. Student information
5. Courses
