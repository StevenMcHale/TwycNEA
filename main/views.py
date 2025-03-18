from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .filters import BookingFilter
from django.contrib.auth.decorators import login_required
from users.decorators import unauthenticated_user, allowed_users
from manual.extras import *
from auto.extras import *
import datetime
import pandas as pd
import random
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.templatetags.static import static
import os

# Create your views here.


def home(request):
    return render(request, 'main/home.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    lvi_students = Student.objects.filter(year_group="LVI").order_by('name')

    uvi_students = Student.objects.filter(year_group="UVI").order_by('name')

    parents = Parent.objects.all().order_by('name')

    teachers = Teacher.objects.all().order_by('name')

    subjects = Subject.objects.all().order_by('name')

    timeslots = Timeslot.objects.all()
    timeslots = sortTimeslots(timeslots)
    
    dates = EveningDate.objects.all()

    buildings = Building.objects.all().order_by('name')

    oldrooms = Room.objects.all()
    rooms = bubbleSortAlphaRooms(oldrooms)

    context = {'parents':parents, 'lvi_students':lvi_students, 'uvi_students':uvi_students, 'teachers':teachers, 'subjects':subjects, 'timeslots':timeslots, 'dates':dates, 'buildings':buildings, 'rooms':rooms}

    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'teacher'])
