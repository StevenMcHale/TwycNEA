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

    finalBookings = sortBookings(bookings)


    context = {'teacher':teacher, 'bookings':finalBookings, 'total_bookings':total_bookings}
    return render(request, 'users/userTeacherBookings.html', context)