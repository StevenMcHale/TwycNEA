from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from main.models import *
from manual.extras import *
# pdf imports
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerStudentPage(request):
    form = CreateUserStudentForm()

    if request.method == 'POST':
        form = CreateUserStudentForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            level = form.cleaned_data.get('level')

            group = Group.objects.get(name='student')
            user.groups.add(group)
            Student.objects.create(
                user=user,
                name=username,
                email=email,
                year_group=level,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('registerStudent')

    context = {'form':form}
    return render(request, 'users/registerStudent.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerTeacherPage(request):
    form = CreateUserTeacherForm()

    if request.method == 'POST':
        form = CreateUserTeacherForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            Teacher.objects.create(
                user=user,
                name=username,
                email=email,
            )
            

            messages.success(request, 'Account was created for ' + username)
            return redirect('registerTeacher')

    context = {'form':form}
    return render(request, 'users/registerTeacher.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def registerParentPage(request):
    form = CreateUserParentForm()

    if request.method == 'POST':
        form = CreateUserParentForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            group = Group.objects.get(name='parent')
            user.groups.add(group)
            Parent.objects.create(
                user=user,
                name=username,
                email=email,
            )
            

            messages.success(request, 'Account was created for ' + username)
            return redirect('registerTeacher')

    context = {'form':form}
    return render(request, 'users/registerParent.html', context)



@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')





@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userStudent(request):
    bookings = request.user.student.booking_set.all()
    student = request.user.student
    total_bookings = bookings.count()
    subjects = student.subjects.all()
    teachers = student.teachers.all()
    date = EveningDate.objects.get(year_group=student.year_group)

    context = {'student':student, 'bookings':bookings, 'total_bookings':total_bookings, 'subjects':subjects, 'teachers':teachers, 'date':date}

    return render(request, 'users/userStudent.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['parent'])
def userParent(request):

    parent = request.user.parent
    students = parent.students.all()

    if request.method == 'POST':
        username = request.POST.get('student')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Password is incorrect')
        


    context = {'parent':parent, 'students':students}

    return render(request, 'users/userParent.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def userTeacher(request):
    teacher = request.user.teacher
    bookings = teacher.booking_set.all()
    total_bookings = bookings.count()
    subjects = teacher.subjects.all()
    students = Student.objects.filter(teachers__name=teacher.name)

    context = {'teacher':teacher, 'bookings':bookings, 'total_bookings':total_bookings, 'subjects':subjects, 'students':students}
    return render(request, 'users/userTeacher.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userStudentBookings(request):
    bookings = request.user.student.booking_set.all()
    student = request.user.student
    total_bookings = bookings.count()

    finalBookings = sortBookings(bookings)


    context = {'student':student, 'bookings':finalBookings, 'total_bookings':total_bookings}

    return render(request, 'users/userStudentBookings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def userTeacherBookings(request):
    teacher = request.user.teacher
    bookings = teacher.booking_set.all()
    total_bookings = bookings.count()
    student = Student.objects.get(name='UCAS')
    ucas_bookings = bookings.filter(student=student)
    ucas_sorted = sortBookings(ucas_bookings)

    final_ucas = []
    finalBookings = sortBookings(bookings)
    for booking in finalBookings:
        if booking.student.name != 'UCAS':
            final_ucas.append(booking)
    final_ucas.append(ucas_sorted[0])
    final_ucas = sortBookings(final_ucas)




    context = {'teacher':teacher, 'bookings':final_ucas, 'total_bookings':total_bookings}
    return render(request, 'users/userTeacherBookings.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def generate_bookings_pdf_students(request):
    # Create a buffer to hold the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Student's Bookings Summary")

    # Table Headers
    p.setFont("Helvetica-Bold", 12)
    headers = ["Start Time", "Teacher", "Subject", "Date","Building", "Room", "Status"]
    x_offset = 50
    y_offset = height - 100

    for i, header in enumerate(headers):
        p.drawString(x_offset + i * 100, y_offset, header)

    # Table Data
    p.setFont("Helvetica", 10)
    y_offset -= 20

    bookings = Booking.objects.filter(student=request.user.student)  # Assuming student is logged in
    bookings = sortBookings(bookings)
    for booking in bookings:
        subjects = ", ".join(
            [subject.name for subject in booking.student.subjects.all() if subject in booking.teacher.subjects.all()]
        )
        
        data = [
            booking.timeslot.start_time.strftime("%H:%M"),
            booking.teacher.name,
            subjects,
            booking.date.date.strftime("%Y-%m-%d"),
            booking.teacher.building.name,
            booking.teacher.room.name,
            booking.status
        ]

        for i, text in enumerate(data):
            p.drawString(x_offset + i * 100, y_offset, text)

        y_offset -= 20

    # Save PDF to buffer
    p.showPage()
    p.save()

    # Send PDF response
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def generate_bookings_pdf_teachers(request):
    # Create a buffer to hold the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Teacher's Bookings Summary")

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

    bookings = Booking.objects.filter(teacher=request.user.teacher)  # Assuming teacher is logged in
    
    student = Student.objects.get(name='UCAS')
    ucas_bookings = request.user.teacher.booking_set.filter(student=student)
    ucas_sorted = sortBookings(ucas_bookings)

    final_ucas = []
    finalBookings = sortBookings(bookings)
    for booking in finalBookings:
        if booking.student.name != 'UCAS':
            final_ucas.append(booking)
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

    # Save PDF to buffer
    p.showPage()
    p.save()

    # Send PDF response
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")