def bookings(request):
    try:

        bookings = Booking.objects.all()
        bookings = bookings.order_by('timeslot')

        total_bookings = bookings.count()
        complete = bookings.filter(status="Complete").count()
        pending = bookings.filter(status="Pending").count()

        myFilter = BookingFilter(request.GET, queryset=bookings)
        bookings = myFilter.qs

        context = {'bookings':bookings, 'total_bookings':total_bookings, 'complete':complete, 'pending':pending, 'myFilter':myFilter}

        return render(request, 'main/bookings.html', context)
    
    except:
        previous_page = request.META.get('HTTP_REFERER', None)
        context = {'previous_page': previous_page}
        return render(request, 'manual/error.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student(request, pk):
    student = Student.objects.get(id=pk)
    bookings = student.booking_set.all()
    total_bookings = bookings.count()
    subjects = student.subjects.all()
    teachers = student.teachers.all()

    finalBookings = sortBookings(bookings)

    context = {'student':student, 'bookings':finalBookings, 'total_bookings':total_bookings, 'subjects':subjects, 'teachers':teachers}

    return render(request, 'main/student.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def teacher(request, pk):
    teacher = Teacher.objects.get(id=pk)
    bookings = teacher.booking_set.all()
    total_bookings = bookings.count()
    subjects = teacher.subjects.all()
    students = Student.objects.filter(teachers__name=teacher.name)

    finalBookings = sortBookings(bookings)

    context = {'teacher':teacher, 'bookings':finalBookings, 'total_bookings':total_bookings, 'subjects':subjects, 'students':students}
    return render(request, 'main/teacher.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def room(request, pk):

    room = Room.objects.get(id=pk)
    teachers = room.teacher_set.all()


    context = {'room':room, 'teachers':teachers}
    return render(request, 'main/room.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def building(request, pk):

    building = Building.objects.get(id=pk)
    rooms = building.room_set.all()
    teachers = building.teacher_set.all()


    context = {'building':building, 'rooms':rooms, 'teachers':teachers}
    return render(request, 'main/building.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def subject(request, pk):

    subject = Subject.objects.get(id=pk)
    students = Student.objects.filter(subjects__name=subject.name)
    teachers = Teacher.objects.filter(subjects__name=subject.name)


    context = {'subject':subject, 'students':students, 'teachers':teachers}
    return render(request, 'main/subject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def date(request, pk):

    date = EveningDate.objects.get(id=pk)
    timeslots = date.timeslots.all()

    finalTimeslots = sortTimeslots(timeslots)


    context = {'date':date, 'timeslots':finalTimeslots}
    return render(request, 'main/date.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def timeslot(request, pk):

    timeslot = Timeslot.objects.get(id=pk)
    dates = EveningDate.objects.filter(timeslots__start_time=timeslot.start_time)


    context = {'timeslot':timeslot, 'dates':dates}
    return render(request, 'main/timeslot.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def spreadsheetLVI(request):

    date = EveningDate.objects.get(year_group='LVI')
    timeslots =  date.timeslots.all()
    teachers = Teacher.objects.all()
    teachers = teachers.order_by('name')

    finalTimeslots = sortTimeslots(timeslots)
    teachersAv = adminteachersAvailability(teachers, finalTimeslots, date)

    context = {'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
    return render(request, 'main/sheetLVI.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def spreadsheetUVI(request):

    date = EveningDate.objects.get(year_group='UVI')
    timeslots =  date.timeslots.all()
    teachers = Teacher.objects.all()
    teachers = teachers.order_by('name')

    finalTimeslots = sortTimeslots(timeslots)
    teachersAv = adminteachersAvailability(teachers, finalTimeslots, date)

    context = {'timeslots':finalTimeslots, 'teachers':teachers, 'teachersAv':teachersAv}
    return render(request, 'main/sheetLVI.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def parent(request, pk):
    parent = Parent.objects.get(id=pk)
    students = parent.students.all()


    context = {'parent':parent, 'students':students}

    return render(request, 'main/parent.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def bookUCAS(request):

    teachers = Teacher.objects.all()
    timeslots = Timeslot.objects.all()
    timeslots = sortTimeslots(timeslots)

    date = EveningDate.objects.get(year_group='LVI')
    student = Student.objects.get(name='UCAS')

    if request.method == 'POST':
        teacher = request.POST.get('teacher')
        timeslotHTML = request.POST.get('timeslot')

        teacher = Teacher.objects.get(name=teacher)



        if timeslotHTML == 'timeslot1':
            for timeslot in timeslots:
                if timeslot.start_time >= datetime.time(16,0,0) and timeslot.start_time < datetime.time(17,0,0):

                    Booking.objects.create(
                            student=student,
                            teacher=teacher,
                            timeslot=timeslot,
                            status='Pending',
                            date=date,
                        )


        elif timeslotHTML == 'timeslot2':
            for timeslot in timeslots:
                if timeslot.start_time >= datetime.time(18,0,0) and timeslot.start_time < datetime.time(19,0,0):

                    Booking.objects.create(
                            student=student,
                            teacher=teacher,
                            timeslot=timeslot,
                            status='Pending',
                            date=date,
                        )
        

        return redirect('bookings')


    

    context = {'teachers':teachers}
    return render(request, 'main/bookUCAS.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def loadTeachers(request):

    if request.method == 'POST':
        
        
        sheet_id = '1XpHVPrkKv2tbUdN7rAS2ThkpUmtsPWFYLWhycZsx7c8'

        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

        records = []

        for _, row in df.iterrows():
            teacher_name = row[0]  # First column contains the username
            teacher_code = row[1]
            teacher_email = row[2]
            teacher_building = row[3]
            teacher_room = row[4]
            subjects = row[5:].dropna().tolist()  # Columns for subjects (Option1 to Option4)
            
            # Append to the list in the format [username, [subjects], [teachers]]
            records.append([teacher_name, teacher_code, teacher_email, teacher_building, teacher_room, subjects])

        

        for record in records:
            name = record[0]
            email = record[2] + "@twycrosshouseschool.org.uk"

            number = random.randint(1000, 9999)
            password = 'twyc' + str(number)

            username = "staff_" + record[1]

            User.objects.create(
                username=username,
                email=email,
                password=password,
            )

            user = User.objects.get(username=username)

            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            newSubjects = []

            for sub in record[5]:
                newSubject = Subject.objects.get(name=sub)
                newSubjects.append(newSubject)

            building = record[3]
            building = Building.objects.get(name=building)
            room = record[4]
            room = Room.objects.get(name=room)


            
            Teacher.objects.create(
                user=user,
                name=name,
                email=email,
                building=building,
                room=room,
            )

            tea = Teacher.objects.get(name=name)
            tea.subjects.set(newSubjects)



        return redirect('dashboard')


    context = {}
    return render(request, 'main/loadTeachers.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def loadLVIStudents(request):

    if request.method == 'POST':

        
        sheet_id = '1EUuN4AYEq-a0VQdZdu5sXpY19vEx2ckSHlnAn7tBsno'

        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

        records = []

        for _, row in df.iterrows():
            student_name = row[0]  # First column contains the username
            subjects = row[1:5].dropna().tolist()  # Columns for subjects (Option1 to Option4)
            teachers = row[5:].dropna().tolist()  # Columns for teachers (Teacher1 to Teacher8)
            
            # Append to the list in the format [username, [subjects], [teachers]]
            records.append([student_name, subjects, teachers])

        

        for record in records:
            username = record[0]
            email = username + "@twycrosshouseschool.org.uk"
            level = 'LVI'

            number = random.randint(1000, 9999)
            password = 'twyc' + str(number)

            User.objects.create(
                username=username,
                email=email,
                password=password,
            )

            user = User.objects.get(username=username)

            group = Group.objects.get(name='student')
            user.groups.add(group)

            newSubjects = []

            for sub in record[1]:
                newSubject = Subject.objects.get(name=sub)
                newSubjects.append(newSubject)

            newTeachers = []
            
            for code in record[2]:
                tUsername = 'staff_' + code
                tUser = User.objects.get(username=tUsername)
                newTeacher = Teacher.objects.get(user=tUser)
                newTeachers.append(newTeacher)

            
            Student.objects.create(
                user=user,
                name=username,
                email=email,
                year_group=level,
            )

            stu = Student.objects.get(name=username)
            stu.subjects.set(newSubjects)
            stu.teachers.set(newTeachers)



        return redirect('dashboard')


    context = {}
    return render(request, 'main/loadLVI.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emailStudent(request, pk):

    student = Student.objects.get(id=pk)
    username = student.user.username
    password = student.user.password
    email = student.email
    link = "https://twyc-nea.vercel.app/login"

    if request.method == 'POST':

        send_mail(
            "Parents' Evening",
            f"Link to login page: {link}, Username: {username}, Password: {password}",
            "twycrossbooking@gmail.com",
            [f"{email}"],
            fail_silently=False,
        )

        return redirect('dashboard')


    context = {'student':student}
    return render(request, 'main/emailStudent.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emailTeacher(request, pk):

    teacher = Teacher.objects.get(id=pk)
    username = teacher.user.username
    password = teacher.user.password
    email = teacher.email
    link = "https://twyc-nea.vercel.app/login"

    if request.method == 'POST':

        send_mail(
            "Parents' Evening",
            f"Link to login page: {link}, Username: {username}, Password: {password}",
            "twycrossbooking@gmail.com",
            [f"{email}"],
            fail_silently=False,
        )

        return redirect('dashboard')


    context = {'teacher':teacher}
    return render(request, 'main/emailTeacher.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emailAllStudents(request):

    students = Student.objects.filter(year_group="LVI")
    link = "https://twyc-nea.vercel.app/login"

    if request.method == 'POST':

        for student in students:
            username = student.user.username
            password = student.user.password
            email = student.email

            if request.method == 'POST':

                send_mail(
                    "Parents' Evening",
                    f"Link to login page: {link}, Username: {username}, Password: {password}",
                    "twycrossbooking@gmail.com",
                    [f"{email}"],
                    fail_silently=False,
                )

        return redirect('dashboard')


    context = {}
    return render(request, 'main/emailAllStudents.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def emailAllTeachers(request):

    teachers = Teacher.objects.all()
    link = "https://twyc-nea.vercel.app/login"

    if request.method == 'POST':

        for teacher in teachers:
            username = teacher.user.username
            password = teacher.user.password
            email = teacher.email

            if request.method == 'POST':

                send_mail(
                    "Parents' Evening",
                    f"Link to login page: {link}, Username: {username}, Password: {password}",
                    "twycrossbooking@gmail.com",
                    [f"{email}"],
                    fail_silently=False,
                )

        return redirect('dashboard')


    context = {}
    return render(request, 'main/emailAllTeachers.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def printTeacherBookings(request):

    # Create a buffer to hold the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    teachers = Teacher.objects.all()

    for teacher in teachers:

        name = teacher.name

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, height - 50, f"{name}'s Bookings Summary")

        # Table Headers
        p.setFont("Helvetica-Bold", 12)
        headers = ["Start Time", "Student", "Subject", "Date", "Status"]
        x_offset = 50
        y_offset = height - 100

        for i, header in enumerate(headers):
            p.drawString(x_offset + i * 100, y_offset, header)

        # Table Data
        p.setFont("Helvetica", 10)
        y_offset -= 20



        bookings = Booking.objects.filter(teacher=teacher)  # Assuming teacher is logged in
        
        student = Student.objects.get(name='UCAS')
        ucas_bookings = request.user.teacher.booking_set.filter(student=student)
        ucas_sorted = sortBookings(ucas_bookings)

        final_ucas = []
        finalBookings = sortBookings(bookings)
        for booking in finalBookings:
            if booking.student.name != 'UCAS':
                final_ucas.append(booking)
        if len(ucas_sorted) != 0:
            final_ucas.append(ucas_sorted[0])
        final_ucas = sortBookings(final_ucas)


        for booking in final_ucas:
            subjects = ", ".join(
                [subject.name for subject in booking.teacher.subjects.all() if subject in booking.student.subjects.all()]
            )
            
            data = [
                booking.timeslot.start_time.strftime("%H:%M"),
                booking.student.name,
                subjects,
                booking.date.date.strftime("%Y-%m-%d"),
                booking.status
            ]

            for i, text in enumerate(data):
                p.drawString(x_offset + i * 100, y_offset, text)

            y_offset -= 20

        p.showPage()

    # Save PDF to buffer
    p.showPage()
    p.save()

    # Send PDF response
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")